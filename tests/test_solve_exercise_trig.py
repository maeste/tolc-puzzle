import math

import pytest

from exercises.solve_exercise import (
    SolveExercise,
    _t1_trig_notable_values,
    _t1_trig_basic_identity,
    _t2_trig_equation_simple,
    _t2_trig_expression,
    _t2_trig_convert_deg_rad,
    _t3_trig_equation_parametric,
    _t3_trig_simplification,
)


# ---------------------------------------------------------------------------
# Level 1 template tests
# ---------------------------------------------------------------------------


class TestT1TrigNotableValues:
    def test_no_exceptions(self):
        for _ in range(20):
            result = _t1_trig_notable_values()
            assert len(result) == 5

    def test_tuple_format(self):
        question, correct_str, distractors, explanation, tip = _t1_trig_notable_values()
        assert isinstance(question, str)
        assert isinstance(correct_str, str)
        assert isinstance(distractors, list)
        assert isinstance(explanation, str)
        assert isinstance(tip, str)

    def test_distractors_not_empty(self):
        for _ in range(10):
            _, _, distractors, _, _ = _t1_trig_notable_values()
            assert len(distractors) >= 1

    def test_correct_not_in_distractors(self):
        for _ in range(10):
            _, correct_str, distractors, _, _ = _t1_trig_notable_values()
            assert correct_str not in distractors

    def test_question_contains_trig_function(self):
        for _ in range(10):
            question, _, _, _, _ = _t1_trig_notable_values()
            assert any(f in question for f in ["sin", "cos", "tan"])


class TestT1TrigBasicIdentity:
    def test_no_exceptions(self):
        for _ in range(20):
            result = _t1_trig_basic_identity()
            assert len(result) == 5

    def test_tuple_format(self):
        question, correct_str, distractors, explanation, tip = _t1_trig_basic_identity()
        assert isinstance(question, str)
        assert isinstance(correct_str, str)
        assert isinstance(distractors, list)
        assert isinstance(explanation, str)
        assert isinstance(tip, str)

    def test_distractors_not_empty(self):
        for _ in range(10):
            _, _, distractors, _, _ = _t1_trig_basic_identity()
            assert len(distractors) >= 1

    def test_correct_not_in_distractors(self):
        for _ in range(10):
            _, correct_str, distractors, _, _ = _t1_trig_basic_identity()
            assert correct_str not in distractors

    def test_question_mentions_identity(self):
        for _ in range(10):
            question, _, _, _, _ = _t1_trig_basic_identity()
            assert "sin" in question or "cos" in question


# ---------------------------------------------------------------------------
# Level 2 template tests
# ---------------------------------------------------------------------------


class TestT2TrigEquationSimple:
    def test_no_exceptions(self):
        for _ in range(20):
            result = _t2_trig_equation_simple()
            assert len(result) == 4

    def test_tuple_format(self):
        question, correct_value, explanation, tip = _t2_trig_equation_simple()
        assert isinstance(question, str)
        assert isinstance(correct_value, float)
        assert isinstance(explanation, str)
        assert isinstance(tip, str)

    def test_answer_is_valid_solution_count(self):
        for _ in range(20):
            _, correct_value, _, _ = _t2_trig_equation_simple()
            assert correct_value in (1.0, 2.0)


class TestT2TrigExpression:
    def test_no_exceptions(self):
        for _ in range(20):
            result = _t2_trig_expression()
            assert len(result) == 4

    def test_tuple_format(self):
        question, correct_value, explanation, tip = _t2_trig_expression()
        assert isinstance(question, str)
        assert isinstance(correct_value, float)
        assert isinstance(explanation, str)
        assert isinstance(tip, str)

    def test_answer_is_finite(self):
        for _ in range(20):
            _, correct_value, _, _ = _t2_trig_expression()
            assert math.isfinite(correct_value)


class TestT2TrigConvertDegRad:
    def test_no_exceptions(self):
        for _ in range(30):
            result = _t2_trig_convert_deg_rad()
            assert len(result) in (4, 5)

    def test_deg_to_rad_variant(self):
        """Run enough times to hit the deg-to-rad variant (5-tuple)."""
        found_5 = False
        for _ in range(50):
            result = _t2_trig_convert_deg_rad()
            if len(result) == 5:
                found_5 = True
                question, correct_str, distractors, explanation, tip = result
                assert isinstance(question, str)
                assert isinstance(correct_str, str)
                assert isinstance(distractors, list)
                assert isinstance(explanation, str)
                assert isinstance(tip, str)
                assert len(distractors) >= 1
                assert correct_str not in distractors
                break
        assert found_5, "Never hit the 5-tuple (deg-to-rad) variant in 50 iterations"

    def test_rad_to_deg_variant(self):
        """Run enough times to hit the rad-to-deg variant (4-tuple)."""
        found_4 = False
        for _ in range(50):
            result = _t2_trig_convert_deg_rad()
            if len(result) == 4:
                found_4 = True
                question, correct_value, explanation, tip = result
                assert isinstance(question, str)
                assert isinstance(correct_value, float)
                assert isinstance(explanation, str)
                assert isinstance(tip, str)
                assert correct_value > 0
                break
        assert found_4, "Never hit the 4-tuple (rad-to-deg) variant in 50 iterations"


# ---------------------------------------------------------------------------
# Level 3 template tests
# ---------------------------------------------------------------------------


class TestT3TrigEquationParametric:
    def test_no_exceptions(self):
        for _ in range(20):
            result = _t3_trig_equation_parametric()
            assert len(result) == 4

    def test_tuple_format(self):
        question, correct_value, explanation, tip = _t3_trig_equation_parametric()
        assert isinstance(question, str)
        assert isinstance(correct_value, float)
        assert isinstance(explanation, str)
        assert isinstance(tip, str)

    def test_answer_is_finite(self):
        for _ in range(20):
            _, correct_value, _, _ = _t3_trig_equation_parametric()
            assert math.isfinite(correct_value)


class TestT3TrigSimplification:
    def test_no_exceptions(self):
        for _ in range(20):
            result = _t3_trig_simplification()
            assert len(result) == 4

    def test_tuple_format(self):
        question, correct_value, explanation, tip = _t3_trig_simplification()
        assert isinstance(question, str)
        assert isinstance(correct_value, float)
        assert isinstance(explanation, str)
        assert isinstance(tip, str)

    def test_answer_is_finite(self):
        for _ in range(20):
            _, correct_value, _, _ = _t3_trig_simplification()
            assert math.isfinite(correct_value)

    def test_answer_is_positive(self):
        for _ in range(20):
            _, correct_value, _, _ = _t3_trig_simplification()
            assert correct_value > 0


# ---------------------------------------------------------------------------
# Integration: full generate() tests for trig exercises
# ---------------------------------------------------------------------------


class TestSolveExerciseTrigIntegration:
    def test_generate_all_levels(self):
        ex = SolveExercise()
        for level in [1, 2, 3]:
            for _ in range(30):
                result = ex.generate(level)
                assert "question" in result
                assert "options" in result
                assert "correct_index" in result
                assert len(result["options"]) >= 4
                assert 0 <= result["correct_index"] < len(result["options"])
