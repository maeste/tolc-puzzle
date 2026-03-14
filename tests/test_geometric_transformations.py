import math
import random

import pytest

from exercises.geometry_sherlock import (
    GeometrySherlock,
    _fmt,
    _t1_axial_symmetry,
    _t1_translation,
    _t1_point_symmetry,
    _t2_rotation_90,
    _t2_similarity_lengths,
    _t2_rotation_180_sum,
    _t3_similarity_area,
    _t3_compose_transformations,
    _t3_transformation_vertices,
)

TRANSFORMATION_TEMPLATES = [
    _t1_axial_symmetry,
    _t1_translation,
    _t1_point_symmetry,
    _t2_rotation_90,
    _t2_similarity_lengths,
    _t2_rotation_180_sum,
    _t3_similarity_area,
    _t3_compose_transformations,
    _t3_transformation_vertices,
]


@pytest.fixture
def geo():
    return GeometrySherlock()


def _validate(result):
    """Common validation for a generated exercise dict."""
    assert "question" in result
    assert "options" in result
    assert len(result["options"]) == 5
    assert "correct_index" in result
    assert 0 <= result["correct_index"] < 5
    assert "explanation" in result
    assert "graph_data" in result
    assert result["graph_data"]  # non-empty SVG


class TestTemplateOutputStructure:
    """Each transformation template must return a valid 5-tuple."""

    @pytest.mark.parametrize("template_fn", TRANSFORMATION_TEMPLATES, ids=lambda f: f.__name__)
    def test_returns_valid_tuple(self, template_fn):
        for _ in range(20):
            question, correct_value, svg, explanation, tip = template_fn()
            assert isinstance(question, str) and len(question) > 10
            assert isinstance(correct_value, (int, float))
            assert isinstance(svg, str) and "<svg" in svg and "</svg>" in svg
            assert isinstance(explanation, str) and len(explanation) > 10
            assert isinstance(tip, str) and len(tip) > 5

    @pytest.mark.parametrize("template_fn", TRANSFORMATION_TEMPLATES, ids=lambda f: f.__name__)
    def test_svg_is_well_formed(self, template_fn):
        for _ in range(5):
            _, _, svg, _, _ = template_fn()
            assert svg.count("<svg") == 1
            assert svg.count("</svg>") == 1
            assert svg.index("<svg") < svg.index("</svg>")


class TestAxialSymmetry:
    """Tests for _t1_axial_symmetry template."""

    def test_x_axis_reflection_formula(self):
        random.seed(42)
        for _ in range(30):
            question, correct_value, svg, explanation, tip = _t1_axial_symmetry()
            # Extract P coords from question: "P(a, b)"
            import re
            m = re.search(r"P\((-?\d+),\s*(-?\d+)\)", question)
            assert m is not None, f"Could not parse point from: {question}"
            a, b = int(m.group(1)), int(m.group(2))
            if "asse x" in question:
                # Reflection across x-axis, asking for y coordinate
                assert correct_value == float(-b), f"Expected {-b}, got {correct_value}"
            else:
                # Reflection across y-axis, asking for x coordinate
                assert correct_value == float(-a), f"Expected {-a}, got {correct_value}"

    def test_question_in_italian(self):
        for _ in range(10):
            question, _, _, _, _ = _t1_axial_symmetry()
            assert "riflesso" in question or "coordinata" in question


class TestTranslation:
    """Tests for _t1_translation template."""

    def test_translation_formula(self):
        random.seed(123)
        for _ in range(30):
            question, correct_value, svg, explanation, tip = _t1_translation()
            import re
            point_m = re.search(r"P\((-?\d+),\s*(-?\d+)\)", question)
            vec_m = re.search(r"vettore\s*\((-?\d+),\s*(-?\d+)\)", question)
            assert point_m and vec_m
            a, b = int(point_m.group(1)), int(point_m.group(2))
            h, k = int(vec_m.group(1)), int(vec_m.group(2))
            if "coordinata x" in question:
                assert correct_value == float(a + h)
            else:
                assert correct_value == float(b + k)


class TestPointSymmetry:
    """Tests for _t1_point_symmetry template."""

    def test_origin_reflection_formula(self):
        random.seed(77)
        for _ in range(30):
            question, correct_value, svg, explanation, tip = _t1_point_symmetry()
            import re
            m = re.search(r"P\((-?\d+),\s*(-?\d+)\)", question)
            assert m is not None
            a, b = int(m.group(1)), int(m.group(2))
            if "coordinata x" in question:
                assert correct_value == float(-a)
            else:
                assert correct_value == float(-b)


class TestRotation90:
    """Tests for _t2_rotation_90 template."""

    def test_rotation_formula(self):
        random.seed(99)
        for _ in range(30):
            question, correct_value, svg, explanation, tip = _t2_rotation_90()
            import re
            m = re.search(r"P\((-?\d+),\s*(-?\d+)\)", question)
            assert m is not None
            a, b = int(m.group(1)), int(m.group(2))
            if "90°" in question and "270°" not in question:
                # 90 CCW: (a,b) -> (-b, a)
                img_x, img_y = -b, a
            else:
                # 270 CCW: (a,b) -> (b, -a)
                img_x, img_y = b, -a
            if "coordinata x" in question:
                assert correct_value == float(img_x)
            else:
                assert correct_value == float(img_y)


class TestSimilarityLengths:
    """Tests for _t2_similarity_lengths template."""

    def test_ratio_calculation(self):
        for _ in range(30):
            question, correct_value, svg, explanation, tip = _t2_similarity_lengths()
            assert correct_value > 0
            # The answer should be a clean number
            assert abs(correct_value - round(correct_value, 2)) < 0.001


