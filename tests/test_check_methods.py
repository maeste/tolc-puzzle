"""Tests for the check() method across multiple exercise types.

Validates that check() correctly identifies right/wrong answers and returns
explanations for: analytic_geometry, statistics, inequalities, simplification.
"""
import pytest
from exercises.analytic_geometry import AnalyticGeometry
from exercises.statistics_exercise import StatisticsExercise
from exercises.inequalities import InequalitiesExercise
from exercises.simplification import SimplificationExercise


EXERCISE_CLASSES = [
    ("analytic_geo", AnalyticGeometry),
    ("statistics", StatisticsExercise),
    ("inequalities", InequalitiesExercise),
    ("simplification", SimplificationExercise),
]


@pytest.mark.parametrize("name,cls", EXERCISE_CLASSES)
class TestCheckCorrect:
    def test_correct_answer_returns_true(self, name, cls):
        ex = cls()
        for difficulty in [1, 2, 3]:
            for _ in range(3):
                exercise = ex.generate(difficulty)
                result = ex.check({
                    "answer": exercise["correct_index"],
                    "exercise": exercise,
                })
                assert result["correct"] is True, (
                    f"{name} d={difficulty}: check() should return True for correct answer"
                )

    def test_correct_index_echoed(self, name, cls):
        ex = cls()
        exercise = ex.generate(1)
        result = ex.check({
            "answer": exercise["correct_index"],
            "exercise": exercise,
        })
        assert result["correct_index"] == exercise["correct_index"]


@pytest.mark.parametrize("name,cls", EXERCISE_CLASSES)
class TestCheckWrong:
    def test_wrong_answer_returns_false(self, name, cls):
        ex = cls()
        for difficulty in [1, 2, 3]:
            exercise = ex.generate(difficulty)
            wrong_idx = (exercise["correct_index"] + 1) % len(exercise["options"])
            result = ex.check({
                "answer": wrong_idx,
                "exercise": exercise,
            })
            assert result["correct"] is False, (
                f"{name} d={difficulty}: check() should return False for wrong answer"
            )


@pytest.mark.parametrize("name,cls", EXERCISE_CLASSES)
class TestCheckExplanation:
    def test_explanation_present(self, name, cls):
        ex = cls()
        exercise = ex.generate(2)
        result = ex.check({
            "answer": exercise["correct_index"],
            "exercise": exercise,
        })
        assert "explanation" in result
        assert isinstance(result["explanation"], str)
        assert len(result["explanation"]) > 0


@pytest.mark.parametrize("name,cls", EXERCISE_CLASSES)
class TestCheckNoneAnswer:
    def test_none_answer_returns_false(self, name, cls):
        ex = cls()
        exercise = ex.generate(1)
        result = ex.check({
            "answer": None,
            "exercise": exercise,
        })
        assert result["correct"] is False
