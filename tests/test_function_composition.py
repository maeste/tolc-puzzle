import pytest

from exercises.function_composition import FunctionComposition


@pytest.fixture
def exercise():
    return FunctionComposition()


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
# L1 — Template: _evaluate_composition
# ---------------------------------------------------------------------------

class TestEvaluateComposition:
    @pytest.mark.parametrize("run", range(5))
    def test_generates_valid_output(self, exercise, run):
        result = exercise._evaluate_composition()
        _validate_exercise_output(result)

    def test_question_mentions_fg(self, exercise):
        result = exercise._evaluate_composition()
        assert "f(g(" in result["question"]

    def test_question_defines_functions(self, exercise):
        result = exercise._evaluate_composition()
        assert "f(x)" in result["question"]
        assert "g(x)" in result["question"]

    def test_correct_answer_is_numeric(self, exercise):
        result = exercise._evaluate_composition()
        correct = result["options"][result["correct_index"]]
        int(correct)  # Should not raise

    def test_has_did_you_know(self, exercise):
        result = exercise._evaluate_composition()
        assert "did_you_know" in result
        assert isinstance(result["did_you_know"], str)
        assert len(result["did_you_know"]) > 0


# ---------------------------------------------------------------------------
# L1 — Template: _identify_composition_formula
# ---------------------------------------------------------------------------

class TestIdentifyCompositionFormula:
    @pytest.mark.parametrize("run", range(5))
    def test_generates_valid_output(self, exercise, run):
        result = exercise._identify_composition_formula()
        _validate_exercise_output(result)

    def test_question_asks_expression(self, exercise):
        result = exercise._identify_composition_formula()
        assert "f(g(x))" in result["question"]

    def test_explanation_mentions_substitute(self, exercise):
        result = exercise._identify_composition_formula()
        assert "sostituiamo" in result["explanation"].lower()


# ---------------------------------------------------------------------------
# L2 — Template: _composition_from_table
# ---------------------------------------------------------------------------

class TestCompositionFromTable:
    @pytest.mark.parametrize("run", range(5))
    def test_generates_valid_output(self, exercise, run):
        result = exercise._composition_from_table()
        _validate_exercise_output(result)

    def test_question_contains_table(self, exercise):
        result = exercise._composition_from_table()
        assert "g(" in result["question"]
        assert "f(" in result["question"]

    def test_question_asks_fg(self, exercise):
        result = exercise._composition_from_table()
        assert "f(g(" in result["question"]

    def test_correct_answer_is_numeric(self, exercise):
        result = exercise._composition_from_table()
        correct = result["options"][result["correct_index"]]
        int(correct)  # Should not raise


# ---------------------------------------------------------------------------
# L2 — Template: _order_matters
# ---------------------------------------------------------------------------

class TestOrderMatters:
    @pytest.mark.parametrize("run", range(5))
    def test_generates_valid_output(self, exercise, run):
        result = exercise._order_matters()
        _validate_exercise_output(result)

    def test_question_asks_for_fg(self, exercise):
        result = exercise._order_matters()
        assert "f(g(x))" in result["question"]

    def test_explanation_mentions_order(self, exercise):
        result = exercise._order_matters()
        assert "ordine" in result["explanation"].lower() or "diverso" in result["explanation"].lower()


# ---------------------------------------------------------------------------
# L2 — Template: _decompose_function
# ---------------------------------------------------------------------------

class TestDecomposeFunction:
    @pytest.mark.parametrize("run", range(5))
    def test_generates_valid_output(self, exercise, run):
        result = exercise._decompose_function()
        _validate_exercise_output(result)

    def test_question_mentions_decomposition(self, exercise):
        result = exercise._decompose_function()
        assert "f(g(x))" in result["question"]

    def test_correct_has_f_and_g(self, exercise):
        result = exercise._decompose_function()
        correct = result["options"][result["correct_index"]]
        assert "f(x)" in correct
        assert "g(x)" in correct

    def test_explanation_mentions_external_internal(self, exercise):
        result = exercise._decompose_function()
        explanation = result["explanation"].lower()
        assert "esterna" in explanation or "interna" in explanation


# ---------------------------------------------------------------------------
# L3 — Template: _domain_of_composition
# ---------------------------------------------------------------------------

class TestDomainOfComposition:
    @pytest.mark.parametrize("run", range(5))
    def test_generates_valid_output(self, exercise, run):
        result = exercise._domain_of_composition()
        _validate_exercise_output(result)

    def test_question_asks_domain(self, exercise):
        result = exercise._domain_of_composition()
        assert "dominio" in result["question"].lower()

    def test_explanation_mentions_domain_condition(self, exercise):
        result = exercise._domain_of_composition()
        explanation = result["explanation"].lower()
        assert "dominio" in explanation


# ---------------------------------------------------------------------------
# L3 — Template: _triple_composition
# ---------------------------------------------------------------------------

class TestTripleComposition:
    @pytest.mark.parametrize("run", range(5))
    def test_generates_valid_output(self, exercise, run):
        result = exercise._triple_composition()
        _validate_exercise_output(result)

    def test_question_mentions_three_functions(self, exercise):
        result = exercise._triple_composition()
        assert "f(x)" in result["question"]
        assert "g(x)" in result["question"]
        assert "h(x)" in result["question"]

    def test_question_asks_fgh(self, exercise):
        result = exercise._triple_composition()
        assert "f(g(h(" in result["question"]

    def test_correct_answer_is_numeric(self, exercise):
        result = exercise._triple_composition()
        correct = result["options"][result["correct_index"]]
        int(correct)  # Should not raise

    def test_explanation_shows_steps(self, exercise):
        result = exercise._triple_composition()
        assert "h(" in result["explanation"]
        assert "g(" in result["explanation"]
        assert "f(" in result["explanation"]


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
    def test_question_contains_italian_words(self, exercise, difficulty):
        result = exercise.generate(difficulty=difficulty)
        question = result["question"].lower()
        italian_words = [
            "quanto", "vale", "quale", "seguenti", "tabelle",
            "espressione", "dominio", "funzione", "corrisponde",
        ]
        assert any(word in question for word in italian_words), (
            f"No Italian words found in question: {question}"
        )

    @pytest.mark.parametrize("difficulty", [1, 2, 3])
    def test_explanation_contains_italian_words(self, exercise, difficulty):
        result = exercise.generate(difficulty=difficulty)
        explanation = result["explanation"].lower()
        italian_words = [
            "calcoliamo", "quindi", "sostituiamo", "dalla", "tabella",
            "trovare", "dominio", "prima", "otteniamo", "verificando",
            "passo", "cerchiamo", "serve", "applichiamo", "decomporre",
            "identifichiamo",
        ]
        assert any(word in explanation for word in italian_words), (
            f"No Italian words found in explanation: {explanation}"
        )

    @pytest.mark.parametrize("difficulty", [1, 2, 3])
    def test_did_you_know_present(self, exercise, difficulty):
        result = exercise.generate(difficulty=difficulty)
        assert "did_you_know" in result
        assert isinstance(result["did_you_know"], str)
        assert len(result["did_you_know"]) > 0


# ---------------------------------------------------------------------------
# Distractors distinctness (stress test)
# ---------------------------------------------------------------------------

class TestDistractorsDistinct:
    @pytest.mark.parametrize("difficulty", [1, 2, 3])
    @pytest.mark.parametrize("run", range(10))
    def test_all_options_distinct(self, exercise, difficulty, run):
        result = exercise.generate(difficulty=difficulty)
        assert len(set(result["options"])) == 5, (
            f"Duplicate options at difficulty {difficulty}: {result['options']}"
        )
