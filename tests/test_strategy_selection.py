import pytest

from exercises.strategy_selection import StrategySelection


class TestBasicStructure:
    """Tests for basic exercise structure across all difficulties."""

    def setup_method(self):
        self.ex = StrategySelection()

    def test_l1_structure(self):
        for _ in range(10):
            result = self.ex.generate(1)
            assert "question" in result
            assert "options" in result
            assert "correct_index" in result
            assert "explanation" in result
            assert "did_you_know" in result
            assert result["difficulty"] == 1

    def test_l2_structure(self):
        for _ in range(10):
            result = self.ex.generate(2)
            assert "question" in result
            assert "options" in result
            assert "correct_index" in result
            assert "explanation" in result
            assert result["difficulty"] == 2

    def test_l3_structure(self):
        for _ in range(10):
            result = self.ex.generate(3)
            assert "question" in result
            assert "options" in result
            assert "correct_index" in result
            assert "explanation" in result
            assert result["difficulty"] == 3


class TestOptions:
    """Tests for option validity."""

    def setup_method(self):
        self.ex = StrategySelection()

    def test_exactly_five_options_l1(self):
        for _ in range(10):
            result = self.ex.generate(1)
            assert len(result["options"]) == 5

    def test_exactly_five_options_l2(self):
        for _ in range(10):
            result = self.ex.generate(2)
            assert len(result["options"]) == 5

    def test_exactly_five_options_l3(self):
        for _ in range(10):
            result = self.ex.generate(3)
            assert len(result["options"]) == 5

    def test_options_are_nonempty_strings(self):
        for difficulty in [1, 2, 3]:
            for _ in range(10):
                result = self.ex.generate(difficulty)
                for opt in result["options"]:
                    assert isinstance(opt, str), f"Option is not string: {opt!r}"
                    assert len(opt) > 0, "Option is empty string"

    def test_options_are_unique(self):
        for difficulty in [1, 2, 3]:
            for _ in range(10):
                result = self.ex.generate(difficulty)
                assert len(set(result["options"])) == 5, (
                    f"Duplicate options at difficulty {difficulty}: {result['options']}"
                )


class TestCorrectIndex:
    """Tests for correct_index validity."""

    def setup_method(self):
        self.ex = StrategySelection()

    def test_correct_index_in_range(self):
        for difficulty in [1, 2, 3]:
            for _ in range(10):
                result = self.ex.generate(difficulty)
                assert 0 <= result["correct_index"] < 5, (
                    f"correct_index {result['correct_index']} out of range"
                )


class TestDifficultyClamping:
    """Tests for difficulty clamping behavior."""

    def setup_method(self):
        self.ex = StrategySelection()

    def test_clamp_zero_to_one(self):
        result = self.ex.generate(0)
        assert result["difficulty"] == 1

    def test_clamp_negative_to_one(self):
        result = self.ex.generate(-5)
        assert result["difficulty"] == 1

    def test_clamp_high_to_three(self):
        result = self.ex.generate(5)
        assert result["difficulty"] == 3

    def test_clamp_very_high_to_three(self):
        result = self.ex.generate(100)
        assert result["difficulty"] == 3


class TestApprofondimento:
    """Tests for approfondimento field."""

    def setup_method(self):
        self.ex = StrategySelection()

    def test_l1_approfondimento_false(self):
        for _ in range(10):
            result = self.ex.generate(1)
            assert result["approfondimento"] is False

    def test_l2_approfondimento_false(self):
        for _ in range(10):
            result = self.ex.generate(2)
            assert result["approfondimento"] is False

    def test_l3_approfondimento_true(self):
        for _ in range(10):
            result = self.ex.generate(3)
            assert result["approfondimento"] is True


class TestCheckMethod:
    """Tests for the check() method."""

    def setup_method(self):
        self.ex = StrategySelection()

    def test_check_correct_answer(self):
        for difficulty in [1, 2, 3]:
            result = self.ex.generate(difficulty)
            check_data = {
                "answer": result["correct_index"],
                "exercise": result,
            }
            response = self.ex.check(check_data)
            assert response["correct"] is True
            assert response["correct_index"] == result["correct_index"]
            assert "explanation" in response

    def test_check_wrong_answer(self):
        for difficulty in [1, 2, 3]:
            result = self.ex.generate(difficulty)
            wrong_index = (result["correct_index"] + 1) % 5
            check_data = {
                "answer": wrong_index,
                "exercise": result,
            }
            response = self.ex.check(check_data)
            assert response["correct"] is False
            assert response["correct_index"] == result["correct_index"]


