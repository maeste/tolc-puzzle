import collections

import pytest

flask = pytest.importorskip("flask", reason="Flask required for app tests")

from app import (
    EXERCISE_TYPES,
    REALISTIC_EXAM_WEIGHTS,
    app,
    exercise_registry,
)


class TestRealisticExamWeightsConfig:
    """Validate the REALISTIC_EXAM_WEIGHTS configuration dictionary."""

    def test_total_questions_is_20(self):
        total = sum(REALISTIC_EXAM_WEIGHTS.values())
        assert total == 20, f"Expected 20 total questions, got {total}"

    def test_all_types_exist_in_exercise_types(self):
        for ex_type in REALISTIC_EXAM_WEIGHTS:
            assert ex_type in EXERCISE_TYPES, (
                f"Type '{ex_type}' in REALISTIC_EXAM_WEIGHTS "
                f"but not in EXERCISE_TYPES"
            )

    def test_all_types_have_registered_exercise_class(self):
        for ex_type in REALISTIC_EXAM_WEIGHTS:
            assert ex_type in exercise_registry, (
                f"Type '{ex_type}' in REALISTIC_EXAM_WEIGHTS "
                f"but no exercise class registered"
            )

    def test_all_counts_are_positive_integers(self):
        for ex_type, count in REALISTIC_EXAM_WEIGHTS.items():
            assert isinstance(count, int), (
                f"Count for '{ex_type}' should be int, got {type(count)}"
            )
            assert count > 0, (
                f"Count for '{ex_type}' should be positive, got {count}"
            )

    def test_estimation_included(self):
        assert "estimation" in REALISTIC_EXAM_WEIGHTS, (
            "estimation type should be included (Aritmetica/Numeri category)"
        )

    def test_graph_included(self):
        assert "graph" in REALISTIC_EXAM_WEIGHTS, (
            "graph type should be included for TOLC-B Funzioni/Grafici category"
        )

    def test_learning_mode_types_excluded_from_exam(self):
        """Types kept for learning mode only should not appear in exam weights."""
        learning_only = ["trap", "always_true", "proportional", "cross_topic"]
        for ex_type in learning_only:
            assert ex_type not in REALISTIC_EXAM_WEIGHTS, (
                f"'{ex_type}' should be excluded from realistic exam weights "
                f"(learning mode only)"
            )

    def test_learning_mode_types_still_in_exercise_types(self):
        """Learning-only types must remain in EXERCISE_TYPES for practice mode."""
        learning_only = ["trap", "always_true", "proportional", "cross_topic"]
        for ex_type in learning_only:
            assert ex_type in EXERCISE_TYPES, (
                f"'{ex_type}' must stay in EXERCISE_TYPES for learning mode"
            )

    def test_learning_mode_types_still_registered(self):
        """Learning-only types must still have registered exercise classes."""
        learning_only = ["trap", "always_true", "proportional", "cross_topic"]
        for ex_type in learning_only:
            assert ex_type in exercise_registry, (
                f"'{ex_type}' must stay registered for learning mode"
            )

    def test_new_types_included(self):
        """number_sense and which_satisfies must be in exam weights."""
        assert "number_sense" in REALISTIC_EXAM_WEIGHTS
        assert "which_satisfies" in REALISTIC_EXAM_WEIGHTS

    def test_learning_only_types_excluded(self):
        """Learning-only types must not appear in exam weights."""
        excluded = ["trap", "always_true", "proportional", "cross_topic"]
        for ex_type in excluded:
            assert ex_type not in REALISTIC_EXAM_WEIGHTS, (
                f"'{ex_type}' should not be in REALISTIC_EXAM_WEIGHTS"
            )

    def test_category_distribution_matches_tolc(self):
        """Validate category percentages within +-5% of target distribution."""
        total = sum(REALISTIC_EXAM_WEIGHTS.values())
        categories = {
            "Aritmetica/Numeri": ["number_sense"],
            "Algebra": ["solve", "inequalities", "simplification"],
            "Geometria": ["geometry", "analytic_geo"],
            "Funzioni/Grafici": ["word", "graph"],
            "Meta-ragionamento": ["which_satisfies"],
            "Prob+Stat+Logica": ["probability", "statistics", "logic"],
        }
        expected_pct = {
            "Aritmetica/Numeri": 15,
            "Algebra": 20,
            "Geometria": 20,
            "Funzioni/Grafici": 20,
            "Meta-ragionamento": 10,
            "Prob+Stat+Logica": 15,
        }
        for cat_name, types in categories.items():
            cat_count = sum(REALISTIC_EXAM_WEIGHTS.get(t, 0) for t in types)
            actual_pct = (cat_count / total) * 100
            target_pct = expected_pct[cat_name]
            assert abs(actual_pct - target_pct) <= 5, (
                f"Category '{cat_name}': {actual_pct:.1f}% vs target {target_pct}% "
                f"(exceeds +-5% tolerance)"
            )


