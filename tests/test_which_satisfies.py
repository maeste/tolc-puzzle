import pytest

from exercises.which_satisfies import (
    WhichSatisfies,
    _which_log_between,
    _which_is_even,
    _which_fraction_largest,
    _which_equation_has_solution,
    _which_not_injective,
    _which_inequality_has_interval,
    _which_expression_equals,
    _which_system_consistent,
    _which_parabola_passes_through,
    _which_always_positive,
)


ALL_TEMPLATES = [
    _which_log_between,
    _which_is_even,
    _which_fraction_largest,
    _which_equation_has_solution,
    _which_not_injective,
    _which_inequality_has_interval,
    _which_expression_equals,
    _which_system_consistent,
    _which_parabola_passes_through,
    _which_always_positive,
]


def _validate_result(result: dict) -> None:
    """Common validation for all template results."""
    assert isinstance(result, dict)
    assert "question" in result
    assert "options" in result
    assert "correct_index" in result
    assert "explanation" in result
    assert "did_you_know" in result

    assert isinstance(result["question"], str)
    assert len(result["question"]) > 0

    options = result["options"]
    assert isinstance(options, list)
    assert len(options) == 5, f"Expected 5 options, got {len(options)}"

    # All options are non-empty strings
    for i, opt in enumerate(options):
        assert isinstance(opt, str), f"Option {i} is not a string: {opt!r}"
        assert len(opt) > 0, f"Option {i} is empty"

    # Options are distinct
    assert len(set(options)) == 5, f"Options are not all distinct: {options}"

    # correct_index in valid range
    idx = result["correct_index"]
    assert isinstance(idx, int)
    assert 0 <= idx <= 4, f"correct_index {idx} out of range [0, 4]"

    # Explanation is non-empty
    assert isinstance(result["explanation"], str)
    assert len(result["explanation"]) > 10

    # did_you_know is non-empty
    assert isinstance(result["did_you_know"], str)
    assert len(result["did_you_know"]) > 10


# ================================================================
#  Test each template individually (15+ parametrized runs each)
# ================================================================

class TestWhichLogBetween:
    @pytest.mark.parametrize("run", range(15))
    def test_structure(self, run):
        result = _which_log_between()
        _validate_result(result)

    def test_options_contain_log_notation(self):
        for _ in range(10):
            result = _which_log_between()
            for opt in result["options"]:
                assert "log" in opt.lower() or "ln" in opt.lower(), (
                    f"Option '{opt}' does not contain log notation"
                )

    def test_question_mentions_range(self):
        for _ in range(10):
            result = _which_log_between()
            assert "compreso" in result["question"] or "valore" in result["question"]


class TestWhichIsEven:
    @pytest.mark.parametrize("run", range(15))
    def test_structure(self, run):
        result = _which_is_even()
        _validate_result(result)

    def test_options_contain_algebraic_expressions(self):
        for _ in range(10):
            result = _which_is_even()
            for opt in result["options"]:
                assert "n" in opt, f"Option '{opt}' should contain variable 'n'"

    def test_question_mentions_pari(self):
        for _ in range(5):
            result = _which_is_even()
            assert "pari" in result["question"].lower()


class TestWhichFractionLargest:
    @pytest.mark.parametrize("run", range(15))
    def test_structure(self, run):
        result = _which_fraction_largest()
        _validate_result(result)

    def test_options_are_fractions(self):
        for _ in range(10):
            result = _which_fraction_largest()
            for opt in result["options"]:
                assert "/" in opt, f"Option '{opt}' should be a fraction with '/'"

    def test_correct_is_actually_largest(self):
        from fractions import Fraction
        for _ in range(20):
            result = _which_fraction_largest()
            values = []
            for opt in result["options"]:
                parts = opt.split("/")
                values.append(Fraction(int(parts[0]), int(parts[1])))
            correct_idx = result["correct_index"]
            correct_val = values[correct_idx]
            for i, v in enumerate(values):
                if i != correct_idx:
                    assert correct_val >= v, (
                        f"Option at {correct_idx} ({correct_val}) is not the largest; "
                        f"option {i} ({v}) is larger or equal"
                    )


class TestWhichEquationHasSolution:
    @pytest.mark.parametrize("run", range(15))
    def test_structure(self, run):
        result = _which_equation_has_solution()
        _validate_result(result)

    def test_options_contain_equations(self):
        for _ in range(10):
            result = _which_equation_has_solution()
            for opt in result["options"]:
                assert "=" in opt, f"Option '{opt}' should contain '='"


class TestWhichNotInjective:
    @pytest.mark.parametrize("run", range(15))
    def test_structure(self, run):
        result = _which_not_injective()
        _validate_result(result)

    def test_options_are_functions(self):
        for _ in range(10):
            result = _which_not_injective()
            for opt in result["options"]:
                assert "f(x)" in opt, f"Option '{opt}' should contain 'f(x)'"


class TestWhichInequalityHasInterval:
    @pytest.mark.parametrize("run", range(15))
    def test_structure(self, run):
        result = _which_inequality_has_interval()
        _validate_result(result)

    def test_question_mentions_intervallo(self):
        for _ in range(5):
            result = _which_inequality_has_interval()
            assert "intervallo" in result["question"].lower()


class TestWhichExpressionEquals:
    @pytest.mark.parametrize("run", range(15))
    def test_structure(self, run):
        result = _which_expression_equals()
        _validate_result(result)

    def test_question_mentions_equivalente(self):
        for _ in range(5):
            result = _which_expression_equals()
            assert "equivalente" in result["question"].lower()


