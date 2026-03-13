import pytest

from exercises.always_true import (
    AlwaysTrueExercise,
    _t1_square_sum,
    _t1_fraction_distribution,
    _t1_root_sum,
    _t2_am_gm,
    _t2_absolute_value,
    _t2_power_inequality,
    _t3_divisibility,
    _t3_log_inequality,
)


ALL_TEMPLATES = [
    _t1_square_sum,
    _t1_fraction_distribution,
    _t1_root_sum,
    _t2_am_gm,
    _t2_absolute_value,
    _t2_power_inequality,
    _t3_divisibility,
    _t3_log_inequality,
]


class TestTemplateFormats:
    """Each template must return a 5-tuple with correct types."""

    @pytest.mark.parametrize("template_fn", ALL_TEMPLATES)
    def test_returns_5_tuple(self, template_fn):
        for _ in range(20):
            result = template_fn()
            assert isinstance(result, tuple), f"{template_fn.__name__} must return a tuple"
            assert len(result) == 5, f"{template_fn.__name__} must return 5-tuple, got {len(result)}"

    @pytest.mark.parametrize("template_fn", ALL_TEMPLATES)
    def test_tuple_types(self, template_fn):
        for _ in range(5):
            question, correct, distractors, explanation, tip = template_fn()
            assert isinstance(question, str) and len(question) > 0
            assert isinstance(correct, str) and len(correct) > 0
            assert isinstance(distractors, list) and len(distractors) >= 3
            assert isinstance(explanation, str) and len(explanation) > 0
            assert isinstance(tip, str) and len(tip) > 0

    @pytest.mark.parametrize("template_fn", ALL_TEMPLATES)
    def test_distractors_distinct_from_correct(self, template_fn):
        for _ in range(10):
            _question, correct, distractors, _expl, _tip = template_fn()
            for d in distractors:
                assert d != correct, (
                    f"{template_fn.__name__}: distractor '{d}' equals correct '{correct}'"
                )

    @pytest.mark.parametrize("template_fn", ALL_TEMPLATES)
    def test_no_exceptions(self, template_fn):
        """Run 20 iterations to catch random-dependent edge cases."""
        for _ in range(20):
            template_fn()  # should not raise


class TestAlwaysTrueExercise:
    """Test the AlwaysTrueExercise.generate() method."""

    def test_generate_difficulty_1(self):
        ex = AlwaysTrueExercise()
        for _ in range(20):
            result = ex.generate(1)
            assert "question" in result
            assert "options" in result
            assert "correct_index" in result
            assert "explanation" in result
            assert len(result["options"]) >= 4
            assert 0 <= result["correct_index"] < len(result["options"])

    def test_generate_difficulty_2(self):
        ex = AlwaysTrueExercise()
        for _ in range(20):
            result = ex.generate(2)
            assert "question" in result
            assert "options" in result
            assert "correct_index" in result
            assert len(result["options"]) >= 4
            assert 0 <= result["correct_index"] < len(result["options"])

    def test_generate_difficulty_3(self):
        ex = AlwaysTrueExercise()
        for _ in range(20):
            result = ex.generate(3)
            assert "question" in result
            assert "options" in result
            assert "correct_index" in result
            assert len(result["options"]) >= 4
            assert 0 <= result["correct_index"] < len(result["options"])

    def test_correct_answer_in_options(self):
        """The correct answer must be present in options at correct_index."""
        ex = AlwaysTrueExercise()
        for difficulty in [1, 2, 3]:
            for _ in range(10):
                result = ex.generate(difficulty)
                idx = result["correct_index"]
                assert idx < len(result["options"])
                # The option at correct_index should be a non-empty string
                assert len(result["options"][idx]) > 0

    def test_difficulty_clamping(self):
        """Difficulty values outside 1-3 should be clamped."""
        ex = AlwaysTrueExercise()
        result_low = ex.generate(0)
        assert result_low["difficulty"] == 1
        result_high = ex.generate(5)
        assert result_high["difficulty"] == 3

    def test_did_you_know_present(self):
        """The tip should be stored in did_you_know."""
        ex = AlwaysTrueExercise()
        for difficulty in [1, 2, 3]:
            result = ex.generate(difficulty)
            assert "did_you_know" in result
            assert len(result["did_you_know"]) > 0

    def test_check_correct_answer(self):
        """Check method should validate correct answers."""
        ex = AlwaysTrueExercise()
        for difficulty in [1, 2, 3]:
            exercise_data = ex.generate(difficulty)
            correct_idx = exercise_data["correct_index"]
            result = ex.check({"answer": correct_idx, "exercise": exercise_data})
            assert result["correct"] is True

    def test_check_wrong_answer(self):
        """Check method should reject wrong answers."""
        ex = AlwaysTrueExercise()
        for difficulty in [1, 2, 3]:
            exercise_data = ex.generate(difficulty)
            correct_idx = exercise_data["correct_index"]
            wrong_idx = (correct_idx + 1) % len(exercise_data["options"])
            result = ex.check({"answer": wrong_idx, "exercise": exercise_data})
            assert result["correct"] is False
