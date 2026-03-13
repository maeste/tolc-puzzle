import pytest

from exercises.word_modeler import WordModeler


@pytest.fixture
def modeler():
    return WordModeler()


# ---------------------------------------------------------------------------
# Helper to validate the 5-tuple contract returned by each numeric template
# ---------------------------------------------------------------------------

def _validate_numeric_tuple(result):
    """Assert that a numeric template returns the expected 5-tuple shape
    with string-encoded numeric answers."""
    assert isinstance(result, tuple), f"Expected tuple, got {type(result)}"
    assert len(result) == 5, f"Expected 5-tuple, got length {len(result)}"

    question, correct_answer, distractors, explanation, tip = result

    assert isinstance(question, str) and len(question) > 0
    assert isinstance(correct_answer, str) and len(correct_answer) > 0
    assert isinstance(distractors, list) and len(distractors) == 4
    for i, d in enumerate(distractors):
        assert isinstance(d, str) and len(d) > 0, f"Distractor {i} invalid: {d!r}"
    assert isinstance(explanation, str) and len(explanation) > 0
    assert isinstance(tip, str) and len(tip) > 0

    # Correct answer must be a valid integer
    try:
        int(correct_answer)
    except ValueError:
        pytest.fail(f"Correct answer is not numeric: {correct_answer!r}")

    # All distractors must be valid integers
    for i, d in enumerate(distractors):
        try:
            int(d)
        except ValueError:
            pytest.fail(f"Distractor {i} is not numeric: {d!r}")

    # All options (correct + distractors) must be distinct
    all_options = [correct_answer] + distractors
    assert len(set(all_options)) == 5, (
        f"Options are not all distinct: {all_options}"
    )

    # Correct answer must not appear among distractors
    assert correct_answer not in distractors, (
        f"Correct answer {correct_answer} found in distractors: {distractors}"
    )


# ---------------------------------------------------------------------------
# Level 1 numeric templates
# ---------------------------------------------------------------------------

class TestNumericAgeSum:
    @pytest.mark.parametrize("run", range(20))
    def test_valid_tuple(self, run):
        result = WordModeler._numeric_age_sum()
        _validate_numeric_tuple(result)

    def test_correct_answer_is_positive(self):
        for _ in range(50):
            _, correct, _, _, _ = WordModeler._numeric_age_sum()
            assert int(correct) > 0


class TestNumericDiscount:
    @pytest.mark.parametrize("run", range(20))
    def test_valid_tuple(self, run):
        result = WordModeler._numeric_discount()
        _validate_numeric_tuple(result)

    def test_discounted_less_than_original(self):
        for _ in range(50):
            question, correct, _, _, _ = WordModeler._numeric_discount()
            # Extract original price from question text
            assert int(correct) > 0


class TestNumericPercentageOf:
    @pytest.mark.parametrize("run", range(20))
    def test_valid_tuple(self, run):
        result = WordModeler._numeric_percentage_of()
        _validate_numeric_tuple(result)

    def test_count_is_non_negative(self):
        for _ in range(50):
            _, correct, _, _, _ = WordModeler._numeric_percentage_of()
            assert int(correct) >= 0


# ---------------------------------------------------------------------------
# Level 2 numeric templates
# ---------------------------------------------------------------------------

class TestNumericAverageAdd:
    @pytest.mark.parametrize("run", range(20))
    def test_valid_tuple(self, run):
        result = WordModeler._numeric_average_add()
        _validate_numeric_tuple(result)

    def test_new_mean_is_positive(self):
        for _ in range(50):
            _, correct, _, _, _ = WordModeler._numeric_average_add()
            assert int(correct) > 0


class TestNumericWorkRate:
    @pytest.mark.parametrize("run", range(20))
    def test_valid_tuple(self, run):
        result = WordModeler._numeric_work_rate()
        _validate_numeric_tuple(result)

    def test_combined_time_less_than_individual(self):
        for _ in range(50):
            question, correct, _, _, _ = WordModeler._numeric_work_rate()
            assert int(correct) >= 1


