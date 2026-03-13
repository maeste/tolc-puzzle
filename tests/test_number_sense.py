import pytest

from exercises.number_sense import NumberSense


@pytest.fixture
def exercise():
    return NumberSense()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _validate_exercise_output(result: dict) -> None:
    """Validate the standard exercise output contract."""
    assert isinstance(result, dict)
    assert "question" in result
    assert "options" in result
    assert "correct_index" in result
    assert "explanation" in result

    assert isinstance(result["question"], str)
    assert len(result["question"]) > 0

    assert isinstance(result["options"], list)
    assert len(result["options"]) == 5, f"Expected 5 options, got {len(result['options'])}: {result['options']}"

    assert isinstance(result["correct_index"], int)
    assert 0 <= result["correct_index"] < 5

    # All options must be non-empty strings
    for i, opt in enumerate(result["options"]):
        assert isinstance(opt, str), f"Option {i} is not a string: {opt!r}"
        assert len(opt) > 0, f"Option {i} is empty"

    # All options must be distinct
    assert len(set(result["options"])) == 5, (
        f"Options are not all distinct: {result['options']}"
    )

    assert isinstance(result["explanation"], str)
    assert len(result["explanation"]) > 0


# ---------------------------------------------------------------------------
# Test generate() across all difficulty levels
# ---------------------------------------------------------------------------

class TestGenerateDifficulty:
    @pytest.mark.parametrize("difficulty", [1, 2, 3])
    @pytest.mark.parametrize("run", range(20))
    def test_generate_valid_output(self, exercise, difficulty, run):
        result = exercise.generate(difficulty=difficulty)
        _validate_exercise_output(result)

    @pytest.mark.parametrize("difficulty", [1, 2, 3])
    def test_difficulty_is_set(self, exercise, difficulty):
        result = exercise.generate(difficulty=difficulty)
        assert result.get("difficulty") == difficulty

    def test_difficulty_clamped_low(self, exercise):
        result = exercise.generate(difficulty=0)
        _validate_exercise_output(result)
        assert result["difficulty"] == 1

    def test_difficulty_clamped_high(self, exercise):
        result = exercise.generate(difficulty=5)
        _validate_exercise_output(result)
        assert result["difficulty"] == 3


# ---------------------------------------------------------------------------
# L1 — Template: _percentage_of_quantity
# ---------------------------------------------------------------------------

class TestPercentageOfQuantity:
    @pytest.mark.parametrize("run", range(20))
    def test_generates_valid_output(self, exercise, run):
        result = exercise._percentage_of_quantity()
        _validate_exercise_output(result)

    def test_question_contains_italian(self, exercise):
        result = exercise._percentage_of_quantity()
        assert "passato" in result["question"].lower() or "%" in result["question"]

    def test_question_mentions_percentage(self, exercise):
        result = exercise._percentage_of_quantity()
        assert "%" in result["question"]

    def test_has_did_you_know(self, exercise):
        result = exercise._percentage_of_quantity()
        assert "did_you_know" in result
        assert isinstance(result["did_you_know"], str)
        assert len(result["did_you_know"]) > 0


# ---------------------------------------------------------------------------
# L1 — Template: _decimal_to_fraction
# ---------------------------------------------------------------------------

class TestDecimalToFraction:
    @pytest.mark.parametrize("run", range(20))
    def test_generates_valid_output(self, exercise, run):
        result = exercise._decimal_to_fraction()
        _validate_exercise_output(result)

    def test_question_contains_decimal(self, exercise):
        result = exercise._decimal_to_fraction()
        assert "0." in result["question"]

    def test_correct_option_is_fraction(self, exercise):
        result = exercise._decimal_to_fraction()
        correct = result["options"][result["correct_index"]]
        assert "/" in correct

    def test_explanation_in_italian(self, exercise):
        result = exercise._decimal_to_fraction()
        # Check for Italian keywords
        assert any(
            word in result["explanation"].lower()
            for word in ["decimale", "corrisponde", "frazione", "verificare", "dividendo"]
        )


# ---------------------------------------------------------------------------
# L1 — Template: _power_small_decimal
# ---------------------------------------------------------------------------

class TestPowerSmallDecimal:
    @pytest.mark.parametrize("run", range(20))
    def test_generates_valid_output(self, exercise, run):
        result = exercise._power_small_decimal()
        _validate_exercise_output(result)

    def test_question_contains_exponent(self, exercise):
        result = exercise._power_small_decimal()
        assert "^" in result["question"]

    def test_correct_in_scientific_notation(self, exercise):
        result = exercise._power_small_decimal()
        correct = result["options"][result["correct_index"]]
        assert "10^" in correct


