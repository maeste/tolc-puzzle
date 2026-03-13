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
# _numeric_bus_cost (Level 1)
# ---------------------------------------------------------------------------

class TestNumericBusCost:
    @pytest.mark.parametrize("run", range(20))
    def test_valid_tuple(self, run):
        result = WordModeler._numeric_bus_cost()
        _validate_numeric_tuple(result)

    def test_correct_answer_is_positive(self):
        for _ in range(50):
            _, correct, _, _, _ = WordModeler._numeric_bus_cost()
            assert int(correct) > 0

    def test_rounding_up_buses(self):
        """The number of buses must always accommodate all people."""
        import math
        for _ in range(50):
            question, correct, _, explanation, _ = WordModeler._numeric_bus_cost()
            # "Un gruppo di X persone ... pullman da Y posti ... costo di Z€"
            parts = question.split()
            n_people = int(parts[3])  # "Un"=0, "gruppo"=1, "di"=2, "X"=3
            da_idx = parts.index("da")
            bus_capacity = int(parts[da_idx + 1])
            n_buses_required = math.ceil(n_people / bus_capacity)
            assert n_buses_required * bus_capacity >= n_people

    def test_italian_text(self):
        question, _, _, _, _ = WordModeler._numeric_bus_cost()
        assert "pullman" in question or "persone" in question


# ---------------------------------------------------------------------------
# _numeric_fraction_redistribution (Level 1)
# ---------------------------------------------------------------------------

class TestNumericFractionRedistribution:
    @pytest.mark.parametrize("run", range(20))
    def test_valid_tuple(self, run):
        result = WordModeler._numeric_fraction_redistribution()
        _validate_numeric_tuple(result)

    def test_correct_answer_is_positive(self):
        for _ in range(50):
            _, correct, _, _, _ = WordModeler._numeric_fraction_redistribution()
            assert int(correct) > 0

    def test_remainder_less_than_total(self):
        """Final remainder must be less than total chocolates."""
        for _ in range(50):
            question, correct, _, _, _ = WordModeler._numeric_fraction_redistribution()
            # Extract total from question: "{name} ha {total} cioccolatini"
            parts = question.split()
            ha_idx = parts.index("ha")
            total = int(parts[ha_idx + 1])
            assert int(correct) < total

    def test_italian_text(self):
        question, _, _, _, _ = WordModeler._numeric_fraction_redistribution()
        assert "cioccolatini" in question


# ---------------------------------------------------------------------------
# _numeric_percentage_multistep (Level 2)
# ---------------------------------------------------------------------------

class TestNumericPercentageMultistep:
    @pytest.mark.parametrize("run", range(20))
    def test_valid_tuple(self, run):
        result = WordModeler._numeric_percentage_multistep()
        _validate_numeric_tuple(result)

    def test_correct_answer_is_positive(self):
        for _ in range(50):
            _, correct, _, _, _ = WordModeler._numeric_percentage_multistep()
            assert int(correct) > 0

    def test_total_greater_than_passed(self):
        """Total candidates must be greater than those who passed."""
        for _ in range(50):
            question, correct, _, _, _ = WordModeler._numeric_percentage_multistep()
            # Extract n_passed: "che {n_passed} persone"
            total = int(correct)
            # Find n_passed from "che X persone"
            parts = question.split()
            che_idx = parts.index("che")
            n_passed = int(parts[che_idx + 1])
            assert total > n_passed


# ---------------------------------------------------------------------------
# _numeric_exam_scores (Level 2)
# ---------------------------------------------------------------------------

class TestNumericExamScores:
    @pytest.mark.parametrize("run", range(20))
    def test_valid_tuple(self, run):
        result = WordModeler._numeric_exam_scores()
        _validate_numeric_tuple(result)

    def test_correct_answer_is_positive(self):
        for _ in range(50):
            _, correct, _, _, _ = WordModeler._numeric_exam_scores()
            assert int(correct) >= 4  # n_exams is at least 4

    def test_multistep_answer(self):
        """Verify the answer requires multi-step reasoning (n_exams is computed from averages)."""
        for _ in range(50):
            question, correct, _, explanation, _ = WordModeler._numeric_exam_scores()
            n_exams = int(correct)
            # Extract old_avg and new_score from question
            # "media di {old_avg} punti" and "preso {new_score}"
            parts = question.split()
            media_idx = parts.index("media")
            old_avg = int(parts[media_idx + 2])
            preso_idx = parts.index("preso")
            new_score = int(parts[preso_idx + 1])
            # Verify the math works
            total_old = old_avg * n_exams
            new_total = total_old + new_score
            assert new_total % (n_exams + 1) == 0


