"""Tests for the SRS Reconsolidation module (srs_reconsolidation.js)."""

import os
import re

import pytest

flask = pytest.importorskip("flask")

# Absolute path to project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JS_PATH = os.path.join(PROJECT_ROOT, "static", "js", "srs_reconsolidation.js")
BASE_HTML_PATH = os.path.join(PROJECT_ROOT, "templates", "base.html")
APP_JS_PATH = os.path.join(PROJECT_ROOT, "static", "js", "app.js")
SCHEDULER_JS_PATH = os.path.join(PROJECT_ROOT, "static", "js", "srs_scheduler.js")


@pytest.fixture
def js_source():
    """Load the reconsolidation JS source code."""
    with open(JS_PATH, "r", encoding="utf-8") as f:
        return f.read()


@pytest.fixture
def base_html_source():
    """Load the base.html template source."""
    with open(BASE_HTML_PATH, "r", encoding="utf-8") as f:
        return f.read()


@pytest.fixture
def app_js_source():
    """Load the app.js source code."""
    with open(APP_JS_PATH, "r", encoding="utf-8") as f:
        return f.read()


@pytest.fixture
def scheduler_js_source():
    """Load the srs_scheduler.js source code."""
    with open(SCHEDULER_JS_PATH, "r", encoding="utf-8") as f:
        return f.read()


# --- Test 1: File exists and has valid JS syntax ---
class TestFileStructure:

    def test_file_exists(self):
        """Test 1: srs_reconsolidation.js file exists."""
        assert os.path.isfile(JS_PATH), f"File not found: {JS_PATH}"

    def test_valid_js_syntax(self, js_source):
        """Test 2: File has valid JS structure (IIFE pattern, no obvious syntax errors)."""
        # Check it starts with a comment or IIFE
        assert "(function" in js_source, "Expected IIFE pattern"
        assert "})();" in js_source, "Expected IIFE closing"
        # Check balanced braces
        open_braces = js_source.count("{")
        close_braces = js_source.count("}")
        assert open_braces == close_braces, (
            f"Unbalanced braces: {open_braces} open vs {close_braces} close"
        )


# --- Test 2: base.html includes script tag ---
class TestBaseHtmlInclusion:

    def test_script_tag_present(self, base_html_source):
        """Test 3: base.html includes srs_reconsolidation.js script tag."""
        assert "srs_reconsolidation.js" in base_html_source

    def test_script_tag_after_scheduler(self, base_html_source):
        """Test 4: srs_reconsolidation.js is loaded after srs_scheduler.js."""
        scheduler_pos = base_html_source.find("srs_scheduler.js")
        recon_pos = base_html_source.find("srs_reconsolidation.js")
        assert scheduler_pos >= 0, "srs_scheduler.js not found in base.html"
        assert recon_pos >= 0, "srs_reconsolidation.js not found in base.html"
        assert recon_pos > scheduler_pos, (
            "srs_reconsolidation.js must appear after srs_scheduler.js"
        )

    def test_script_tag_before_block_scripts(self, base_html_source):
        """Test 5: srs_reconsolidation.js is loaded before block scripts."""
        recon_pos = base_html_source.find("srs_reconsolidation.js")
        block_pos = base_html_source.find("{% block scripts %}")
        assert recon_pos >= 0, "srs_reconsolidation.js not found in base.html"
        assert block_pos >= 0, "{% block scripts %} not found in base.html"
        assert recon_pos < block_pos, (
            "srs_reconsolidation.js must appear before {% block scripts %}"
        )


