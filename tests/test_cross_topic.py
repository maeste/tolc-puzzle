import pytest

from exercises.cross_topic import (
    CrossTopicExercise,
    _t1_algebra_geometry_area,
    _t2_quadratic_analytic_geo,
    _t2_probability_combinatorics,
    _t3_trig_geometry,
    _t3_functions_statistics,
)


ALL_TEMPLATES = [
    _t1_algebra_geometry_area,
    _t2_quadratic_analytic_geo,
    _t2_probability_combinatorics,
    _t3_trig_geometry,
    _t3_functions_statistics,
]


class TestTemplateFunctions:
    """Test each template function for correctness and format."""

    @pytest.mark.parametrize("template_fn", ALL_TEMPLATES)
    def test_template_no_exceptions(self, template_fn):
        """Each template should run without exceptions over 20 iterations."""
        for _ in range(20):
            result = template_fn()
            assert result is not None

    @pytest.mark.parametrize("template_fn", ALL_TEMPLATES)
    def test_template_returns_5_tuple(self, template_fn):
        """Each template must return a 5-tuple."""
        for _ in range(20):
            result = template_fn()
            assert isinstance(result, tuple), f"Expected tuple, got {type(result)}"
            assert len(result) == 5, f"Expected 5-tuple, got {len(result)}-tuple"

    @pytest.mark.parametrize("template_fn", ALL_TEMPLATES)
    def test_tuple_types(self, template_fn):
        """Check types: (str, str, list, str, str)."""
        for _ in range(10):
            question, correct_str, distractors, explanation, tip = template_fn()
            assert isinstance(question, str) and len(question) > 0
            assert isinstance(correct_str, str) and len(correct_str) > 0
            assert isinstance(distractors, list)
            assert len(distractors) >= 4
            assert isinstance(explanation, str) and len(explanation) > 0
            assert isinstance(tip, str) and len(tip) > 0

    @pytest.mark.parametrize("template_fn", ALL_TEMPLATES)
    def test_distractors_distinct_from_correct(self, template_fn):
        """All distractors must differ from the correct answer."""
        for _ in range(20):
            _, correct_str, distractors, _, _ = template_fn()
            for d in distractors:
                assert d != correct_str, (
                    f"Distractor '{d}' matches correct answer '{correct_str}'"
                )

    @pytest.mark.parametrize("template_fn", ALL_TEMPLATES)
    def test_distractors_are_distinct(self, template_fn):
        """All distractors must be distinct from each other."""
        for _ in range(20):
            _, _, distractors, _, _ = template_fn()
            assert len(set(distractors)) == len(distractors), (
                f"Duplicate distractors found: {distractors}"
            )


class TestCrossTopicExercise:
    """Test the CrossTopicExercise.generate() method."""

    @pytest.mark.parametrize("difficulty", [1, 2, 3])
    def test_generate_all_levels(self, difficulty):
        """generate() works for all difficulty levels."""
        ex = CrossTopicExercise()
        for _ in range(20):
            result = ex.generate(difficulty)
            assert "question" in result
            assert "options" in result
            assert "correct_index" in result
            assert "explanation" in result
            assert "did_you_know" in result
            assert len(result["options"]) >= 5
            assert 0 <= result["correct_index"] < len(result["options"])

    def test_generate_clamps_difficulty(self):
        """Difficulty outside 1-3 range is clamped."""
        ex = CrossTopicExercise()
        result_low = ex.generate(0)
        assert result_low["difficulty"] == 1
        result_high = ex.generate(5)
        assert result_high["difficulty"] == 3


class TestExplanationsCrossTopicMention:
    """Explanations and tips should mention both topic areas."""

    def test_t1_mentions_algebra_and_geometry(self):
        for _ in range(10):
            _, _, _, explanation, tip = _t1_algebra_geometry_area()
            combined = (explanation + " " + tip).lower()
            assert "algebra" in combined or "equazion" in combined
            assert "geometri" in combined or "area" in combined

    def test_t2_quadratic_mentions_both_topics(self):
        for _ in range(10):
            _, _, _, explanation, tip = _t2_quadratic_analytic_geo()
            combined = (explanation + " " + tip).lower()
            assert "algebra" in combined or "equazion" in combined or "sistema" in combined
            assert "geometria analitica" in combined or "vertice" in combined or "parabola" in combined

    def test_t2_probability_mentions_both_topics(self):
        for _ in range(10):
            _, _, _, explanation, tip = _t2_probability_combinatorics()
            combined = (explanation + " " + tip).lower()
            assert "combinatoric" in combined or "combinazion" in combined
            assert "probabilit" in combined

    def test_t3_trig_mentions_both_topics(self):
        for _ in range(10):
            _, _, _, explanation, tip = _t3_trig_geometry()
            combined = (explanation + " " + tip).lower()
            assert "trigonometri" in combined or "sin" in combined or "cos" in combined
            assert "geometri" in combined or "area" in combined

    def test_t3_functions_mentions_both_topics(self):
        for _ in range(10):
            _, _, _, explanation, tip = _t3_functions_statistics()
            combined = (explanation + " " + tip).lower()
            assert "funzion" in combined or "valutazion" in combined
            assert "statistic" in combined or "media" in combined
