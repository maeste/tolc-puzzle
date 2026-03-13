import pytest

from exercises.simplification import (
    SimplificationExercise,
    _t1_negative_exponents,
    _t1_common_factor,
    _t1_power_of_power,
    _t1_fraction_sum,
    _t2_log_simplification,
    _t2_notable_products,
    _t2_algebraic_fractions,
    _t3_nested_radicals,
    _t3_compound_algebraic,
    _t3_mixed_log_exp,
)


TEMPLATE_FUNCTIONS = [
    _t1_negative_exponents,
    _t1_common_factor,
    _t1_power_of_power,
    _t1_fraction_sum,
    _t2_log_simplification,
    _t2_notable_products,
    _t2_algebraic_fractions,
    _t3_nested_radicals,
    _t3_compound_algebraic,
    _t3_mixed_log_exp,
]


@pytest.mark.parametrize("template_fn", TEMPLATE_FUNCTIONS, ids=lambda f: f.__name__)
def test_template_no_exceptions(template_fn):
    """Each template must run 20 times without raising."""
    for _ in range(20):
        result = template_fn()
        assert result is not None


@pytest.mark.parametrize("template_fn", TEMPLATE_FUNCTIONS, ids=lambda f: f.__name__)
def test_template_returns_5_tuple(template_fn):
    """Each template must return (question, correct, distractors, explanation, tip)."""
    for _ in range(20):
        result = template_fn()
        assert isinstance(result, tuple), f"Expected tuple, got {type(result)}"
        assert len(result) == 5, f"Expected 5-tuple, got {len(result)}-tuple"

        question, correct, distractors, explanation, tip = result
        assert isinstance(question, str) and len(question) > 0
        assert isinstance(correct, str) and len(correct) > 0
        assert isinstance(distractors, list) and len(distractors) >= 4
        assert isinstance(explanation, str) and len(explanation) > 0
        assert isinstance(tip, str) and len(tip) > 0


@pytest.mark.parametrize("template_fn", TEMPLATE_FUNCTIONS, ids=lambda f: f.__name__)
def test_distractors_distinct_from_correct(template_fn):
    """Distractors must not contain the correct answer."""
    for _ in range(20):
        _, correct, distractors, _, _ = template_fn()
        for d in distractors:
            assert d != correct, (
                f"Distractor '{d}' matches correct answer '{correct}' "
                f"in {template_fn.__name__}"
            )


@pytest.mark.parametrize("template_fn", TEMPLATE_FUNCTIONS, ids=lambda f: f.__name__)
def test_question_format_italian(template_fn):
    """Question must contain the Italian simplification prompt."""
    for _ in range(5):
        question, _, _, _, _ = template_fn()
        assert "è uguale a:" in question, (
            f"Question missing 'è uguale a:' in {template_fn.__name__}: {question}"
        )


def test_generate_all_levels():
    """Exercise.generate must work for difficulty 1, 2, 3."""
    ex = SimplificationExercise()
    for difficulty in [1, 2, 3]:
        for _ in range(20):
            result = ex.generate(difficulty)
            assert "question" in result
            assert "options" in result
            assert "correct_index" in result
            assert "explanation" in result
            assert len(result["options"]) == 5
            assert 0 <= result["correct_index"] < len(result["options"])
            assert result["difficulty"] == difficulty


def test_options_are_unique():
    """All 5 options in a single exercise should be unique."""
    ex = SimplificationExercise()
    for difficulty in [1, 2, 3]:
        for _ in range(20):
            result = ex.generate(difficulty)
            options = result["options"]
            assert len(options) == len(set(options)), (
                f"Duplicate options found at difficulty {difficulty}: {options}"
            )


def test_difficulty_clamping():
    """Difficulty outside 1-3 should be clamped."""
    ex = SimplificationExercise()
    result = ex.generate(0)
    assert result["difficulty"] == 1
    result = ex.generate(5)
    assert result["difficulty"] == 3