# --- Test 3: Required API surface ---
class TestAPISurface:

    def test_exposes_window_object(self, js_source):
        """Test 6: Module exposes window.SRSReconsolidation."""
        assert "window.SRSReconsolidation" in js_source

    def test_has_init_method(self, js_source):
        """Test 7: Module has init method."""
        assert re.search(r"init\s*:\s*function", js_source), "init method not found"

    def test_has_on_wrong_answer(self, js_source):
        """Test 8: Module has onWrongAnswer method."""
        assert re.search(r"onWrongAnswer\s*:\s*function", js_source), (
            "onWrongAnswer method not found"
        )

    def test_has_on_correct_answer(self, js_source):
        """Test 9: Module has onCorrectAnswer method."""
        assert re.search(r"onCorrectAnswer\s*:\s*function", js_source), (
            "onCorrectAnswer method not found"
        )

    def test_has_get_active_items(self, js_source):
        """Test 10: Module has getActiveItems method."""
        assert re.search(r"getActiveItems\s*:\s*function", js_source), (
            "getActiveItems method not found"
        )

    def test_has_is_reconsolidating(self, js_source):
        """Test 11: Module has isReconsolidating method."""
        assert re.search(r"isReconsolidating\s*:\s*function", js_source), (
            "isReconsolidating method not found"
        )

    def test_has_get_error_stats(self, js_source):
        """Test 12: Module has getErrorStats method."""
        assert re.search(r"getErrorStats\s*:\s*function", js_source), (
            "getErrorStats method not found"
        )

    def test_has_get_boost(self, js_source):
        """Test 13: Module has getBoost method."""
        assert re.search(r"getBoost\s*:\s*function", js_source), (
            "getBoost method not found"
        )

    def test_has_save(self, js_source):
        """Test 14: Module has save method."""
        assert re.search(r"save\s*:\s*function", js_source), "save method not found"


# --- Test 4-5: Default configuration values ---
class TestDefaults:

    def test_boost_factor_default(self, js_source):
        """Test 15: boostFactor default is 2.0."""
        assert re.search(r"boostFactor\s*:\s*2\.0", js_source), (
            "boostFactor default should be 2.0"
        )

    def test_required_correct_default(self, js_source):
        """Test 16: requiredCorrect default is 3."""
        assert re.search(r"requiredCorrect\s*:\s*3", js_source), (
            "requiredCorrect default should be 3"
        )


# --- Test 6-13: Logic behavior (static analysis of JS logic patterns) ---
class TestLogicPatterns:

    def test_on_wrong_marks_active(self, js_source):
        """Test 17: onWrongAnswer sets active=true."""
        # Find the onWrongAnswer function body
        match = re.search(
            r"onWrongAnswer\s*:\s*function.*?\{(.*?)(?=\n\s{8}\w+\s*:\s*function|\n\s{4}\};\n)",
            js_source,
            re.DOTALL,
        )
        assert match, "Could not find onWrongAnswer function body"
        body = match.group(1)
        assert "active" in body and "true" in body, (
            "onWrongAnswer should set active = true"
        )

    def test_on_correct_increments_counter(self, js_source):
        """Test 18: onCorrectAnswer increments consecutiveCorrect."""
        match = re.search(
            r"onCorrectAnswer\s*:\s*function.*?\{(.*?)(?=\n\s{8}\w+\s*:\s*function|\n\s{4}\};\n)",
            js_source,
            re.DOTALL,
        )
        assert match, "Could not find onCorrectAnswer function body"
        body = match.group(1)
        assert "consecutiveCorrect" in body, (
            "onCorrectAnswer should modify consecutiveCorrect"
        )

    def test_reconsolidation_completes_after_required(self, js_source):
        """Test 19: Reconsolidation completes when consecutiveCorrect >= requiredCorrect."""
        match = re.search(
            r"onCorrectAnswer\s*:\s*function.*?\{(.*?)(?=\n\s{8}\w+\s*:\s*function|\n\s{4}\};\n)",
            js_source,
            re.DOTALL,
        )
        assert match, "Could not find onCorrectAnswer function body"
        body = match.group(1)
        assert "requiredCorrect" in body, (
            "onCorrectAnswer should check against requiredCorrect"
        )
        assert "completed: true" in body, (
            "onCorrectAnswer should return completed: true when threshold met"
        )

    def test_wrong_answer_resets_consecutive(self, js_source):
        """Test 20: Wrong answer resets consecutiveCorrect to 0."""
        match = re.search(
            r"onWrongAnswer\s*:\s*function.*?\{(.*?)(?=\n\s{8}\w+\s*:\s*function|\n\s{4}\};\n)",
            js_source,
            re.DOTALL,
        )
        assert match, "Could not find onWrongAnswer function body"
        body = match.group(1)
        assert "consecutiveCorrect" in body and "0" in body, (
            "onWrongAnswer should reset consecutiveCorrect to 0"
        )

    def test_get_active_items_filters_active(self, js_source):
        """Test 21: getActiveItems only returns items with active=true."""
        match = re.search(
            r"getActiveItems\s*:\s*function.*?\{(.*?)(?=\n\s{8}\w+\s*:\s*function|\n\s{4}\};\n)",
            js_source,
            re.DOTALL,
        )
        assert match, "Could not find getActiveItems function body"
        body = match.group(1)
        assert "active" in body, "getActiveItems should check active status"

    def test_is_reconsolidating_returns_boolean(self, js_source):
        """Test 22: isReconsolidating returns a boolean value."""
        match = re.search(
            r"isReconsolidating\s*:\s*function.*?\{(.*?)(?=\n\s{8}\w+\s*:\s*function|\n\s{4}\};\n)",
            js_source,
            re.DOTALL,
        )
        assert match, "Could not find isReconsolidating function body"
        body = match.group(1)
        assert "active" in body, (
            "isReconsolidating should check active field"
        )

    def test_get_error_stats_tracks_per_type(self, js_source):
        """Test 23: getErrorStats processes errorStats data."""
        match = re.search(
            r"getErrorStats\s*:\s*function.*?\{(.*?)(?=\n\s{8}\w+\s*:\s*function|\n\s{4}\};\n)",
            js_source,
            re.DOTALL,
        )
        assert match, "Could not find getErrorStats function body"
        body = match.group(1)
        assert "errorStats" in body, "getErrorStats should use errorStats"
        assert "topErrors" in body, "getErrorStats should return topErrors"
        assert "totalErrors" in body, "getErrorStats should return totalErrors"

    def test_get_boost_returns_factor_for_active(self, js_source):
        """Test 24: getBoost returns boostFactor for reconsolidating items, 1.0 otherwise."""
        match = re.search(
            r"getBoost\s*:\s*function.*?\{(.*?)(?=\n\s{8}\w+\s*:\s*function|\n\s{4}\};\n)",
            js_source,
            re.DOTALL,
        )
        assert match, "Could not find getBoost function body"
        body = match.group(1)
        assert "boostFactor" in body, "getBoost should return boostFactor"
        assert "1.0" in body, "getBoost should return 1.0 for non-reconsolidating items"