# ---------------------------------------------------------------------------
# L1 — Template: _fraction_of_quantity
# ---------------------------------------------------------------------------

class TestFractionOfQuantity:
    @pytest.mark.parametrize("run", range(20))
    def test_generates_valid_output(self, exercise, run):
        result = exercise._fraction_of_quantity()
        _validate_exercise_output(result)

    def test_question_is_narrative(self, exercise):
        result = exercise._fraction_of_quantity()
        # Should contain a name and items
        assert any(
            name in result["question"]
            for name in ["Marco", "Giulia", "Luca", "Sara", "Anna"]
        )

    def test_correct_answer_is_integer(self, exercise):
        result = exercise._fraction_of_quantity()
        correct = result["options"][result["correct_index"]]
        # Should be parseable as integer
        int(correct)  # Raises if not


# ---------------------------------------------------------------------------
# L2 — Template: _order_of_magnitude_sum
# ---------------------------------------------------------------------------

class TestOrderOfMagnitudeSum:
    @pytest.mark.parametrize("run", range(20))
    def test_generates_valid_output(self, exercise, run):
        result = exercise._order_of_magnitude_sum()
        _validate_exercise_output(result)

    def test_question_contains_powers_of_ten(self, exercise):
        result = exercise._order_of_magnitude_sum()
        assert "10^" in result["question"]

    def test_correct_in_scientific_notation(self, exercise):
        result = exercise._order_of_magnitude_sum()
        correct = result["options"][result["correct_index"]]
        assert "10^" in correct


# ---------------------------------------------------------------------------
# L2 — Template: _percentage_time_conversion
# ---------------------------------------------------------------------------

class TestPercentageTimeConversion:
    @pytest.mark.parametrize("run", range(20))
    def test_generates_valid_output(self, exercise, run):
        result = exercise._percentage_time_conversion()
        _validate_exercise_output(result)

    def test_question_mentions_hours_and_minutes(self, exercise):
        result = exercise._percentage_time_conversion()
        assert "or" in result["question"].lower()  # ore/ora
        assert "minut" in result["question"].lower()


# ---------------------------------------------------------------------------
# L2 — Template: _power_rules_numeric
# ---------------------------------------------------------------------------

class TestPowerRulesNumeric:
    @pytest.mark.parametrize("run", range(20))
    def test_generates_valid_output(self, exercise, run):
        result = exercise._power_rules_numeric()
        _validate_exercise_output(result)

    def test_question_contains_expression(self, exercise):
        result = exercise._power_rules_numeric()
        assert "2^" in result["question"]
        assert "4^" in result["question"]
        assert "8^" in result["question"]

    def test_explanation_mentions_base_conversion(self, exercise):
        result = exercise._power_rules_numeric()
        assert "base 2" in result["explanation"].lower()


# ---------------------------------------------------------------------------
# L2 — Template: _scientific_notation_order
# ---------------------------------------------------------------------------

class TestScientificNotationOrder:
    @pytest.mark.parametrize("run", range(20))
    def test_generates_valid_output(self, exercise, run):
        result = exercise._scientific_notation_order()
        _validate_exercise_output(result)

    def test_question_asks_for_largest(self, exercise):
        result = exercise._scientific_notation_order()
        assert "più grande" in result["question"].lower() or "piu grande" in result["question"].lower()


# ---------------------------------------------------------------------------
# L3 — Template: _successive_percentage
# ---------------------------------------------------------------------------

class TestSuccessivePercentage:
    @pytest.mark.parametrize("run", range(20))
    def test_generates_valid_output(self, exercise, run):
        result = exercise._successive_percentage()
        _validate_exercise_output(result)

    def test_question_mentions_increase_and_discount(self, exercise):
        result = exercise._successive_percentage()
        assert "aumento" in result["question"].lower()
        assert "sconto" in result["question"].lower()

    def test_correct_has_euro_symbol(self, exercise):
        result = exercise._successive_percentage()
        correct = result["options"][result["correct_index"]]
        assert "€" in correct


# ---------------------------------------------------------------------------
# L3 — Template: _nested_fraction_compute
# ---------------------------------------------------------------------------

class TestNestedFractionCompute:
    @pytest.mark.parametrize("run", range(20))
    def test_generates_valid_output(self, exercise, run):
        result = exercise._nested_fraction_compute()
        _validate_exercise_output(result)

    def test_question_contains_di(self, exercise):
        result = exercise._nested_fraction_compute()
        assert " di " in result["question"].lower()

    def test_correct_is_integer(self, exercise):
        result = exercise._nested_fraction_compute()
        correct = result["options"][result["correct_index"]]
        # Should parse as integer (possibly negative)
        int(correct)


# ---------------------------------------------------------------------------
# L3 — Template: _estimation_product
# ---------------------------------------------------------------------------

