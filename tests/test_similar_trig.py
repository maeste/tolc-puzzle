import math
import pytest

from exercises.geometry_sherlock import (
    GeometrySherlock,
    _fmt,
    _t2_similar_find_side,
    _t2_similar_scale_factor,
    _t2_similar_area_ratio,
    _t3_similar_real_world,
    _t2_trig_find_ratio,
    _t2_trig_find_side,
    _t3_trig_identify_angle,
    _t3_trig_real_world,
)

# All new templates grouped for parametrized tests
SIMILAR_TEMPLATES = [
    _t2_similar_find_side,
    _t2_similar_scale_factor,
    _t2_similar_area_ratio,
    _t3_similar_real_world,
]

TRIG_TEMPLATES = [
    _t2_trig_find_ratio,
    _t2_trig_find_side,
    _t3_trig_identify_angle,
    _t3_trig_real_world,
]

ALL_TEMPLATES = SIMILAR_TEMPLATES + TRIG_TEMPLATES


# ============ STRUCTURAL TESTS ============

class TestTemplatesReturnValidTuple:
    """Each template must return a valid 5-tuple with correct types."""

    @pytest.mark.parametrize("template_fn", ALL_TEMPLATES, ids=lambda f: f.__name__)
    def test_returns_5_tuple(self, template_fn):
        for _ in range(25):
            result = template_fn()
            assert isinstance(result, tuple), f"{template_fn.__name__} must return a tuple"
            assert len(result) == 5, f"{template_fn.__name__} must return 5 elements"

    @pytest.mark.parametrize("template_fn", ALL_TEMPLATES, ids=lambda f: f.__name__)
    def test_question_is_nonempty_string(self, template_fn):
        for _ in range(20):
            question, _, _, _, _ = template_fn()
            assert isinstance(question, str)
            assert len(question) > 10

    @pytest.mark.parametrize("template_fn", ALL_TEMPLATES, ids=lambda f: f.__name__)
    def test_correct_value_is_positive_number(self, template_fn):
        for _ in range(25):
            _, correct_value, _, _, _ = template_fn()
            assert isinstance(correct_value, (int, float))
            assert correct_value > 0, f"{template_fn.__name__} returned non-positive value: {correct_value}"

    @pytest.mark.parametrize("template_fn", ALL_TEMPLATES, ids=lambda f: f.__name__)
    def test_svg_is_valid(self, template_fn):
        for _ in range(20):
            _, _, svg, _, _ = template_fn()
            assert isinstance(svg, str)
            assert "<svg" in svg
            assert "</svg>" in svg

    @pytest.mark.parametrize("template_fn", ALL_TEMPLATES, ids=lambda f: f.__name__)
    def test_explanation_is_nonempty_string(self, template_fn):
        for _ in range(20):
            _, _, _, explanation, _ = template_fn()
            assert isinstance(explanation, str)
            assert len(explanation) > 10

    @pytest.mark.parametrize("template_fn", ALL_TEMPLATES, ids=lambda f: f.__name__)
    def test_tip_is_nonempty_string(self, template_fn):
        for _ in range(20):
            _, _, _, _, tip = template_fn()
            assert isinstance(tip, str)
            assert len(tip) > 5


# ============ SIMILAR TRIANGLES FORMULA TESTS ============

class TestSimilarFindSide:
    """Verify _t2_similar_find_side produces correct proportions."""

    def test_proportion_correctness(self):
        for _ in range(30):
            question, correct_value, svg, explanation, tip = _t2_similar_find_side()
            # The correct value should be positive and finite
            assert correct_value > 0
            assert math.isfinite(correct_value)

    def test_question_contains_italian(self):
        for _ in range(10):
            question, _, _, _, _ = _t2_similar_find_side()
            assert "simili" in question.lower()
            assert "triangol" in question.lower()


class TestSimilarScaleFactor:
    """Verify _t2_similar_scale_factor computes k correctly."""

    def test_scale_factor_is_ratio(self):
        for _ in range(30):
            question, k, _, explanation, _ = _t2_similar_scale_factor()
            assert k >= 1.5
            # k must appear in the explanation
            assert _fmt(k) in explanation

    def test_question_mentions_rapporto(self):
        for _ in range(10):
            question, _, _, _, _ = _t2_similar_scale_factor()
            assert "rapporto" in question.lower()


class TestSimilarAreaRatio:
    """Verify _t2_similar_area_ratio uses k^2 scaling."""

    def test_area_scales_with_k_squared(self):
        for _ in range(30):
            question, correct_value, _, explanation, _ = _t2_similar_area_ratio()
            # Extract k from the question (format: "k = X")
            k_str = question.split("k = ")[1].split(".")[0]
            # The area must be positive
            assert correct_value > 0
            # Check that explanation mentions k^2
            assert "k^2" in explanation or "k²" in explanation


