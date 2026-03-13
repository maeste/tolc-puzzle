"""Tests for GraphReader inverse templates (given graph, answer question)."""

import pytest

from exercises.graph_reader import GraphReader


REQUIRED_KEYS = {"question", "graph_data", "options", "correct_index", "explanation", "did_you_know"}

ITERATIONS = 20


@pytest.fixture
def reader():
    return GraphReader()


class TestTemplateInversePreimage:
    """Tests for _template_inverse_preimage."""

    def test_no_exceptions(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_inverse_preimage()
            assert isinstance(result, dict)

    def test_required_keys(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_inverse_preimage()
            assert REQUIRED_KEYS.issubset(result.keys()), (
                f"Missing keys: {REQUIRED_KEYS - result.keys()}"
            )

    def test_svg_present(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_inverse_preimage()
            assert result["graph_data"].startswith("<svg")

    def test_five_options(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_inverse_preimage()
            assert len(result["options"]) == 5

    def test_correct_index_valid(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_inverse_preimage()
            assert 0 <= result["correct_index"] < len(result["options"])


class TestTemplateInverseSign:
    """Tests for _template_inverse_sign."""

    def test_no_exceptions(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_inverse_sign()
            assert isinstance(result, dict)

    def test_required_keys(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_inverse_sign()
            assert REQUIRED_KEYS.issubset(result.keys()), (
                f"Missing keys: {REQUIRED_KEYS - result.keys()}"
            )

    def test_svg_present(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_inverse_sign()
            assert result["graph_data"].startswith("<svg")

    def test_five_options(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_inverse_sign()
            assert len(result["options"]) == 5

    def test_correct_index_valid(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_inverse_sign()
            assert 0 <= result["correct_index"] < len(result["options"])


class TestTemplateInverseIncreasing:
    """Tests for _template_inverse_increasing."""

    def test_no_exceptions(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_inverse_increasing()
            assert isinstance(result, dict)

    def test_required_keys(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_inverse_increasing()
            assert REQUIRED_KEYS.issubset(result.keys()), (
                f"Missing keys: {REQUIRED_KEYS - result.keys()}"
            )

    def test_svg_present(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_inverse_increasing()
            assert result["graph_data"].startswith("<svg")

    def test_five_options(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_inverse_increasing()
            assert len(result["options"]) == 5

    def test_correct_index_valid(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_inverse_increasing()
            assert 0 <= result["correct_index"] < len(result["options"])


class TestTemplateInverseMaxMin:
    """Tests for _template_inverse_max_min."""

    def test_no_exceptions(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_inverse_max_min()
            assert isinstance(result, dict)

    def test_required_keys(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_inverse_max_min()
            assert REQUIRED_KEYS.issubset(result.keys()), (
                f"Missing keys: {REQUIRED_KEYS - result.keys()}"
            )

    def test_svg_present(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_inverse_max_min()
            assert result["graph_data"].startswith("<svg")

    def test_five_options(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_inverse_max_min()
            assert len(result["options"]) == 5

    def test_correct_index_valid(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_inverse_max_min()
            assert 0 <= result["correct_index"] < len(result["options"])


class TestTemplateInverseRange:
    """Tests for _template_inverse_range."""

    def test_no_exceptions(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_inverse_range()
            assert isinstance(result, dict)

    def test_required_keys(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_inverse_range()
            assert REQUIRED_KEYS.issubset(result.keys()), (
                f"Missing keys: {REQUIRED_KEYS - result.keys()}"
            )

    def test_svg_present(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_inverse_range()
            assert result["graph_data"].startswith("<svg")

    def test_five_options(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_inverse_range()
            assert len(result["options"]) == 5

    def test_correct_index_valid(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_inverse_range()
            assert 0 <= result["correct_index"] < len(result["options"])


class TestTemplateInverseIntersections:
    """Tests for _template_inverse_intersections."""

    def test_no_exceptions(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_inverse_intersections()
            assert isinstance(result, dict)

    def test_required_keys(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_inverse_intersections()
            assert REQUIRED_KEYS.issubset(result.keys()), (
                f"Missing keys: {REQUIRED_KEYS - result.keys()}"
            )

    def test_svg_present(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_inverse_intersections()
            assert result["graph_data"].startswith("<svg")

    def test_svg_has_horizontal_line(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_inverse_intersections()
            assert "stroke-dasharray" in result["graph_data"]
            assert "y =" in result["graph_data"]

    def test_five_options(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_inverse_intersections()
            assert len(result["options"]) == 5

    def test_correct_index_valid(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_inverse_intersections()
            assert 0 <= result["correct_index"] < len(result["options"])


class TestGenerateIntegrationInverse:
    """Test that inverse templates are reachable through generate()."""

    def test_generate_level2_no_exceptions(self, reader):
        """Run generate at L2 many times to exercise inverse templates."""
        for _ in range(50):
            result = reader.generate(difficulty=2)
            assert isinstance(result, dict)
            assert REQUIRED_KEYS.issubset(result.keys())
            assert 0 <= result["correct_index"] < len(result["options"])

    def test_generate_level3_no_exceptions(self, reader):
        """Run generate at L3 many times to exercise inverse templates."""
        for _ in range(50):
            result = reader.generate(difficulty=3)
            assert isinstance(result, dict)
            assert REQUIRED_KEYS.issubset(result.keys())
            assert 0 <= result["correct_index"] < len(result["options"])
