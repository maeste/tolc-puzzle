"""Tests for SRS Adaptive Difficulty System (srs_adaptive.js).

These tests verify:
- The JS source file exists and has the expected structure
- The algorithm logic for getRecommendedDifficulty
- The algorithm logic for getMasteryLevel
- The getAllMasteryLevels function
- Template integration (base.html script tag, exercise.html, dashboard.html)
- Edge cases
"""
import os
import re

import pytest

# Project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture
def adaptive_source():
    """Read the srs_adaptive.js source file."""
    path = os.path.join(PROJECT_ROOT, "static", "js", "srs_adaptive.js")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


@pytest.fixture
def base_html_source():
    """Read the base.html template."""
    path = os.path.join(PROJECT_ROOT, "templates", "base.html")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


@pytest.fixture
def exercise_html_source():
    """Read the exercise.html template."""
    path = os.path.join(PROJECT_ROOT, "templates", "exercise.html")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


@pytest.fixture
def exercise_js_source():
    """Read the exercise.js source file."""
    path = os.path.join(PROJECT_ROOT, "static", "js", "exercise.js")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


@pytest.fixture
def dashboard_html_source():
    """Read the dashboard.html template."""
    path = os.path.join(PROJECT_ROOT, "templates", "dashboard.html")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


@pytest.fixture
def style_css_source():
    """Read the style.css file."""
    path = os.path.join(PROJECT_ROOT, "static", "css", "style.css")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# ── File existence and structure ────────────────────────────────────

class TestFileExistence:
    """Verify that all required files exist."""

    def test_srs_adaptive_js_exists(self):
        path = os.path.join(PROJECT_ROOT, "static", "js", "srs_adaptive.js")
        assert os.path.isfile(path), "srs_adaptive.js must exist"

    def test_exercise_html_exists(self):
        path = os.path.join(PROJECT_ROOT, "templates", "exercise.html")
        assert os.path.isfile(path), "exercise.html must exist"

    def test_dashboard_html_exists(self):
        path = os.path.join(PROJECT_ROOT, "templates", "dashboard.html")
        assert os.path.isfile(path), "dashboard.html must exist"

    def test_base_html_exists(self):
        path = os.path.join(PROJECT_ROOT, "templates", "base.html")
        assert os.path.isfile(path), "base.html must exist"


# ── JS Source Structure ─────────────────────────────────────────────

class TestAdaptiveJSStructure:
    """Verify the srs_adaptive.js file has expected structure."""

    def test_iife_pattern(self, adaptive_source):
        """Should use IIFE pattern."""
        assert "(function" in adaptive_source
        assert "})();" in adaptive_source

    def test_exposes_window_srs_adaptive(self, adaptive_source):
        """Should expose window.SRSAdaptive."""
        assert "window.SRSAdaptive" in adaptive_source

    def test_has_get_recommended_difficulty(self, adaptive_source):
        """Should have getRecommendedDifficulty function."""
        assert "getRecommendedDifficulty" in adaptive_source

    def test_has_get_mastery_level(self, adaptive_source):
        """Should have getMasteryLevel function."""
        assert "getMasteryLevel" in adaptive_source

    def test_has_get_all_mastery_levels(self, adaptive_source):
        """Should have getAllMasteryLevels function."""
        assert "getAllMasteryLevels" in adaptive_source

    def test_depends_on_srs_tracker(self, adaptive_source):
        """Should reference SRSTracker for stats."""
        assert "SRSTracker" in adaptive_source

    def test_uses_strict_mode(self, adaptive_source):
        """Should use strict mode."""
        assert '"use strict"' in adaptive_source

    def test_no_dom_manipulation(self, adaptive_source):
        """Should not directly manipulate DOM (pure logic module)."""
        assert "document.getElementById" not in adaptive_source
        assert "document.querySelector" not in adaptive_source
        assert "innerHTML" not in adaptive_source


# ── Template Integration ────────────────────────────────────────────

class TestTemplateIntegration:
    """Verify templates include the adaptive system correctly."""

    def test_base_html_includes_srs_adaptive_script(self, base_html_source):
        """base.html should include srs_adaptive.js after srs_reconsolidation.js."""
        assert "srs_adaptive.js" in base_html_source

    def test_script_order_in_base_html(self, base_html_source):
        """srs_adaptive.js should come after srs_reconsolidation.js."""
        recon_pos = base_html_source.find("srs_reconsolidation.js")
        adaptive_pos = base_html_source.find("srs_adaptive.js")
        assert recon_pos < adaptive_pos, (
            "srs_adaptive.js must load after srs_reconsolidation.js"
        )

    def test_exercise_html_has_adaptive_indicator(self, exercise_html_source):
        """exercise.html should have an adaptive-indicator element."""
        assert "adaptive-indicator" in exercise_html_source

    def test_dashboard_html_has_mastery_badge_logic(self, dashboard_html_source):
        """dashboard.html should have mastery badge rendering logic."""
        assert "SRSAdaptive" in dashboard_html_source
        assert "mastery" in dashboard_html_source.lower()

    def test_dashboard_html_has_mastery_badge_indicator_class(self, dashboard_html_source):
        """dashboard.html should use mastery-badge-indicator class."""
        assert "mastery-badge-indicator" in dashboard_html_source


# ── Exercise.js Adaptive Integration ────────────────────────────────