class TestRotation180Sum:
    """Tests for _t2_rotation_180_sum template."""

    def test_sum_formula(self):
        random.seed(55)
        for _ in range(30):
            question, correct_value, svg, explanation, tip = _t2_rotation_180_sum()
            import re
            m = re.search(r"P\((-?\d+),\s*(-?\d+)\)", question)
            assert m is not None
            a, b = int(m.group(1)), int(m.group(2))
            expected = float(-a + (-b))
            assert correct_value == expected, f"Expected {expected}, got {correct_value}"


class TestSimilarityArea:
    """Tests for _t3_similarity_area template."""

    def test_area_or_volume_scaling(self):
        for _ in range(30):
            question, correct_value, svg, explanation, tip = _t3_similarity_area()
            assert correct_value > 0
            # The answer should involve k^2 or k^3 scaling
            assert "k" in tip or "simili" in tip


class TestComposeTransformations:
    """Tests for _t3_compose_transformations template."""

    def test_compose_formula(self):
        random.seed(11)
        for _ in range(30):
            question, correct_value, svg, explanation, tip = _t3_compose_transformations()
            import re
            point_m = re.search(r"P\((-?\d+),\s*(-?\d+)\)", question)
            vec_m = re.search(r"vettore\s*\((-?\d+),\s*(-?\d+)\)", question)
            assert point_m and vec_m
            a, b = int(point_m.group(1)), int(point_m.group(2))
            h, k = int(vec_m.group(1)), int(vec_m.group(2))
            # translate then reflect across x-axis
            mid_y = b + k
            final_y = -mid_y
            assert correct_value == float(final_y)


class TestTransformationVertices:
    """Tests for _t3_transformation_vertices template."""

    def test_sum_of_x_coordinates(self):
        random.seed(33)
        for _ in range(30):
            question, correct_value, svg, explanation, tip = _t3_transformation_vertices()
            import re
            points = re.findall(r"[ABC]\((-?\d+),(-?\d+)\)", question)
            vec_m = re.search(r"vettore\s*\((-?\d+),\s*(-?\d+)\)", question)
            assert len(points) == 3
            assert vec_m is not None
            x_sum = sum(int(p[0]) for p in points)
            h = int(vec_m.group(1))
            expected = float(x_sum + 3 * h)
            assert correct_value == expected


class TestGenerateIntegration:
    """Integration tests via GeometrySherlock.generate()."""

    def test_generate_difficulty_1_produces_transformations(self, geo):
        """Over 100 runs, at least one transformation template should appear."""
        random.seed(0)
        found_transformation = False
        for _ in range(100):
            result = geo.generate(difficulty=1)
            _validate(result)
            q = result["question"]
            if any(kw in q for kw in ["riflesso", "traslato", "simmetria"]):
                found_transformation = True
                break
        assert found_transformation, "No transformation template appeared in 100 L1 runs"

    def test_generate_difficulty_2_produces_transformations(self, geo):
        random.seed(0)
        found = False
        for _ in range(100):
            result = geo.generate(difficulty=2)
            _validate(result)
            q = result["question"]
            if any(kw in q for kw in ["ruotato", "similitudine", "rotazione"]):
                found = True
                break
        assert found, "No transformation template appeared in 100 L2 runs"

    def test_generate_difficulty_3_produces_transformations(self, geo):
        random.seed(0)
        found = False
        for _ in range(100):
            result = geo.generate(difficulty=3)
            _validate(result)
            q = result["question"]
            if any(kw in q for kw in ["simili", "traslato", "prima traslato", "somma delle coordinate"]):
                found = True
                break
        assert found, "No transformation template appeared in 100 L3 runs"

    def test_check_correct_answer(self, geo):
        random.seed(42)
        result = geo.generate(difficulty=1)
        check_result = geo.check({
            "answer": result["correct_index"],
            "exercise": result,
        })
        assert check_result["correct"] is True

    def test_check_wrong_answer(self, geo):
        random.seed(42)
        result = geo.generate(difficulty=1)
        wrong_index = (result["correct_index"] + 1) % 5
        check_result = geo.check({
            "answer": wrong_index,
            "exercise": result,
        })
        assert check_result["correct"] is False

    def test_options_are_distinct(self, geo):
        """All 5 options must be unique strings."""
        for difficulty in [1, 2, 3]:
            for _ in range(50):
                result = geo.generate(difficulty=difficulty)
                options = result["options"]
                assert len(set(options)) == len(options), (
                    f"Duplicate options found: {options}"
                )

    def test_correct_option_is_valid_index(self, geo):
        for difficulty in [1, 2, 3]:
            for _ in range(30):
                result = geo.generate(difficulty=difficulty)
                idx = result["correct_index"]
                assert 0 <= idx < len(result["options"])

    def test_graph_data_is_string(self, geo):
        for difficulty in [1, 2, 3]:
            for _ in range(20):
                result = geo.generate(difficulty=difficulty)
                svg = result["graph_data"]
                assert isinstance(svg, str)


class TestItalianText:
    """Verify questions are in Italian."""

    @pytest.mark.parametrize("template_fn", TRANSFORMATION_TEMPLATES, ids=lambda f: f.__name__)
    def test_italian_keywords(self, template_fn):
        for _ in range(5):
            question, _, _, explanation, tip = template_fn()
            # Check for Italian keywords in question or explanation
            italian_markers = [
                "punto", "coordinata", "asse", "vettore", "riflesso",
                "ruotato", "traslato", "simili", "triangolo", "origine",
                "misura", "rapporto", "lato", "area", "volume", "figura",
                "prima", "somma", "vertici",
            ]
            combined = (question + explanation + tip).lower()
            found = any(m in combined for m in italian_markers)
            assert found, f"No Italian markers found in: {question[:80]}..."
