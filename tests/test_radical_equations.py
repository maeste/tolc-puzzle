"""Tests for radical equation templates in solve_exercise.py."""

import math
import re

import pytest

from exercises.solve_exercise import (
    SolveExercise,
    _t2_solve_radical_simple,
    _t2_solve_radical_linear,
    _t3_solve_radical_two_radicals,
    _t3_solve_radical_extraneous,
)


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _parse_x_value(s):
    """Extract numeric x value from strings like 'x = 4' or 'x = -2'."""
    m = re.search(r"x\s*=\s*(-?\d+)", s)
    if m:
        return int(m.group(1))
    return None


def _eval_expr_at_x(expr_str, x_val):
    """Evaluate a math expression string at a given x value.

    Handles implicit multiplication like '2x' -> '2*x'.
    """
    s = expr_str.strip()
    # Insert * between digit and x: "2x" -> "2*x"
    s = re.sub(r"(\d)(x)", r"\1*\2", s)
    s = s.replace("x", f"({x_val})")
    return eval(s)


# ---------------------------------------------------------------------------
# _t2_solve_radical_simple tests
# ---------------------------------------------------------------------------

class TestT2SolveRadicalSimple:
    """Tests for _t2_solve_radical_simple (5-tuple string template)."""

    def test_returns_5_tuple(self):
        result = _t2_solve_radical_simple()
        assert len(result) == 5

    def test_tuple_types(self):
        question, correct_str, distractors, explanation, tip = _t2_solve_radical_simple()
        assert isinstance(question, str)
        assert isinstance(correct_str, str)
        assert isinstance(distractors, list)
        assert isinstance(explanation, str)
        assert isinstance(tip, str)

    def test_distractors_count(self):
        _, _, distractors, _, _ = _t2_solve_radical_simple()
        assert len(distractors) == 4

    def test_distractors_are_strings(self):
        _, _, distractors, _, _ = _t2_solve_radical_simple()
        for d in distractors:
            assert isinstance(d, str)

    def test_correct_not_in_distractors(self):
        _, correct_str, distractors, _, _ = _t2_solve_radical_simple()
        assert correct_str not in distractors

    def test_solution_satisfies_equation(self):
        """Verify the solution actually satisfies sqrt(ax+b) = c."""
        for _ in range(20):
            question, correct_str, _, _, _ = _t2_solve_radical_simple()
            x_val = _parse_x_value(correct_str)
            assert x_val is not None, f"Could not parse x from '{correct_str}'"
            # Extract c from question: "... = {c}"
            m = re.search(r"=\s*(\d+)\s*$", question)
            assert m is not None
            c = int(m.group(1))
            # Extract radicand coefficients from question
            # The radicand is inside sqrt(...)
            rad_m = re.search(r"√\((.+?)\)", question)
            assert rad_m is not None
            radicand_str = rad_m.group(1)
            # Evaluate radicand at x_val
            radicand_val = _eval_expr_at_x(radicand_str, x_val)
            assert radicand_val >= 0, "Domain violated"
            assert abs(math.sqrt(radicand_val) - c) < 1e-9, "Solution incorrect"

    def test_no_crash_multiple_runs(self):
        """Run 15 times to verify no crashes."""
        for _ in range(15):
            result = _t2_solve_radical_simple()
            assert len(result) == 5

    def test_question_in_italian(self):
        question, _, _, _, _ = _t2_solve_radical_simple()
        assert "Risolvi" in question


# ---------------------------------------------------------------------------
# _t2_solve_radical_linear tests
# ---------------------------------------------------------------------------

