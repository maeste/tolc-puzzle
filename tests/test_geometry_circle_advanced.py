"""Tests for advanced circle geometry templates in GeometrySherlock."""

import math

from exercises.geometry_sherlock import (
    GeometrySherlock,
    _t2_inscribed_angle,
    _t2_chord_distance,
    _t3_arc_length,
    _t3_power_of_point,
)


class TestInscribedAngle:
    """Tests for _t2_inscribed_angle template."""

    def test_no_exceptions(self):
        for _ in range(20):
            result = _t2_inscribed_angle()
            assert result is not None

    def test_returns_5_tuple(self):
        result = _t2_inscribed_angle()
        assert isinstance(result, tuple)
        assert len(result) == 5

    def test_tuple_types(self):
        question, correct_value, svg, explanation, tip = _t2_inscribed_angle()
        assert isinstance(question, str)
        assert isinstance(correct_value, (int, float))
        assert isinstance(svg, str)
        assert isinstance(explanation, str)
        assert isinstance(tip, str)

    def test_correct_value_positive_finite(self):
        for _ in range(20):
            _, correct_value, _, _, _ = _t2_inscribed_angle()
            assert correct_value > 0
            assert math.isfinite(correct_value)

    def test_svg_contains_svg_tag(self):
        _, _, svg, _, _ = _t2_inscribed_angle()
        assert "<svg" in svg


class TestChordDistance:
    """Tests for _t2_chord_distance template."""

    def test_no_exceptions(self):
        for _ in range(20):
            result = _t2_chord_distance()
            assert result is not None

    def test_returns_5_tuple(self):
        result = _t2_chord_distance()
        assert isinstance(result, tuple)
        assert len(result) == 5

    def test_tuple_types(self):
        question, correct_value, svg, explanation, tip = _t2_chord_distance()
        assert isinstance(question, str)
        assert isinstance(correct_value, (int, float))
        assert isinstance(svg, str)
        assert isinstance(explanation, str)
        assert isinstance(tip, str)

    def test_correct_value_positive_finite(self):
        for _ in range(20):
            _, correct_value, _, _, _ = _t2_chord_distance()
            assert correct_value > 0
            assert math.isfinite(correct_value)

    def test_svg_contains_svg_tag(self):
        _, _, svg, _, _ = _t2_chord_distance()
        assert "<svg" in svg

    def test_answer_is_integer(self):
        """Chord distance should always be a clean integer due to Pythagorean triples."""
        for _ in range(20):
            _, correct_value, _, _, _ = _t2_chord_distance()
            assert correct_value == int(correct_value)


class TestArcLength:
    """Tests for _t3_arc_length template."""

    def test_no_exceptions(self):
        for _ in range(20):
            result = _t3_arc_length()
            assert result is not None

    def test_returns_5_tuple(self):
        result = _t3_arc_length()
        assert isinstance(result, tuple)
        assert len(result) == 5

    def test_tuple_types(self):
        question, correct_value, svg, explanation, tip = _t3_arc_length()
        assert isinstance(question, str)
        assert isinstance(correct_value, (int, float))
        assert isinstance(svg, str)
        assert isinstance(explanation, str)
        assert isinstance(tip, str)

    def test_correct_value_positive_finite(self):
        for _ in range(20):
            _, correct_value, _, _, _ = _t3_arc_length()
            assert correct_value > 0
            assert math.isfinite(correct_value)

    def test_svg_contains_svg_tag(self):
        _, _, svg, _, _ = _t3_arc_length()
        assert "<svg" in svg


class TestPowerOfPoint:
    """Tests for _t3_power_of_point template."""

    def test_no_exceptions(self):
        for _ in range(20):
            result = _t3_power_of_point()
            assert result is not None

    def test_returns_5_tuple(self):
        result = _t3_power_of_point()
        assert isinstance(result, tuple)
        assert len(result) == 5

    def test_tuple_types(self):
        question, correct_value, svg, explanation, tip = _t3_power_of_point()
        assert isinstance(question, str)
        assert isinstance(correct_value, (int, float))
        assert isinstance(svg, str)
        assert isinstance(explanation, str)
        assert isinstance(tip, str)

    def test_correct_value_positive_finite(self):
        for _ in range(20):
            _, correct_value, _, _, _ = _t3_power_of_point()
            assert correct_value > 0
            assert math.isfinite(correct_value)

    def test_svg_contains_svg_tag(self):
        _, _, svg, _, _ = _t3_power_of_point()
        assert "<svg" in svg

    def test_answer_is_integer(self):
        """Power of point answers should always be clean integers."""
        for _ in range(20):
            _, correct_value, _, _, _ = _t3_power_of_point()
            assert correct_value == int(correct_value)


class TestGeometrySherlockIntegration:
    """Integration tests for GeometrySherlock with new templates."""

    def test_generate_difficulty_2(self):
        sherlock = GeometrySherlock()
        for _ in range(20):
            result = sherlock.generate(difficulty=2)
            assert "question" in result
            assert "options" in result
            assert "correct_index" in result
            assert "graph_data" in result
            assert "explanation" in result

    def test_generate_difficulty_3(self):
        sherlock = GeometrySherlock()
        for _ in range(20):
            result = sherlock.generate(difficulty=3)
            assert "question" in result
            assert "options" in result
            assert "correct_index" in result
            assert "graph_data" in result
            assert "explanation" in result

    def test_new_templates_in_l2(self):
        assert _t2_inscribed_angle in GeometrySherlock.TEMPLATES_L2
        assert _t2_chord_distance in GeometrySherlock.TEMPLATES_L2

    def test_new_templates_in_l3(self):
        assert _t3_arc_length in GeometrySherlock.TEMPLATES_L3
        assert _t3_power_of_point in GeometrySherlock.TEMPLATES_L3
