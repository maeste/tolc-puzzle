import pytest

from exercises.proportional_reasoning import (
    ProportionalReasoning,
    _t1_direct_proportion,
    _t1_inverse_proportion,
    _t2_squared_proportion,
    _t2_compound_percentage,
    _t3_parameter_variation,
    _t3_combined_variation,
)


# ---------------------------------------------------------------------------
# Helper: verify 5-tuple format returned by template functions
# ---------------------------------------------------------------------------

def _check_5tuple(result):
    assert isinstance(result, tuple), f"Expected tuple, got {type(result)}"
    assert len(result) == 5, f"Expected 5-tuple, got {len(result)}-tuple"
    question, correct_str, distractors, explanation, tip = result
    assert isinstance(question, str) and len(question) > 0
    assert isinstance(correct_str, str) and len(correct_str) > 0
    assert isinstance(distractors, list) and len(distractors) >= 4
    assert isinstance(explanation, str) and len(explanation) > 0
    assert isinstance(tip, str) and len(tip) > 0
    # Correct must not appear in distractors
    assert correct_str not in distractors, (
        f"Correct answer '{correct_str}' found in distractors {distractors}"
    )
    # All distractors must be distinct
    assert len(set(distractors)) == len(distractors), (
        f"Duplicate distractors: {distractors}"
    )


# ---------------------------------------------------------------------------
# Test each template function (20 iterations, no exceptions)
# ---------------------------------------------------------------------------

class TestTemplateNoExceptions:
    def test_t1_direct_proportion(self):
        for _ in range(20):
            result = _t1_direct_proportion()
            _check_5tuple(result)

    def test_t1_inverse_proportion(self):
        for _ in range(20):
            result = _t1_inverse_proportion()
            _check_5tuple(result)

    def test_t2_squared_proportion(self):
        for _ in range(20):
            result = _t2_squared_proportion()
            _check_5tuple(result)

    def test_t2_compound_percentage(self):
        for _ in range(20):
            result = _t2_compound_percentage()
            _check_5tuple(result)

    def test_t3_parameter_variation(self):
        for _ in range(20):
            result = _t3_parameter_variation()
            _check_5tuple(result)

    def test_t3_combined_variation(self):
        for _ in range(20):
            result = _t3_combined_variation()
            _check_5tuple(result)


# ---------------------------------------------------------------------------
# Test generate() for each difficulty level
# ---------------------------------------------------------------------------

class TestGenerate:
    def test_difficulty_1(self):
        ex = ProportionalReasoning()
        for _ in range(20):
            result = ex.generate(1)
            assert "question" in result
            assert "options" in result
            assert "correct_index" in result
            assert "explanation" in result
            assert len(result["options"]) >= 5
            assert 0 <= result["correct_index"] < len(result["options"])
            assert result["difficulty"] == 1

    def test_difficulty_2(self):
        ex = ProportionalReasoning()
        for _ in range(20):
            result = ex.generate(2)
            assert result["difficulty"] == 2
            assert len(result["options"]) >= 5
            assert 0 <= result["correct_index"] < len(result["options"])

    def test_difficulty_3(self):
        ex = ProportionalReasoning()
        for _ in range(20):
            result = ex.generate(3)
            assert result["difficulty"] == 3
            assert len(result["options"]) >= 5
            assert 0 <= result["correct_index"] < len(result["options"])

    def test_difficulty_clamping(self):
        ex = ProportionalReasoning()
        result = ex.generate(0)
        assert result["difficulty"] == 1
        result = ex.generate(5)
        assert result["difficulty"] == 3


# ---------------------------------------------------------------------------
# Test that explanations contain formula steps
# ---------------------------------------------------------------------------

class TestExplanationContent:
    def test_explanations_have_steps(self):
        """Explanations should contain numbered steps and formula references."""
        ex = ProportionalReasoning()
        for difficulty in [1, 2, 3]:
            for _ in range(10):
                result = ex.generate(difficulty)
                expl = result["explanation"]
                # Should contain step numbers
                assert "1)" in expl, f"Missing step 1 in explanation: {expl}"
                assert "2)" in expl, f"Missing step 2 in explanation: {expl}"


# ---------------------------------------------------------------------------
# Test distractors are distinct from correct answer
# ---------------------------------------------------------------------------

class TestDistractors:
    def test_correct_not_in_wrong_options(self):
        ex = ProportionalReasoning()
        for difficulty in [1, 2, 3]:
            for _ in range(20):
                result = ex.generate(difficulty)
                correct = result["options"][result["correct_index"]]
                wrong = [
                    opt for i, opt in enumerate(result["options"])
                    if i != result["correct_index"]
                ]
                assert correct not in wrong, (
                    f"Correct '{correct}' duplicated in options {result['options']}"
                )

    def test_options_are_unique(self):
        ex = ProportionalReasoning()
        for difficulty in [1, 2, 3]:
            for _ in range(20):
                result = ex.generate(difficulty)
                options = result["options"]
                assert len(options) == len(set(options)), (
                    f"Duplicate options: {options}"
                )
