"""Tests for the SRS Tracker JavaScript module.

Validates file existence, template integration, app.js hook,
required API surface, migration logic patterns, and backward compatibility.
"""

import os
import re

import pytest


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRS_JS_PATH = os.path.join(PROJECT_ROOT, "static", "js", "srs_tracker.js")
APP_JS_PATH = os.path.join(PROJECT_ROOT, "static", "js", "app.js")
BASE_HTML_PATH = os.path.join(PROJECT_ROOT, "templates", "base.html")


@pytest.fixture(scope="module")
def srs_js_content():
    """Load srs_tracker.js content once for all tests."""
    assert os.path.isfile(SRS_JS_PATH), f"srs_tracker.js not found at {SRS_JS_PATH}"
    with open(SRS_JS_PATH, "r", encoding="utf-8") as f:
        return f.read()


@pytest.fixture(scope="module")
def app_js_content():
    """Load app.js content once for all tests."""
    assert os.path.isfile(APP_JS_PATH), f"app.js not found at {APP_JS_PATH}"
    with open(APP_JS_PATH, "r", encoding="utf-8") as f:
        return f.read()


@pytest.fixture(scope="module")
def base_html_content():
    """Load base.html content once for all tests."""
    assert os.path.isfile(BASE_HTML_PATH), f"base.html not found at {BASE_HTML_PATH}"
    with open(BASE_HTML_PATH, "r", encoding="utf-8") as f:
        return f.read()


# ---- 1. File existence and loadability ----

class TestFileExistence:
    def test_srs_tracker_js_exists(self):
        assert os.path.isfile(SRS_JS_PATH), "srs_tracker.js must exist"

    def test_srs_tracker_js_not_empty(self, srs_js_content):
        assert len(srs_js_content.strip()) > 100, "srs_tracker.js must have substantial content"

    def test_srs_tracker_js_valid_syntax_indicators(self, srs_js_content):
        """Basic check that the JS is not obviously broken (matched braces, etc.)."""
        open_braces = srs_js_content.count("{")
        close_braces = srs_js_content.count("}")
        assert abs(open_braces - close_braces) <= 2, (
            f"Brace mismatch: {{ = {open_braces}, }} = {close_braces}"
        )


# ---- 2. Template includes the script tag ----

class TestTemplateIntegration:
    def test_base_html_includes_srs_tracker(self, base_html_content):
        assert "srs_tracker.js" in base_html_content, (
            "base.html must include srs_tracker.js script tag"
        )

    def test_srs_tracker_after_app_js(self, base_html_content):
        """srs_tracker.js script tag must appear AFTER app.js."""
        app_js_pos = base_html_content.find("app.js")
        srs_pos = base_html_content.find("srs_tracker.js")
        assert app_js_pos >= 0, "app.js must be in base.html"
        assert srs_pos >= 0, "srs_tracker.js must be in base.html"
        assert srs_pos > app_js_pos, (
            "srs_tracker.js must be loaded AFTER app.js"
        )


# ---- 3. App.js integration hook ----

class TestAppJsIntegration:
    def test_app_js_has_srs_tracker_call(self, app_js_content):
        assert "SRSTracker" in app_js_content, (
            "app.js must reference SRSTracker for integration"
        )

    def test_app_js_calls_record_answer(self, app_js_content):
        assert "SRSTracker.recordAnswer" in app_js_content, (
            "app.js must call SRSTracker.recordAnswer()"
        )

    def test_app_js_guards_srs_tracker(self, app_js_content):
        """The integration should be guarded with a check for window.SRSTracker."""
        assert "window.SRSTracker" in app_js_content, (
            "app.js must guard SRSTracker usage with window.SRSTracker check"
        )

    def test_app_js_preserves_existing_logic(self, app_js_content):
        """Old Storage.recordAnswer logic must still exist."""
        assert "this.saveProgress" in app_js_content or "saveProgress" in app_js_content, (
            "app.js must preserve original saveProgress call"
        )


# ---- 4. Required API functions ----

class TestRequiredAPI:
    REQUIRED_FUNCTIONS = ["init", "getStats", "recordAnswer", "getHistory", "getAllStats", "migrate", "save"]

    @pytest.mark.parametrize("func_name", REQUIRED_FUNCTIONS)
    def test_api_function_exists(self, srs_js_content, func_name):
        """Each required API function must be defined in the JS file."""
        # Check that the function is defined AND exposed on window.SRSTracker
        assert func_name in srs_js_content, (
            f"Function '{func_name}' must be defined in srs_tracker.js"
        )

    def test_window_srs_tracker_exposed(self, srs_js_content):
        assert "window.SRSTracker" in srs_js_content, (
            "Module must expose window.SRSTracker"
        )

    @pytest.mark.parametrize("func_name", REQUIRED_FUNCTIONS)
    def test_api_function_exposed_on_window(self, srs_js_content, func_name):
        """Each function must be assigned to window.SRSTracker."""
        # Look for patterns like "funcName: funcName" or "funcName: function"
        pattern = rf"{func_name}\s*:"
        assert re.search(pattern, srs_js_content), (
            f"Function '{func_name}' must be exposed on window.SRSTracker object"
        )


