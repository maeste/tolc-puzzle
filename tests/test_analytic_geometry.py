import pytest
from exercises.analytic_geometry import AnalyticGeometry


def test_generate_all_levels():
    ex = AnalyticGeometry()
    for difficulty in [1, 2, 3]:
        for _ in range(10):
            result = ex.generate(difficulty)
            assert "question" in result
            assert "options" in result
            assert "correct_index" in result
            assert "explanation" in result
            assert len(result["options"]) >= 4
            assert 0 <= result["correct_index"] < len(result["options"])
