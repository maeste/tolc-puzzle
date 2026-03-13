import pytest

from exercises.statistics_exercise import (
    StatisticsExercise,
    _t_variable_classification_basic,
    _t_variable_classification_with_graph,
    _t_discrete_vs_continuous,
    _t_variable_classification_dataset,
    _ALL_CLASSIFICATIONS,
    _ALL_GRAPH_TYPES,
)


class TestVariableClassificationBasic:
    """Tests for L1 variable classification template."""

    def setup_method(self):
        self.se = StatisticsExercise()

    def test_basic_structure(self):
        for _ in range(5):
            result = _t_variable_classification_basic()
            assert "question" in result
            assert "options" in result
            assert "correct_index" in result
            assert "explanation" in result
            assert "did_you_know" in result
            assert "difficulty" in result
            assert len(result["options"]) == 5
            assert 0 <= result["correct_index"] <= 4

    def test_basic_correct_classification(self):
        for _ in range(20):
            result = _t_variable_classification_basic()
            correct = result["options"][result["correct_index"]]
            assert correct in _ALL_CLASSIFICATIONS

    def test_basic_all_options_unique(self):
        for _ in range(10):
            result = _t_variable_classification_basic()
            assert len(set(result["options"])) == 5, (
                f"Duplicate options found: {result['options']}"
            )

    def test_basic_difficulty_is_one(self):
        result = _t_variable_classification_basic()
        assert result["difficulty"] == 1

    def test_basic_question_contains_variable(self):
        for _ in range(10):
            result = _t_variable_classification_basic()
            assert "Come si classifica" in result["question"]

    def test_basic_explanation_contains_classification(self):
        for _ in range(5):
            result = _t_variable_classification_basic()
            correct = result["options"][result["correct_index"]]
            assert correct in result["explanation"]


class TestVariableClassificationWithGraph:
    """Tests for L2 variable + graph type template."""

    def test_graph_structure(self):
        for _ in range(5):
            result = _t_variable_classification_with_graph()
            assert "question" in result
            assert len(result["options"]) == 5
            assert 0 <= result["correct_index"] <= 4

    def test_graph_correct_answer_is_valid_graph(self):
        for _ in range(20):
            result = _t_variable_classification_with_graph()
            correct = result["options"][result["correct_index"]]
            assert correct in _ALL_GRAPH_TYPES, (
                f"Correct answer '{correct}' not in valid graph types"
            )

    def test_graph_all_options_unique(self):
        for _ in range(10):
            result = _t_variable_classification_with_graph()
            assert len(set(result["options"])) == 5

    def test_graph_difficulty_is_two(self):
        result = _t_variable_classification_with_graph()
        assert result["difficulty"] == 2

    def test_graph_question_mentions_variable_type(self):
        for _ in range(10):
            result = _t_variable_classification_with_graph()
            q = result["question"].lower()
            assert any(
                t.lower() in q
                for t in _ALL_CLASSIFICATIONS
            ), f"Question does not mention a variable type: {result['question']}"


class TestDiscreteVsContinuous:
    """Tests for L2 discrete vs continuous template."""

    def test_dvc_structure(self):
        for _ in range(5):
            result = _t_discrete_vs_continuous()
            assert "question" in result
            assert len(result["options"]) == 5
            assert 0 <= result["correct_index"] <= 4

    def test_dvc_all_options_unique(self):
        for _ in range(10):
            result = _t_discrete_vs_continuous()
            assert len(set(result["options"])) == 5, (
                f"Duplicate options: {result['options']}"
            )

    def test_dvc_question_asks_for_type(self):
        for _ in range(10):
            result = _t_discrete_vs_continuous()
            q = result["question"]
            assert "continua" in q or "discreta" in q

    def test_dvc_difficulty_is_two(self):
        result = _t_discrete_vs_continuous()
        assert result["difficulty"] == 2


class TestVariableClassificationDataset:
    """Tests for L3 dataset analysis template."""

    def test_dataset_structure(self):
        for _ in range(5):
            result = _t_variable_classification_dataset()
            assert "question" in result
            assert len(result["options"]) == 5
            assert 0 <= result["correct_index"] <= 4

    def test_dataset_correct_answer_is_number(self):
        for _ in range(10):
            result = _t_variable_classification_dataset()
            correct = result["options"][result["correct_index"]]
            assert correct.isdigit(), f"Expected numeric answer, got '{correct}'"

    def test_dataset_all_options_unique(self):
        for _ in range(10):
            result = _t_variable_classification_dataset()
            assert len(set(result["options"])) == 5

    def test_dataset_difficulty_is_three(self):
        result = _t_variable_classification_dataset()
        assert result["difficulty"] == 3

    def test_dataset_approfondimento_is_true(self):
        result = _t_variable_classification_dataset()
        assert result["approfondimento"] is True

    def test_dataset_question_mentions_indagine(self):
        for _ in range(5):
            result = _t_variable_classification_dataset()
            assert "indagine" in result["question"].lower()


class TestGenerateIntegration:
    """Tests for integration with generate() method."""

    def setup_method(self):
        self.se = StatisticsExercise()

    def test_generate_l1_includes_classification(self):
        """Verify classification template is in L1 list and callable via generate()."""
        from exercises.statistics_exercise import _t_variable_classification_basic
        assert _t_variable_classification_basic in self.se.TEMPLATES_L1
        result = _t_variable_classification_basic()
        assert "Come si classifica" in result["question"]
        assert len(result["options"]) == 5

    def test_generate_l2_includes_graph(self):
        """Verify graph template is in L2 list and callable via generate()."""
        from exercises.statistics_exercise import _t_variable_classification_with_graph
        assert _t_variable_classification_with_graph in self.se.TEMPLATES_L2
        result = _t_variable_classification_with_graph()
        assert "grafico" in result["question"].lower()
        assert len(result["options"]) == 5

    def test_generate_l3_includes_dataset(self):
        """Verify dataset template is in L3 list and callable via generate()."""
        from exercises.statistics_exercise import _t_variable_classification_dataset
        assert _t_variable_classification_dataset in self.se.TEMPLATES_L3
        result = _t_variable_classification_dataset()
        assert "indagine" in result["question"].lower()
        assert len(result["options"]) == 5

    def test_generate_all_difficulties_valid(self):
        """All difficulty levels produce valid exercise dicts."""
        for difficulty in [1, 2, 3]:
            for _ in range(5):
                result = self.se.generate(difficulty)
                assert isinstance(result, dict)
                assert "question" in result
                assert "options" in result
                assert "correct_index" in result
                assert "explanation" in result
                assert len(result["options"]) == 5
                assert 0 <= result["correct_index"] <= 4
                for opt in result["options"]:
                    assert isinstance(opt, str), f"Option is not string: {opt!r}"


class TestParametricVariation:
    """Test that templates produce varied outputs."""

    def test_basic_produces_different_variables(self):
        questions = set()
        for _ in range(30):
            result = _t_variable_classification_basic()
            questions.add(result["question"])
        assert len(questions) >= 5, (
            f"Expected at least 5 different questions, got {len(questions)}"
        )

    def test_graph_produces_different_variables(self):
        questions = set()
        for _ in range(30):
            result = _t_variable_classification_with_graph()
            questions.add(result["question"])
        assert len(questions) >= 5

    def test_dataset_produces_different_compositions(self):
        questions = set()
        for _ in range(30):
            result = _t_variable_classification_dataset()
            questions.add(result["question"])
        assert len(questions) >= 5