class TestTemplateCoverage:
    """Tests that all templates are reachable."""

    def setup_method(self):
        self.ex = StrategySelection()

    def test_l1_hits_multiple_templates(self):
        questions = set()
        for _ in range(100):
            result = self.ex.generate(1)
            # Extract a signature from the question to distinguish templates
            q = result["question"]
            if "lineare" in result.get("explanation", "").lower() or "isolamento" in str(result["options"]):
                questions.add("linear")
            elif "fattorizza" in result.get("explanation", "").lower():
                questions.add("factorable")
            elif "discriminante" in result.get("explanation", "").lower():
                questions.add("irrational")
            elif "quadrato perfetto" in result.get("explanation", "").lower():
                questions.add("perfect_square")
        assert len(questions) >= 3, (
            f"Expected at least 3 L1 templates hit, got {len(questions)}: {questions}"
        )

    def test_l2_hits_multiple_templates(self):
        questions = set()
        for _ in range(100):
            result = self.ex.generate(2)
            explanation = result.get("explanation", "").lower()
            if "fattore comune" in explanation:
                questions.add("common_factor")
            elif "differenza di quadrati" in explanation:
                questions.add("diff_squares")
            elif "cubi" in explanation:
                questions.add("cubes")
            elif "forma canonica" in explanation:
                questions.add("completing")
        assert len(questions) >= 3, (
            f"Expected at least 3 L2 templates hit, got {len(questions)}: {questions}"
        )

    def test_l3_hits_multiple_templates(self):
        questions = set()
        for _ in range(100):
            result = self.ex.generate(3)
            explanation = result.get("explanation", "").lower()
            if "collinear" in explanation or "allineati" in explanation:
                questions.add("collinear")
            elif "coseno" in explanation:
                questions.add("angle")
            elif "gauss" in explanation or "laccio" in explanation:
                questions.add("area")
            elif "asse" in explanation or "equidistant" in explanation:
                questions.add("bisector")
        assert len(questions) >= 3, (
            f"Expected at least 3 L3 templates hit, got {len(questions)}: {questions}"
        )


class TestQuestionContent:
    """Tests for question content quality."""

    def setup_method(self):
        self.ex = StrategySelection()

    def test_l1_question_contains_strategy_keyword(self):
        for _ in range(10):
            result = self.ex.generate(1)
            assert "strategia" in result["question"].lower()

    def test_l2_question_contains_strategy_keyword(self):
        for _ in range(10):
            result = self.ex.generate(2)
            assert "strategia" in result["question"].lower()

    def test_l3_question_contains_approccio_keyword(self):
        for _ in range(10):
            result = self.ex.generate(3)
            assert "approccio" in result["question"].lower()

    def test_explanation_is_nonempty(self):
        for difficulty in [1, 2, 3]:
            for _ in range(5):
                result = self.ex.generate(difficulty)
                assert len(result["explanation"]) > 20, (
                    f"Explanation too short: {result['explanation']}"
                )


class TestVariation:
    """Tests that generated exercises vary across runs."""

    def setup_method(self):
        self.ex = StrategySelection()

    def test_l1_produces_varied_questions(self):
        questions = set()
        for _ in range(50):
            result = self.ex.generate(1)
            questions.add(result["question"])
        assert len(questions) >= 5, (
            f"Expected at least 5 unique L1 questions, got {len(questions)}"
        )

    def test_l2_produces_varied_questions(self):
        questions = set()
        for _ in range(50):
            result = self.ex.generate(2)
            questions.add(result["question"])
        assert len(questions) >= 5, (
            f"Expected at least 5 unique L2 questions, got {len(questions)}"
        )

    def test_l3_produces_varied_questions(self):
        questions = set()
        for _ in range(50):
            result = self.ex.generate(3)
            questions.add(result["question"])
        assert len(questions) >= 5, (
            f"Expected at least 5 unique L3 questions, got {len(questions)}"
        )