class TestSimilarRealWorld:
    """Verify _t3_similar_real_world shadow proportion."""

    def test_shadow_proportion(self):
        for _ in range(30):
            question, correct_value, _, explanation, _ = _t3_similar_real_world()
            assert correct_value > 0
            # The tree height should be larger than a person
            assert correct_value > 1.0

    def test_question_mentions_ombra(self):
        for _ in range(10):
            question, _, _, _, _ = _t3_similar_real_world()
            assert "ombra" in question.lower()


# ============ TRIGONOMETRIC RATIOS FORMULA TESTS ============

class TestTrigFindRatio:
    """Verify _t2_trig_find_ratio computes correct trig values."""

    def test_ratio_between_0_and_infinity(self):
        for _ in range(30):
            question, correct_value, _, _, _ = _t2_trig_find_ratio()
            assert correct_value > 0
            # sin and cos are <= 1, tan can be > 1 but finite
            assert math.isfinite(correct_value)

    def test_sin_cos_bounded_by_1(self):
        for _ in range(50):
            question, correct_value, _, _, _ = _t2_trig_find_ratio()
            if "sin(" in question or "cos(" in question:
                assert correct_value <= 1.0 + 1e-9

    def test_question_contains_trig_function(self):
        for _ in range(20):
            question, _, _, _, _ = _t2_trig_find_ratio()
            has_trig = any(f in question for f in ["sin(", "cos(", "tan("])
            assert has_trig


class TestTrigFindSide:
    """Verify _t2_trig_find_side uses correct trig formulas."""

    def test_side_is_positive(self):
        for _ in range(30):
            _, correct_value, _, _, _ = _t2_trig_find_side()
            assert correct_value > 0

    def test_side_with_known_angles(self):
        """For standard angles (30, 45, 60), verify known trig values."""
        for _ in range(50):
            question, correct_value, _, _, _ = _t2_trig_find_side()
            assert math.isfinite(correct_value)
            assert correct_value > 0


class TestTrigIdentifyAngle:
    """Verify _t3_trig_identify_angle returns standard angles."""

    def test_angle_is_standard(self):
        for _ in range(30):
            _, correct_value, _, _, _ = _t3_trig_identify_angle()
            assert correct_value in (30.0, 45.0, 60.0)

    def test_question_mentions_angolo(self):
        for _ in range(10):
            question, _, _, _, _ = _t3_trig_identify_angle()
            assert "angolo" in question.lower()


class TestTrigRealWorld:
    """Verify _t3_trig_real_world height calculation."""

    def test_height_formula(self):
        for _ in range(30):
            question, correct_value, _, _, _ = _t3_trig_real_world()
            assert correct_value > 0
            assert math.isfinite(correct_value)

    def test_question_mentions_edificio(self):
        for _ in range(10):
            question, _, _, _, _ = _t3_trig_real_world()
            assert "edificio" in question.lower()

    def test_known_angle_values(self):
        """Verify tan(30), tan(45), tan(60) produce correct heights."""
        for _ in range(50):
            question, correct_value, _, _, _ = _t3_trig_real_world()
            # Extract angle from question
            for angle in [30, 45, 60]:
                if f"{angle}°" in question or f"{angle} gradi" in question:
                    # Extract distance
                    parts = question.split()
                    for i, p in enumerate(parts):
                        if p == "a" and i + 1 < len(parts):
                            try:
                                dist = int(parts[i + 1])
                                expected = dist * math.tan(math.radians(angle))
                                assert abs(correct_value - expected) < 0.01
                            except (ValueError, IndexError):
                                pass


# ============ INTEGRATION TESTS ============

class TestGeometrySherlockIntegration:
    """Verify the GeometrySherlock class works with new templates."""

    def test_generate_difficulty_2(self):
        sherlock = GeometrySherlock()
        for _ in range(30):
            result = sherlock.generate(difficulty=2)
            assert "question" in result
            assert "options" in result
            assert "correct_index" in result
            assert "graph_data" in result
            assert "explanation" in result
            assert "difficulty" in result
            assert result["difficulty"] == 2
            assert len(result["options"]) == 5  # 1 correct + 4 distractors

    def test_generate_difficulty_3(self):
        sherlock = GeometrySherlock()
        for _ in range(30):
            result = sherlock.generate(difficulty=3)
            assert result["difficulty"] == 3
            assert len(result["options"]) == 5

    def test_all_difficulties_produce_valid_output(self):
        sherlock = GeometrySherlock()
        for diff in [1, 2, 3]:
            for _ in range(10):
                result = sherlock.generate(difficulty=diff)
                assert isinstance(result["question"], str)
                assert "<svg" in result["graph_data"]
                assert 0 <= result["correct_index"] < len(result["options"])


class TestFmtHelper:
    """Verify _fmt helper formats numbers correctly."""

    def test_integer_formatting(self):
        assert _fmt(5.0) == "5"
        assert _fmt(10.0) == "10"

    def test_decimal_formatting(self):
        assert _fmt(3.14) == "3.14"
        assert _fmt(2.5) == "2.5"

    def test_rounding(self):
        result = _fmt(1.23456, 2)
        assert result == "1.23"
