"""Tests for the SRS Scheduling Engine (static/js/srs_scheduler.js)."""

import os
import re
import pytest

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCHEDULER_PATH = os.path.join(PROJECT_ROOT, "static", "js", "srs_scheduler.js")
TRACKER_PATH = os.path.join(PROJECT_ROOT, "static", "js", "srs_tracker.js")
BASE_HTML_PATH = os.path.join(PROJECT_ROOT, "templates", "base.html")


@pytest.fixture(scope="module")
def scheduler_source():
    """Read the scheduler JS source once for all tests."""
    with open(SCHEDULER_PATH, "r", encoding="utf-8") as fh:
        return fh.read()


@pytest.fixture(scope="module")
def base_html_source():
    """Read base.html once for all tests."""
    with open(BASE_HTML_PATH, "r", encoding="utf-8") as fh:
        return fh.read()


# ===================================================================
# 1. File existence and basic validity
# ===================================================================

class TestFileExists:
    """Verify the JS file exists and is syntactically plausible."""

    def test_scheduler_file_exists(self):
        assert os.path.isfile(SCHEDULER_PATH), "srs_scheduler.js must exist"

    def test_scheduler_file_not_empty(self, scheduler_source):
        assert len(scheduler_source.strip()) > 100, "File should contain substantial code"

    def test_iife_pattern(self, scheduler_source):
        """Module should use an IIFE matching srs_tracker.js style."""
        assert "(function" in scheduler_source, "Should use IIFE pattern"
        assert "})();" in scheduler_source, "IIFE should be self-invoking"

    def test_use_strict(self, scheduler_source):
        assert '"use strict"' in scheduler_source, "Should use strict mode"


# ===================================================================
# 2. base.html integration
# ===================================================================

class TestBaseHtmlIntegration:
    """Verify the script tag is correctly placed in base.html."""

    def test_scheduler_script_tag_present(self, base_html_source):
        assert "srs_scheduler.js" in base_html_source, (
            "base.html must include srs_scheduler.js"
        )

    def test_scheduler_after_tracker(self, base_html_source):
        tracker_pos = base_html_source.index("srs_tracker.js")
        scheduler_pos = base_html_source.index("srs_scheduler.js")
        assert scheduler_pos > tracker_pos, (
            "srs_scheduler.js must be loaded AFTER srs_tracker.js"
        )

    def test_scheduler_before_block_scripts(self, base_html_source):
        scheduler_pos = base_html_source.index("srs_scheduler.js")
        block_pos = base_html_source.index("{% block scripts %}")
        assert scheduler_pos < block_pos, (
            "srs_scheduler.js must appear before the scripts block"
        )


# ===================================================================
# 3. Required API surface
# ===================================================================

class TestAPISurface:
    """Verify that all required API members are exposed."""

    def test_exposes_window_srs_scheduler(self, scheduler_source):
        assert "window.SRSScheduler" in scheduler_source

    def test_has_get_retention(self, scheduler_source):
        assert "getRetention" in scheduler_source

    def test_has_get_due_items(self, scheduler_source):
        assert "getDueItems" in scheduler_source

    def test_has_get_recommended_session(self, scheduler_source):
        assert "getRecommendedSession" in scheduler_source

    def test_has_get_summary(self, scheduler_source):
        assert "getSummary" in scheduler_source

    def test_has_retention_target(self, scheduler_source):
        assert "retentionTarget" in scheduler_source


# ===================================================================
# 4. Retrievability formula
# ===================================================================

class TestRetentionFormula:
    """Verify the FSRS-inspired formula is present."""

    def test_uses_math_exp(self, scheduler_source):
        assert "Math.exp" in scheduler_source, "Formula must use Math.exp"

    def test_formula_pattern(self, scheduler_source):
        """Check for the R(t) = e^(-t/S) pattern."""
        # Look for division of elapsed by stability inside Math.exp
        pattern = r"Math\.exp\s*\(\s*-\s*\w+\s*/\s*\w+\s*\)"
        assert re.search(pattern, scheduler_source), (
            "Should contain Math.exp(-elapsed/stability) pattern"
        )

    def test_stability_used(self, scheduler_source):
        assert "stability" in scheduler_source, "Formula must reference stability"

    def test_days_calculation(self, scheduler_source):
        """Should convert milliseconds to days (divide by ms-per-day)."""
        # 86400000 = 24*60*60*1000 or equivalent expressions
        has_ms_per_day = (
            "86400000" in scheduler_source
            or ("1000" in scheduler_source and "60" in scheduler_source and "24" in scheduler_source)
        )
        assert has_ms_per_day, "Must convert timestamps to days"