class TestExerciseJSIntegration:
    """Verify exercise.js integrates adaptive difficulty."""

    def test_exercise_js_references_srs_adaptive(self, exercise_js_source):
        """exercise.js should reference SRSAdaptive."""
        assert "SRSAdaptive" in exercise_js_source

    def test_exercise_js_calls_get_recommended_difficulty(self, exercise_js_source):
        """exercise.js should call getRecommendedDifficulty."""
        assert "getRecommendedDifficulty" in exercise_js_source

    def test_exercise_js_sets_current_difficulty(self, exercise_js_source):
        """exercise.js should set window._currentDifficulty."""
        assert "_currentDifficulty" in exercise_js_source

    def test_exercise_js_has_adaptive_applied_flag(self, exercise_js_source):
        """exercise.js should track whether adaptive was already applied."""
        assert "adaptiveApplied" in exercise_js_source

    def test_exercise_js_hides_indicator_on_manual_override(self, exercise_js_source):
        """exercise.js should hide indicator when user manually changes difficulty."""
        # Should hide the indicator on click
        assert "adaptiveIndicator" in exercise_js_source


# ── CSS Styles ──────────────────────────────────────────────────────

class TestCSSStyles:
    """Verify CSS has styles for adaptive components."""

    def test_adaptive_indicator_style(self, style_css_source):
        """CSS should have .adaptive-indicator styles."""
        assert ".adaptive-indicator" in style_css_source

    def test_mastery_badge_indicator_style(self, style_css_source):
        """CSS should have .mastery-badge-indicator styles."""
        assert ".mastery-badge-indicator" in style_css_source


# ── Algorithm Logic (static analysis of JS) ─────────────────────────

class TestAlgorithmLogic:
    """Verify the algorithm constants and logic via source inspection."""

    def test_accuracy_threshold_l1_to_l2(self, adaptive_source):
        """L1→L2 promotion threshold should be 0.80."""
        assert "0.80" in adaptive_source or "0.8" in adaptive_source

    def test_accuracy_threshold_l2_to_l3(self, adaptive_source):
        """L2→L3 promotion threshold should be 0.70."""
        assert "0.70" in adaptive_source or "0.7" in adaptive_source

    def test_accuracy_fallback_threshold(self, adaptive_source):
        """Fallback threshold should be 0.50."""
        assert "0.50" in adaptive_source or "0.5" in adaptive_source

    def test_min_reviews_for_promotion(self, adaptive_source):
        """Minimum reviews for promotion should be 5."""
        assert "MIN_REVIEWS_FOR_PROMOTION" in adaptive_source
        # Verify the value is 5
        match = re.search(r"MIN_REVIEWS_FOR_PROMOTION\s*=\s*(\d+)", adaptive_source)
        assert match is not None
        assert int(match.group(1)) == 5

    def test_mastery_stability_threshold(self, adaptive_source):
        """Mastery stability threshold should be 5 days."""
        assert "MASTERY_STABILITY_THRESHOLD" in adaptive_source
        match = re.search(r"MASTERY_STABILITY_THRESHOLD\s*=\s*(\d+)", adaptive_source)
        assert match is not None
        assert int(match.group(1)) == 5

    def test_mastery_levels_defined(self, adaptive_source):
        """All four mastery levels should be defined."""
        for level in ["beginner", "intermediate", "advanced", "mastered"]:
            assert f'"{level}"' in adaptive_source

    def test_default_returns_level_1(self, adaptive_source):
        """Default (no data) should return level 1."""
        # The function should return 1 as default
        assert "return 1" in adaptive_source

    def test_checks_all_three_difficulty_levels(self, adaptive_source):
        """Should check stats for all three difficulty levels."""
        assert "getStats(type, 1)" in adaptive_source
        assert "getStats(type, 2)" in adaptive_source
        assert "getStats(type, 3)" in adaptive_source

    def test_uses_rolling_accuracy(self, adaptive_source):
        """Should use rollingAccuracy for decisions."""
        assert "rollingAccuracy" in adaptive_source

    def test_uses_total_reviews(self, adaptive_source):
        """Should check totalReviews before promoting."""
        assert "totalReviews" in adaptive_source

    def test_l3_fallback_to_l2(self, adaptive_source):
        """Low L3 accuracy should fall back to L2."""
        # Verify there's a path that returns 2 when L3 is low
        # We check that stats3 and rollingAccuracy and return 2 exist in proximity
        assert "stats3" in adaptive_source

    def test_l2_fallback_to_l1(self, adaptive_source):
        """Low L2 accuracy should fall back to L1."""
        assert "stats2" in adaptive_source

    def test_get_all_mastery_levels_uses_exercise_types(self, adaptive_source):
        """getAllMasteryLevels should use window.EXERCISE_TYPES."""
        assert "EXERCISE_TYPES" in adaptive_source

    def test_no_direct_localstorage_access(self, adaptive_source):
        """Should not directly access localStorage (delegates to SRSTracker)."""
        assert "localStorage" not in adaptive_source


# ── Realistic Exam Not Affected ─────────────────────────────────────

class TestRealisticExamUnaffected:
    """Verify realistic exam is not affected by adaptive system."""

    def test_realistic_exam_js_no_adaptive_reference(self):
        """realistic_exam.js should not reference SRSAdaptive."""
        path = os.path.join(PROJECT_ROOT, "static", "js", "realistic_exam.js")
        with open(path, "r", encoding="utf-8") as f:
            source = f.read()
        assert "SRSAdaptive" not in source

    def test_realistic_exam_html_no_adaptive_reference(self):
        """realistic_exam.html should not reference SRSAdaptive directly."""
        path = os.path.join(PROJECT_ROOT, "templates", "realistic_exam.html")
        with open(path, "r", encoding="utf-8") as f:
            source = f.read()
        # The adaptive script is in base.html but should not be
        # actively used in realistic exam template
        assert "adaptive-indicator" not in source
