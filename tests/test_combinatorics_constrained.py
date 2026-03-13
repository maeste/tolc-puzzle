import math
import random

import pytest

from exercises.probability_game import ProbabilityGame


@pytest.fixture
def game():
    return ProbabilityGame()


# ------------------------------------------------------------------ helpers

def _validate_result(result: dict) -> None:
    """Common validation for all exercise results."""
    assert "question" in result
    assert "options" in result
    assert "correct_index" in result
    assert "explanation" in result

    assert isinstance(result["options"], list)
    assert len(result["options"]) == 5, f"Expected 5 options, got {len(result['options'])}"
    assert len(set(result["options"])) == 5, f"Options not distinct: {result['options']}"
    assert 0 <= result["correct_index"] <= 4
    assert len(result["explanation"]) > 0

    correct_val = int(result["options"][result["correct_index"]])
    assert correct_val > 0


# ------------------------------------------------------------------ CC1: digit constraint

class TestCombDigitConstraint:

    @pytest.mark.parametrize("run", range(20))
    def test_produces_valid_result(self, game, run):
        random.seed(run)
        result = game._comb_digit_constraint(2)
        _validate_result(result)

    @pytest.mark.parametrize("run", range(15))
    def test_correct_answer_positive_integer(self, game, run):
        random.seed(run + 100)
        result = game._comb_digit_constraint(2)
        correct = int(result["options"][result["correct_index"]])
        assert correct > 0

    def test_question_mentions_cifre(self, game):
        random.seed(42)
        result = game._comb_digit_constraint(2)
        assert "cifre" in result["question"].lower()

    def test_question_mentions_constraint(self, game):
        random.seed(42)
        result = game._comb_digit_constraint(2)
        q = result["question"].lower()
        assert "dispari" in q or "pari" in q


# ------------------------------------------------------------------ CC2: seating adjacent

class TestCombSeatingAdjacent:

    @pytest.mark.parametrize("run", range(20))
    def test_produces_valid_result(self, game, run):
        random.seed(run + 200)
        result = game._comb_seating_adjacent(2)
        _validate_result(result)

    @pytest.mark.parametrize("run", range(15))
    def test_correct_answer_is_2_times_n_minus_1_factorial(self, game, run):
        random.seed(run + 300)
        result = game._comb_seating_adjacent(2)
        correct = int(result["options"][result["correct_index"]])
        # correct must be 2*(n-1)! for some n in {4,5,6}
        valid_answers = {2 * math.factorial(n - 1) for n in [4, 5, 6]}
        assert correct in valid_answers, f"Got {correct}, expected one of {valid_answers}"

    def test_question_mentions_persone(self, game):
        random.seed(55)
        result = game._comb_seating_adjacent(2)
        assert "persone" in result["question"].lower()

    def test_question_mentions_fila(self, game):
        random.seed(55)
        result = game._comb_seating_adjacent(2)
        assert "fila" in result["question"].lower()

    def test_question_mentions_vicini(self, game):
        random.seed(55)
        result = game._comb_seating_adjacent(2)
        assert "vicini" in result["question"].lower()


# ------------------------------------------------------------------ CC3: distinct digits > threshold

class TestCombDigitsNoRepeat:

    @pytest.mark.parametrize("run", range(20))
    def test_produces_valid_result(self, game, run):
        random.seed(run + 400)
        result = game._comb_digits_no_repeat(3)
        _validate_result(result)

    @pytest.mark.parametrize("run", range(15))
    def test_correct_answer_positive_integer(self, game, run):
        random.seed(run + 500)
        result = game._comb_digits_no_repeat(3)
        correct = int(result["options"][result["correct_index"]])
        assert correct > 0

    def test_question_mentions_distinte(self, game):
        random.seed(77)
        result = game._comb_digits_no_repeat(3)
        assert "distinte" in result["question"].lower()

    def test_question_mentions_maggiori(self, game):
        random.seed(77)
        result = game._comb_digits_no_repeat(3)
        assert "maggiori" in result["question"].lower()

    def test_question_mentions_cifre(self, game):
        random.seed(77)
        result = game._comb_digits_no_repeat(3)
        assert "cifre" in result["question"].lower()


# ------------------------------------------------------------------ CC4: selection exclusion

class TestCombSelectionExclusion:

    @pytest.mark.parametrize("run", range(20))
    def test_produces_valid_result(self, game, run):
        random.seed(run + 600)
        result = game._comb_selection_exclusion(3)
        _validate_result(result)

    @pytest.mark.parametrize("run", range(15))
    def test_correct_is_total_minus_both(self, game, run):
        random.seed(run + 700)
        result = game._comb_selection_exclusion(3)
        correct = int(result["options"][result["correct_index"]])
        assert correct > 0

    def test_question_mentions_comitato(self, game):
        random.seed(99)
        result = game._comb_selection_exclusion(3)
        assert "comitato" in result["question"].lower()

    def test_question_mentions_persone(self, game):
        random.seed(99)
        result = game._comb_selection_exclusion(3)
        assert "persone" in result["question"].lower()

    def test_question_mentions_contemporaneamente(self, game):
        random.seed(99)
        result = game._comb_selection_exclusion(3)
        assert "contemporaneamente" in result["question"].lower()


# ------------------------------------------------------------------ integration tests

class TestIntegration:

    @pytest.mark.parametrize("run", range(30))
    def test_generate_difficulty_2_valid(self, game, run):
        random.seed(run + 800)
        result = game.generate(2)
        assert "question" in result
        assert len(result["options"]) == 5
        assert len(set(result["options"])) == 5
        assert 0 <= result["correct_index"] <= 4

    @pytest.mark.parametrize("run", range(30))
    def test_generate_difficulty_3_valid(self, game, run):
        random.seed(run + 900)
        result = game.generate(3)
        assert "question" in result
        assert len(result["options"]) == 5
        assert len(set(result["options"])) == 5
        assert 0 <= result["correct_index"] <= 4

    def test_new_templates_appear_in_difficulty_2(self, game):
        """Over many runs, at least one new template should be selected."""
        questions = set()
        for i in range(200):
            random.seed(i + 1000)
            result = game.generate(2)
            questions.add(result["question"][:30])
        # Check that at least one question about digits or seating appeared
        all_text = " ".join(questions).lower()
        has_digit = "cifre" in all_text
        has_seating = "fila" in all_text or "vicini" in all_text
        assert has_digit or has_seating, "New L2 templates never appeared in 200 runs"

    def test_new_templates_appear_in_difficulty_3(self, game):
        """Over many runs, at least one new template should be selected."""
        questions = []
        for i in range(500):
            random.seed(i + 2000)
            result = game.generate(3)
            questions.append(result["question"].lower())
        all_text = " ".join(questions)
        has_digits_no_rep = "distinte" in all_text
        has_exclusion = "comitato" in all_text
        assert has_digits_no_rep or has_exclusion, "New L3 templates never appeared in 500 runs"