class TestT2SolveRadicalLinear:
    """Tests for _t2_solve_radical_linear (5-tuple string template)."""

    def test_returns_5_tuple(self):
        result = _t2_solve_radical_linear()
        assert len(result) == 5

    def test_tuple_types(self):
        question, correct_str, distractors, explanation, tip = _t2_solve_radical_linear()
        assert isinstance(question, str)
        assert isinstance(correct_str, str)
        assert isinstance(distractors, list)
        assert isinstance(explanation, str)
        assert isinstance(tip, str)

    def test_distractors_count(self):
        _, _, distractors, _, _ = _t2_solve_radical_linear()
        assert len(distractors) == 4

    def test_distractors_are_strings(self):
        _, _, distractors, _, _ = _t2_solve_radical_linear()
        for d in distractors:
            assert isinstance(d, str)

    def test_correct_not_in_distractors(self):
        _, correct_str, distractors, _, _ = _t2_solve_radical_linear()
        assert correct_str not in distractors

    def test_solution_satisfies_equation(self):
        """Verify valid solutions satisfy sqrt(x+b) = x+d."""
        for _ in range(20):
            question, correct_str, _, _, _ = _t2_solve_radical_linear()
            # Parse all x values from correct_str
            x_values = re.findall(r"x\s*=\s*(-?\d+)", correct_str)
            assert len(x_values) >= 1, f"No solution found in '{correct_str}'"
            # Extract radicand and rhs from question
            rad_m = re.search(r"√\((.+?)\)", question)
            assert rad_m is not None
            radicand_expr = rad_m.group(1)
            # Extract rhs (after "= ")
            rhs_m = re.search(r"=\s*(.+?)\.", question)
            assert rhs_m is not None
            rhs_expr = rhs_m.group(1).strip()
            for x_str in x_values:
                x_val = int(x_str)
                rad_val = _eval_expr_at_x(radicand_expr, x_val)
                rhs_val = _eval_expr_at_x(rhs_expr, x_val)
                assert rad_val >= 0, f"Domain violated for x={x_val}"
                assert rhs_val >= 0, f"RHS negative for x={x_val}"
                assert abs(math.sqrt(rad_val) - rhs_val) < 1e-9, \
                    f"Solution x={x_val} incorrect"

    def test_no_crash_multiple_runs(self):
        for _ in range(15):
            result = _t2_solve_radical_linear()
            assert len(result) == 5

    def test_question_in_italian(self):
        question, _, _, _, _ = _t2_solve_radical_linear()
        assert "Risolvi" in question

    def test_mentions_domain_in_tip(self):
        _, _, _, _, tip = _t2_solve_radical_linear()
        assert "verifica" in tip.lower() or "estranee" in tip.lower()


# ---------------------------------------------------------------------------
# _t3_solve_radical_two_radicals tests
# ---------------------------------------------------------------------------

class TestT3SolveRadicalTwoRadicals:
    """Tests for _t3_solve_radical_two_radicals (5-tuple string template)."""

    def test_returns_5_tuple(self):
        result = _t3_solve_radical_two_radicals()
        assert len(result) == 5

    def test_tuple_types(self):
        question, correct_str, distractors, explanation, tip = _t3_solve_radical_two_radicals()
        assert isinstance(question, str)
        assert isinstance(correct_str, str)
        assert isinstance(distractors, list)
        assert isinstance(explanation, str)
        assert isinstance(tip, str)

    def test_distractors_count(self):
        _, _, distractors, _, _ = _t3_solve_radical_two_radicals()
        assert len(distractors) == 4

    def test_distractors_are_strings(self):
        _, _, distractors, _, _ = _t3_solve_radical_two_radicals()
        for d in distractors:
            assert isinstance(d, str)

    def test_correct_not_in_distractors(self):
        _, correct_str, distractors, _, _ = _t3_solve_radical_two_radicals()
        assert correct_str not in distractors

    def test_solution_satisfies_equation(self):
        """Verify sqrt(x+b) + sqrt(x+d) = e."""
        for _ in range(20):
            question, correct_str, _, _, _ = _t3_solve_radical_two_radicals()
            x_val = _parse_x_value(correct_str)
            assert x_val is not None
            # Parse the two radicands and e from the question
            rads = re.findall(r"√\((.+?)\)", question)
            assert len(rads) == 2
            e_m = re.search(r"=\s*(\d+)\s*$", question)
            assert e_m is not None
            e = int(e_m.group(1))
            val1 = _eval_expr_at_x(rads[0], x_val)
            val2 = _eval_expr_at_x(rads[1], x_val)
            assert val1 >= 0 and val2 >= 0, "Domain violated"
            assert abs(math.sqrt(val1) + math.sqrt(val2) - e) < 1e-9

    def test_no_crash_multiple_runs(self):
        for _ in range(15):
            result = _t3_solve_radical_two_radicals()
            assert len(result) == 5

    def test_question_in_italian(self):
        question, _, _, _, _ = _t3_solve_radical_two_radicals()
        assert "Risolvi" in question


