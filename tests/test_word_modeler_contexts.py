import pytest

from exercises.word_modeler import WordModeler


@pytest.fixture
def modeler():
    return WordModeler()


# ---------------------------------------------------------------------------
# Helper to validate the 5-tuple contract returned by each static template
# ---------------------------------------------------------------------------

def _validate_tuple(result):
    """Assert that a template returns the expected 5-tuple shape."""
    assert isinstance(result, tuple), f"Expected tuple, got {type(result)}"
    assert len(result) == 5, f"Expected 5-tuple, got length {len(result)}"

    question, correct_eq, distractors, explanation, tip = result

    assert isinstance(question, str) and len(question) > 0
    assert isinstance(correct_eq, str) and len(correct_eq) > 0
    assert isinstance(distractors, list) and len(distractors) == 4
    for i, d in enumerate(distractors):
        assert isinstance(d, str) and len(d) > 0, f"Distractor {i} invalid: {d!r}"
    assert isinstance(explanation, str) and len(explanation) > 0
    assert isinstance(tip, str) and len(tip) > 0

    # All options (correct + distractors) must be distinct
    all_options = [correct_eq] + distractors
    assert len(set(all_options)) == 5, (
        f"Options are not all distinct: {all_options}"
    )


# ---------------------------------------------------------------------------
# Level 1 — new Italian context templates
# ---------------------------------------------------------------------------

class TestSupermarketShopping:
    @pytest.mark.parametrize("run", range(10))
    def test_no_exception_and_valid_tuple(self, run):
        result = WordModeler._supermarket_shopping()
        _validate_tuple(result)


class TestPhonePlan:
    @pytest.mark.parametrize("run", range(10))
    def test_no_exception_and_valid_tuple(self, run):
        result = WordModeler._phone_plan()
        _validate_tuple(result)


class TestCookingRecipe:
    @pytest.mark.parametrize("run", range(10))
    def test_no_exception_and_valid_tuple(self, run):
        result = WordModeler._cooking_recipe()
        _validate_tuple(result)


# ---------------------------------------------------------------------------
# Level 2 — new Italian context templates
# ---------------------------------------------------------------------------

class TestTrainTickets:
    @pytest.mark.parametrize("run", range(10))
    def test_no_exception_and_valid_tuple(self, run):
        result = WordModeler._train_tickets()
        _validate_tuple(result)


class TestSportsTraining:
    @pytest.mark.parametrize("run", range(10))
    def test_no_exception_and_valid_tuple(self, run):
        result = WordModeler._sports_training()
        _validate_tuple(result)


class TestElectricityBill:
    @pytest.mark.parametrize("run", range(10))
    def test_no_exception_and_valid_tuple(self, run):
        result = WordModeler._electricity_bill()
        _validate_tuple(result)


# ---------------------------------------------------------------------------
# Level 3 — new Italian context templates
# ---------------------------------------------------------------------------

class TestTravelPlanning:
    @pytest.mark.parametrize("run", range(10))
    def test_no_exception_and_valid_tuple(self, run):
        result = WordModeler._travel_planning()
        _validate_tuple(result)


class TestSharedApartment:
    @pytest.mark.parametrize("run", range(10))
    def test_no_exception_and_valid_tuple(self, run):
        result = WordModeler._shared_apartment()
        _validate_tuple(result)


# ---------------------------------------------------------------------------
# Full generate() integration tests at each difficulty level
# ---------------------------------------------------------------------------

class TestGenerateIntegration:
    @pytest.mark.parametrize("difficulty", [1, 2, 3])
    def test_generate_returns_valid_dict(self, modeler, difficulty):
        for _ in range(20):
            result = modeler.generate(difficulty)
            assert isinstance(result, dict)
            assert "question" in result
            assert "options" in result
            assert "correct_index" in result
            assert "explanation" in result
            assert "did_you_know" in result
            assert "difficulty" in result

            assert isinstance(result["options"], list)
            assert len(result["options"]) == 5
            assert 0 <= result["correct_index"] < 5
            assert result["difficulty"] == difficulty

    @pytest.mark.parametrize("difficulty", [1, 2, 3])
    def test_generate_options_are_distinct(self, modeler, difficulty):
        for _ in range(20):
            result = modeler.generate(difficulty)
            options = result["options"]
            assert len(set(options)) == len(options), (
                f"Duplicate options found: {options}"
            )

    @pytest.mark.parametrize("difficulty", [1, 2, 3])
    def test_generate_all_options_are_nonempty_strings(self, modeler, difficulty):
        for _ in range(10):
            result = modeler.generate(difficulty)
            for opt in result["options"]:
                assert isinstance(opt, str) and len(opt) > 0
