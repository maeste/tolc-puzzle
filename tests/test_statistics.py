import pytest
from exercises.statistics_exercise import StatisticsExercise


@pytest.fixture
def ex():
    return StatisticsExercise()


# ---------------------------------------------------------------------------
# Structure validation per difficulty level
# ---------------------------------------------------------------------------

class TestGenerateLevel1:
    def test_basic_structure(self, ex):
        for _ in range(20):
            result = ex.generate(1)
            assert "question" in result
            assert "options" in result
            assert "correct_index" in result
            assert "explanation" in result
            assert len(result["options"]) >= 4
            assert 0 <= result["correct_index"] < len(result["options"])

    def test_approfondimento_false(self, ex):
        for _ in range(10):
            result = ex.generate(1)
            assert result["approfondimento"] is False

    def test_difficulty_stored(self, ex):
        result = ex.generate(1)
        assert result["difficulty"] == 1


class TestGenerateLevel2:
    def test_basic_structure(self, ex):
        for _ in range(20):
            result = ex.generate(2)
            assert "question" in result
            assert "options" in result
            assert "correct_index" in result
            assert "explanation" in result
            assert len(result["options"]) >= 4
            assert 0 <= result["correct_index"] < len(result["options"])

    def test_approfondimento_false(self, ex):
        for _ in range(10):
            result = ex.generate(2)
            assert result["approfondimento"] is False

    def test_difficulty_stored(self, ex):
        result = ex.generate(2)
        assert result["difficulty"] == 2


class TestGenerateLevel3:
    def test_basic_structure(self, ex):
        for _ in range(20):
            result = ex.generate(3)
            assert "question" in result
            assert "options" in result
            assert "correct_index" in result
            assert "explanation" in result
            assert len(result["options"]) >= 4
            assert 0 <= result["correct_index"] < len(result["options"])

    def test_approfondimento_true(self, ex):
        for _ in range(10):
            result = ex.generate(3)
            assert result["approfondimento"] is True

    def test_difficulty_stored(self, ex):
        result = ex.generate(3)
        assert result["difficulty"] == 3


# ---------------------------------------------------------------------------
# Options quality
# ---------------------------------------------------------------------------

class TestOptionsQuality:
    def test_options_are_strings(self, ex):
        for difficulty in [1, 2, 3]:
            result = ex.generate(difficulty)
            for opt in result["options"]:
                assert isinstance(opt, str)

    def test_options_not_empty(self, ex):
        for difficulty in [1, 2, 3]:
            result = ex.generate(difficulty)
            for opt in result["options"]:
                assert len(opt.strip()) > 0

    def test_correct_answer_in_options(self, ex):
        for difficulty in [1, 2, 3]:
            for _ in range(10):
                result = ex.generate(difficulty)
                idx = result["correct_index"]
                assert idx < len(result["options"])


# ---------------------------------------------------------------------------
# Difficulty clamping
# ---------------------------------------------------------------------------

class TestDifficultyClamping:
    def test_clamp_below(self, ex):
        result = ex.generate(0)
        assert result["difficulty"] == 1

    def test_clamp_above(self, ex):
        result = ex.generate(5)
        assert result["difficulty"] == 3


# ---------------------------------------------------------------------------
# Template coverage (run many times)
# ---------------------------------------------------------------------------

class TestTemplateCoverage:
    def test_l1_many_runs(self, ex):
        """L1 has 8 templates — run enough times to hit most."""
        for _ in range(50):
            result = ex.generate(1)
            assert result is not None

    def test_l2_many_runs(self, ex):
        for _ in range(50):
            result = ex.generate(2)
            assert result is not None

    def test_l3_many_runs(self, ex):
        """L3 has 7 templates."""
        for _ in range(50):
            result = ex.generate(3)
            assert result is not None


# ---------------------------------------------------------------------------
# Graph reading templates (L1 includes histogram, pie chart, bar chart)
# ---------------------------------------------------------------------------

class TestGraphReadingTemplates:
    def test_l1_questions_contain_data(self, ex):
        """L1 templates should include data descriptions in the question."""
        for _ in range(30):
            result = ex.generate(1)
            # All L1 questions should mention data
            assert len(result["question"]) > 20

    def test_explanation_has_steps(self, ex):
        """Explanations should show calculation steps."""
        for _ in range(10):
            result = ex.generate(1)
            assert len(result["explanation"]) > 20


# ---------------------------------------------------------------------------
# check() method
# ---------------------------------------------------------------------------

class TestCheck:
    def test_correct_answer(self, ex):
        for difficulty in [1, 2, 3]:
            for _ in range(5):
                exercise = ex.generate(difficulty)
                result = ex.check({
                    "answer": exercise["correct_index"],
                    "exercise": exercise,
                })
                assert result["correct"] is True
                assert result["correct_index"] == exercise["correct_index"]
                assert "explanation" in result

    def test_wrong_answer(self, ex):
        for difficulty in [1, 2, 3]:
            exercise = ex.generate(difficulty)
            wrong_idx = (exercise["correct_index"] + 1) % len(exercise["options"])
            result = ex.check({
                "answer": wrong_idx,
                "exercise": exercise,
            })
            assert result["correct"] is False

    def test_explanation_returned(self, ex):
        exercise = ex.generate(2)
        result = ex.check({
            "answer": exercise["correct_index"],
            "exercise": exercise,
        })
        assert len(result["explanation"]) > 0
