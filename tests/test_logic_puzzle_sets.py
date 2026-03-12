import pytest

from exercises.logic_puzzle import LogicPuzzle


@pytest.fixture
def puzzle():
    return LogicPuzzle()


# ------------------------------------------------------------------
# Individual template smoke tests (10 iterations each, no exceptions)
# ------------------------------------------------------------------

class TestSetMembership:
    def test_returns_valid_tuple(self):
        for _ in range(10):
            result = LogicPuzzle._set_membership()
            assert isinstance(result, tuple)
            assert len(result) == 5
            question, correct, distractors, explanation, tip = result
            assert isinstance(question, str)
            assert isinstance(correct, str)
            assert isinstance(distractors, list)
            assert len(distractors) == 4
            assert isinstance(explanation, str)
            assert isinstance(tip, str)

    def test_correct_uses_membership_symbol(self):
        for _ in range(10):
            _, correct, _, _, _ = LogicPuzzle._set_membership()
            assert "∈" in correct


class TestSetBasicOperations:
    def test_returns_valid_tuple(self):
        for _ in range(10):
            result = LogicPuzzle._set_basic_operations()
            assert isinstance(result, tuple)
            assert len(result) == 5
            question, correct, distractors, explanation, tip = result
            assert isinstance(question, str)
            assert isinstance(correct, str)
            assert isinstance(distractors, list)
            assert len(distractors) == 4

    def test_correct_is_set_notation(self):
        for _ in range(10):
            _, correct, _, _, _ = LogicPuzzle._set_basic_operations()
            assert correct.startswith("{")
            assert correct.endswith("}")


class TestSetInclusion:
    def test_returns_valid_tuple(self):
        for _ in range(10):
            result = LogicPuzzle._set_inclusion()
            assert isinstance(result, tuple)
            assert len(result) == 5
            _, _, distractors, _, _ = result
            assert len(distractors) == 4

    def test_correct_answer_is_subset(self):
        for _ in range(10):
            _, correct, _, _, _ = LogicPuzzle._set_inclusion()
            assert "A ⊂ B" in correct


class TestSetComplementDifference:
    def test_returns_valid_tuple(self):
        for _ in range(10):
            result = LogicPuzzle._set_complement_difference()
            assert isinstance(result, tuple)
            assert len(result) == 5
            _, _, distractors, _, _ = result
            assert len(distractors) == 4


class TestSetCompoundOperations:
    def test_returns_valid_tuple(self):
        for _ in range(10):
            result = LogicPuzzle._set_compound_operations()
            assert isinstance(result, tuple)
            assert len(result) == 5
            _, _, distractors, _, _ = result
            assert len(distractors) == 4

    def test_question_has_parentheses(self):
        for _ in range(10):
            question, _, _, _, _ = LogicPuzzle._set_compound_operations()
            assert "(" in question and ")" in question


class TestSetVennCounting:
    def test_returns_valid_tuple(self):
        for _ in range(10):
            result = LogicPuzzle._set_venn_counting()
            assert isinstance(result, tuple)
            assert len(result) == 5
            _, correct, distractors, _, _ = result
            assert len(distractors) == 4
            # correct answer should be a number
            assert correct.isdigit()

    def test_inclusion_exclusion_is_correct(self):
        """Verify the math: union = a + b - both."""
        for _ in range(10):
            question, correct, distractors, _, _ = LogicPuzzle._set_venn_counting()
            union = int(correct)
            # the first distractor is a + b (no subtraction)
            sum_ab = int(distractors[0])
            both = int(distractors[1])
            assert union == sum_ab - both


class TestSetThreeSetsVenn:
    def test_returns_valid_tuple(self):
        for _ in range(10):
            result = LogicPuzzle._set_three_sets_venn()
            assert isinstance(result, tuple)
            assert len(result) == 5
            _, correct, distractors, _, _ = result
            assert len(distractors) == 4
            assert correct.isdigit()


# ------------------------------------------------------------------
# Integration: generate() at each difficulty level
# ------------------------------------------------------------------

class TestGenerateIntegration:
    def test_generate_level_1(self, puzzle):
        for _ in range(20):
            result = puzzle.generate(1)
            assert "question" in result
            assert "options" in result
            assert "correct_index" in result
            assert "explanation" in result
            assert len(result["options"]) == 5
            assert 0 <= result["correct_index"] < 5

    def test_generate_level_2(self, puzzle):
        for _ in range(20):
            result = puzzle.generate(2)
            assert "question" in result
            assert "options" in result
            assert "correct_index" in result
            assert "explanation" in result
            assert len(result["options"]) == 5
            assert 0 <= result["correct_index"] < 5

    def test_generate_level_3(self, puzzle):
        for _ in range(20):
            result = puzzle.generate(3)
            assert "question" in result
            assert "options" in result
            assert "correct_index" in result
            assert "explanation" in result
            assert len(result["options"]) == 5
            assert 0 <= result["correct_index"] < 5

    def test_difficulty_clamping(self, puzzle):
        result_low = puzzle.generate(0)
        assert result_low["difficulty"] == 1
        result_high = puzzle.generate(99)
        assert result_high["difficulty"] == 3
