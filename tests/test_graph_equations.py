"""Tests for GraphReader functional equation/inequality templates."""

import pytest

from exercises.graph_reader import GraphReader


REQUIRED_KEYS = {"question", "graph_data", "options", "correct_index", "explanation", "did_you_know"}

ITERATIONS = 20


@pytest.fixture
def reader():
    return GraphReader()


# ---------------------------------------------------------------------------
# _template_equation_simple (Level 1)
# ---------------------------------------------------------------------------

class TestTemplateEquationSimple:
    """Tests for _template_equation_simple."""

    def test_no_exceptions(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_equation_simple()
            assert isinstance(result, dict)

    def test_required_keys(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_equation_simple()
            assert REQUIRED_KEYS.issubset(result.keys()), (
                f"Missing keys: {REQUIRED_KEYS - result.keys()}"
            )

    def test_svg_present(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_equation_simple()
            assert result["graph_data"].startswith("<svg")
            assert result["graph_data"].endswith("</svg>")

    def test_five_options(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_equation_simple()
            assert len(result["options"]) == 5

    def test_correct_index_valid(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_equation_simple()
            assert 0 <= result["correct_index"] < len(result["options"])

    def test_dashed_line_in_svg(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_equation_simple()
            assert "stroke-dasharray" in result["graph_data"]

    def test_question_in_italian(self, reader):
        result = reader._template_equation_simple()
        assert "f(x) =" in result["question"]
        assert "Osserva" in result["question"]

    def test_options_are_distinct(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_equation_simple()
            assert len(set(result["options"])) == len(result["options"])


# ---------------------------------------------------------------------------
# _template_equation_count (Level 1)
# ---------------------------------------------------------------------------

class TestTemplateEquationCount:
    """Tests for _template_equation_count."""

    def test_no_exceptions(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_equation_count()
            assert isinstance(result, dict)

    def test_required_keys(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_equation_count()
            assert REQUIRED_KEYS.issubset(result.keys()), (
                f"Missing keys: {REQUIRED_KEYS - result.keys()}"
            )

    def test_svg_present(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_equation_count()
            assert result["graph_data"].startswith("<svg")
            assert result["graph_data"].endswith("</svg>")

    def test_five_options(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_equation_count()
            assert len(result["options"]) == 5

    def test_correct_index_valid(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_equation_count()
            assert 0 <= result["correct_index"] < len(result["options"])

    def test_correct_answer_is_count(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_equation_count()
            correct = result["options"][result["correct_index"]]
            assert "soluzion" in correct.lower() or "nessuna" in correct.lower()

    def test_dashed_line_in_svg(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_equation_count()
            assert "stroke-dasharray" in result["graph_data"]


# ---------------------------------------------------------------------------
# _template_inequality_interval (Level 2)
# ---------------------------------------------------------------------------

class TestTemplateInequalityInterval:
    """Tests for _template_inequality_interval."""

    def test_no_exceptions(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_inequality_interval()
            assert isinstance(result, dict)

    def test_required_keys(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_inequality_interval()
            assert REQUIRED_KEYS.issubset(result.keys()), (
                f"Missing keys: {REQUIRED_KEYS - result.keys()}"
            )

    def test_svg_present(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_inequality_interval()
            assert result["graph_data"].startswith("<svg")

    def test_five_options(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_inequality_interval()
            assert len(result["options"]) == 5

    def test_correct_index_valid(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_inequality_interval()
            assert 0 <= result["correct_index"] < len(result["options"])

    def test_question_has_inequality(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_inequality_interval()
            assert ">" in result["question"] or "<" in result["question"]

    def test_correct_answer_has_interval(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_inequality_interval()
            correct = result["options"][result["correct_index"]]
            assert "\u2208" in correct  # ∈


# ---------------------------------------------------------------------------
# _template_inequality_sign (Level 2)
# ---------------------------------------------------------------------------

class TestTemplateInequalitySign:
    """Tests for _template_inequality_sign."""

    def test_no_exceptions(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_inequality_sign()
            assert isinstance(result, dict)

    def test_required_keys(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_inequality_sign()
            assert REQUIRED_KEYS.issubset(result.keys()), (
                f"Missing keys: {REQUIRED_KEYS - result.keys()}"
            )

    def test_svg_present(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_inequality_sign()
            assert result["graph_data"].startswith("<svg")

    def test_five_options(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_inequality_sign()
            assert len(result["options"]) == 5

    def test_correct_index_valid(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_inequality_sign()
            assert 0 <= result["correct_index"] < len(result["options"])

    def test_question_references_zero(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_inequality_sign()
            assert "0" in result["question"]

    def test_axis_highlight_in_svg(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_inequality_sign()
            assert "stroke-dasharray" in result["graph_data"]


# ---------------------------------------------------------------------------
# _template_equation_two_functions (Level 3)
# ---------------------------------------------------------------------------

class TestTemplateEquationTwoFunctions:
    """Tests for _template_equation_two_functions."""

    def test_no_exceptions(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_equation_two_functions()
            assert isinstance(result, dict)

    def test_required_keys(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_equation_two_functions()
            assert REQUIRED_KEYS.issubset(result.keys()), (
                f"Missing keys: {REQUIRED_KEYS - result.keys()}"
            )

    def test_svg_present(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_equation_two_functions()
            assert result["graph_data"].startswith("<svg")

    def test_five_options(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_equation_two_functions()
            assert len(result["options"]) == 5

    def test_correct_index_valid(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_equation_two_functions()
            assert 0 <= result["correct_index"] < len(result["options"])

    def test_two_curves_in_svg(self, reader):
        """SVG should contain at least 2 polyline elements (two curves)."""
        for _ in range(ITERATIONS):
            result = reader._template_equation_two_functions()
            svg = result["graph_data"]
            polyline_count = svg.count("<polyline")
            assert polyline_count >= 2, f"Expected >=2 polylines, got {polyline_count}"

    def test_question_mentions_both_functions(self, reader):
        result = reader._template_equation_two_functions()
        assert "f(x)" in result["question"]
        assert "g(x)" in result["question"]


# ---------------------------------------------------------------------------
# _template_inequality_two_functions (Level 3)
# ---------------------------------------------------------------------------

class TestTemplateInequalityTwoFunctions:
    """Tests for _template_inequality_two_functions."""

    def test_no_exceptions(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_inequality_two_functions()
            assert isinstance(result, dict)

    def test_required_keys(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_inequality_two_functions()
            assert REQUIRED_KEYS.issubset(result.keys()), (
                f"Missing keys: {REQUIRED_KEYS - result.keys()}"
            )

    def test_svg_present(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_inequality_two_functions()
            assert result["graph_data"].startswith("<svg")

    def test_five_options(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_inequality_two_functions()
            assert len(result["options"]) == 5

    def test_correct_index_valid(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_inequality_two_functions()
            assert 0 <= result["correct_index"] < len(result["options"])

    def test_correct_answer_has_interval(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_inequality_two_functions()
            correct = result["options"][result["correct_index"]]
            assert "\u2208" in correct or "Tutti" in correct or "Nessun" in correct

    def test_question_has_inequality(self, reader):
        result = reader._template_inequality_two_functions()
        assert ">" in result["question"]


# ---------------------------------------------------------------------------
# _template_equation_solutions_range (Level 3)
# ---------------------------------------------------------------------------

class TestTemplateEquationSolutionsRange:
    """Tests for _template_equation_solutions_range."""

    def test_no_exceptions(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_equation_solutions_range()
            assert isinstance(result, dict)

    def test_required_keys(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_equation_solutions_range()
            assert REQUIRED_KEYS.issubset(result.keys()), (
                f"Missing keys: {REQUIRED_KEYS - result.keys()}"
            )

    def test_svg_present(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_equation_solutions_range()
            assert result["graph_data"].startswith("<svg")

    def test_five_options(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_equation_solutions_range()
            assert len(result["options"]) == 5

    def test_correct_index_valid(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_equation_solutions_range()
            assert 0 <= result["correct_index"] < len(result["options"])

    def test_question_mentions_interval(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_equation_solutions_range()
            assert "intervallo" in result["question"].lower()

    def test_vertical_boundaries_in_svg(self, reader):
        """SVG should have vertical dashed lines for interval boundaries."""
        for _ in range(ITERATIONS):
            result = reader._template_equation_solutions_range()
            svg = result["graph_data"]
            assert svg.count("stroke-dasharray") >= 2

    def test_correct_answer_is_count(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_equation_solutions_range()
            correct = result["options"][result["correct_index"]]
            assert "soluzion" in correct.lower() or "nessuna" in correct.lower()


# ---------------------------------------------------------------------------
# Integration: generate() at all difficulty levels
# ---------------------------------------------------------------------------

class TestGenerateIntegration:
    """Test that generate() can produce equation/inequality templates."""

    def test_generate_level1_no_crash(self, reader):
        for _ in range(50):
            result = reader.generate(1)
            assert isinstance(result, dict)
            assert "question" in result
            assert "options" in result
            assert "correct_index" in result

    def test_generate_level2_no_crash(self, reader):
        for _ in range(50):
            result = reader.generate(2)
            assert isinstance(result, dict)
            assert "question" in result
            assert "options" in result
            assert "correct_index" in result

    def test_generate_level3_no_crash(self, reader):
        for _ in range(50):
            result = reader.generate(3)
            assert isinstance(result, dict)
            assert "question" in result
            assert "options" in result
            assert "correct_index" in result

    def test_generate_correct_index_always_valid(self, reader):
        for difficulty in [1, 2, 3]:
            for _ in range(30):
                result = reader.generate(difficulty)
                assert 0 <= result["correct_index"] < len(result["options"])


# ---------------------------------------------------------------------------
# Helper method tests
# ---------------------------------------------------------------------------

class TestHelperMethods:
    """Tests for static helper methods on GraphReader."""

    def test_format_x_set_single(self):
        assert GraphReader._format_x_set([3]) == "x = 3"

    def test_format_x_set_multiple(self):
        result = GraphReader._format_x_set([-2, 3])
        assert result == "x = -2, x = 3"

    def test_format_x_set_sorts(self):
        result = GraphReader._format_x_set([3, -2])
        assert result == "x = -2, x = 3"

    def test_nice_int_integer(self):
        assert GraphReader._nice_int(3.0) == 3
        assert GraphReader._nice_int(3.001) == 3
        assert GraphReader._nice_int(-2.0) == -2

    def test_nice_int_float(self):
        assert GraphReader._nice_int(3.7) == 3.7

    def test_add_horizontal_line(self):
        from exercises.graph_reader import _build_svg, _linear
        func = _linear(1, 0)
        svg = _build_svg(func, (-5, 5), (-5, 5))
        result = GraphReader._add_horizontal_line(svg, 2, (-5, 5), (-5, 5))
        assert "stroke-dasharray" in result
        assert "y = 2" in result
        assert result.endswith("</svg>")

    def test_find_intersections_linear(self):
        """A linear function y=x should cross y=2 at x=2."""
        func = lambda x: x
        crossings = GraphReader._find_intersections_with_value(func, 2.0, (-5, 5))
        assert len(crossings) == 1
        assert abs(crossings[0] - 2.0) < 0.2

    def test_find_intersections_quadratic(self):
        """y = x^2 should cross y=4 at x=-2 and x=2."""
        func = lambda x: x * x
        crossings = GraphReader._find_intersections_with_value(func, 4.0, (-5, 5))
        assert len(crossings) == 2
        assert abs(crossings[0] - (-2.0)) < 0.2
        assert abs(crossings[1] - 2.0) < 0.2

    def test_find_intersections_no_crossing(self):
        """y = x^2 should not cross y=-1."""
        func = lambda x: x * x
        crossings = GraphReader._find_intersections_with_value(func, -1.0, (-5, 5))
        assert len(crossings) == 0
