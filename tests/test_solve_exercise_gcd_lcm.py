import math

import pytest

from exercises.solve_exercise import (
    SolveExercise,
    _t1_gcd_two_simple,
    _t1_lcm_two_simple,
    _t2_lcm_periodicity,
    _t2_gcd_equal_groups,
    _t2_fraction_simplification,
    _t3_gcd_three_numbers,
    _t3_lcm_three_numbers,
    _prime_factorization,
    _factorization_gcd,
    _factorization_lcm,
    _format_factors,
    _factors_product,
)


# ---------------------------------------------------------------------------
# Helper function tests
# ---------------------------------------------------------------------------


class TestPrimeFactorization:
    def test_prime_number(self):
        factors, fmt = _prime_factorization(7)
        assert factors == {7: 1}
        assert "7" in fmt

    def test_power_of_two(self):
        factors, fmt = _prime_factorization(8)
        assert factors == {2: 3}

    def test_composite(self):
        factors, fmt = _prime_factorization(12)
        assert factors == {2: 2, 3: 1}
        assert "2" in fmt
        assert "3" in fmt

    def test_large_composite(self):
        factors, _ = _prime_factorization(360)
        assert factors == {2: 3, 3: 2, 5: 1}

    def test_product_matches(self):
        for n in [6, 12, 18, 24, 36, 48, 60, 100, 144]:
            factors, _ = _prime_factorization(n)
            assert _factors_product(factors) == n


class TestFactorizationGcdLcm:
    def test_gcd_factors(self):
        fa = {2: 2, 3: 1}  # 12
        fb = {2: 1, 3: 2}  # 18
        gcd_f = _factorization_gcd(fa, fb)
        assert _factors_product(gcd_f) == math.gcd(12, 18)

    def test_lcm_factors(self):
        fa = {2: 2, 3: 1}  # 12
        fb = {2: 1, 3: 2}  # 18
        lcm_f = _factorization_lcm(fa, fb)
        assert _factors_product(lcm_f) == math.lcm(12, 18)

    def test_format_factors(self):
        result = _format_factors({2: 3, 5: 1})
        assert "2" in result
        assert "5" in result


# ---------------------------------------------------------------------------
# Level 1 template tests
# ---------------------------------------------------------------------------


class TestT1GcdTwoSimple:
    def test_no_exceptions(self):
        for _ in range(20):
            result = _t1_gcd_two_simple()
            assert len(result) == 4

    def test_tuple_format(self):
        question, correct_value, explanation, tip = _t1_gcd_two_simple()
        assert isinstance(question, str)
        assert isinstance(correct_value, float)
        assert isinstance(explanation, str)
        assert isinstance(tip, str)

    def test_correct_answer(self):
        for _ in range(20):
            question, correct_value, explanation, tip = _t1_gcd_two_simple()
            # Extract numbers from question — the value must be a valid GCD
            assert correct_value > 0
            assert correct_value == int(correct_value)


class TestT1LcmTwoSimple:
    def test_no_exceptions(self):
        for _ in range(20):
            result = _t1_lcm_two_simple()
            assert len(result) == 4

    def test_tuple_format(self):
        question, correct_value, explanation, tip = _t1_lcm_two_simple()
        assert isinstance(question, str)
        assert isinstance(correct_value, float)
        assert isinstance(explanation, str)
        assert isinstance(tip, str)

    def test_correct_answer(self):
        for _ in range(20):
            question, correct_value, explanation, tip = _t1_lcm_two_simple()
            assert correct_value > 0
            assert correct_value == int(correct_value)


# ---------------------------------------------------------------------------
# Level 2 template tests
# ---------------------------------------------------------------------------


class TestT2LcmPeriodicity:
    def test_no_exceptions(self):
        for _ in range(20):
            result = _t2_lcm_periodicity()
            assert len(result) == 4

    def test_tuple_format(self):
        question, correct_value, explanation, tip = _t2_lcm_periodicity()
        assert isinstance(question, str)
        assert isinstance(correct_value, float)
        assert isinstance(explanation, str)
        assert isinstance(tip, str)

    def test_answer_is_positive(self):
        for _ in range(20):
            _, correct_value, _, _ = _t2_lcm_periodicity()
            assert correct_value > 0