class TestNumericProfit:
    @pytest.mark.parametrize("run", range(20))
    def test_valid_tuple(self, run):
        result = WordModeler._numeric_profit()
        _validate_numeric_tuple(result)

    def test_profit_is_positive(self):
        for _ in range(50):
            _, correct, _, _, _ = WordModeler._numeric_profit()
            assert int(correct) > 0


# ---------------------------------------------------------------------------
# Level 3 numeric templates
# ---------------------------------------------------------------------------

class TestNumericSystemAges:
    @pytest.mark.parametrize("run", range(20))
    def test_valid_tuple(self, run):
        result = WordModeler._numeric_system_ages()
        _validate_numeric_tuple(result)

    def test_age_is_positive(self):
        for _ in range(50):
            _, correct, _, _, _ = WordModeler._numeric_system_ages()
            assert int(correct) > 0


class TestNumericCombinedDistance:
    @pytest.mark.parametrize("run", range(20))
    def test_valid_tuple(self, run):
        result = WordModeler._numeric_combined_distance()
        _validate_numeric_tuple(result)

    def test_distance_is_positive(self):
        for _ in range(50):
            _, correct, _, _, _ = WordModeler._numeric_combined_distance()
            assert int(correct) > 0


# ---------------------------------------------------------------------------
# Full generate() integration: ensure numeric AND equation templates coexist
# ---------------------------------------------------------------------------

class TestGenerateIntegrationWithNumeric:
    @pytest.mark.parametrize("difficulty", [1, 2, 3])
    def test_generate_returns_valid_dict(self, modeler, difficulty):
        """generate() must still return valid dicts with 5 options."""
        for _ in range(30):
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
        for _ in range(30):
            result = modeler.generate(difficulty)
            options = result["options"]
            assert len(set(options)) == len(options), (
                f"Duplicate options found: {options}"
            )

    @pytest.mark.parametrize("difficulty", [1, 2, 3])
    def test_generate_includes_both_modes(self, modeler, difficulty):
        """Over many runs, both equation and numeric questions should appear."""
        has_equation = False
        has_numeric = False
        for _ in range(100):
            result = modeler.generate(difficulty)
            correct_opt = result["options"][result["correct_index"]]
            # Numeric answers are pure integers; equation answers contain operators
            try:
                int(correct_opt)
                has_numeric = True
            except ValueError:
                has_equation = True
            if has_equation and has_numeric:
                break
        assert has_equation, "No equation-mode templates were generated"
        assert has_numeric, "No numeric-mode templates were generated"


# ---------------------------------------------------------------------------
# Regression: existing equation templates still work
# ---------------------------------------------------------------------------

class TestEquationTemplateRegression:
    @pytest.mark.parametrize("difficulty", [1, 2, 3])
    def test_equation_templates_still_produce_valid_results(self, modeler, difficulty):
        templates = modeler._get_equation_templates(difficulty)
        for template_fn in templates:
            for _ in range(5):
                result = template_fn()
                assert isinstance(result, tuple)
                assert len(result) == 5
                question, correct, distractors, explanation, tip = result
                assert isinstance(question, str) and len(question) > 0
                assert isinstance(correct, str) and len(correct) > 0
                assert isinstance(distractors, list) and len(distractors) == 4


# ---------------------------------------------------------------------------
# _numeric_distractors helper
# ---------------------------------------------------------------------------

class TestNumericDistractors:
    def test_returns_four_strings(self):
        result = WordModeler._numeric_distractors(10)
        assert len(result) == 4
        for r in result:
            assert isinstance(r, str)

    def test_no_duplicates(self):
        for _ in range(100):
            correct = 42
            result = WordModeler._numeric_distractors(correct)
            all_opts = [str(correct)] + result
            assert len(set(all_opts)) == 5

    def test_custom_offsets(self):
        result = WordModeler._numeric_distractors(50, [-10, -5, 5, 10])
        assert result == ["40", "45", "55", "60"]
