import math
import pytest

from exercises.geometry_sherlock import (
    GeometrySherlock,
    _fmt,
    _t1_cylinder_volume,
    _t1_rectangular_prism_volume,
    _t2_cone_volume,
    _t2_sphere_volume,
    _t2_pyramid_volume,
    _t3_composite_cylinder_cone,
    _t3_sphere_inscribed_in_cylinder,
)

SOLID_TEMPLATES = [
    _t1_cylinder_volume,
    _t1_rectangular_prism_volume,
    _t2_cone_volume,
    _t2_sphere_volume,
    _t2_pyramid_volume,
    _t3_composite_cylinder_cone,
    _t3_sphere_inscribed_in_cylinder,
]


class TestSolidTemplatesOutput:
    """Each template must return a valid 5-tuple with non-empty strings and positive correct value."""

    @pytest.mark.parametrize("template_fn", SOLID_TEMPLATES, ids=lambda f: f.__name__)
    def test_returns_valid_tuple(self, template_fn):
        for _ in range(20):
            question, correct_value, svg, explanation, tip = template_fn()
            assert isinstance(question, str) and len(question) > 10
            assert isinstance(correct_value, (int, float))
            assert correct_value > 0
            assert isinstance(svg, str) and "<svg" in svg and "</svg>" in svg
            assert isinstance(explanation, str) and len(explanation) > 10
            assert isinstance(tip, str) and len(tip) > 5


class TestSolidFormulas:
    """Verify that the correct values match the expected formulas."""

    def test_cylinder_volume_formula(self):
        for _ in range(30):
            question, correct_value, svg, explanation, tip = _t1_cylinder_volume()
            # Extract r and h from the question text
            # Question format: "...raggio di base {r} cm e altezza {h} cm..."
            parts = question.split()
            r_idx = parts.index("base") + 1
            r = int(parts[r_idx])
            h_idx = parts.index("altezza") + 1
            h = int(parts[h_idx])
            expected = math.pi * r * r * h
            assert abs(correct_value - expected) < 1e-6

    def test_rectangular_prism_volume_formula(self):
        for _ in range(30):
            question, correct_value, svg, explanation, tip = _t1_rectangular_prism_volume()
            # Extract l, w, h from question
            parts = question.split()
            l_idx = parts.index("lunghezza") + 1
            l = int(parts[l_idx])
            w_idx = parts.index("larghezza") + 1
            w = int(parts[w_idx])
            h_idx = parts.index("altezza") + 1
            h = int(parts[h_idx])
            expected = l * w * h
            assert abs(correct_value - expected) < 1e-6

    def test_cone_volume_formula(self):
        for _ in range(30):
            question, correct_value, svg, explanation, tip = _t2_cone_volume()
            parts = question.split()
            r_idx = parts.index("base") + 1
            r = int(parts[r_idx])
            h_idx = parts.index("altezza") + 1
            h = int(parts[h_idx])
            expected = math.pi * r * r * h / 3
            assert abs(correct_value - expected) < 1e-6

    def test_sphere_volume_formula(self):
        for _ in range(30):
            question, correct_value, svg, explanation, tip = _t2_sphere_volume()
            parts = question.split()
            d_idx = parts.index("diametro") + 1
            d = int(parts[d_idx])
            r = d / 2
            expected = 4 * math.pi * r ** 3 / 3
            assert abs(correct_value - expected) < 1e-6

    def test_pyramid_volume_formula(self):
        for _ in range(30):
            question, correct_value, svg, explanation, tip = _t2_pyramid_volume()
            parts = question.split()
            # "...lato di base {l} cm e altezza {h} cm..."
            lato_idx = parts.index("lato") + 3  # "lato di base X"
            l = int(parts[lato_idx])
            h_idx = parts.index("altezza") + 1
            h = int(parts[h_idx])
            expected = l * l * h / 3
            assert abs(correct_value - expected) < 1e-6

    def test_composite_cylinder_cone_formula(self):
        for _ in range(30):
            question, correct_value, svg, explanation, tip = _t3_composite_cylinder_cone()
            # Extract r, h_cyl, h_cone from question
            parts = question.split()
            r_idx = parts.index("(raggio") + 1
            r = int(parts[r_idx])
            # Find "altezza X cm)" for cylinder
            h_cyl_idx = parts.index("altezza") + 1
            h_cyl = int(parts[h_cyl_idx])
            # The cone height follows the second "altezza"
            second_parts = question.split("altezza")
            h_cone_text = second_parts[2].strip().split()[0]
            h_cone = int(h_cone_text)
            expected = math.pi * r * r * h_cyl + math.pi * r * r * h_cone / 3
            assert abs(correct_value - expected) < 1e-6

    def test_sphere_inscribed_in_cylinder_formula(self):
        for _ in range(30):
            question, correct_value, svg, explanation, tip = _t3_sphere_inscribed_in_cylinder()
            parts = question.split()
            r_idx = parts.index("raggio") + 1
            r = int(parts[r_idx])
            h = 2 * r
            v_cyl = math.pi * r * r * h
            v_sphere = 4 * math.pi * r ** 3 / 3
            expected = v_cyl - v_sphere
            assert abs(correct_value - expected) < 1e-6


class TestSVGContent:
    """Verify SVG strings contain expected structural elements."""

    @pytest.mark.parametrize("template_fn", SOLID_TEMPLATES, ids=lambda f: f.__name__)
    def test_svg_has_structure(self, template_fn):
        for _ in range(5):
            _, _, svg, _, _ = template_fn()
            assert svg.startswith("<svg")
            assert svg.endswith("</svg>")
            assert len(svg) > 100


class TestDistractorsExcludeCorrect:
    """Distractors generated through the GeometrySherlock class must not contain the correct answer."""

    def test_no_correct_in_distractors(self):
        ex = GeometrySherlock()
        for difficulty in [1, 2, 3]:
            for _ in range(20):
                result = ex.generate(difficulty)
                correct_idx = result["correct_index"]
                correct_val = result["options"][correct_idx]
                other_options = [
                    opt for i, opt in enumerate(result["options"]) if i != correct_idx
                ]
                for opt in other_options:
                    assert opt != correct_val, (
                        f"Distractor matches correct answer {correct_val}"
                    )


class TestGenerateIntegration:
    """Full integration: GeometrySherlock.generate must produce valid exercise dicts at all levels."""

    @pytest.mark.parametrize("difficulty", [1, 2, 3])
    def test_generate_returns_valid_dict(self, difficulty):
        ex = GeometrySherlock()
        for _ in range(30):
            result = ex.generate(difficulty)
            assert "question" in result
            assert "options" in result
            assert "correct_index" in result
            assert "explanation" in result
            assert "graph_data" in result
            assert len(result["options"]) >= 4
            assert 0 <= result["correct_index"] < len(result["options"])
            assert result["difficulty"] == difficulty
