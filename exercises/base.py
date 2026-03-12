import abc
import random


class Exercise(abc.ABC):
    """Base class for all exercise types."""

    DIFFICULTY_LABELS = {1: "⭐", 2: "⭐⭐", 3: "⭐⭐⭐"}

    @abc.abstractmethod
    def generate(self, difficulty: int) -> dict:
        """Generate an exercise at the given difficulty (1-3).

        Must return a dict with at least:
            - question: str
            - options: list[str]  (or steps: list[str] for trap-type)
            - correct_index: int
            - explanation: str
            - did_you_know: str (optional)
        """

    def check(self, data: dict) -> dict:
        """Check the user's answer against the exercise data.

        Args:
            data: dict with 'answer' (int index), 'exercise' (the original exercise dict)

        Returns:
            dict with 'correct', 'correct_index', 'explanation', 'did_you_know'
        """
        answer = data.get("answer")
        exercise = data.get("exercise", {})
        correct_index = exercise.get("correct_index")
        is_correct = answer == correct_index

        return {
            "correct": is_correct,
            "correct_index": correct_index,
            "explanation": exercise.get("explanation", ""),
            "did_you_know": exercise.get("did_you_know", ""),
        }

    @staticmethod
    def shuffle_options(options: list[str], correct_index: int) -> tuple[list[str], int]:
        """Shuffle options while tracking the correct answer index."""
        indexed = list(enumerate(options))
        random.shuffle(indexed)
        new_correct = next(i for i, (orig, _) in enumerate(indexed) if orig == correct_index)
        shuffled = [opt for _, opt in indexed]
        return shuffled, new_correct