# ===================================================================
# 5. Interleaving logic
# ===================================================================

class TestInterleavingLogic:
    """Verify interleaving is implemented in getRecommendedSession."""

    def test_interleaving_type_check(self, scheduler_source):
        """Should compare types to avoid consecutive duplicates."""
        # Look for comparing lastType or similar pattern
        assert "lastType" in scheduler_source or "last_type" in scheduler_source or (
            "session[session.length - 1].type" in scheduler_source
        ), "Should track the last added type for interleaving"

    def test_deadlock_handling(self, scheduler_source):
        """Should handle the case where only one type remains."""
        # Look for a fallback pass allowing same type
        assert "deadlock" in scheduler_source.lower() or (
            scheduler_source.count("for") >= 2
            and "picked === -1" in scheduler_source
        ), "Should handle interleaving deadlock"


# ===================================================================
# 6. Retention target default
# ===================================================================

class TestRetentionTarget:

    def test_default_value_085(self, scheduler_source):
        assert "0.85" in scheduler_source, "Default retentionTarget should be 0.85"

    def test_retention_target_property(self, scheduler_source):
        pattern = r"retentionTarget\s*:\s*[\w_]+"
        match = re.search(pattern, scheduler_source)
        assert match, "retentionTarget should be set as a property"


# ===================================================================
# 7. New items handling
# ===================================================================

class TestNewItems:
    """Items never attempted should be treated as 'new' with R=0."""

    def test_new_item_retention_zero(self, scheduler_source):
        """New items should have retention 0."""
        # Pattern: setting retention to 0 for unseen items
        assert "retention: 0" in scheduler_source, (
            "New items (unseen) should have retention: 0"
        )

    def test_new_item_label(self, scheduler_source):
        assert '"new"' in scheduler_source, "New items should have reason 'new'"

    def test_enumerates_all_types(self, scheduler_source):
        """Should enumerate all exercise types x difficulties for completeness."""
        assert "DIFFICULTY_LEVELS" in scheduler_source or "DIFFICULTY" in scheduler_source, (
            "Should enumerate difficulty levels"
        )
        # Should iterate over types and difficulties
        assert "getExerciseTypes" in scheduler_source or "EXERCISE_TYPES" in scheduler_source


# ===================================================================
# 8. getSummary return fields
# ===================================================================

class TestGetSummaryFields:
    """Verify getSummary returns the expected fields."""

    def test_total_items_field(self, scheduler_source):
        assert "totalItems" in scheduler_source

    def test_overdue_count_field(self, scheduler_source):
        assert "overdueCount" in scheduler_source

    def test_new_count_field(self, scheduler_source):
        assert "newCount" in scheduler_source

    def test_avg_retention_field(self, scheduler_source):
        assert "avgRetention" in scheduler_source

    def test_next_due_in_field(self, scheduler_source):
        assert "nextDueIn" in scheduler_source


# ===================================================================
# 9. getDueItems sorting
# ===================================================================

class TestGetDueItemsSorting:
    """Verify items are sorted by retention ascending."""

    def test_sort_call_present(self, scheduler_source):
        assert ".sort(" in scheduler_source, "getDueItems must sort the items array"

    def test_sort_ascending(self, scheduler_source):
        """Sort comparator should sort by retention ascending."""
        pattern = r"\.sort\s*\(\s*function\s*\(\s*\w+\s*,\s*\w+\s*\)\s*\{[^}]*retention"
        assert re.search(pattern, scheduler_source), (
            "Sort comparator should reference retention"
        )

    def test_sort_a_minus_b(self, scheduler_source):
        """Ascending sort uses a.retention - b.retention."""
        assert "a.retention - b.retention" in scheduler_source, (
            "Should sort ascending: a.retention - b.retention"
        )


