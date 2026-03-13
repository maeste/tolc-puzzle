"""Tests for GraphReader parameter-effect templates (TOLC-55)."""

import pytest

from exercises.graph_reader import GraphReader


REQUIRED_KEYS = {"question", "graph_data", "options", "correct_index", "explanation", "did_you_know"}

ITERATIONS = 15


@pytest.fixture
def reader():
    return GraphReader()


# ---------------------------------------------------------------------------
# Structural helpers
# ---------------------------------------------------------------------------

def _validate_result(result):
    """Common structural assertions for every template result."""
    assert isinstance(result, dict)
    assert REQUIRED_KEYS.issubset(result.keys()), (
        f"Missing keys: {REQUIRED_KEYS - result.keys()}"
    )
    assert 0 <= result["correct_index"] < len(result["options"])
    assert len(result["options"]) == 5
    assert "<svg" in result["graph_data"]
    assert "</svg>" in result["graph_data"]
    # options must be distinct
    assert len(set(result["options"])) == len(result["options"]), "Options are not distinct"


def _has_multiple_curves(svg_text):
    """Check that SVG contains at least two polyline elements (two curves)."""
    return svg_text.count("<polyline") >= 2


# ---------------------------------------------------------------------------
# Template: _template_param_quadratic_a
# ---------------------------------------------------------------------------

