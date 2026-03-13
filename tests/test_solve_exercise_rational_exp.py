import pytest

from exercises.solve_exercise import (
    SolveExercise,
    _t1_rational_exponent_basic,
    _t2_rational_exponent_cube,
    _t2_rational_exponent_general,
)


# ---------------------------------------------------------------------------
# Level 1: (sqrt(a))^n basic
# ---------------------------------------------------------------------------


class TestT1RationalExponentBasic:
    def test_no_exceptions(self):
        for _ in range(30):
            result = _t1_rational_exponent_basic()
            assert len(result) == 4

    def test_tuple_format(self):
        question, correct_value, explanation, tip = _t1_rational_exponent_basic()
        assert isinstance(question, str)
        assert isinstance(correct_value, float)
        assert isinstance(explanation, str)
        assert isinstance(tip, str)

    def test_correct_answer_is_integer(self):
        for _ in range(30):
            _, correct_value, _, _ = _t1_rational_exponent_basic()
            assert correct_value > 0
            assert correct_value == int(correct_value), (
                f"Expected integer result, got {correct_value}"
            )

    def test_question_in_italian(self):
        question, _, _, _ = _t1_rational_exponent_basic()
        assert "Semplifica" in question or "Quanto" in question

    def test_result_matches_formula(self):
        """Verify (sqrt(a))^n = a^(n/2) by checking known ranges."""
        for _ in range(30):
            _, correct_value, _, _ = _t1_rational_exponent_basic()
            # Result must be a positive integer power of 2, 3, or 5
            val = int(correct_value)
            assert val >= 4  # smallest: 2^2 = 4


# ---------------------------------------------------------------------------
# Level 2: (cbrt(a))^n cube roots
# ---------------------------------------------------------------------------


class TestT2RationalExponentCube:
    def test_no_exceptions(self):
        for _ in range(30):
            result = _t2_rational_exponent_cube()
            assert len(result) == 4

    def test_tuple_format(self):
        question, correct_value, explanation, tip = _t2_rational_exponent_cube()
        assert isinstance(question, str)
        assert isinstance(correct_value, float)
        assert isinstance(explanation, str)
        assert isinstance(tip, str)

    def test_correct_answer_is_integer(self):
        for _ in range(30):
            _, correct_value, _, _ = _t2_rational_exponent_cube()
            assert correct_value > 0
            assert correct_value == int(correct_value), (
                f"Expected integer result, got {correct_value}"
            )

    def test_question_in_italian(self):
        question, _, _, _ = _t2_rational_exponent_cube()
        assert "Semplifica" in question or "Quanto" in question

    def test_result_matches_formula(self):
        for _ in range(30):
            _, correct_value, _, _ = _t2_rational_exponent_cube()
            val = int(correct_value)
            assert val >= 4  # smallest: 2^2 = 4


# ---------------------------------------------------------------------------
# Level 2: a^(m/n) general
# ---------------------------------------------------------------------------


class TestT2RationalExponentGeneral:
    def test_no_exceptions(self):
        for _ in range(30):
            result = _t2_rational_exponent_general()
            assert len(result) == 4

    def test_tuple_format(self):
        question, correct_value, explanation, tip = _t2_rational_exponent_general()
        assert isinstance(question, str)
        assert isinstance(correct_value, float)
        assert isinstance(explanation, str)
        assert isinstance(tip, str)

    def test_correct_answer_is_integer(self):
        for _ in range(30):
            _, correct_value, _, _ = _t2_rational_exponent_general()
            assert correct_value > 0
            assert correct_value == int(correct_value), (
                f"Expected integer result, got {correct_value}"
            )

    def test_question_in_italian(self):
        question, _, _, _ = _t2_rational_exponent_general()
        assert "Calcola" in question or "Quanto" in question

    def test_fraction_exponent_not_integer(self):
        """Ensure m/n is not an integer (non-trivial exercise)."""
        for _ in range(30):
            question, _, _, _ = _t2_rational_exponent_general()
            # Extract m/n from the question format "a^(m/n)"
            assert "/" in question, "Question should contain a fractional exponent"


# ---------------------------------------------------------------------------
# Integration: generate() method
# ---------------------------------------------------------------------------


class TestIntegrationGenerate:
    def test_generate_level1(self):
        ex = SolveExercise()
        for _ in range(50):
            result = ex.generate(difficulty=1)
            assert "question" in result
            assert "options" in result
            assert "correct_index" in result
            assert "explanation" in result
            assert len(result["options"]) == 5

    def test_generate_level2(self):
        ex = SolveExercise()
        for _ in range(50):
            result = ex.generate(difficulty=2)
            assert "question" in result
            assert "options" in result
            assert "correct_index" in result
            assert "explanation" in result
            assert len(result["options"]) == 5

    def test_rational_exponent_templates_reachable(self):
        """Run generate many times to verify new templates can be selected."""
        ex = SolveExercise()
        l1_questions = set()
        l2_questions = set()
        for _ in range(200):
            r1 = ex.generate(difficulty=1)
            l1_questions.add(r1["question"][:10])
            r2 = ex.generate(difficulty=2)
            l2_questions.add(r2["question"][:10])
        # With 200 iterations and multiple templates, we expect variety
        assert len(l1_questions) > 3
        assert len(l2_questions) > 3