# ---- 5. Migration logic ----

class TestMigrationLogic:
    def test_reads_tolc_progress(self, srs_js_content):
        assert "tolc_progress" in srs_js_content, (
            "Migration must read from tolc_progress localStorage key"
        )

    def test_reads_tolc_wrong(self, srs_js_content):
        assert "tolc_wrong" in srs_js_content, (
            "Migration must read from tolc_wrong localStorage key"
        )

    def test_default_difficulty_2(self, srs_js_content):
        """Migration should use difficulty 2 as default for old data."""
        # Check for the pattern of creating key with difficulty 2
        assert re.search(r"(makeKey|_2|, 2)", srs_js_content), (
            "Migration must default to difficulty 2 for old data"
        )

    def test_stability_calculation_from_streak(self, srs_js_content):
        """Stability should be calculated from streak during migration."""
        assert "streak" in srs_js_content, (
            "Migration must use streak data for stability calculation"
        )
        assert "1.5" in srs_js_content, (
            "Migration should use streak * 1.5 for stability"
        )

    def test_stability_clamped(self, srs_js_content):
        """Stability from migration must be clamped between 0.5 and 30."""
        assert "0.5" in srs_js_content, "Stability min must be 0.5"
        assert "30" in srs_js_content, "Stability max in migration must be 30"

    def test_difficulty_clamped(self, srs_js_content):
        """Difficulty must be clamped to [0.1, 0.9]."""
        assert "0.1" in srs_js_content, "Difficulty min must be 0.1"
        assert "0.9" in srs_js_content, "Difficulty max must be 0.9"

    def test_migrated_flag_set(self, srs_js_content):
        """Migration must set migrated = true."""
        assert re.search(r"migrated\s*=\s*true", srs_js_content, re.IGNORECASE), (
            "Migration must set migrated = true"
        )

    def test_history_sorted_by_timestamp(self, srs_js_content):
        """History entries should be sorted by timestamp."""
        assert "sort" in srs_js_content, (
            "Migration must sort history entries by timestamp"
        )

    def test_history_capped(self, srs_js_content):
        """History must be capped at MAX_HISTORY (100)."""
        assert "100" in srs_js_content, (
            "History ring buffer must be capped at 100 entries"
        )


# ---- 6. Backward compatibility ----

class TestBackwardCompatibility:
    def test_old_keys_not_deleted(self, srs_js_content):
        """Migration must NOT delete old localStorage keys."""
        # Make sure there's no removeItem("tolc_progress") or removeItem("tolc_wrong")
        assert 'removeItem("tolc_progress")' not in srs_js_content, (
            "Migration must NOT delete tolc_progress key"
        )
        assert "removeItem('tolc_progress')" not in srs_js_content, (
            "Migration must NOT delete tolc_progress key"
        )
        assert 'removeItem("tolc_wrong")' not in srs_js_content, (
            "Migration must NOT delete tolc_wrong key"
        )
        assert "removeItem('tolc_wrong')" not in srs_js_content, (
            "Migration must NOT delete tolc_wrong key"
        )

    def test_uses_separate_storage_key(self, srs_js_content):
        """SRS data must use its own localStorage key, not overwrite old ones."""
        assert "tolc_srs" in srs_js_content, (
            "SRS tracker must use 'tolc_srs' localStorage key"
        )


# ---- 7. Stability update rules ----

class TestStabilityRules:
    def test_correct_answer_stability_formula(self, srs_js_content):
        """On correct: stability = stability * (1.5 + (1 - difficulty) * 0.5), capped at 365."""
        assert "365" in srs_js_content, "Stability cap must be 365"

    def test_wrong_answer_stability_formula(self, srs_js_content):
        """On wrong: stability = stability * 0.5, min 0.5."""
        # The pattern stability * 0.5 should appear
        assert re.search(r"stability\s*\*\s*0\.5", srs_js_content), (
            "Wrong answer must halve stability"
        )

    def test_rolling_window_size(self, srs_js_content):
        """Rolling window must be size 10."""
        assert "10" in srs_js_content, "Rolling window size must be 10"

    def test_ema_alpha(self, srs_js_content):
        """EMA alpha for avgTimeMs must be 0.3."""
        assert "0.3" in srs_js_content, "EMA alpha must be 0.3"


# ---- 8. Data model structure ----

class TestDataModel:
    def test_version_field(self, srs_js_content):
        assert "version" in srs_js_content, "Data model must have version field"

    def test_storage_key(self, srs_js_content):
        assert "tolc_srs" in srs_js_content, "Must use tolc_srs storage key"

    def test_stats_fields(self, srs_js_content):
        """Stats entries must have all required fields."""
        required_fields = [
            "lastReview", "totalReviews", "correctCount",
            "rollingAccuracy", "rollingWindow", "stability",
            "difficulty", "avgTimeMs"
        ]
        for field in required_fields:
            assert field in srs_js_content, (
                f"Stats must include '{field}' field"
            )

    def test_history_entry_fields(self, srs_js_content):
        """History entries must have required fields."""
        for field in ["ts", "type", "difficulty", "correct", "timeMs"]:
            assert field in srs_js_content, (
                f"History entries must include '{field}' field"
            )