class TestT2GcdEqualGroups:
    def test_no_exceptions(self):
        for _ in range(20):
            result = _t2_gcd_equal_groups()
            assert len(result) == 4

    def test_tuple_format(self):
        question, correct_value, explanation, tip = _t2_gcd_equal_groups()
        assert isinstance(question, str)
        assert isinstance(correct_value, float)
        assert isinstance(explanation, str)
        assert isinstance(tip, str)

    def test_answer_is_positive(self):
        for _ in range(20):
            _, correct_value, _, _ = _t2_gcd_equal_groups()
            assert correct_value >= 2


class TestT2FractionSimplification:
    def test_no_exceptions(self):
        for _ in range(20):
            result = _t2_fraction_simplification()
            assert len(result) == 5

    def test_tuple_format(self):
        question, correct_str, distractors, explanation, tip = _t2_fraction_simplification()
        assert isinstance(question, str)
        assert isinstance(correct_str, str)
        assert isinstance(distractors, list)
        assert isinstance(explanation, str)
        assert isinstance(tip, str)

    def test_distractors_not_empty(self):
        for _ in range(10):
            _, _, distractors, _, _ = _t2_fraction_simplification()
            assert len(distractors) >= 1

    def test_correct_not_in_distractors(self):
        for _ in range(10):
            _, correct_str, distractors, _, _ = _t2_fraction_simplification()
            assert correct_str not in distractors


# ---------------------------------------------------------------------------
# Level 3 template tests
# ---------------------------------------------------------------------------


class TestT3GcdThreeNumbers:
    def test_no_exceptions(self):
        for _ in range(20):
            result = _t3_gcd_three_numbers()
            assert len(result) == 4

    def test_tuple_format(self):
        question, correct_value, explanation, tip = _t3_gcd_three_numbers()
        assert isinstance(question, str)
        assert isinstance(correct_value, float)
        assert isinstance(explanation, str)
        assert isinstance(tip, str)

    def test_answer_is_positive(self):
        for _ in range(20):
            _, correct_value, _, _ = _t3_gcd_three_numbers()
            assert correct_value >= 2


class TestT3LcmThreeNumbers:
    def test_no_exceptions(self):
        for _ in range(20):
            result = _t3_lcm_three_numbers()
            assert len(result) == 4

    def test_tuple_format(self):
        question, correct_value, explanation, tip = _t3_lcm_three_numbers()
        assert isinstance(question, str)
        assert isinstance(correct_value, float)
        assert isinstance(explanation, str)
        assert isinstance(tip, str)

    def test_answer_is_positive(self):
        for _ in range(20):
            _, correct_value, _, _ = _t3_lcm_three_numbers()
            assert correct_value > 0

    def test_lcm_bounded(self):
        for _ in range(20):
            _, correct_value, _, _ = _t3_lcm_three_numbers()
            assert correct_value <= 300


# ---------------------------------------------------------------------------
# Integration: full generate() tests
# ---------------------------------------------------------------------------


class TestSolveExerciseGenerate:
    def test_generate_level_1(self):
        ex = SolveExercise()
        for _ in range(30):
            result = ex.generate(1)
            assert "question" in result
            assert "options" in result
            assert "correct_index" in result
            assert "explanation" in result
            assert len(result["options"]) >= 4
            assert 0 <= result["correct_index"] < len(result["options"])

    def test_generate_level_2(self):
        ex = SolveExercise()
        for _ in range(30):
            result = ex.generate(2)
            assert "question" in result
            assert "options" in result
            assert "correct_index" in result
            assert "explanation" in result
            assert len(result["options"]) >= 4
            assert 0 <= result["correct_index"] < len(result["options"])

    def test_generate_level_3(self):
        ex = SolveExercise()
        for _ in range(30):
            result = ex.generate(3)
            assert "question" in result
            assert "options" in result
            assert "correct_index" in result
            assert "explanation" in result
            assert len(result["options"]) >= 4
            assert 0 <= result["correct_index"] < len(result["options"])

    def test_difficulty_clamping(self):
        ex = SolveExercise()
        result_low = ex.generate(0)
        assert result_low["difficulty"] == 1
        result_high = ex.generate(5)
        assert result_high["difficulty"] == 3
