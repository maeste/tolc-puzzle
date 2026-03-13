"""Integration test: generate a full 20-question realistic exam and validate all exercises."""
import pytest
import random

from exercises.base import Exercise
from exercises.geometry_sherlock import GeometrySherlock
from exercises.analytic_geometry import AnalyticGeometry
from exercises.statistics_exercise import StatisticsExercise
from exercises.inequalities import InequalitiesExercise
from exercises.simplification import SimplificationExercise
from exercises.solve_exercise import SolveExercise
from exercises.number_sense import NumberSense
from exercises.which_satisfies import WhichSatisfies
from exercises.probability_game import ProbabilityGame
from exercises.logic_puzzle import LogicPuzzle
from exercises.word_modeler import WordModeler
from exercises.graph_reader import GraphReader
from exercises.estimation_blitz import EstimationBlitz
from exercises.function_composition import FunctionComposition

# Mirror REALISTIC_EXAM_WEIGHTS from app.py
REALISTIC_EXAM_WEIGHTS = {
    "number_sense": 2,
    "solve": 2,
    "inequalities": 1,
    "simplification": 1,
    "which_satisfies": 2,
    "geometry": 2,
    "analytic_geo": 2,
    "word": 1,
    "composition": 1,
    "probability": 1,
    "statistics": 1,
    "logic": 1,
    "graph": 2,
    "estimation": 1,
}

REGISTRY = {
    "number_sense": NumberSense,
    "solve": SolveExercise,
    "inequalities": InequalitiesExercise,
    "simplification": SimplificationExercise,
    "which_satisfies": WhichSatisfies,
    "geometry": GeometrySherlock,
    "analytic_geo": AnalyticGeometry,
    "word": WordModeler,
    "composition": FunctionComposition,
    "probability": ProbabilityGame,
    "statistics": StatisticsExercise,
    "logic": LogicPuzzle,
    "graph": GraphReader,
    "estimation": EstimationBlitz,
}


class TestFullExam:
    def test_generate_full_20_question_exam(self):
        """Generate a realistic 20-question exam and validate all exercises."""
        exam_types = []
        for ex_type, count in REALISTIC_EXAM_WEIGHTS.items():
            exam_types.extend([ex_type] * count)
        random.shuffle(exam_types)

        assert len(exam_types) == 20, "Exam should have exactly 20 questions"

        exercises = []
        for ex_type in exam_types:
            difficulty = random.choice([1, 2, 2, 2, 3])
            ex = REGISTRY[ex_type]()
            if ex_type in ("word", "estimation"):
                data = ex.generate(difficulty, exam_mode=True)
            elif ex_type == "geometry":
                data = ex.generate(difficulty, text_only=True)
            else:
                data = ex.generate(difficulty)

            data["type"] = ex_type
            data["difficulty"] = difficulty

            # Normalize to options
            if "options" not in data and "steps" in data:
                data["options"] = data.pop("steps")

            exercises.append(data)

        # Validate all exercises
        for i, data in enumerate(exercises):
            assert "question" in data, f"Exercise {i} ({data['type']}) missing 'question'"
            assert isinstance(data["question"], str), f"Exercise {i} question not a string"
            assert len(data["question"]) > 10, f"Exercise {i} question too short"

            assert "options" in data, f"Exercise {i} ({data['type']}) missing 'options'"
            assert len(data["options"]) >= 4, f"Exercise {i} has fewer than 4 options"

            assert "correct_index" in data, f"Exercise {i} ({data['type']}) missing 'correct_index'"
            assert 0 <= data["correct_index"] < len(data["options"]), (
                f"Exercise {i} correct_index {data['correct_index']} out of range"
            )

            assert "explanation" in data, f"Exercise {i} ({data['type']}) missing 'explanation'"

    def test_geometry_text_only_in_exam(self):
        """Geometry exercises should have no graph_data in exam mode."""
        ex = GeometrySherlock()
        for _ in range(10):
            difficulty = random.choice([1, 2, 3])
            data = ex.generate(difficulty, text_only=True)
            assert data.get("graph_data") is None, (
                "Geometry in text_only mode should have no graph_data"
            )

    def test_geometry_has_svg_in_learning_mode(self):
        """Geometry exercises should have graph_data in normal (learning) mode."""
        ex = GeometrySherlock()
        for _ in range(10):
            difficulty = random.choice([1, 2, 3])
            data = ex.generate(difficulty, text_only=False)
            assert data.get("graph_data") is not None, (
                "Geometry in normal mode should have graph_data (SVG)"
            )
            assert "<svg" in data["graph_data"], "graph_data should contain SVG markup"

    def test_geometry_default_has_svg(self):
        """Default generate() should include SVG (text_only defaults to False)."""
        ex = GeometrySherlock()
        data = ex.generate(1)
        assert data.get("graph_data") is not None

    def test_exam_type_distribution(self):
        """Verify the exam has the correct distribution of question types."""
        exam_types = []
        for ex_type, count in REALISTIC_EXAM_WEIGHTS.items():
            exam_types.extend([ex_type] * count)

        from collections import Counter
        dist = Counter(exam_types)

        assert dist["geometry"] == 2
        assert dist["analytic_geo"] == 2
        assert dist["number_sense"] == 2
        assert dist["solve"] == 2
        assert dist["graph"] == 2
        assert dist["which_satisfies"] == 2
        assert dist["probability"] == 1
        assert dist["statistics"] == 1
        assert dist["logic"] == 1
        assert sum(dist.values()) == 20