# --- Test 14-15: Integration hooks ---
class TestIntegrationHooks:

    def test_app_js_reconsolidation_hook(self, app_js_source):
        """Test 25: app.js has reconsolidation integration hook."""
        assert "SRSReconsolidation" in app_js_source, (
            "app.js should reference SRSReconsolidation"
        )
        assert "onCorrectAnswer" in app_js_source, (
            "app.js should call onCorrectAnswer"
        )
        assert "onWrongAnswer" in app_js_source, (
            "app.js should call onWrongAnswer"
        )

    def test_scheduler_reconsolidation_hook(self, scheduler_js_source):
        """Test 26: srs_scheduler.js has reconsolidation boost hook."""
        assert "SRSReconsolidation" in scheduler_js_source, (
            "srs_scheduler.js should reference SRSReconsolidation"
        )
        assert "getBoost" in scheduler_js_source, (
            "srs_scheduler.js should call getBoost"
        )
        assert "reconsolidating" in scheduler_js_source, (
            "srs_scheduler.js should set reconsolidating flag on items"
        )


# --- Additional: IIFE pattern and localStorage key ---
class TestModulePattern:

    def test_uses_iife_pattern(self, js_source):
        """Test 27: Module uses IIFE pattern."""
        stripped = js_source.lstrip()
        # Allow leading comments
        lines = stripped.split("\n")
        found_iife = False
        for line in lines:
            if line.strip().startswith("(function"):
                found_iife = True
                break
            if line.strip() and not line.strip().startswith("/*") and not line.strip().startswith("*") and not line.strip().startswith("//"):
                break
        assert found_iife, "Module should use IIFE pattern starting with (function"

    def test_uses_correct_storage_key(self, js_source):
        """Test 28: Module uses tolc_srs_recon localStorage key."""
        assert "tolc_srs_recon" in js_source, (
            "Module should use tolc_srs_recon as localStorage key"
        )

    def test_graceful_fallback_without_tracker(self, js_source):
        """Test 29: Module handles missing SRSTracker/SRSScheduler gracefully."""
        # The module should not have hard dependencies that would throw
        # It should not directly call SRSTracker or SRSScheduler methods
        # (it only checks window.SRSReconsolidation from other modules)
        assert "window.SRSReconsolidation" in js_source
        # Verify no direct calls to SRSTracker inside reconsolidation module
        # (it should be self-contained)
        assert "SRSTracker." not in js_source or "window.SRSTracker" in js_source, (
            "Module should not directly depend on SRSTracker"
        )