# ---------------------------------------------------------------------------
# _t3_solve_radical_extraneous tests
# ---------------------------------------------------------------------------

class TestT3SolveRadicalExtraneous:
    """Tests for _t3_solve_radical_extraneous (5-tuple string template)."""

    def test_returns_5_tuple(self):
        result = _t3_solve_radical_extraneous()
        assert len(result) == 5

    def test_tuple_types(self):
        question, correct_str, distractors, explanation, tip = _t3_solve_radical_extraneous()
        assert isinstance(question, str)
        assert isinstance(correct_str, str)
        assert isinstance(distractors, list)
        assert isinstance(explanation, str)
        assert isinstance(tip, str)

    def test_distractors_count(self):
        _, _, distractors, _, _ = _t3_solve_radical_extraneous()
        assert len(distractors) == 4

    def test_distractors_are_strings(self):
        _, _, distractors, _, _ = _t3_solve_radical_extraneous()
        for d in distractors:
            assert isinstance(d, str)

    def test_correct_not_in_distractors(self):
        _, correct_str, distractors, _, _ = _t3_solve_radical_extraneous()
        assert correct_str not in distractors

    def test_valid_solutions_satisfy_equation(self):
        """Verify claimed valid solutions actually satisfy sqrt(a-x) = x-c."""
        for _ in range(20):
            question, correct_str, _, _, _ = _t3_solve_radical_extraneous()
            # Parse valid x values from correct_str
            x_values = re.findall(r"x\s*=\s*(-?\d+)", correct_str)
            # Extract radicand and rhs
            rad_m = re.search(r"√\((.+?)\)", question)
            assert rad_m is not None
            radicand_expr = rad_m.group(1)
            rhs_m = re.search(r"=\s*(.+?)\.", question)
            assert rhs_m is not None
            rhs_expr = rhs_m.group(1).strip()
            for x_str in x_values:
                x_val = int(x_str)
                rad_val = _eval_expr_at_x(radicand_expr, x_val)
                rhs_val = _eval_expr_at_x(rhs_expr, x_val)
                assert rad_val >= 0, f"Domain violated: radicand < 0 for x={x_val}"
                assert rhs_val >= 0, f"RHS < 0 for x={x_val}"
                assert abs(math.sqrt(rad_val) - rhs_val) < 1e-9, \
                    f"Solution x={x_val} doesn't satisfy equation"

    def test_no_crash_multiple_runs(self):
        for _ in range(15):
            result = _t3_solve_radical_extraneous()
            assert len(result) == 5

    def test_mentions_extraneous_in_tip(self):
        _, _, _, _, tip = _t3_solve_radical_extraneous()
        assert "estranee" in tip.lower() or "verifica" in tip.lower()

    def test_question_mentions_solutions(self):
        question, _, _, _, _ = _t3_solve_radical_extraneous()
        assert "soluzion" in question.lower()


# ---------------------------------------------------------------------------
# Integration through SolveExercise.generate()
# ---------------------------------------------------------------------------

class TestSolveExerciseIntegration:
    """Test that new templates work through the SolveExercise class."""

    def test_generate_difficulty_2_no_crash(self):
        ex = SolveExercise()
        for _ in range(30):
            result = ex.generate(difficulty=2)
            assert "question" in result
            assert "options" in result
            assert "correct_index" in result
            assert len(result["options"]) == 5

    def test_generate_difficulty_3_no_crash(self):
        ex = SolveExercise()
        for _ in range(30):
            result = ex.generate(difficulty=3)
            assert "question" in result
            assert "options" in result
            assert "correct_index" in result
            assert len(result["options"]) == 5

    def test_correct_answer_in_options(self):
        """The correct answer is always one of the options."""
        ex = SolveExercise()
        for _ in range(20):
            for diff in [2, 3]:
                result = ex.generate(difficulty=diff)
                idx = result["correct_index"]
                assert 0 <= idx < len(result["options"])
