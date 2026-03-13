import math

import pytest

from exercises.solve_exercise import (
    SolveExercise,
    _t1_exp_basic,
    _t1_log_basic,
    _t2_exp_equation_different_bases,
    _t2_log_properties,
    _t3_log_domain,
    _t3_exp_inequality,
)


# ---------------------------------------------------------------------------
# Level 1 template tests
# ---------------------------------------------------------------------------


class TestT1ExpBasic:
    def test_no_exceptions(self):
        for _ in range(20):
            result = _t1_exp_basic()
            assert len(result) == 4

    def test_tuple_format(self):
        question, correct_value, explanation, tip = _t1_exp_basic()
        assert isinstance(question, str)
        assert isinstance(correct_value, float)
        assert isinstance(explanation, str)
        assert isinstance(tip, str)

    def test_correct_answer(self):
        for _ in range(20):
            question, correct_value, explanation, tip = _t1_exp_basic()
            assert correct_value > 0
            assert correct_value == int(correct_value)  # integer solution


class TestT1LogBasic:
    def test_no_exceptions(self):
        for _ in range(20):
            result = _t1_log_basic()
            assert len(result) == 4

    def test_tuple_format(self):
        question, correct_value, explanation, tip = _t1_log_basic()
        assert isinstance(question, str)
        assert isinstance(correct_value, float)
        assert isinstance(explanation, str)
        assert isinstance(tip, str)

    def test_correct_answer(self):
        for _ in range(20):
            question, correct_value, explanation, tip = _t1_log_basic()
            assert correct_value > 0
            assert correct_value == int(correct_value)  # integer solution


# ---------------------------------------------------------------------------
# Level 2 template tests
# ---------------------------------------------------------------------------


class TestT2ExpEquationDifferentBases:
    def test_no_exceptions(self):
        for _ in range(20):
            result = _t2_exp_equation_different_bases()
            assert len(result) == 4

    def test_tuple_format(self):
        question, correct_value, explanation, tip = _t2_exp_equation_different_bases()
        assert isinstance(question, str)
        assert isinstance(correct_value, float)
        assert isinstance(explanation, str)
        assert isinstance(tip, str)

    def test_correct_answer(self):
        for _ in range(20):
            question, correct_value, explanation, tip = _t2_exp_equation_different_bases()
            assert correct_value > 0


class TestT2LogProperties:
    def test_no_exceptions(self):
        for _ in range(20):
            result = _t2_log_properties()
            assert len(result) == 4

    def test_tuple_format(self):
        question, correct_value, explanation, tip = _t2_log_properties()
        assert isinstance(question, str)
        assert isinstance(correct_value, float)
        assert isinstance(explanation, str)
        assert isinstance(tip, str)

    def test_answer_is_number(self):
        for _ in range(20):
            question, correct_value, explanation, tip = _t2_log_properties()
            assert isinstance(correct_value, (int, float))
            assert math.isfinite(correct_value)


# ---------------------------------------------------------------------------
# Level 3 template tests
# ---------------------------------------------------------------------------


class TestT3LogDomain:
    def test_no_exceptions(self):
        for _ in range(20):
            result = _t3_log_domain()
            assert len(result) == 4

    def test_tuple_format(self):
        question, correct_value, explanation, tip = _t3_log_domain()
        assert isinstance(question, str)
        assert isinstance(correct_value, float)
        assert isinstance(explanation, str)
        assert isinstance(tip, str)

    def test_answer_is_float(self):
        for _ in range(20):
            question, correct_value, explanation, tip = _t3_log_domain()
            assert isinstance(correct_value, float)
            assert math.isfinite(correct_value)


class TestT3ExpInequality:
    def test_no_exceptions(self):
        for _ in range(20):
            result = _t3_exp_inequality()
            assert len(result) == 4

    def test_tuple_format(self):
        question, correct_value, explanation, tip = _t3_exp_inequality()
        assert isinstance(question, str)
        assert isinstance(correct_value, float)
        assert isinstance(explanation, str)
        assert isinstance(tip, str)

    def test_answer_is_positive(self):
        for _ in range(20):
            question, correct_value, explanation, tip = _t3_exp_inequality()
            assert correct_value > 0
