import pytest

from exercises.statistics_exercise import (
    StatisticsExercise,
    _t_frequency_absolute_from_data,
    _t_frequency_from_histogram,
    _t_frequency_relative_percentage,
    _t_frequency_compare,
    _t_frequency_reconstruct_stats,
)


@pytest.fixture
def ex():
    return StatisticsExercise()


# ---------------------------------------------------------------------------
# Direct template tests
# ---------------------------------------------------------------------------


class TestFrequencyAbsoluteFromData:
    def test_structure(self):
        for _ in range(30):
            result = _t_frequency_absolute_from_data()
            assert "question" in result
            assert "options" in result
            assert "correct_index" in result
            assert "explanation" in result
            assert "did_you_know" in result
            assert result["difficulty"] == 1
            assert result["approfondimento"] is False

    def test_options_valid(self):
        for _ in range(20):
            result = _t_frequency_absolute_from_data()
            assert len(result["options"]) == 5
            assert 0 <= result["correct_index"] < 5
            for opt in result["options"]:
                assert isinstance(opt, str)
                assert len(opt.strip()) > 0

    def test_question_mentions_frequenza(self):
        for _ in range(20):
            result = _t_frequency_absolute_from_data()
            assert "frequenza" in result["question"].lower()


class TestFrequencyFromHistogram:
    def test_structure(self):
        for _ in range(30):
            result = _t_frequency_from_histogram()
            assert "question" in result
            assert "options" in result
            assert "correct_index" in result
            assert "explanation" in result
            assert result["difficulty"] == 1
            assert result["approfondimento"] is False

    def test_options_valid(self):
        for _ in range(20):
            result = _t_frequency_from_histogram()
            assert len(result["options"]) == 5
            assert 0 <= result["correct_index"] < 5
            for opt in result["options"]:
                assert isinstance(opt, str)
                assert len(opt.strip()) > 0

    def test_question_mentions_istogramma(self):
        for _ in range(20):
            result = _t_frequency_from_histogram()
            q = result["question"].lower()
            assert "istogramma" in q or "frequenza" in q


class TestFrequencyRelativePercentage:
    def test_structure(self):
        for _ in range(30):
            result = _t_frequency_relative_percentage()
            assert "question" in result
            assert "options" in result
            assert "correct_index" in result
            assert "explanation" in result
            assert result["difficulty"] == 2
            assert result["approfondimento"] is False

    def test_question_mentions_relative(self):
        for _ in range(20):
            result = _t_frequency_relative_percentage()
            q = result["question"].lower()
            assert "frequenza relativa" in q

    def test_options_valid(self):
        for _ in range(20):
            result = _t_frequency_relative_percentage()
            assert len(result["options"]) == 5
            assert 0 <= result["correct_index"] < 5
            for opt in result["options"]:
                assert isinstance(opt, str)
                assert len(opt.strip()) > 0


class TestFrequencyCompare:
    def test_structure(self):
        for _ in range(30):
            result = _t_frequency_compare()
            assert "question" in result
            assert "options" in result
            assert "correct_index" in result
            assert "explanation" in result
            assert result["difficulty"] == 2
            assert result["approfondimento"] is False

    def test_options_valid(self):
        for _ in range(20):
            result = _t_frequency_compare()
            assert len(result["options"]) == 5
            assert 0 <= result["correct_index"] < 5


class TestFrequencyReconstructStats:
    def test_structure(self):
        for _ in range(30):
            result = _t_frequency_reconstruct_stats()
            assert "question" in result
            assert "options" in result
            assert "correct_index" in result
            assert "explanation" in result
            assert result["difficulty"] == 3
            assert result["approfondimento"] is True

    def test_options_valid(self):
        for _ in range(20):
            result = _t_frequency_reconstruct_stats()
            assert len(result["options"]) == 5
            assert 0 <= result["correct_index"] < 5
            for opt in result["options"]:
                assert isinstance(opt, str)
                assert len(opt.strip()) > 0


# ---------------------------------------------------------------------------
# Integration via generate()
# ---------------------------------------------------------------------------


class TestFrequencyViaGenerate:
    """Run generate() many times to verify frequency templates integrate properly."""

    def test_l1_generates_frequency_questions(self, ex):
        """Run L1 enough times that frequency templates are hit."""
        found_freq = False
        for _ in range(100):
            result = ex.generate(1)
            assert result is not None
            q = result["question"].lower()
            if "frequenza" in q or "istogramma" in q:
                found_freq = True
        assert found_freq, "Expected at least one frequency question in 100 L1 runs"

    def test_l2_generates_frequency_questions(self, ex):
        """Run L2 enough times that frequency templates are hit."""
        found_freq = False
        for _ in range(100):
            result = ex.generate(2)
            assert result is not None
            q = result["question"].lower()
            if "frequenza relativa" in q:
                found_freq = True
        assert found_freq, "Expected at least one relative frequency question in 100 L2 runs"

    def test_l3_generates_frequency_questions(self, ex):
        """Run L3 enough times that frequency reconstruct templates are hit."""
        found_freq = False
        for _ in range(100):
            result = ex.generate(3)
            assert result is not None
            q = result["question"].lower()
            if "tabella di frequenza" in q:
                found_freq = True
        assert found_freq, "Expected at least one frequency table question in 100 L3 runs"


# ---------------------------------------------------------------------------
# check() method
# ---------------------------------------------------------------------------


class TestFrequencyCheck:
    def test_check_correct(self, ex):
        """Verify check() returns correct=True for all frequency templates."""
        templates = [
            _t_frequency_absolute_from_data,
            _t_frequency_from_histogram,
            _t_frequency_relative_percentage,
            _t_frequency_compare,
            _t_frequency_reconstruct_stats,
        ]
        for template_fn in templates:
            for _ in range(5):
                exercise = template_fn()
                result = ex.check({
                    "answer": exercise["correct_index"],
                    "exercise": exercise,
                })
                assert result["correct"] is True
                assert result["correct_index"] == exercise["correct_index"]
                assert "explanation" in result

    def test_check_wrong(self, ex):
        """Verify check() returns correct=False for wrong answers."""
        templates = [
            _t_frequency_absolute_from_data,
            _t_frequency_from_histogram,
            _t_frequency_relative_percentage,
            _t_frequency_compare,
            _t_frequency_reconstruct_stats,
        ]
        for template_fn in templates:
            exercise = template_fn()
            wrong_idx = (exercise["correct_index"] + 1) % len(exercise["options"])
            result = ex.check({
                "answer": wrong_idx,
                "exercise": exercise,
            })
            assert result["correct"] is False
