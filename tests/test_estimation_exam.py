import pytest

from exercises.estimation_blitz import EstimationBlitz


@pytest.fixture
def exercise():
    return EstimationBlitz()


class TestExamMode:
    @pytest.mark.parametrize("difficulty", [1, 2, 3])
    @pytest.mark.parametrize("run", range(10))
    def test_exam_mode_no_time_limit(self, exercise, difficulty, run):
        result = exercise.generate(difficulty=difficulty, exam_mode=True)
        assert "time_limit" not in result
        assert "question" in result
        assert "options" in result
        assert len(result["options"]) == 5
        assert len(set(result["options"])) == 5
        assert 0 <= result["correct_index"] < 5

    @pytest.mark.parametrize("difficulty", [1, 2, 3])
    @pytest.mark.parametrize("run", range(10))
    def test_learning_mode_has_time_limit(self, exercise, difficulty, run):
        result = exercise.generate(difficulty=difficulty, exam_mode=False)
        assert "time_limit" in result

    @pytest.mark.parametrize("difficulty", [1, 2, 3])
    def test_exam_mode_question_is_italian(self, exercise, difficulty):
        result = exercise.generate(difficulty=difficulty, exam_mode=True)
        assert isinstance(result["question"], str)
        assert len(result["question"]) > 10

    @pytest.mark.parametrize("difficulty", [1, 2, 3])
    @pytest.mark.parametrize("run", range(5))
    def test_exam_mode_no_speed_reference(self, exercise, difficulty, run):
        """Exam mode questions should not reference speed or timer."""
        result = exercise.generate(difficulty=difficulty, exam_mode=True)
        question = result["question"].lower()
        assert "velocemente" not in question

    @pytest.mark.parametrize("difficulty", [1, 2, 3])
    @pytest.mark.parametrize("run", range(5))
    def test_exam_mode_has_senza_calcolatrice(self, exercise, difficulty, run):
        """Exam mode questions should include 'Senza calcolatrice' prefix."""
        result = exercise.generate(difficulty=difficulty, exam_mode=True)
        assert "Senza calcolatrice" in result["question"]


class TestExamWeights:
    @staticmethod
    def _parse_weights_from_source():
        """Parse REALISTIC_EXAM_WEIGHTS from app.py source without importing Flask."""
        import ast
        import pathlib
        app_path = pathlib.Path(__file__).resolve().parent.parent / "app.py"
        source = app_path.read_text()
        tree = ast.parse(source)
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == "REALISTIC_EXAM_WEIGHTS":
                        return ast.literal_eval(node.value)
        raise RuntimeError("REALISTIC_EXAM_WEIGHTS not found in app.py")

    def test_total_exam_questions_is_20(self):
        """REALISTIC_EXAM_WEIGHTS must sum to exactly 20."""
        weights = self._parse_weights_from_source()
        total = sum(weights.values())
        assert total == 20, f"Expected 20 total questions, got {total}"

    def test_estimation_included_in_weights(self):
        """Estimation must be included in realistic exam weights."""
        weights = self._parse_weights_from_source()
        assert "estimation" in weights
        assert weights["estimation"] >= 1


class TestBackwardCompatibility:
    @pytest.mark.parametrize("difficulty", [1, 2, 3])
    @pytest.mark.parametrize("run", range(5))
    def test_default_mode_unchanged(self, exercise, difficulty, run):
        """Default generate() should still work as before (with time_limit)."""
        result = exercise.generate(difficulty=difficulty)
        assert "time_limit" in result
        assert "question" in result
        assert len(result["options"]) == 5

    @pytest.mark.parametrize("difficulty", [1, 2, 3])
    def test_default_mode_has_stima_velocemente(self, exercise, difficulty):
        """Default mode should keep the original speed-oriented prompt."""
        result = exercise.generate(difficulty=difficulty)
        assert "Stima velocemente" in result["question"]