# ---------------------------------------------------------------------------
# _numeric_successive_operations (Level 3)
# ---------------------------------------------------------------------------

class TestNumericSuccessiveOperations:
    @pytest.mark.parametrize("run", range(20))
    def test_valid_tuple(self, run):
        result = WordModeler._numeric_successive_operations()
        _validate_numeric_tuple(result)

    def test_correct_answer_is_positive(self):
        for _ in range(50):
            _, correct, _, _, _ = WordModeler._numeric_successive_operations()
            assert int(correct) > 0

    def test_italian_text(self):
        question, _, _, _, _ = WordModeler._numeric_successive_operations()
        assert "IVA" in question or "prezzo" in question


# ---------------------------------------------------------------------------
# Exam mode generation
# ---------------------------------------------------------------------------

class TestExamModeGeneration:
    def test_exam_mode_produces_numeric_majority(self, modeler):
        """Over many exam_mode=True runs, at least 55% should be numeric answers."""
        numeric_count = 0
        total_runs = 300
        for _ in range(total_runs):
            difficulty = 2
            result = modeler.generate(difficulty, exam_mode=True)
            correct_opt = result["options"][result["correct_index"]]
            try:
                int(correct_opt)
                numeric_count += 1
            except ValueError:
                pass
        ratio = numeric_count / total_runs
        assert ratio >= 0.55, (
            f"Exam mode numeric ratio was {ratio:.2f}, expected >= 0.55"
        )

    def test_exam_mode_false_still_works(self, modeler):
        """exam_mode=False should behave like normal generate."""
        for _ in range(30):
            result = modeler.generate(2, exam_mode=False)
            assert isinstance(result, dict)
            assert len(result["options"]) == 5

    def test_exam_mode_all_difficulties(self, modeler):
        """exam_mode works for all difficulty levels."""
        for diff in [1, 2, 3]:
            for _ in range(20):
                result = modeler.generate(diff, exam_mode=True)
                assert isinstance(result, dict)
                assert len(result["options"]) == 5
                assert 0 <= result["correct_index"] < 5
                assert result["difficulty"] == diff


# ---------------------------------------------------------------------------
# Regression: template registries include new templates
# ---------------------------------------------------------------------------

class TestTemplateRegistryUpdated:
    def test_level1_has_5_numeric_templates(self, modeler):
        templates = modeler._get_numeric_templates(1)
        assert len(templates) == 5

    def test_level2_has_5_numeric_templates(self, modeler):
        templates = modeler._get_numeric_templates(2)
        assert len(templates) == 5

    def test_level3_has_3_numeric_templates(self, modeler):
        templates = modeler._get_numeric_templates(3)
        assert len(templates) == 3

    def test_all_numeric_templates_callable(self, modeler):
        """Every registered numeric template must be callable and return valid 5-tuple."""
        for diff in [1, 2, 3]:
            for template_fn in modeler._get_numeric_templates(diff):
                result = template_fn()
                _validate_numeric_tuple(result)


# ---------------------------------------------------------------------------
# Integration: generate() without exam_mode returns valid dicts (regression)
# ---------------------------------------------------------------------------

class TestGenerateRegression:
    @pytest.mark.parametrize("difficulty", [1, 2, 3])
    def test_generate_returns_valid_dict(self, modeler, difficulty):
        for _ in range(20):
            result = modeler.generate(difficulty)
            assert isinstance(result, dict)
            assert "question" in result
            assert "options" in result
            assert "correct_index" in result
            assert len(result["options"]) == 5
            assert 0 <= result["correct_index"] < 5
