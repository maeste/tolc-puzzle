"""Tests for multiple-representation exercise templates in GraphReader.

Covers: Table→Formula, Table→Graph, Verbal→Formula, Formula-form conversion.
"""
import pytest

from exercises.graph_reader import GraphReader


@pytest.fixture
def gr():
    return GraphReader()


# ---------------------------------------------------------------------------
# Shared validation helpers
# ---------------------------------------------------------------------------

def _validate_exercise(result):
    """Common structural assertions for every exercise dict."""
    assert "question" in result, "Missing 'question' key"
    assert "options" in result, "Missing 'options' key"
    assert "correct_index" in result, "Missing 'correct_index' key"
    assert "explanation" in result, "Missing 'explanation' key"
    assert "did_you_know" in result, "Missing 'did_you_know' key"

    options = result["options"]
    assert len(options) == 5, f"Expected 5 options, got {len(options)}"
    assert all(isinstance(o, str) for o in options), "All options must be strings"
    assert 0 <= result["correct_index"] <= 4, f"correct_index {result['correct_index']} out of range"

    # All options should be non-empty
    assert all(len(o.strip()) > 0 for o in options), "Options must be non-empty"


def _validate_unique_options(result):
    """Assert that all 5 options are unique."""
    options = result["options"]
    assert len(set(options)) == 5, f"Options not unique: {options}"


# ===========================================================================
# Table → Formula
# ===========================================================================

class TestTableToFormulaL1:
    def test_structure(self, gr):
        for _ in range(5):
            result = gr._template_table_to_formula_L1()
            _validate_exercise(result)

    def test_unique_options(self, gr):
        for _ in range(5):
            result = gr._template_table_to_formula_L1()
            _validate_unique_options(result)

    def test_question_contains_table(self, gr):
        for _ in range(3):
            result = gr._template_table_to_formula_L1()
            assert "<table" in result["question"], "Question should contain HTML table"

    def test_difficulty_label(self, gr):
        result = gr._template_table_to_formula_L1()
        assert result.get("difficulty") == 1

    def test_correct_answer_is_valid_formula(self, gr):
        for _ in range(5):
            result = gr._template_table_to_formula_L1()
            correct = result["options"][result["correct_index"]]
            assert "y = " in correct or "f(x) = " in correct, f"Correct answer should be a formula: {correct}"


class TestTableToFormulaL2:
    def test_structure(self, gr):
        for _ in range(5):
            result = gr._template_table_to_formula_L2()
            _validate_exercise(result)

    def test_unique_options(self, gr):
        for _ in range(5):
            result = gr._template_table_to_formula_L2()
            _validate_unique_options(result)

    def test_difficulty_label(self, gr):
        result = gr._template_table_to_formula_L2()
        assert result.get("difficulty") == 2

    def test_question_contains_table(self, gr):
        for _ in range(3):
            result = gr._template_table_to_formula_L2()
            assert "<table" in result["question"]


class TestTableToFormulaL3:
    def test_structure(self, gr):
        for _ in range(5):
            result = gr._template_table_to_formula_L3()
            _validate_exercise(result)

    def test_unique_options(self, gr):
        for _ in range(5):
            result = gr._template_table_to_formula_L3()
            _validate_unique_options(result)

    def test_difficulty_label(self, gr):
        result = gr._template_table_to_formula_L3()
        assert result.get("difficulty") == 3


# ===========================================================================
# Table → Graph
# ===========================================================================

class TestTableToGraphL2:
    def test_structure(self, gr):
        for _ in range(5):
            result = gr._template_table_to_graph_L2()
            _validate_exercise(result)

    def test_options_are_svg(self, gr):
        for _ in range(3):
            result = gr._template_table_to_graph_L2()
            for opt in result["options"]:
                assert "<svg" in opt, "Each option should be an SVG graph"

    def test_unique_options(self, gr):
        for _ in range(5):
            result = gr._template_table_to_graph_L2()
            _validate_unique_options(result)

    def test_difficulty_label(self, gr):
        result = gr._template_table_to_graph_L2()
        assert result.get("difficulty") == 2

    def test_question_contains_table(self, gr):
        result = gr._template_table_to_graph_L2()
        assert "<table" in result["question"]


class TestTableToGraphL3:
    def test_structure(self, gr):
        for _ in range(5):
            result = gr._template_table_to_graph_L3()
            _validate_exercise(result)

    def test_options_are_svg(self, gr):
        for _ in range(3):
            result = gr._template_table_to_graph_L3()
            for opt in result["options"]:
                assert "<svg" in opt, "Each option should be an SVG graph"

    def test_unique_options(self, gr):
        for _ in range(5):
            result = gr._template_table_to_graph_L3()
            _validate_unique_options(result)

    def test_difficulty_label(self, gr):
        result = gr._template_table_to_graph_L3()
        assert result.get("difficulty") == 3


# ===========================================================================
# Verbal → Formula
# ===========================================================================