# ===================================================================
# 10. Edge cases
# ===================================================================

class TestEdgeCases:
    """Verify edge case handling."""

    def test_handles_no_srs_tracker(self, scheduler_source):
        """Should guard against SRSTracker not being available."""
        assert "window.SRSTracker" in scheduler_source
        # Should have a guard/check
        has_guard = (
            "!window.SRSTracker" in scheduler_source
            or "window.SRSTracker &&" in scheduler_source
        )
        assert has_guard, "Should guard against missing SRSTracker"

    def test_handles_zero_stability(self, scheduler_source):
        """Formula should handle stability <= 0."""
        assert "stability <= 0" in scheduler_source or "stability < " in scheduler_source

    def test_handles_infinity(self, scheduler_source):
        """Should handle Infinity for elapsed time (never reviewed)."""
        assert "Infinity" in scheduler_source or "isFinite" in scheduler_source

    def test_empty_session_request(self, scheduler_source):
        """getRecommendedSession(0) should return empty."""
        assert "n <= 0" in scheduler_source or "!n" in scheduler_source

    def test_overdue_flag(self, scheduler_source):
        """Items should have overdue boolean flag."""
        assert "overdue" in scheduler_source

    def test_math_log_for_next_due(self, scheduler_source):
        """getSummary should use Math.log to compute nextDueIn."""
        assert "Math.log" in scheduler_source, (
            "Should use Math.log to solve for time until threshold"
        )

    def test_exercise_types_fallback(self, scheduler_source):
        """Should have fallback exercise types list."""
        for exercise_type in ["solve", "geometry", "graph", "probability", "statistics"]:
            assert (
                '"%s"' % exercise_type in scheduler_source
                or "'%s'" % exercise_type in scheduler_source
            ), "Fallback list should include '%s'" % exercise_type

    def test_all_19_exercise_types(self, scheduler_source):
        """Should list all 19 exercise types in fallback."""
        expected_types = [
            "solve", "geometry", "graph", "word", "trap", "logic",
            "probability", "statistics", "always_true", "proportional",
            "cross_topic", "simplification", "inequalities", "analytic_geo",
            "number_sense", "which_satisfies", "estimation", "composition",
            "strategy"
        ]
        for et in expected_types:
            assert et in scheduler_source, "Missing exercise type: %s" % et

    def test_reason_values(self, scheduler_source):
        """Session items should use known reason values."""
        for reason in ["overdue", "new", "review", "practice"]:
            assert '"%s"' % reason in scheduler_source, (
                "Should use reason '%s'" % reason
            )

    def test_three_difficulty_levels(self, scheduler_source):
        """Should support difficulties 1, 2, 3."""
        assert "[1, 2, 3]" in scheduler_source or (
            "1" in scheduler_source and "2" in scheduler_source and "3" in scheduler_source
        )

    def test_lastReview_null_for_new(self, scheduler_source):
        """New items should have lastReview: null."""
        assert "lastReview: null" in scheduler_source

    def test_window_exercise_types_check(self, scheduler_source):
        """Should check for window.EXERCISE_TYPES before using fallback."""
        assert "EXERCISE_TYPES" in scheduler_source
        assert "Array.isArray" in scheduler_source or "typeof" in scheduler_source


# ===================================================================
# Bonus: structural integrity
# ===================================================================

class TestStructuralIntegrity:
    """Additional structural checks."""

    def test_no_import_statements(self, scheduler_source):
        """Should not use ES module imports (vanilla JS, loaded via script tag)."""
        assert "import " not in scheduler_source.split("/*")[0][:50]

    def test_no_require(self, scheduler_source):
        assert "require(" not in scheduler_source

    def test_depends_on_tracker_only(self, scheduler_source):
        """Should only depend on window.SRSTracker, not other modules."""
        # Should not reference other window globals besides SRSTracker, SRSScheduler, EXERCISE_TYPES
        window_refs = re.findall(r"window\.(\w+)", scheduler_source)
        allowed = {"SRSTracker", "SRSScheduler", "SRSReconsolidation", "EXERCISE_TYPES"}
        for ref in window_refs:
            assert ref in allowed, "Unexpected window dependency: window.%s" % ref
