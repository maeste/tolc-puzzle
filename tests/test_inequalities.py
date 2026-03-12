import pytest

from exercises.inequalities import InequalitiesExercise


def test_generate_all_levels():
    ex = InequalitiesExercise()
    for difficulty in [1, 2, 3]:
        for _ in range(10):
            result = ex.generate(difficulty)
            assert "question" in result
            assert "options" in result
            assert "correct_index" in result
            assert "explanation" in result
            assert len(result["options"]) >= 4
            assert 0 <= result["correct_index"] < len(result["options"])


def test_interval_notation():
    """Verify answers contain interval notation symbols."""
    ex = InequalitiesExercise()
    for _ in range(20):
        result = ex.generate(2)
        correct = result["options"][result["correct_index"]]
        # Should contain interval notation
        assert any(s in correct for s in ["\u2208", "\u2200", "Nessuna", "x ="]), (
            f"Bad answer format: {correct}"
        )


def test_level1_interval_notation():
    """Level 1 answers should use interval notation."""
    ex = InequalitiesExercise()
    for _ in range(20):
        result = ex.generate(1)
        correct = result["options"][result["correct_index"]]
        assert any(s in correct for s in ["\u2208", "\u2200", "Nessuna"]), (
            f"Bad answer format for level 1: {correct}"
        )


def test_level3_interval_notation():
    """Level 3 answers should use interval notation."""
    ex = InequalitiesExercise()
    for _ in range(20):
        result = ex.generate(3)
        correct = result["options"][result["correct_index"]]
        assert any(s in correct for s in ["\u2208", "\u2200", "Nessuna", "x ="]), (
            f"Bad answer format for level 3: {correct}"
        )


def test_options_are_unique():
    """All options in a single exercise should be unique."""
    ex = InequalitiesExercise()
    for difficulty in [1, 2, 3]:
        for _ in range(10):
            result = ex.generate(difficulty)
            options = result["options"]
            assert len(options) == len(set(options)), (
                f"Duplicate options found: {options}"
            )


def test_difficulty_clamping():
    """Difficulty outside 1-3 should be clamped."""
    ex = InequalitiesExercise()
    result = ex.generate(0)
    assert result["difficulty"] == 1
    result = ex.generate(5)
    assert result["difficulty"] == 3