class TestRealisticExamEndpoint:
    """Test the /api/realistic-exam/exercises endpoint."""

    @pytest.fixture()
    def client(self):
        app.config["TESTING"] = True
        with app.test_client() as client:
            yield client

    def test_returns_20_exercises(self, client):
        response = client.get("/api/realistic-exam/exercises")
        assert response.status_code == 200
        exercises = response.get_json()
        assert len(exercises) == 20

    def test_exercise_structure(self, client):
        response = client.get("/api/realistic-exam/exercises")
        exercises = response.get_json()
        for ex in exercises:
            assert "question" in ex, "Exercise missing 'question' field"
            assert "options" in ex, "Exercise missing 'options' field"
            assert "correct_index" in ex, "Exercise missing 'correct_index' field"
            assert "explanation" in ex, "Exercise missing 'explanation' field"
            assert "type" in ex, "Exercise missing 'type' field"
            assert "difficulty" in ex, "Exercise missing 'difficulty' field"

    def test_exercises_have_exactly_5_options(self, client):
        response = client.get("/api/realistic-exam/exercises")
        exercises = response.get_json()
        for i, ex in enumerate(exercises):
            assert len(ex["options"]) == 5, (
                f"Exercise {i} ({ex['type']}) has {len(ex['options'])} options, expected 5"
            )

    def test_correct_index_within_bounds(self, client):
        response = client.get("/api/realistic-exam/exercises")
        exercises = response.get_json()
        for i, ex in enumerate(exercises):
            assert 0 <= ex["correct_index"] < len(ex["options"]), (
                f"Exercise {i} correct_index {ex['correct_index']} "
                f"out of bounds for {len(ex['options'])} options"
            )

    def test_graph_exercises_have_graph_data(self, client):
        """Graph-type exercises should retain graph_data for SVG rendering."""
        response = client.get("/api/realistic-exam/exercises")
        exercises = response.get_json()
        graph_exercises = [ex for ex in exercises if ex["type"] == "graph"]
        for ex in graph_exercises:
            assert "graph_data" in ex, (
                "Graph exercise should have graph_data for client-side SVG rendering"
            )

    def test_distribution_matches_weights(self, client):
        """Run multiple simulations and verify type proportions are correct.

        Each simulation produces exactly the counts from REALISTIC_EXAM_WEIGHTS,
        so we verify every single run has the exact expected distribution.
        """
        for _ in range(50):
            response = client.get("/api/realistic-exam/exercises")
            exercises = response.get_json()
            type_counts = collections.Counter(ex["type"] for ex in exercises)
            for ex_type, expected_count in REALISTIC_EXAM_WEIGHTS.items():
                actual_count = type_counts.get(ex_type, 0)
                assert actual_count == expected_count, (
                    f"Expected {expected_count} '{ex_type}' exercises, "
                    f"got {actual_count}"
                )

    def test_only_weighted_types_appear(self, client):
        """No exercise types outside REALISTIC_EXAM_WEIGHTS should appear."""
        for _ in range(20):
            response = client.get("/api/realistic-exam/exercises")
            exercises = response.get_json()
            for ex in exercises:
                assert ex["type"] in REALISTIC_EXAM_WEIGHTS, (
                    f"Unexpected exercise type '{ex['type']}' not in weights config"
                )

    def test_difficulty_values_valid(self, client):
        response = client.get("/api/realistic-exam/exercises")
        exercises = response.get_json()
        for ex in exercises:
            assert ex["difficulty"] in (1, 2, 3), (
                f"Invalid difficulty {ex['difficulty']} for type '{ex['type']}'"
            )
