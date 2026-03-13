import pytest
import re

from exercises.number_sense import NumberSense


class TestDivisionRemainderBasic:
    """Tests for L1 — _division_remainder_basic."""

    def test_structure(self):
        ns = NumberSense()
        for _ in range(10):
            result = ns._division_remainder_basic()
            assert "question" in result
            assert "options" in result
            assert "correct_index" in result
            assert "explanation" in result
            assert "did_you_know" in result
            assert len(result["options"]) == 5
            assert 0 <= result["correct_index"] <= 4

    def test_all_options_are_strings(self):
        ns = NumberSense()
        for _ in range(10):
            result = ns._division_remainder_basic()
            for opt in result["options"]:
                assert isinstance(opt, str)

    def test_five_distinct_options(self):
        ns = NumberSense()
        for _ in range(10):
            result = ns._division_remainder_basic()
            assert len(set(result["options"])) == 5, (
                f"Options not distinct: {result['options']}"
            )

    def test_correct_answer_is_valid_remainder(self):
        ns = NumberSense()
        for _ in range(20):
            result = ns._division_remainder_basic()
            correct = result["options"][result["correct_index"]]
            # Extract a and b from the question
            match = re.search(r"divisione di (\d+) per (\d+)", result["question"])
            assert match is not None
            a, b = int(match.group(1)), int(match.group(2))
            expected_remainder = a % b
            assert int(correct) == expected_remainder

    def test_remainder_is_nonzero(self):
        ns = NumberSense()
        for _ in range(20):
            result = ns._division_remainder_basic()
            correct = result["options"][result["correct_index"]]
            assert int(correct) > 0


class TestDivisionRemainderFindNumber:
    """Tests for L2 — _division_remainder_find_number."""

    def test_structure(self):
        ns = NumberSense()
        for _ in range(10):
            result = ns._division_remainder_find_number()
            assert "question" in result
            assert len(result["options"]) == 5
            assert 0 <= result["correct_index"] <= 4

    def test_correct_answer_gives_expected_remainder(self):
        ns = NumberSense()
        for _ in range(20):
            result = ns._division_remainder_find_number()
            correct = int(result["options"][result["correct_index"]])
            # Extract d and r from the question
            match = re.search(r"diviso per (\d+), dà resto (\d+)", result["question"])
            assert match is not None
            d, r = int(match.group(1)), int(match.group(2))
            assert correct % d == r

    def test_five_distinct_options(self):
        ns = NumberSense()
        for _ in range(10):
            result = ns._division_remainder_find_number()
            assert len(set(result["options"])) == 5


class TestDivisionRemainderWordProblem:
    """Tests for L3 — _division_remainder_word_problem."""

    def test_structure(self):
        ns = NumberSense()
        for _ in range(10):
            result = ns._division_remainder_word_problem()
            assert "question" in result
            assert len(result["options"]) == 5
            assert 0 <= result["correct_index"] <= 4

    def test_correct_answer_format(self):
        ns = NumberSense()
        for _ in range(10):
            result = ns._division_remainder_word_problem()
            correct = result["options"][result["correct_index"]]
            # Should contain "completi" and a number pattern
            assert "completi" in correct

    def test_five_distinct_options(self):
        ns = NumberSense()
        for _ in range(10):
            result = ns._division_remainder_word_problem()
            assert len(set(result["options"])) == 5, (
                f"Options not distinct: {result['options']}"
            )

    def test_nonzero_remainder_in_problem(self):
        ns = NumberSense()
        for _ in range(20):
            result = ns._division_remainder_word_problem()
            correct = result["options"][result["correct_index"]]
            # Extract the remainder number from the correct answer
            # Format: "X gruppi completi, Y items verb"
            match = re.search(r"(\d+) \w+ completi, (\d+)", correct)
            assert match is not None
            remainder = int(match.group(2))
            assert remainder > 0


class TestDivisionRemainderProperties:
    """Tests for L2 — _division_remainder_properties."""

    def test_structure(self):
        ns = NumberSense()
        for _ in range(10):
            result = ns._division_remainder_properties()
            assert "question" in result
            assert len(result["options"]) == 5
            assert 0 <= result["correct_index"] <= 4

    def test_correct_answer_is_valid(self):
        ns = NumberSense()
        for _ in range(20):
            result = ns._division_remainder_properties()
            correct = int(result["options"][result["correct_index"]])
            # Extract d1 and r1 from question
            match = re.search(
                r"divisione di n per (\d+) è (\d+).*per (\d+)\?",
                result["question"],
            )
            assert match is not None
            d1, r1, d2 = int(match.group(1)), int(match.group(2)), int(match.group(3))
            # The correct answer should be r1 % d2
            assert correct == r1 % d2

    def test_five_distinct_options(self):
        ns = NumberSense()
        for _ in range(10):
            result = ns._division_remainder_properties()
            assert len(set(result["options"])) == 5


class TestDivisionRemainderIntegration:
    """Test that new templates integrate correctly with generate()."""

    def test_generate_difficulty_1_can_produce_remainder(self):
        ns = NumberSense()
        found = False
        for _ in range(200):
            result = ns.generate(difficulty=1)
            if "resto della divisione" in result.get("question", ""):
                found = True
                break
        assert found, "L1 generate() never produced a division remainder question"

    def test_generate_difficulty_2_can_produce_find_number(self):
        ns = NumberSense()
        found_find = False
        found_props = False
        for _ in range(200):
            result = ns.generate(difficulty=2)
            q = result.get("question", "")
            if "diviso per" in q and "dà resto" in q:
                found_find = True
            if "resto della divisione di n per" in q:
                found_props = True
            if found_find and found_props:
                break
        assert found_find, "L2 generate() never produced find-number question"
        assert found_props, "L2 generate() never produced properties question"

    def test_generate_difficulty_3_can_produce_word_problem(self):
        ns = NumberSense()
        found = False
        for _ in range(200):
            result = ns.generate(difficulty=3)
            if "completi" in result.get("question", ""):
                found = True
                break
        assert found, "L3 generate() never produced a word problem question"

    def test_generate_returns_difficulty(self):
        ns = NumberSense()
        for diff in [1, 2, 3]:
            result = ns.generate(difficulty=diff)
            assert result["difficulty"] == diff