class TestEstimationProduct:
    @pytest.mark.parametrize("run", range(20))
    def test_generates_valid_output(self, exercise, run):
        result = exercise._estimation_product()
        _validate_exercise_output(result)

    def test_question_contains_multiplication(self, exercise):
        result = exercise._estimation_product()
        assert "×" in result["question"] or "x" in result["question"].lower()

    def test_explanation_mentions_identity(self, exercise):
        result = exercise._estimation_product()
        assert "a²" in result["explanation"] or "a² - b²" in result["explanation"]


# ---------------------------------------------------------------------------
# L3 — Template: _percentage_reverse
# ---------------------------------------------------------------------------

class TestPercentageReverse:
    @pytest.mark.parametrize("run", range(20))
    def test_generates_valid_output(self, exercise, run):
        result = exercise._percentage_reverse()
        _validate_exercise_output(result)

    def test_question_asks_original_price(self, exercise):
        result = exercise._percentage_reverse()
        assert "originale" in result["question"].lower()

    def test_correct_has_euro(self, exercise):
        result = exercise._percentage_reverse()
        correct = result["options"][result["correct_index"]]
        assert "€" in correct

    def test_explanation_warns_about_common_error(self, exercise):
        result = exercise._percentage_reverse()
        assert "errore" in result["explanation"].lower() or "sbagliato" in result["explanation"].lower()


# ---------------------------------------------------------------------------
# Check method
# ---------------------------------------------------------------------------

class TestCheckMethod:
    def test_check_correct_answer(self, exercise):
        result = exercise.generate(difficulty=1)
        check_result = exercise.check({
            "answer": result["correct_index"],
            "exercise": result,
        })
        assert check_result["correct"] is True

    def test_check_wrong_answer(self, exercise):
        result = exercise.generate(difficulty=1)
        wrong = (result["correct_index"] + 1) % 5
        check_result = exercise.check({
            "answer": wrong,
            "exercise": result,
        })
        assert check_result["correct"] is False

    def test_check_returns_explanation(self, exercise):
        result = exercise.generate(difficulty=2)
        check_result = exercise.check({
            "answer": result["correct_index"],
            "exercise": result,
        })
        assert "explanation" in check_result
        assert len(check_result["explanation"]) > 0


# ---------------------------------------------------------------------------
# Italian text validation
# ---------------------------------------------------------------------------

class TestItalianText:
    @pytest.mark.parametrize("difficulty", [1, 2, 3])
    def test_explanation_contains_italian_words(self, exercise, difficulty):
        result = exercise.generate(difficulty=difficulty)
        explanation = result["explanation"].lower()
        italian_words = [
            "quindi", "risultato", "esatto", "circa", "corrisponde",
            "calcola", "valore", "dopo", "prezzo", "tempo",
            "totale", "minuti", "converti", "frazione", "potenza",
            "base", "notazione", "attenzione", "risposta", "primo",
            "usando", "originale", "aumento", "sconto", "uguale",
            "numero", "resto", "diviso", "verifica", "forma",
        ]
        assert any(word in explanation for word in italian_words), (
            f"No Italian words found in explanation: {explanation}"
        )

    @pytest.mark.parametrize("difficulty", [1, 2, 3])
    def test_did_you_know_present(self, exercise, difficulty):
        result = exercise.generate(difficulty=difficulty)
        if "did_you_know" in result:
            assert isinstance(result["did_you_know"], str)
            assert len(result["did_you_know"]) > 0


# ---------------------------------------------------------------------------
# _make_numeric_distractors helper
# ---------------------------------------------------------------------------

class TestMakeNumericDistractors:
    def test_returns_five_options(self, exercise):
        options, idx = NumberSense._make_numeric_distractors(
            "42", ["43", "44", "45", "46"]
        )
        assert len(options) == 5

    def test_correct_is_among_options(self, exercise):
        options, idx = NumberSense._make_numeric_distractors(
            "42", ["43", "44", "45", "46"]
        )
        assert options[idx] == "42"

    def test_all_distinct(self, exercise):
        options, idx = NumberSense._make_numeric_distractors(
            "42", ["43", "44", "45", "46"]
        )
        assert len(set(options)) == 5

    def test_handles_duplicate_variants(self, exercise):
        options, idx = NumberSense._make_numeric_distractors(
            "10", ["10", "10", "20", "30", "40", "50"]
        )
        assert len(set(options)) == 5
        assert options[idx] == "10"

    def test_fills_when_not_enough_variants(self, exercise):
        options, idx = NumberSense._make_numeric_distractors(
            "100", ["200"]
        )
        assert len(options) == 5
        assert len(set(options)) == 5
