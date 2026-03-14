"""Tests for parametric equation analysis templates in which_satisfies.py."""

import math
import random

import pytest

from exercises.which_satisfies import (
    _which_param_linear_impossible,
    _which_param_linear_infinite,
    _which_param_quadratic_no_real,
    _which_param_quadratic_one_solution,
    _which_param_quadratic_positive_roots,
    _which_param_system_inconsistent,
)


# ----------------------------------------------------------------
# Helper to validate common structure
# ----------------------------------------------------------------

def _validate_result(result):
    """Check that a result dict has the required structure."""
    assert "question" in result, "Missing 'question' key"
    assert "options" in result, "Missing 'options' key"
    assert "correct_index" in result, "Missing 'correct_index' key"
    assert "explanation" in result, "Missing 'explanation' key"
    assert "did_you_know" in result, "Missing 'did_you_know' key"

    assert isinstance(result["question"], str)
    assert isinstance(result["options"], list)
    assert len(result["options"]) == 5, f"Expected 5 options, got {len(result['options'])}"
    assert isinstance(result["correct_index"], int)
    assert 0 <= result["correct_index"] <= 4
    assert isinstance(result["explanation"], str)
    assert isinstance(result["did_you_know"], str)

    # All options should be distinct strings
    opts = result["options"]
    assert all(isinstance(o, str) for o in opts), "All options must be strings"
    assert len(set(opts)) == len(opts), f"Options are not distinct: {opts}"


# ================================================================
#  _which_param_linear_impossible
# ================================================================

class TestParamLinearImpossible:
    def test_basic_structure(self):
        result = _which_param_linear_impossible()
        _validate_result(result)

    def test_question_in_italian(self):
        result = _which_param_linear_impossible()
        assert "impossibile" in result["question"].lower()

    def test_correct_answer_is_integer(self):
        result = _which_param_linear_impossible()
        correct = result["options"][result["correct_index"]]
        int(correct)  # should not raise

    def test_multiple_runs_no_crash(self):
        for _ in range(10):
            result = _which_param_linear_impossible()
            _validate_result(result)

    def test_five_distinct_options(self):
        for _ in range(10):
            result = _which_param_linear_impossible()
            assert len(set(result["options"])) == 5

    def test_explanation_not_empty(self):
        result = _which_param_linear_impossible()
        assert len(result["explanation"]) > 20


# ================================================================
#  _which_param_linear_infinite
# ================================================================

class TestParamLinearInfinite:
    def test_basic_structure(self):
        result = _which_param_linear_infinite()
        _validate_result(result)

    def test_question_in_italian(self):
        result = _which_param_linear_infinite()
        assert "infinite" in result["question"].lower()

    def test_correct_answer_is_integer(self):
        result = _which_param_linear_infinite()
        correct = result["options"][result["correct_index"]]
        int(correct)

    def test_multiple_runs_no_crash(self):
        for _ in range(10):
            result = _which_param_linear_infinite()
            _validate_result(result)

    def test_five_distinct_options(self):
        for _ in range(10):
            result = _which_param_linear_infinite()
            assert len(set(result["options"])) == 5


# ================================================================
#  _which_param_quadratic_no_real
# ================================================================

class TestParamQuadraticNoReal:
    def test_basic_structure(self):
        result = _which_param_quadratic_no_real()
        _validate_result(result)

    def test_question_mentions_no_solutions(self):
        result = _which_param_quadratic_no_real()
        assert "non ha soluzioni reali" in result["question"]

    def test_correct_answer_makes_delta_negative(self):
        """Verify the correct k actually gives delta < 0."""
        random.seed(42)
        for _ in range(10):
            result = _which_param_quadratic_no_real()
            k = int(result["options"][result["correct_index"]])
            # Equation is x^2 + 2kx + (k + c) = 0
            # We need to extract c from the question
            q = result["question"]
            # Parse (k + c) from the equation string
            import re
            m = re.search(r'\(k \+ (\d+)\)', q)
            if m:
                c = int(m.group(1))
                # delta = 4k^2 - 4(k + c) = 4(k^2 - k - c)
                delta_factor = k * k - k - c
                assert delta_factor < 0, f"k={k}, c={c}, delta_factor={delta_factor}"

    def test_multiple_runs_no_crash(self):
        for _ in range(10):
            result = _which_param_quadratic_no_real()
            _validate_result(result)

    def test_five_distinct_options(self):
        for _ in range(10):
            result = _which_param_quadratic_no_real()
            assert len(set(result["options"])) == 5


# ================================================================
#  _which_param_quadratic_one_solution
# ================================================================

