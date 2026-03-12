"""Tests for GraphReader injectivity, invertibility, codomain, and injectivity-intervals templates."""

import pytest

from exercises.graph_reader import GraphReader


REQUIRED_KEYS = {"question", "graph_data", "options", "correct_index", "explanation", "did_you_know"}

ITERATIONS = 10


@pytest.fixture
def reader():
    return GraphReader()


class TestTemplateInjectivity:
    """Tests for _template_injectivity."""

    def test_no_exceptions(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_injectivity()
            assert isinstance(result, dict)

    def test_required_keys(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_injectivity()
            assert REQUIRED_KEYS.issubset(result.keys()), (
                f"Missing keys: {REQUIRED_KEYS - result.keys()}"
            )

    def test_correct_index_valid(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_injectivity()
            assert 0 <= result["correct_index"] < len(result["options"])

    def test_five_options(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_injectivity()
            assert len(result["options"]) == 5

    def test_question_is_italian(self, reader):
        result = reader._template_injectivity()
        assert "iniettiva" in result["question"]


class TestTemplateInvertibility:
    """Tests for _template_invertibility."""

    def test_no_exceptions(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_invertibility()
            assert isinstance(result, dict)

    def test_required_keys(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_invertibility()
            assert REQUIRED_KEYS.issubset(result.keys()), (
                f"Missing keys: {REQUIRED_KEYS - result.keys()}"
            )

    def test_correct_index_valid(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_invertibility()
            assert 0 <= result["correct_index"] < len(result["options"])

    def test_five_options(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_invertibility()
            assert len(result["options"]) == 5

    def test_question_is_italian(self, reader):
        result = reader._template_invertibility()
        assert "invertibile" in result["question"]


class TestTemplateCodomain:
    """Tests for _template_codomain."""

    def test_no_exceptions(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_codomain()
            assert isinstance(result, dict)

    def test_required_keys(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_codomain()
            assert REQUIRED_KEYS.issubset(result.keys()), (
                f"Missing keys: {REQUIRED_KEYS - result.keys()}"
            )

    def test_correct_index_valid(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_codomain()
            assert 0 <= result["correct_index"] < len(result["options"])

    def test_five_options(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_codomain()
            assert len(result["options"]) == 5

    def test_question_is_italian(self, reader):
        result = reader._template_codomain()
        assert "immagine" in result["question"]


class TestTemplateInjectivityIntervals:
    """Tests for _template_injectivity_intervals."""

    def test_no_exceptions(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_injectivity_intervals()
            assert isinstance(result, dict)

    def test_required_keys(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_injectivity_intervals()
            assert REQUIRED_KEYS.issubset(result.keys()), (
                f"Missing keys: {REQUIRED_KEYS - result.keys()}"
            )

    def test_correct_index_valid(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_injectivity_intervals()
            assert 0 <= result["correct_index"] < len(result["options"])

    def test_five_options(self, reader):
        for _ in range(ITERATIONS):
            result = reader._template_injectivity_intervals()
            assert len(result["options"]) == 5

    def test_question_is_italian(self, reader):
        result = reader._template_injectivity_intervals()
        assert "iniettiva" in result["question"]


class TestGenerateIntegration:
    """Test that the new templates are reachable through generate()."""

    def test_generate_level2_no_exceptions(self, reader):
        """Run generate at L2 many times to exercise new templates."""
        for _ in range(50):
            result = reader.generate(difficulty=2)
            assert isinstance(result, dict)
            assert REQUIRED_KEYS.issubset(result.keys())
            assert 0 <= result["correct_index"] < len(result["options"])

    def test_generate_level3_no_exceptions(self, reader):
        """Run generate at L3 many times to exercise new templates."""
        for _ in range(50):
            result = reader.generate(difficulty=3)
            assert isinstance(result, dict)
            assert REQUIRED_KEYS.issubset(result.keys())
            assert 0 <= result["correct_index"] < len(result["options"])