class TestParamQuadraticA:
    def test_no_exceptions(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_param_quadratic_a()
            _validate_result(result)

    def test_question_italian(self, reader):
        result = reader._template_param_quadratic_a()
        assert "grafico" in result["question"].lower() or "grafici" in result["question"].lower()

    def test_two_curves(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_param_quadratic_a()
            assert _has_multiple_curves(result["graph_data"]), "SVG should contain two curves"

    def test_correct_answer_content(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_param_quadratic_a()
            correct = result["options"][result["correct_index"]]
            assert "stringe" in correct.lower() or "stretta" in correct.lower()


# ---------------------------------------------------------------------------
# Template: _template_param_vertical_shift
# ---------------------------------------------------------------------------

class TestParamVerticalShift:
    def test_no_exceptions(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_param_vertical_shift()
            _validate_result(result)

    def test_question_italian(self, reader):
        result = reader._template_param_vertical_shift()
        assert "traslazione" in result["question"].lower()

    def test_two_curves(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_param_vertical_shift()
            assert _has_multiple_curves(result["graph_data"])

    def test_correct_answer_mentions_direction(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_param_vertical_shift()
            correct = result["options"][result["correct_index"]]
            assert "alto" in correct or "basso" in correct


# ---------------------------------------------------------------------------
# Template: _template_param_horizontal_shift
# ---------------------------------------------------------------------------

class TestParamHorizontalShift:
    def test_no_exceptions(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_param_horizontal_shift()
            _validate_result(result)

    def test_question_italian(self, reader):
        result = reader._template_param_horizontal_shift()
        assert "traslazione" in result["question"].lower()

    def test_two_curves(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_param_horizontal_shift()
            assert _has_multiple_curves(result["graph_data"])

    def test_correct_answer_mentions_direction(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_param_horizontal_shift()
            correct = result["options"][result["correct_index"]]
            assert "destra" in correct or "sinistra" in correct


# ---------------------------------------------------------------------------
# Template: _template_param_vertical_stretch
# ---------------------------------------------------------------------------

class TestParamVerticalStretch:
    def test_no_exceptions(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_param_vertical_stretch()
            _validate_result(result)

    def test_question_italian(self, reader):
        result = reader._template_param_vertical_stretch()
        assert "trasformazione" in result["question"].lower()

    def test_two_curves(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_param_vertical_stretch()
            assert _has_multiple_curves(result["graph_data"])

    def test_correct_answer_mentions_dilation(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_param_vertical_stretch()
            correct = result["options"][result["correct_index"]]
            assert "dilatazione verticale" in correct.lower()


# ---------------------------------------------------------------------------
# Template: _template_param_reflection
# ---------------------------------------------------------------------------

class TestParamReflection:
    def test_no_exceptions(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_param_reflection()
            _validate_result(result)

    def test_question_italian(self, reader):
        result = reader._template_param_reflection()
        assert "trasformazione" in result["question"].lower()

    def test_two_curves(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_param_reflection()
            assert _has_multiple_curves(result["graph_data"])

    def test_correct_answer_mentions_reflection(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_param_reflection()
            correct = result["options"][result["correct_index"]]
            assert "riflessione" in correct.lower()


# ---------------------------------------------------------------------------
# Template: _template_param_combined
# ---------------------------------------------------------------------------

class TestParamCombined:
    def test_no_exceptions(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_param_combined()
            _validate_result(result)

    def test_question_italian(self, reader):
        result = reader._template_param_combined()
        assert "formula" in result["question"].lower() or "grafico" in result["question"].lower()

    def test_two_curves(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_param_combined()
            assert _has_multiple_curves(result["graph_data"])

    def test_correct_answer_is_expression(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_param_combined()
            correct = result["options"][result["correct_index"]]
            assert "y = " in correct


# ---------------------------------------------------------------------------
# Template: _template_param_family_effect
# ---------------------------------------------------------------------------

class TestParamFamilyEffect:
    def test_no_exceptions(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_param_family_effect()
            _validate_result(result)

    def test_question_italian(self, reader):
        result = reader._template_param_family_effect()
        q = result["question"].lower()
        assert "grafici" in q or "osserva" in q or "cambia" in q

    def test_two_curves(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_param_family_effect()
            assert _has_multiple_curves(result["graph_data"])


# ---------------------------------------------------------------------------
# Template: _template_param_identify_formula
# ---------------------------------------------------------------------------

class TestParamIdentifyFormula:
    def test_no_exceptions(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_param_identify_formula()
            _validate_result(result)

    def test_question_italian(self, reader):
        result = reader._template_param_identify_formula()
        assert "formula" in result["question"].lower() or "grafico" in result["question"].lower()

    def test_single_curve_svg(self, reader):
        """This template shows one graph, not two."""
        for _ in range(ITERATIONS):
            result = reader._template_param_identify_formula()
            assert "<svg" in result["graph_data"]

    def test_correct_answer_is_expression(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_param_identify_formula()
            correct = result["options"][result["correct_index"]]
            assert "y = " in correct or "f(x) = " in correct


# ---------------------------------------------------------------------------
# Integration: generate() picks parameter templates
# ---------------------------------------------------------------------------

class TestGenerateIntegration:
    """Verify generate() can produce parameter-effect exercises at all levels."""

    def test_generate_level1_no_crash(self, reader):
        """Level 1 generation should never crash, even with param templates."""
        for _ in range(50):
            result = reader.generate(1)
            assert isinstance(result, dict)
            assert "question" in result
            assert "options" in result
            assert "graph_data" in result

    def test_generate_level2_no_crash(self, reader):
        for _ in range(50):
            result = reader.generate(2)
            assert isinstance(result, dict)
            assert "question" in result

    def test_generate_level3_no_crash(self, reader):
        for _ in range(50):
            result = reader.generate(3)
            assert isinstance(result, dict)
            assert "question" in result

    def test_svg_well_formed(self, reader):
        """All SVGs from generate() must be well-formed."""
        for difficulty in [1, 2, 3]:
            for _ in range(20):
                result = reader.generate(difficulty)
                svg = result.get("graph_data", "")
                if svg:
                    assert "<svg" in svg
                    assert "</svg>" in svg

    def test_correct_index_bounds_all_levels(self, reader):
        for difficulty in [1, 2, 3]:
            for _ in range(20):
                result = reader.generate(difficulty)
                assert 0 <= result["correct_index"] < len(result["options"])

    def test_options_distinct_all_levels(self, reader):
        for difficulty in [1, 2, 3]:
            for _ in range(20):
                result = reader.generate(difficulty)
                opts = result["options"]
                assert len(set(opts)) == len(opts), f"Duplicate options at L{difficulty}: {opts}"


# ---------------------------------------------------------------------------
# Multi-curve SVG validation
# ---------------------------------------------------------------------------

class TestMultiCurveSVG:
    """Verify that comparison templates produce SVGs with multiple stroke colors."""

    def test_different_stroke_colors(self, reader):
        """Templates that compare two functions should use different colors."""
        templates = [
            reader._template_param_quadratic_a,
            reader._template_param_vertical_shift,
            reader._template_param_horizontal_shift,
            reader._template_param_vertical_stretch,
            reader._template_param_reflection,
            reader._template_param_combined,
            reader._template_param_family_effect,
        ]
        for tmpl in templates:
            result = tmpl()
            svg = result["graph_data"]
            assert '#2563eb' in svg or '#dc2626' in svg, (
                f"SVG from {tmpl.__name__} should contain colored curves"
            )
            assert svg.count("<polyline") >= 2, (
                f"SVG from {tmpl.__name__} should have at least 2 polylines"
            )