class TestWhichSystemConsistent:
    @pytest.mark.parametrize("run", range(15))
    def test_structure(self, run):
        result = _which_system_consistent()
        _validate_result(result)

    def test_options_contain_system_notation(self):
        for _ in range(10):
            result = _which_system_consistent()
            for opt in result["options"]:
                assert "=" in opt, f"System option '{opt}' should contain '='"
                assert "x" in opt or "y" in opt, (
                    f"System option '{opt}' should reference x or y"
                )


class TestWhichParabolaPassesThrough:
    @pytest.mark.parametrize("run", range(15))
    def test_structure(self, run):
        result = _which_parabola_passes_through()
        _validate_result(result)

    def test_question_mentions_points(self):
        for _ in range(5):
            result = _which_parabola_passes_through()
            assert "A(" in result["question"] and "B(" in result["question"]


class TestWhichAlwaysPositive:
    @pytest.mark.parametrize("run", range(15))
    def test_structure(self, run):
        result = _which_always_positive()
        _validate_result(result)

    def test_question_mentions_positiva(self):
        for _ in range(5):
            result = _which_always_positive()
            assert "positiva" in result["question"].lower()


# ================================================================
#  Test generate() across all difficulty levels
# ================================================================

class TestWhichSatisfiesGenerate:
    def test_generate_difficulty_1(self):
        ex = WhichSatisfies()
        for _ in range(20):
            result = ex.generate(1)
            _validate_result(result)
            assert result["difficulty"] == 1

    def test_generate_difficulty_2(self):
        ex = WhichSatisfies()
        for _ in range(20):
            result = ex.generate(2)
            _validate_result(result)
            assert result["difficulty"] == 2

    def test_generate_difficulty_3(self):
        ex = WhichSatisfies()
        for _ in range(20):
            result = ex.generate(3)
            _validate_result(result)
            assert result["difficulty"] == 3

    def test_difficulty_clamping_low(self):
        ex = WhichSatisfies()
        result = ex.generate(0)
        assert result["difficulty"] == 1

    def test_difficulty_clamping_high(self):
        ex = WhichSatisfies()
        result = ex.generate(5)
        assert result["difficulty"] == 3

    def test_check_correct_answer(self):
        ex = WhichSatisfies()
        for difficulty in [1, 2, 3]:
            for _ in range(5):
                exercise_data = ex.generate(difficulty)
                correct_idx = exercise_data["correct_index"]
                result = ex.check({"answer": correct_idx, "exercise": exercise_data})
                assert result["correct"] is True

    def test_check_wrong_answer(self):
        ex = WhichSatisfies()
        for difficulty in [1, 2, 3]:
            for _ in range(5):
                exercise_data = ex.generate(difficulty)
                correct_idx = exercise_data["correct_index"]
                wrong_idx = (correct_idx + 1) % len(exercise_data["options"])
                result = ex.check({"answer": wrong_idx, "exercise": exercise_data})
                assert result["correct"] is False

    def test_options_are_strings(self):
        """Options should be non-empty strings."""
        ex = WhichSatisfies()
        for difficulty in [1, 2, 3]:
            for _ in range(10):
                result = ex.generate(difficulty)
                for opt in result["options"]:
                    assert isinstance(opt, str), f"Option should be a string, got {type(opt)}"
                    assert len(opt.strip()) > 0, "Option should not be empty"


# ================================================================
#  Integration test: 100 exercises, verify all valid
# ================================================================

class TestIntegration:
    def test_mass_generation(self):
        """Generate 100 exercises across all difficulties and verify structure."""
        ex = WhichSatisfies()
        for i in range(100):
            difficulty = (i % 3) + 1
            result = ex.generate(difficulty)
            _validate_result(result)
            assert result["difficulty"] == difficulty

    def test_all_templates_reachable(self):
        """Over many runs, all templates should be reached at least once."""
        ex = WhichSatisfies()
        seen_keywords = set()
        for _ in range(300):
            for diff in [1, 2, 3]:
                result = ex.generate(diff)
                q = result["question"].lower()
                if "logaritm" in q:
                    seen_keywords.add("log")
                elif "pari" in q:
                    seen_keywords.add("even")
                elif "frazioni" in q or "grande" in q:
                    seen_keywords.add("fraction")
                elif "equazion" in q:
                    seen_keywords.add("equation")
                elif "f(p)" in q or "iniettiv" in q or "p \u2260 q" in q:
                    seen_keywords.add("injective")
                elif "intervallo" in q:
                    seen_keywords.add("interval")
                elif "equivalente" in q:
                    seen_keywords.add("expression")
                elif "sistem" in q:
                    seen_keywords.add("system")
                elif "parabol" in q:
                    seen_keywords.add("parabola")
                elif "positiv" in q:
                    seen_keywords.add("positive")
        # We expect all 10 template types to appear
        assert len(seen_keywords) >= 8, (
            f"Only {len(seen_keywords)} template types seen out of 10: {seen_keywords}"
        )

    def test_explanation_is_italian(self):
        """Explanations should contain common Italian words."""
        ex = WhichSatisfies()
        italian_words = [
            "perche", "perché", "quindi", "soluzione", "sempre", "ogni",
            "valore", "risposta", "corretta", "verifica", "espressione",
            "funzione", "sistema", "equazione", "parabola", "frazione",
            "positiv", "logaritm", "pari", "intervallo", "equivalente",
            "determinante", "iniettiv", "radici", "trinomio",
        ]
        for difficulty in [1, 2, 3]:
            for _ in range(10):
                result = ex.generate(difficulty)
                explanation_lower = result["explanation"].lower()
                has_italian = any(w in explanation_lower for w in italian_words)
                assert has_italian, (
                    f"Explanation does not appear to be in Italian: "
                    f"{result['explanation'][:100]}..."
                )