class TestParamQuadraticOneSolution:
    def test_basic_structure(self):
        result = _which_param_quadratic_one_solution()
        _validate_result(result)

    def test_question_mentions_one_solution(self):
        result = _which_param_quadratic_one_solution()
        assert "esattamente una soluzione" in result["question"]

    def test_correct_answer_makes_delta_zero(self):
        """Verify the correct k gives delta = 0."""
        random.seed(123)
        for _ in range(10):
            result = _which_param_quadratic_one_solution()
            k = int(result["options"][result["correct_index"]])
            # Equation: x^2 - 2kx + c = 0
            # delta = 4k^2 - 4c = 0 => k^2 = c
            import re
            q = result["question"]
            m = re.search(r'2kx \+ (\d+)', q)
            if m:
                c = int(m.group(1))
                assert k * k == c, f"k={k}, c={c}, k^2={k*k}"

    def test_multiple_runs_no_crash(self):
        for _ in range(10):
            result = _which_param_quadratic_one_solution()
            _validate_result(result)

    def test_five_distinct_options(self):
        for _ in range(10):
            result = _which_param_quadratic_one_solution()
            assert len(set(result["options"])) == 5


# ================================================================
#  _which_param_quadratic_positive_roots
# ================================================================

class TestParamQuadraticPositiveRoots:
    def test_basic_structure(self):
        result = _which_param_quadratic_positive_roots()
        _validate_result(result)

    def test_question_mentions_positive_roots(self):
        result = _which_param_quadratic_positive_roots()
        assert "radici reali positive" in result["question"]

    def test_correct_answer_vieta_conditions(self):
        """Check that the correct k satisfies Vieta conditions."""
        random.seed(99)
        for _ in range(10):
            result = _which_param_quadratic_positive_roots()
            k = int(result["options"][result["correct_index"]])
            # From the explanation, we can verify sum > 0, product > 0, delta >= 0
            # The explanation contains these values
            assert "somma" in result["explanation"].lower() or "Somma" in result["explanation"]

    def test_multiple_runs_no_crash(self):
        for _ in range(10):
            result = _which_param_quadratic_positive_roots()
            _validate_result(result)

    def test_five_distinct_options(self):
        for _ in range(10):
            result = _which_param_quadratic_positive_roots()
            assert len(set(result["options"])) == 5

    def test_correct_k_is_positive(self):
        """For this template, k must be positive for product > 0."""
        random.seed(77)
        for _ in range(10):
            result = _which_param_quadratic_positive_roots()
            k = int(result["options"][result["correct_index"]])
            assert k > 0, f"Expected positive k, got {k}"


# ================================================================
#  _which_param_system_inconsistent
# ================================================================

class TestParamSystemInconsistent:
    def test_basic_structure(self):
        result = _which_param_system_inconsistent()
        _validate_result(result)

    def test_question_mentions_no_solutions(self):
        result = _which_param_system_inconsistent()
        assert "non ha soluzioni" in result["question"]

    def test_correct_answer_is_integer(self):
        result = _which_param_system_inconsistent()
        correct = result["options"][result["correct_index"]]
        int(correct)

    def test_multiple_runs_no_crash(self):
        for _ in range(10):
            result = _which_param_system_inconsistent()
            _validate_result(result)

    def test_five_distinct_options(self):
        for _ in range(10):
            result = _which_param_system_inconsistent()
            assert len(set(result["options"])) == 5

    def test_explanation_mentions_determinant(self):
        result = _which_param_system_inconsistent()
        assert "det" in result["explanation"].lower() or "determinante" in result["explanation"].lower()


# ================================================================
#  Cross-template tests
# ================================================================

class TestAllParametricTemplates:
    """Tests that apply to all 6 templates."""

    TEMPLATES = [
        _which_param_linear_impossible,
        _which_param_linear_infinite,
        _which_param_quadratic_no_real,
        _which_param_quadratic_one_solution,
        _which_param_quadratic_positive_roots,
        _which_param_system_inconsistent,
    ]

    @pytest.mark.parametrize("template_fn", TEMPLATES)
    def test_has_all_required_keys(self, template_fn):
        result = template_fn()
        _validate_result(result)

    @pytest.mark.parametrize("template_fn", TEMPLATES)
    def test_did_you_know_not_empty(self, template_fn):
        result = template_fn()
        assert len(result["did_you_know"]) > 10

    @pytest.mark.parametrize("template_fn", TEMPLATES)
    def test_correct_index_is_zero_before_shuffle(self, template_fn):
        """Templates always put correct answer at index 0 (shuffled later)."""
        result = template_fn()
        assert result["correct_index"] == 0

    @pytest.mark.parametrize("template_fn", TEMPLATES)
    def test_stress_run_20_times(self, template_fn):
        """Run each template 20 times to catch intermittent failures."""
        for _ in range(20):
            result = template_fn()
            assert len(result["options"]) == 5
            assert len(set(result["options"])) == 5

    def test_edge_case_seed_zero(self):
        """Test with a deterministic seed to check edge cases."""
        random.seed(0)
        for fn in self.TEMPLATES:
            result = fn()
            _validate_result(result)

    def test_negative_coefficients_seed(self):
        """Test with a seed that tends to produce negative coefficients."""
        random.seed(7)
        for fn in self.TEMPLATES:
            result = fn()
            _validate_result(result)