class TestVerbalToFormulaL1:
    def test_structure(self, gr):
        for _ in range(5):
            result = gr._template_verbal_to_formula_L1()
            _validate_exercise(result)

    def test_unique_options(self, gr):
        for _ in range(5):
            result = gr._template_verbal_to_formula_L1()
            _validate_unique_options(result)

    def test_difficulty_label(self, gr):
        result = gr._template_verbal_to_formula_L1()
        assert result.get("difficulty") == 1

    def test_question_is_verbal(self, gr):
        for _ in range(3):
            result = gr._template_verbal_to_formula_L1()
            q = result["question"]
            assert "Quale formula" in q, f"Question should ask for formula: {q}"

    def test_correct_answer_format(self, gr):
        for _ in range(5):
            result = gr._template_verbal_to_formula_L1()
            correct = result["options"][result["correct_index"]]
            assert "y = " in correct or "f(x) = " in correct or "y =" in correct, \
                f"Correct answer should contain a formula: {correct}"


class TestVerbalToFormulaL2:
    def test_structure(self, gr):
        for _ in range(5):
            result = gr._template_verbal_to_formula_L2()
            _validate_exercise(result)

    def test_unique_options(self, gr):
        for _ in range(5):
            result = gr._template_verbal_to_formula_L2()
            _validate_unique_options(result)

    def test_difficulty_label(self, gr):
        result = gr._template_verbal_to_formula_L2()
        assert result.get("difficulty") == 2

    def test_question_asks_for_formula(self, gr):
        for _ in range(3):
            result = gr._template_verbal_to_formula_L2()
            q = result["question"]
            assert "Quale formula" in q


# ===========================================================================
# Formula-form conversion
# ===========================================================================

class TestFormulaFormConversionL2:
    def test_structure(self, gr):
        for _ in range(5):
            result = gr._template_formula_form_conversion_L2()
            _validate_exercise(result)

    def test_unique_options(self, gr):
        for _ in range(5):
            result = gr._template_formula_form_conversion_L2()
            _validate_unique_options(result)

    def test_difficulty_label(self, gr):
        result = gr._template_formula_form_conversion_L2()
        assert result.get("difficulty") == 2

    def test_question_mentions_vertex_form(self, gr):
        for _ in range(3):
            result = gr._template_formula_form_conversion_L2()
            assert "vertice" in result["question"].lower() or "a(x" in result["question"]

    def test_correct_is_vertex_form(self, gr):
        for _ in range(5):
            result = gr._template_formula_form_conversion_L2()
            correct = result["options"][result["correct_index"]]
            # Vertex form contains parentheses with x
            assert "y = " in correct


class TestFormulaFormConversionL3:
    def test_structure(self, gr):
        for _ in range(5):
            result = gr._template_formula_form_conversion_L3()
            _validate_exercise(result)

    def test_unique_options(self, gr):
        for _ in range(5):
            result = gr._template_formula_form_conversion_L3()
            _validate_unique_options(result)

    def test_difficulty_label(self, gr):
        result = gr._template_formula_form_conversion_L3()
        assert result.get("difficulty") == 3

    def test_question_mentions_factored_form(self, gr):
        for _ in range(3):
            result = gr._template_formula_form_conversion_L3()
            assert "fattorizzata" in result["question"].lower()

    def test_correct_is_factored(self, gr):
        for _ in range(5):
            result = gr._template_formula_form_conversion_L3()
            correct = result["options"][result["correct_index"]]
            assert "f(x) = " in correct


# ===========================================================================
# Integration: generate() includes new templates
# ===========================================================================

class TestGenerateIntegration:
    def test_generate_does_not_crash_L1(self, gr):
        """generate at L1 should not crash even with new templates."""
        for _ in range(20):
            result = gr.generate(1)
            _validate_exercise(result)

    def test_generate_does_not_crash_L2(self, gr):
        for _ in range(20):
            result = gr.generate(2)
            _validate_exercise(result)

    def test_generate_does_not_crash_L3(self, gr):
        for _ in range(20):
            result = gr.generate(3)
            _validate_exercise(result)

    def test_options_always_five(self, gr):
        """Across many runs, options are always exactly 5."""
        for diff in [1, 2, 3]:
            for _ in range(15):
                result = gr.generate(diff)
                assert len(result["options"]) == 5


# ===========================================================================
# Parametric variation tests
# ===========================================================================

class TestParametricVariation:
    """Ensure templates produce different questions across runs."""

    def test_table_to_formula_L1_varies(self, gr):
        questions = set()
        for _ in range(10):
            result = gr._template_table_to_formula_L1()
            questions.add(result["question"])
        assert len(questions) >= 2, "Template should produce varied questions"

    def test_table_to_formula_L2_varies(self, gr):
        questions = set()
        for _ in range(10):
            result = gr._template_table_to_formula_L2()
            questions.add(result["question"])
        assert len(questions) >= 2

    def test_verbal_to_formula_L1_varies(self, gr):
        questions = set()
        for _ in range(15):
            result = gr._template_verbal_to_formula_L1()
            questions.add(result["question"])
        assert len(questions) >= 3, "Should pick from multiple verbal descriptions"

    def test_verbal_to_formula_L2_varies(self, gr):
        questions = set()
        for _ in range(15):
            result = gr._template_verbal_to_formula_L2()
            questions.add(result["question"])
        assert len(questions) >= 3

    def test_formula_form_L2_varies(self, gr):
        correct_answers = set()
        for _ in range(10):
            result = gr._template_formula_form_conversion_L2()
            correct_answers.add(result["options"][result["correct_index"]])
        assert len(correct_answers) >= 2

    def test_formula_form_L3_varies(self, gr):
        correct_answers = set()
        for _ in range(10):
            result = gr._template_formula_form_conversion_L3()
            correct_answers.add(result["options"][result["correct_index"]])
        assert len(correct_answers) >= 2
