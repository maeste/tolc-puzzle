import pytest
from exercises.statistics_exercise import StatisticsExercise


def test_generate_all_levels():
    ex = StatisticsExercise()
    for difficulty in [1, 2, 3]:
        for _ in range(10):
            result = ex.generate(difficulty)
            assert "question" in result
            assert "options" in result
            assert "correct_index" in result
            assert "explanation" in result
            assert len(result["options"]) >= 4
            assert 0 <= result["correct_index"] < len(result["options"])
            assert "approfondimento" in result


def test_approfondimento_flag():
    ex = StatisticsExercise()
    for _ in range(10):
        r1 = ex.generate(1)
        assert r1["approfondimento"] is False
        r2 = ex.generate(2)
        assert r2["approfondimento"] is False
        r3 = ex.generate(3)
        assert r3["approfondimento"] is True
