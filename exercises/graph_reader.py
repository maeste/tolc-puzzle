import math
import random

from exercises.base import Exercise


# ---------------------------------------------------------------------------
# SVG helper utilities
# ---------------------------------------------------------------------------

_SVG_W = 300
_SVG_H = 200
_PAD = 30  # padding around plot area
_PLOT_W = _SVG_W - 2 * _PAD
_PLOT_H = _SVG_H - 2 * _PAD


def _world_to_svg(wx, wy, x_range, y_range):
    """Convert world (math) coordinates to SVG pixel coordinates."""
    x_min, x_max = x_range
    y_min, y_max = y_range
    sx = _PAD + (wx - x_min) / (x_max - x_min) * _PLOT_W
    sy = _PAD + (y_max - wy) / (y_max - y_min) * _PLOT_H  # flip y
    return sx, sy


def _build_svg(func, x_range=(-5, 5), y_range=(-5, 5), n_points=120, color="#2563eb", label=""):
    """Build an SVG string plotting *func* over the given ranges.

    Parameters
    ----------
    func : callable  – f(x) -> y  (may raise / return None for domain holes)
    x_range, y_range : tuple of (min, max) in math coords
    n_points : int – number of sample points
    color : str – stroke color for the curve
    label : str – optional label placed top-left inside the SVG
    """
    x_min, x_max = x_range
    y_min, y_max = y_range

    parts = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {_SVG_W} {_SVG_H}" '
        f'width="{_SVG_W}" height="{_SVG_H}" '
        f'style="background:#fff;border:1px solid #ddd;border-radius:6px">'
    )

    # light grid
    grid_color = "#e5e7eb"
    for gx in range(int(math.floor(x_min)), int(math.ceil(x_max)) + 1):
        sx, _ = _world_to_svg(gx, 0, x_range, y_range)
        parts.append(f'<line x1="{sx:.1f}" y1="{_PAD}" x2="{sx:.1f}" y2="{_PAD + _PLOT_H}" stroke="{grid_color}" stroke-width="0.5"/>')
    for gy in range(int(math.floor(y_min)), int(math.ceil(y_max)) + 1):
        _, sy = _world_to_svg(0, gy, x_range, y_range)
        parts.append(f'<line x1="{_PAD}" y1="{sy:.1f}" x2="{_PAD + _PLOT_W}" y2="{sy:.1f}" stroke="{grid_color}" stroke-width="0.5"/>')

    # axes
    ax_color = "#374151"
    ox, oy = _world_to_svg(0, 0, x_range, y_range)
    # x-axis
    parts.append(f'<line x1="{_PAD}" y1="{oy:.1f}" x2="{_PAD + _PLOT_W}" y2="{oy:.1f}" stroke="{ax_color}" stroke-width="1.2"/>')
    # y-axis
    parts.append(f'<line x1="{ox:.1f}" y1="{_PAD}" x2="{ox:.1f}" y2="{_PAD + _PLOT_H}" stroke="{ax_color}" stroke-width="1.2"/>')

    # tick labels on axes
    tick_font = 'font-size="7" fill="#6b7280" font-family="sans-serif" text-anchor="middle"'
    for gx in range(int(math.floor(x_min)), int(math.ceil(x_max)) + 1):
        if gx == 0:
            continue
        sx, _ = _world_to_svg(gx, 0, x_range, y_range)
        parts.append(f'<text x="{sx:.1f}" y="{oy + 11:.1f}" {tick_font}>{gx}</text>')
    for gy in range(int(math.floor(y_min)), int(math.ceil(y_max)) + 1):
        if gy == 0:
            continue
        _, sy = _world_to_svg(0, gy, x_range, y_range)
        parts.append(f'<text x="{ox - 10:.1f}" y="{sy + 3:.1f}" {tick_font}>{gy}</text>')

    # plot curve – build polyline segments (break on domain errors)
    segments = []
    current_seg = []
    step = (x_max - x_min) / n_points
    for i in range(n_points + 1):
        wx = x_min + i * step
        try:
            wy = func(wx)
            if wy is None or not math.isfinite(wy):
                raise ValueError
        except (ValueError, ZeroDivisionError, OverflowError):
            if current_seg:
                segments.append(current_seg)
                current_seg = []
            continue
        # clip to view
        if wy < y_min - 2 or wy > y_max + 2:
            if current_seg:
                segments.append(current_seg)
                current_seg = []
            continue
        sx, sy = _world_to_svg(wx, wy, x_range, y_range)
        current_seg.append((sx, sy))
    if current_seg:
        segments.append(current_seg)

    for seg in segments:
        if len(seg) < 2:
            continue
        pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in seg)
        parts.append(f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round"/>')

    # optional label
    if label:
        parts.append(f'<text x="{_PAD + 4}" y="{_PAD + 12}" font-size="10" fill="#111" font-family="monospace">{label}</text>')

    parts.append("</svg>")
    return "".join(parts)


# ---------------------------------------------------------------------------
# Function catalogue
# ---------------------------------------------------------------------------

def _linear(m, q):
    """y = mx + q"""
    return lambda x: m * x + q


def _quadratic(a, h, k):
    """y = a(x - h)^2 + k"""
    return lambda x: a * (x - h) ** 2 + k


def _exponential(a, b, k):
    """y = a * b^x + k"""
    def f(x):
        try:
            return a * (b ** x) + k
        except OverflowError:
            return None
    return f


def _logarithmic(a, h, k):
    """y = a * ln(x - h) + k"""
    def f(x):
        arg = x - h
        if arg <= 0:
            return None
        return a * math.log(arg) + k
    return f


def _abs_value(a, h, k):
    """y = a|x - h| + k"""
    return lambda x: a * abs(x - h) + k


def _reciprocal(a, h, k):
    """y = a / (x - h) + k"""
    def f(x):
        d = x - h
        if abs(d) < 1e-9:
            return None
        return a / d + k
    return f


def _sin_func(a, b, h, k):
    """y = a * sin(b(x - h)) + k"""
    return lambda x: a * math.sin(b * (x - h)) + k


def _cos_func(a, b, h, k):
    """y = a * cos(b(x - h)) + k"""
    return lambda x: a * math.cos(b * (x - h)) + k


def _sqrt_func(a, h, k):
    """y = a * sqrt(x - h) + k"""
    def f(x):
        arg = x - h
        if arg < 0:
            return None
        return a * math.sqrt(arg) + k
    return f


# ---------------------------------------------------------------------------
# Expression formatting helpers
# ---------------------------------------------------------------------------

def _fmt_num(v, always_sign=False):
    """Format a number nicely (integer if possible)."""
    if v == int(v):
        v = int(v)
    s = str(v)
    if always_sign and v > 0:
        s = "+" + s
    return s


def _expr_linear(m, q):
    parts = []
    if m == 1:
        parts.append("x")
    elif m == -1:
        parts.append("-x")
    else:
        parts.append(f"{_fmt_num(m)}x")
    if q != 0:
        parts.append(_fmt_num(q, always_sign=True))
    return "y = " + "".join(parts) if parts else "y = 0"


def _expr_quadratic(a, h, k):
    base = ""
    if a == 1:
        base = ""
    elif a == -1:
        base = "-"
    else:
        base = _fmt_num(a)
    if h == 0:
        base += "x²"
    else:
        base += f"(x{_fmt_num(-h, always_sign=True)})²"
    if k != 0:
        base += f" {_fmt_num(k, always_sign=True)}"
    return "y = " + base


def _expr_exponential(a, b, k):
    base = ""
    if a == 1:
        base = ""
    elif a == -1:
        base = "-"
    else:
        base = _fmt_num(a) + "·"
    base += f"{_fmt_num(b)}^x"
    if k != 0:
        base += f" {_fmt_num(k, always_sign=True)}"
    return "y = " + base


def _expr_logarithmic(a, h, k):
    coeff = ""
    if a == 1:
        coeff = ""
    elif a == -1:
        coeff = "-"
    else:
        coeff = _fmt_num(a) + "·"
    if h == 0:
        arg = "x"
    else:
        arg = f"(x{_fmt_num(-h, always_sign=True)})"
    base = f"{coeff}ln{arg}"
    if k != 0:
        base += f" {_fmt_num(k, always_sign=True)}"
    return "y = " + base


def _expr_abs(a, h, k):
    coeff = ""
    if a == 1:
        coeff = ""
    elif a == -1:
        coeff = "-"
    else:
        coeff = _fmt_num(a)
    if h == 0:
        inner = "x"
    else:
        inner = f"x{_fmt_num(-h, always_sign=True)}"
    base = f"{coeff}|{inner}|"
    if k != 0:
        base += f" {_fmt_num(k, always_sign=True)}"
    return "y = " + base


def _expr_reciprocal(a, h, k):
    if h == 0:
        denom = "x"
    else:
        denom = f"(x{_fmt_num(-h, always_sign=True)})"
    if a == 1:
        base = f"1/{denom}"
    elif a == -1:
        base = f"-1/{denom}"
    else:
        base = f"{_fmt_num(a)}/{denom}"
    if k != 0:
        base += f" {_fmt_num(k, always_sign=True)}"
    return "y = " + base


def _expr_sin(a, b, h, k):
    coeff = ""
    if a == 1:
        coeff = ""
    elif a == -1:
        coeff = "-"
    else:
        coeff = _fmt_num(a)
    if b == 1 and h == 0:
        arg = "x"
    elif h == 0:
        arg = f"{_fmt_num(b)}x"
    else:
        arg = f"{_fmt_num(b)}(x{_fmt_num(-h, always_sign=True)})"
    base = f"{coeff}sin({arg})"
    if k != 0:
        base += f" {_fmt_num(k, always_sign=True)}"
    return "y = " + base


def _expr_cos(a, b, h, k):
    coeff = ""
    if a == 1:
        coeff = ""
    elif a == -1:
        coeff = "-"
    else:
        coeff = _fmt_num(a)
    if b == 1 and h == 0:
        arg = "x"
    elif h == 0:
        arg = f"{_fmt_num(b)}x"
    else:
        arg = f"{_fmt_num(b)}(x{_fmt_num(-h, always_sign=True)})"
    base = f"{coeff}cos({arg})"
    if k != 0:
        base += f" {_fmt_num(k, always_sign=True)}"
    return "y = " + base


def _expr_sqrt(a, h, k):
    coeff = ""
    if a == 1:
        coeff = ""
    elif a == -1:
        coeff = "-"
    else:
        coeff = _fmt_num(a) + "·"
    if h == 0:
        arg = "x"
    else:
        arg = f"(x{_fmt_num(-h, always_sign=True)})"
    base = f"{coeff}√{arg}"
    if k != 0:
        base += f" {_fmt_num(k, always_sign=True)}"
    return "f(x) = " + base


def _expr_quadratic_standard(a, b, c):
    """Format ax² + bx + c in standard form."""
    parts = []
    if a == 1:
        parts.append("x²")
    elif a == -1:
        parts.append("-x²")
    else:
        parts.append(f"{_fmt_num(a)}x²")
    if b != 0:
        if b == 1:
            parts.append(" + x")
        elif b == -1:
            parts.append(" - x")
        elif b > 0:
            parts.append(f" + {_fmt_num(b)}x")
        else:
            parts.append(f" - {_fmt_num(abs(b))}x")
    if c != 0:
        parts.append(f" {_fmt_num(c, always_sign=True)}")
    return "f(x) = " + "".join(parts)


# ---------------------------------------------------------------------------
# Function spec: (func_callable, expression_str, family_name, explanation_hint)
# ---------------------------------------------------------------------------

_FAMILIES = [
    "lineare",
    "quadratica",
    "esponenziale",
    "logaritmica",
    "valore assoluto",
    "reciproca (1/x)",
    "sinusoidale",
    "cosinusoidale",
]

_DID_YOU_KNOW = [
    "Le funzioni lineari hanno sempre un tasso di variazione costante: la pendenza!",
    "Le parabole sono le curve che descrivono la traiettoria di un proiettile (senza attrito).",
    "Le funzioni esponenziali modellano la crescita della popolazione e il decadimento radioattivo.",
    "Il logaritmo naturale è l'inversa dell'esponenziale: se y = e^x, allora x = ln(y).",
    "La funzione valore assoluto |x| crea sempre una forma a V: utile per descrivere distanze.",
    "La funzione 1/x ha due asintoti: uno verticale e uno orizzontale. Mai dividi per zero!",
    "Le funzioni seno e coseno sono periodiche con periodo 2π ≈ 6.28.",
    "Traslare un grafico a destra di h unità si ottiene sostituendo x con (x − h).",
    "Moltiplicare una funzione per −1 riflette il grafico rispetto all'asse x.",
    "Moltiplicare x per un fattore > 1 dentro la funzione comprime il grafico orizzontalmente.",
]


def _random_spec_level1():
    """Generate a random function spec suitable for level 1 (basic type recognition)."""
    family = random.choice(["linear", "quadratic", "exponential", "logarithmic", "abs", "reciprocal", "sin", "cos"])
    return _make_spec(family, transformed=False)


def _random_spec_level2():
    """Level 2: transformed functions (translations, reflections, stretch)."""
    family = random.choice(["linear", "quadratic", "exponential", "logarithmic", "abs", "reciprocal", "sin", "cos"])
    return _make_spec(family, transformed=True)


def _random_spec_level3():
    """Level 3: compositions and more complex transformations."""
    family = random.choice(["quadratic", "exponential", "logarithmic", "sin", "cos", "reciprocal"])
    return _make_spec(family, transformed=True, complex_transforms=True)


def _make_spec(family, transformed=False, complex_transforms=False):
    """Return (func, expr_str, family_it, hint, x_range, y_range)."""
    if family == "linear":
        if transformed:
            m = random.choice([-3, -2, -1, -0.5, 0.5, 1, 2, 3])
            q = random.choice([-3, -2, -1, 0, 1, 2, 3])
        else:
            m = random.choice([1, 2, -1, -2])
            q = 0
        func = _linear(m, q)
        expr = _expr_linear(m, q)
        hint = f"La retta ha pendenza {_fmt_num(m)}"
        if q != 0:
            hint += f" e intercetta y in {_fmt_num(q)}"
        return func, expr, "lineare", hint, (-5, 5), (-6, 6)

    elif family == "quadratic":
        if complex_transforms:
            a = random.choice([-2, -1, -0.5, 0.5, 1, 2])
            h = random.choice([-2, -1, 0, 1, 2])
            k = random.choice([-3, -2, -1, 0, 1, 2, 3])
        elif transformed:
            a = random.choice([-1, 1, 2, -2])
            h = random.choice([-2, -1, 0, 1, 2])
            k = random.choice([-2, -1, 0, 1, 2])
        else:
            a = random.choice([1, -1])
            h, k = 0, 0
        func = _quadratic(a, h, k)
        expr = _expr_quadratic(a, h, k)
        direction = "verso l'alto" if a > 0 else "verso il basso"
        hint = f"Parabola con apertura {direction}, vertice in ({_fmt_num(h)}, {_fmt_num(k)})"
        yr = max(abs(k) + 5, 6)
        return func, expr, "quadratica", hint, (-5, 5), (-yr, yr)

    elif family == "exponential":
        if complex_transforms:
            a = random.choice([-2, -1, 1, 2])
            b = random.choice([2, 3, 0.5])
            k = random.choice([-2, -1, 0, 1, 2])
        elif transformed:
            a = random.choice([-1, 1])
            b = random.choice([2, 3])
            k = random.choice([-1, 0, 1])
        else:
            a = 1
            b = random.choice([2, 3])
            k = 0
        func = _exponential(a, b, k)
        expr = _expr_exponential(a, b, k)
        growth = "crescente" if a * (1 if b > 1 else -1) > 0 else "decrescente"
        hint = f"Esponenziale {growth} con base {_fmt_num(b)}"
        if k != 0:
            hint += f" e asintoto orizzontale y = {_fmt_num(k)}"
        return func, expr, "esponenziale", hint, (-3, 4), (-5, 10)

    elif family == "logarithmic":
        if complex_transforms:
            a = random.choice([-2, -1, 1, 2])
            h = random.choice([-1, 0, 1])
            k = random.choice([-2, -1, 0, 1, 2])
        elif transformed:
            a = random.choice([-1, 1])
            h = random.choice([0, 1])
            k = random.choice([-1, 0, 1])
        else:
            a = 1
            h, k = 0, 0
        func = _logarithmic(a, h, k)
        expr = _expr_logarithmic(a, h, k)
        hint = f"Logaritmo con dominio x > {_fmt_num(h)}"
        if a < 0:
            hint += ", riflesso rispetto all'asse x"
        return func, expr, "logaritmica", hint, (-1 + h, 8), (-5, 5)

    elif family == "abs":
        if complex_transforms:
            a = random.choice([-2, -1, -0.5, 0.5, 1, 2])
            h = random.choice([-2, -1, 0, 1, 2])
            k = random.choice([-3, -2, -1, 0, 1, 2, 3])
        elif transformed:
            a = random.choice([-1, 1, 2])
            h = random.choice([-1, 0, 1])
            k = random.choice([-1, 0, 1])
        else:
            a = 1
            h, k = 0, 0
        func = _abs_value(a, h, k)
        expr = _expr_abs(a, h, k)
        direction = "V" if a > 0 else "V rovesciata"
        hint = f"Valore assoluto a forma di {direction} con vertice in ({_fmt_num(h)}, {_fmt_num(k)})"
        return func, expr, "valore assoluto", hint, (-5, 5), (-5, 6)

    elif family == "reciprocal":
        if complex_transforms:
            a = random.choice([-2, -1, 1, 2])
            h = random.choice([-2, -1, 0, 1, 2])
            k = random.choice([-2, -1, 0, 1, 2])
        elif transformed:
            a = random.choice([-1, 1])
            h = random.choice([-1, 0, 1])
            k = random.choice([-1, 0, 1])
        else:
            a = 1
            h, k = 0, 0
        func = _reciprocal(a, h, k)
        expr = _expr_reciprocal(a, h, k)
        hint = f"Iperbole con asintoto verticale x = {_fmt_num(h)} e orizzontale y = {_fmt_num(k)}"
        return func, expr, "reciproca (1/x)", hint, (-6, 6), (-6, 6)

    elif family == "sin":
        if complex_transforms:
            a = random.choice([-2, -1, 1, 2])
            b = random.choice([1, 2])
            h = random.choice([-1, 0, 1])
            k = random.choice([-1, 0, 1])
        elif transformed:
            a = random.choice([-1, 1, 2])
            b = random.choice([1, 2])
            h = 0
            k = random.choice([-1, 0, 1])
        else:
            a, b, h, k = 1, 1, 0, 0
        func = _sin_func(a, b, h, k)
        expr = _expr_sin(a, b, h, k)
        hint = f"Sinusoide con ampiezza {_fmt_num(abs(a))} e periodo {_fmt_num(round(2 * math.pi / b, 2))}"
        return func, expr, "sinusoidale", hint, (-7, 7), (-4, 4)

    else:  # cos
        if complex_transforms:
            a = random.choice([-2, -1, 1, 2])
            b = random.choice([1, 2])
            h = random.choice([-1, 0, 1])
            k = random.choice([-1, 0, 1])
        elif transformed:
            a = random.choice([-1, 1, 2])
            b = random.choice([1, 2])
            h = 0
            k = random.choice([-1, 0, 1])
        else:
            a, b, h, k = 1, 1, 0, 0
        func = _cos_func(a, b, h, k)
        expr = _expr_cos(a, b, h, k)
        hint = f"Cosinusoide con ampiezza {_fmt_num(abs(a))} e periodo {_fmt_num(round(2 * math.pi / b, 2))}"
        return func, expr, "cosinusoidale", hint, (-7, 7), (-4, 4)


# ---------------------------------------------------------------------------
# Distractor generation
# ---------------------------------------------------------------------------

_ALL_FAMILIES = ["linear", "quadratic", "exponential", "logarithmic", "abs", "reciprocal", "sin", "cos"]


def _generate_distractors(correct_family, difficulty, count=4):
    """Generate *count* distractor specs that differ from the correct one."""
    distractors = []
    other_families = [f for f in _ALL_FAMILIES if f != correct_family]

    if difficulty == 1:
        # distractors are different families with simple params
        chosen = random.sample(other_families, min(count, len(other_families)))
        for fam in chosen:
            distractors.append(_make_spec(fam, transformed=False))
    elif difficulty == 2:
        # mix: some same family different params, some different families
        same_count = random.randint(1, min(2, count))
        diff_count = count - same_count
        for _ in range(same_count):
            distractors.append(_make_spec(correct_family, transformed=True))
        chosen_others = random.sample(other_families, min(diff_count, len(other_families)))
        for fam in chosen_others:
            distractors.append(_make_spec(fam, transformed=True))
    else:
        # level 3: all transformed, mix of same and different families
        same_count = random.randint(1, 2)
        diff_count = count - same_count
        for _ in range(same_count):
            distractors.append(_make_spec(correct_family, transformed=True, complex_transforms=True))
        chosen_others = random.sample(other_families, min(diff_count, len(other_families)))
        for fam in chosen_others:
            distractors.append(_make_spec(fam, transformed=True, complex_transforms=True))

    # ensure we have exactly count
    while len(distractors) < count:
        fam = random.choice(other_families)
        distractors.append(_make_spec(fam, transformed=(difficulty > 1), complex_transforms=(difficulty == 3)))
    return distractors[:count]


def _family_from_name(family_it):
    """Map Italian family name back to internal key."""
    mapping = {
        "lineare": "linear",
        "quadratica": "quadratic",
        "esponenziale": "exponential",
        "logaritmica": "logarithmic",
        "valore assoluto": "abs",
        "reciproca (1/x)": "reciprocal",
        "sinusoidale": "sin",
        "cosinusoidale": "cos",
    }
    return mapping.get(family_it, "linear")


# ---------------------------------------------------------------------------
# Main exercise class
# ---------------------------------------------------------------------------

class GraphReader(Exercise):
    """'Che Funzione Sono?' – function-graph association exercises."""

    # ------------------------------------------------------------------
    # Domain / Codomain / Evaluation templates
    # ------------------------------------------------------------------

    def _template_domain_logarithmic(self) -> dict:
        """Dominio di f(x) = ln(x - a)."""
        a = random.choice([-3, -2, -1, 0, 1, 2, 3])
        func = _logarithmic(1, a, 0)
        if a == 0:
            expr_str = "f(x) = ln(x)"
        else:
            expr_str = f"f(x) = ln(x{_fmt_num(-a, always_sign=True)})"
        graph_svg = _build_svg(func, (a - 1, a + 8), (-5, 5), label=expr_str)

        correct = f"x > {_fmt_num(a)}"
        distractors = [
            f"x ≥ {_fmt_num(a)}",
            "x > 0",
            "x ≥ 0",
            "Tutti i reali",
            f"x > {_fmt_num(a + 1)}",
            f"x ≥ {_fmt_num(a - 1)}",
        ]
        # remove correct from distractors if present, then sample 4
        distractors = [d for d in distractors if d != correct]
        random.shuffle(distractors)
        distractors = distractors[:4]

        options_raw = [correct] + distractors
        correct_index = 0
        options, correct_index = self.shuffle_options(options_raw, correct_index)

        explanation = (
            f"Il logaritmo naturale ln(t) è definito solo per t > 0. "
            f"Quindi ln(x{_fmt_num(-a, always_sign=True)}) richiede "
            f"x{_fmt_num(-a, always_sign=True)} > 0, cioè x > {_fmt_num(a)}."
        )
        return {
            "question": f"Qual è il dominio di {expr_str}?",
            "graph_data": graph_svg,
            "options": options,
            "correct_index": correct_index,
            "explanation": explanation,
            "did_you_know": "Il logaritmo naturale ln(x) non è definito per x ≤ 0: il suo dominio è (0, +∞).",
        }

    def _template_domain_rational(self) -> dict:
        """Dominio di f(x) = 1/(x - a)."""
        a = random.choice([-3, -2, -1, 0, 1, 2, 3])
        func = _reciprocal(1, a, 0)
        if a == 0:
            expr_str = "f(x) = 1/x"
        else:
            expr_str = f"f(x) = 1/(x{_fmt_num(-a, always_sign=True)})"
        graph_svg = _build_svg(func, (a - 5, a + 5), (-6, 6), label=expr_str)

        correct = f"x ≠ {_fmt_num(a)}"
        distractors = [
            f"x > {_fmt_num(a)}",
            "x ≠ 0",
            "Tutti i reali",
            "x > 0",
            f"x ≠ {_fmt_num(a + 1)}",
            f"x < {_fmt_num(a)}",
        ]
        distractors = [d for d in distractors if d != correct]
        random.shuffle(distractors)
        distractors = distractors[:4]

        options_raw = [correct] + distractors
        correct_index = 0
        options, correct_index = self.shuffle_options(options_raw, correct_index)

        explanation = (
            f"Una funzione razionale non è definita dove il denominatore è zero. "
            f"Qui il denominatore è (x{_fmt_num(-a, always_sign=True)}), "
            f"che vale zero per x = {_fmt_num(a)}. "
            f"Il dominio è quindi tutti i reali tranne x = {_fmt_num(a)}."
        )
        return {
            "question": f"Qual è il dominio di {expr_str}?",
            "graph_data": graph_svg,
            "options": options,
            "correct_index": correct_index,
            "explanation": explanation,
            "did_you_know": "Non si può dividere per zero! L'asintoto verticale indica il valore escluso dal dominio.",
        }

    def _template_domain_sqrt(self) -> dict:
        """Dominio di f(x) = sqrt(x - a)."""
        a = random.choice([-3, -2, -1, 0, 1, 2, 3])
        func = _sqrt_func(1, a, 0)
        if a == 0:
            expr_str = "f(x) = √x"
        else:
            expr_str = f"f(x) = √(x{_fmt_num(-a, always_sign=True)})"
        graph_svg = _build_svg(func, (a - 1, a + 8), (-1, 5), label=expr_str)

        correct = f"x ≥ {_fmt_num(a)}"
        distractors = [
            f"x > {_fmt_num(a)}",
            "x ≥ 0",
            "Tutti i reali",
            "x > 0",
            f"x ≥ {_fmt_num(a + 1)}",
            f"x > {_fmt_num(a - 1)}",
        ]
        distractors = [d for d in distractors if d != correct]
        random.shuffle(distractors)
        distractors = distractors[:4]

        options_raw = [correct] + distractors
        correct_index = 0
        options, correct_index = self.shuffle_options(options_raw, correct_index)

        explanation = (
            f"La radice quadrata √t è definita per t ≥ 0. "
            f"Quindi √(x{_fmt_num(-a, always_sign=True)}) richiede "
            f"x{_fmt_num(-a, always_sign=True)} ≥ 0, cioè x ≥ {_fmt_num(a)}."
        )
        return {
            "question": f"Qual è il dominio di {expr_str}?",
            "graph_data": graph_svg,
            "options": options,
            "correct_index": correct_index,
            "explanation": explanation,
            "did_you_know": "La radice quadrata di un numero negativo non è un numero reale: ecco perché il dominio è limitato!",
        }

    def _template_function_evaluation(self) -> dict:
        """Data f(x) = ax² + bx + c, quanto vale f(n)?"""
        a_coeff = random.choice([-2, -1, 1, 2])
        b_coeff = random.choice([-3, -2, -1, 0, 1, 2, 3])
        c_coeff = random.choice([-4, -3, -2, -1, 0, 1, 2, 3, 4])
        n = random.choice([-3, -2, -1, 0, 1, 2, 3])

        correct_value = a_coeff * n * n + b_coeff * n + c_coeff
        expr_str = _expr_quadratic_standard(a_coeff, b_coeff, c_coeff)

        func = lambda x: a_coeff * x * x + b_coeff * x + c_coeff
        graph_svg = _build_svg(
            func,
            (-5, 5),
            (min(-5, correct_value - 2), max(5, correct_value + 2)),
            label=expr_str,
        )

        # Generate numeric distractors that are plausible but wrong
        distractor_set = set()
        # Common mistakes: sign error, forgetting a term, off-by-one
        candidates = [
            -a_coeff * n * n + b_coeff * n + c_coeff,  # sign of a wrong
            a_coeff * n * n - b_coeff * n + c_coeff,    # sign of b wrong
            a_coeff * n * n + b_coeff * n - c_coeff,    # sign of c wrong
            a_coeff * n + b_coeff + c_coeff,             # forgot to square
            a_coeff * n * n + b_coeff * n,               # forgot c
            correct_value + 1,
            correct_value - 1,
            correct_value + 2,
            correct_value - 2,
            a_coeff * (n + 1) * (n + 1) + b_coeff * (n + 1) + c_coeff,  # f(n+1) instead
        ]
        for v in candidates:
            if v != correct_value:
                distractor_set.add(v)
        distractor_list = list(distractor_set)
        random.shuffle(distractor_list)
        distractors = [str(int(d)) if d == int(d) else str(d) for d in distractor_list[:4]]

        # Ensure we have 4 distractors
        fallback = correct_value + 3
        while len(distractors) < 4:
            if fallback != correct_value and str(int(fallback)) not in distractors:
                distractors.append(str(int(fallback)))
            fallback += 1

        correct_str = str(int(correct_value)) if correct_value == int(correct_value) else str(correct_value)
        options_raw = [correct_str] + distractors[:4]
        correct_index = 0
        options, correct_index = self.shuffle_options(options_raw, correct_index)

        explanation = (
            f"Sostituendo x = {_fmt_num(n)} in {expr_str}: "
            f"f({_fmt_num(n)}) = {_fmt_num(a_coeff)}·({_fmt_num(n)})² "
            f"{_fmt_num(b_coeff, always_sign=True)}·({_fmt_num(n)}) "
            f"{_fmt_num(c_coeff, always_sign=True)} = {correct_str}."
        )
        return {
            "question": f"Data {expr_str}, quanto vale f({_fmt_num(n)})?",
            "graph_data": graph_svg,
            "options": options,
            "correct_index": correct_index,
            "explanation": explanation,
            "did_you_know": "Valutare una funzione significa sostituire il valore dato al posto della variabile x e calcolare il risultato.",
        }

    def _template_sign_of_function(self) -> dict:
        """Per quali x vale f(x) > 0? (quadratica con radici intere note)."""
        # Generate a quadratic a(x - r1)(x - r2) with known integer roots
        r1 = random.randint(-4, 0)
        r2 = random.randint(r1 + 1, 4)
        a_coeff = random.choice([-1, 1])

        # f(x) = a_coeff * (x - r1)(x - r2)
        func = lambda x, _a=a_coeff, _r1=r1, _r2=r2: _a * (x - _r1) * (x - _r2)

        # Expanded: a*(x^2 - (r1+r2)x + r1*r2)
        ea = a_coeff
        eb = -a_coeff * (r1 + r2)
        ec = a_coeff * r1 * r2
        expr_str = _expr_quadratic_standard(ea, eb, ec)

        graph_svg = _build_svg(func, (-5, 5), (-6, 6), label=expr_str)

        # f(x) > 0 depends on the sign of a_coeff
        if a_coeff > 0:
            # parabola opens up: f(x) > 0 for x < r1 or x > r2
            correct = f"x < {_fmt_num(r1)} oppure x > {_fmt_num(r2)}"
            wrong_interval = f"{_fmt_num(r1)} < x < {_fmt_num(r2)}"
        else:
            # parabola opens down: f(x) > 0 for r1 < x < r2
            correct = f"{_fmt_num(r1)} < x < {_fmt_num(r2)}"
            wrong_interval = f"x < {_fmt_num(r1)} oppure x > {_fmt_num(r2)}"

        distractors = [
            wrong_interval,
            f"x > {_fmt_num(r2)}",
            f"x > {_fmt_num(r1)}",
            "Tutti i reali",
            "Nessun valore di x",
            f"x < {_fmt_num(r1)}",
        ]
        distractors = [d for d in distractors if d != correct]
        random.shuffle(distractors)
        distractors = distractors[:4]

        options_raw = [correct] + distractors
        correct_index = 0
        options, correct_index = self.shuffle_options(options_raw, correct_index)

        if a_coeff > 0:
            sign_expl = (
                f"La parabola si apre verso l'alto (a > 0) con zeri in "
                f"x = {_fmt_num(r1)} e x = {_fmt_num(r2)}. "
                f"f(x) > 0 negli intervalli esterni: x < {_fmt_num(r1)} oppure x > {_fmt_num(r2)}."
            )
        else:
            sign_expl = (
                f"La parabola si apre verso il basso (a < 0) con zeri in "
                f"x = {_fmt_num(r1)} e x = {_fmt_num(r2)}. "
                f"f(x) > 0 nell'intervallo interno: {_fmt_num(r1)} < x < {_fmt_num(r2)}."
            )
        return {
            "question": f"Data {expr_str}, per quali valori di x vale f(x) > 0?",
            "graph_data": graph_svg,
            "options": options,
            "correct_index": correct_index,
            "explanation": sign_expl,
            "did_you_know": "Lo studio del segno di una funzione quadratica dipende dal segno del coefficiente di x² e dalle radici dell'equazione.",
        }

    # ------------------------------------------------------------------
    # Injectivity / Invertibility / Codomain / Injectivity-intervals
    # ------------------------------------------------------------------

    def _template_injectivity(self) -> dict:
        """La funzione è iniettiva? (test della retta orizzontale)."""
        # Catalogue: (family_key, injective?, builder, expr_builder, extra_info)
        catalogue = []

        # Linear: always injective (m != 0)
        m = random.choice([-3, -2, -1, 1, 2, 3])
        q = random.choice([-2, -1, 0, 1, 2])
        catalogue.append((
            "linear", True,
            _linear(m, q), _expr_linear(m, q),
            (-5, 5), (-6, 6),
            "Una funzione lineare (con m ≠ 0) è sempre iniettiva: "
            "ogni retta orizzontale interseca il grafico al più in un punto.",
        ))

        # Quadratic: NOT injective
        a = random.choice([-2, -1, 1, 2])
        h = random.choice([-2, -1, 0, 1, 2])
        k = random.choice([-2, -1, 0, 1, 2])
        yr = max(abs(k) + 5, 6)
        catalogue.append((
            "quadratic", False,
            _quadratic(a, h, k), _expr_quadratic(a, h, k),
            (-5, 5), (-yr, yr),
            f"Una parabola non è iniettiva: ad esempio la retta orizzontale "
            f"y = {_fmt_num(k + abs(a))} interseca il grafico in due punti.",
        ))

        # Abs: NOT injective
        a_abs = random.choice([-2, -1, 1, 2])
        h_abs = random.choice([-2, -1, 0, 1, 2])
        k_abs = random.choice([-2, -1, 0, 1, 2])
        catalogue.append((
            "abs", False,
            _abs_value(a_abs, h_abs, k_abs), _expr_abs(a_abs, h_abs, k_abs),
            (-5, 5), (-5, 6),
            f"La funzione valore assoluto non è iniettiva: la retta orizzontale "
            f"y = {_fmt_num(k_abs + abs(a_abs))} interseca il grafico in due punti.",
        ))

        # Exponential: always injective
        a_exp = random.choice([-1, 1])
        b_exp = random.choice([2, 3])
        k_exp = random.choice([-1, 0, 1])
        catalogue.append((
            "exponential", True,
            _exponential(a_exp, b_exp, k_exp), _expr_exponential(a_exp, b_exp, k_exp),
            (-3, 4), (-5, 10),
            "Una funzione esponenziale è sempre iniettiva: "
            "è strettamente monotona (sempre crescente o sempre decrescente).",
        ))

        # Logarithmic: always injective
        a_log = random.choice([-1, 1])
        h_log = random.choice([0, 1])
        k_log = random.choice([-1, 0, 1])
        catalogue.append((
            "logarithmic", True,
            _logarithmic(a_log, h_log, k_log), _expr_logarithmic(a_log, h_log, k_log),
            (-1 + h_log, 8), (-5, 5),
            "Una funzione logaritmica è sempre iniettiva: "
            "è strettamente monotona sul suo dominio.",
        ))

        # Sin: NOT injective
        a_sin = random.choice([1, 2])
        b_sin = random.choice([1, 2])
        catalogue.append((
            "sin", False,
            _sin_func(a_sin, b_sin, 0, 0), _expr_sin(a_sin, b_sin, 0, 0),
            (-7, 7), (-4, 4),
            "La funzione seno non è iniettiva: essendo periodica, "
            "ogni retta orizzontale y = c (con |c| ≤ ampiezza) interseca il grafico in infiniti punti.",
        ))

        # Cos: NOT injective
        a_cos = random.choice([1, 2])
        b_cos = random.choice([1, 2])
        catalogue.append((
            "cos", False,
            _cos_func(a_cos, b_cos, 0, 0), _expr_cos(a_cos, b_cos, 0, 0),
            (-7, 7), (-4, 4),
            "La funzione coseno non è iniettiva: essendo periodica, "
            "ogni retta orizzontale y = c (con |c| ≤ ampiezza) interseca il grafico in infiniti punti.",
        ))

        # Sqrt: always injective
        a_sq = random.choice([1, 2])
        h_sq = random.choice([0, 1, 2])
        k_sq = random.choice([-1, 0, 1])
        catalogue.append((
            "sqrt", True,
            _sqrt_func(a_sq, h_sq, k_sq), _expr_sqrt(a_sq, h_sq, k_sq),
            (h_sq - 1, h_sq + 8), (-1, 5),
            "La funzione radice quadrata è sempre iniettiva: "
            "è strettamente crescente sul suo dominio.",
        ))

        # Reciprocal: injective on each branch (we consider the full domain)
        a_rec = random.choice([-1, 1])
        h_rec = random.choice([-1, 0, 1])
        k_rec = random.choice([-1, 0, 1])
        catalogue.append((
            "reciprocal", True,
            _reciprocal(a_rec, h_rec, k_rec), _expr_reciprocal(a_rec, h_rec, k_rec),
            (-6, 6), (-6, 6),
            f"La funzione reciproca y = {_expr_reciprocal(a_rec, h_rec, k_rec)[4:]} è iniettiva "
            f"sul suo dominio (x ≠ {_fmt_num(h_rec)}): è strettamente monotona su ciascun ramo "
            f"e i due rami hanno immagini disgiunte.",
        ))

        choice = random.choice(catalogue)
        family_key, is_injective, func, expr_str, x_range, y_range, reason = choice

        graph_svg = _build_svg(func, x_range, y_range, label=expr_str)

        if is_injective:
            correct = "Sì, è iniettiva"
        else:
            correct = "No, non è iniettiva"

        distractors = [
            "No, non è iniettiva" if is_injective else "Sì, è iniettiva",
            "Solo per x > 0",
            "Solo per x ≥ 0",
            "Dipende dal dominio considerato",
            "Sì, ma solo se restringiamo il codominio",
            "Non si può determinare dal grafico",
        ]
        distractors = [d for d in distractors if d != correct]
        random.shuffle(distractors)
        distractors = distractors[:4]

        options_raw = [correct] + distractors
        correct_index = 0
        options, correct_index = self.shuffle_options(options_raw, correct_index)

        explanation = (
            f"Una funzione è iniettiva se ogni elemento del codominio è immagine di "
            f"al più un elemento del dominio. Graficamente, si usa il "
            f"test della retta orizzontale: se ogni retta orizzontale interseca "
            f"il grafico in al più un punto, la funzione è iniettiva. "
            f"{reason}"
        )

        return {
            "question": f"Data {expr_str}, la funzione è iniettiva?",
            "graph_data": graph_svg,
            "options": options,
            "correct_index": correct_index,
            "explanation": explanation,
            "did_you_know": (
                "Il test della retta orizzontale è il metodo grafico per verificare "
                "l'iniettività: traccia rette orizzontali e verifica che ciascuna "
                "intersechi il grafico in al più un punto."
            ),
        }

    def _template_invertibility(self) -> dict:
        """La funzione è invertibile? (iniettiva + suriettiva sul codominio)."""
        catalogue = []

        # Linear: invertible (bijective R -> R)
        m = random.choice([-3, -2, -1, 1, 2, 3])
        q = random.choice([-2, -1, 0, 1, 2])
        catalogue.append((
            True,
            _linear(m, q), _expr_linear(m, q),
            (-5, 5), (-6, 6),
            f"La funzione lineare {_expr_linear(m, q)} è invertibile: "
            f"è iniettiva (strettamente monotona) e suriettiva su ℝ. "
            f"La sua inversa è x = (y{_fmt_num(-q, always_sign=True)})/{_fmt_num(m)}.",
        ))

        # Quadratic: NOT invertible (not injective on R)
        a = random.choice([-2, -1, 1, 2])
        h = random.choice([-1, 0, 1])
        k = random.choice([-2, -1, 0, 1, 2])
        yr = max(abs(k) + 5, 6)
        catalogue.append((
            False,
            _quadratic(a, h, k), _expr_quadratic(a, h, k),
            (-5, 5), (-yr, yr),
            f"La parabola {_expr_quadratic(a, h, k)} non è invertibile su tutto ℝ: "
            f"non è iniettiva (la retta orizzontale y = {_fmt_num(k + abs(a))} "
            f"interseca il grafico in due punti). "
            f"Sarebbe invertibile se restringessimo il dominio a x ≥ {_fmt_num(h)} "
            f"oppure x ≤ {_fmt_num(h)}.",
        ))

        # Exponential: invertible (its inverse is the logarithm)
        a_exp = 1
        b_exp = random.choice([2, 3])
        k_exp = 0
        catalogue.append((
            True,
            _exponential(a_exp, b_exp, k_exp), _expr_exponential(a_exp, b_exp, k_exp),
            (-3, 4), (-1, 10),
            f"La funzione esponenziale {_expr_exponential(a_exp, b_exp, k_exp)} è invertibile: "
            f"è strettamente crescente (iniettiva) e la sua immagine è (0, +∞). "
            f"La sua inversa è il logaritmo in base {_fmt_num(b_exp)}.",
        ))

        # Abs: NOT invertible
        a_abs = random.choice([1, 2])
        h_abs = random.choice([-1, 0, 1])
        k_abs = random.choice([-1, 0, 1])
        catalogue.append((
            False,
            _abs_value(a_abs, h_abs, k_abs), _expr_abs(a_abs, h_abs, k_abs),
            (-5, 5), (-5, 6),
            f"La funzione valore assoluto {_expr_abs(a_abs, h_abs, k_abs)} non è invertibile "
            f"su tutto ℝ: non è iniettiva. "
            f"Sarebbe invertibile restringendo il dominio a x ≥ {_fmt_num(h_abs)} "
            f"oppure x ≤ {_fmt_num(h_abs)}.",
        ))

        # Logarithmic: invertible (its inverse is the exponential)
        a_log = 1
        h_log = 0
        k_log = 0
        catalogue.append((
            True,
            _logarithmic(a_log, h_log, k_log), _expr_logarithmic(a_log, h_log, k_log),
            (-1, 8), (-5, 5),
            "La funzione logaritmo naturale ln(x) è invertibile: "
            "è strettamente crescente su (0, +∞) e la sua inversa è e^x.",
        ))

        # Sin: NOT invertible (periodic)
        catalogue.append((
            False,
            _sin_func(1, 1, 0, 0), _expr_sin(1, 1, 0, 0),
            (-7, 7), (-2, 2),
            "La funzione sin(x) non è invertibile su tutto ℝ: essendo periodica, "
            "non è iniettiva. Si definisce la funzione arcoseno restringendo "
            "il dominio a [-π/2, π/2].",
        ))

        choice = random.choice(catalogue)
        is_invertible, func, expr_str, x_range, y_range, reason = choice

        graph_svg = _build_svg(func, x_range, y_range, label=expr_str)

        if is_invertible:
            correct = "Sì, è invertibile"
        else:
            correct = "No, non è invertibile"

        distractors = [
            "No, non è invertibile" if is_invertible else "Sì, è invertibile",
            "Solo restringendo il dominio",
            "Sì, ma l'inversa non è una funzione",
            "Dipende dal codominio scelto",
            "Solo per x > 0",
            "Non si può determinare",
        ]
        distractors = [d for d in distractors if d != correct]
        random.shuffle(distractors)
        distractors = distractors[:4]

        options_raw = [correct] + distractors
        correct_index = 0
        options, correct_index = self.shuffle_options(options_raw, correct_index)

        explanation = (
            f"Una funzione è invertibile se è biiettiva, cioè iniettiva e suriettiva "
            f"(sul codominio considerato). "
            f"Graficamente, deve superare il test della retta orizzontale. "
            f"{reason}"
        )

        return {
            "question": f"Data {expr_str}, la funzione è invertibile (sul suo dominio naturale)?",
            "graph_data": graph_svg,
            "options": options,
            "correct_index": correct_index,
            "explanation": explanation,
            "did_you_know": (
                "Una funzione invertibile ha un'inversa f⁻¹ tale che f(f⁻¹(y)) = y e "
                "f⁻¹(f(x)) = x. Il grafico dell'inversa è il simmetrico rispetto "
                "alla retta y = x."
            ),
        }

    def _template_codomain(self) -> dict:
        """Qual è l'immagine (codominio effettivo) di f?"""
        catalogue = []

        # Linear: image = R
        m = random.choice([-3, -2, -1, 1, 2, 3])
        q = random.choice([-2, -1, 0, 1, 2])
        catalogue.append((
            "ℝ (tutti i reali)",
            _linear(m, q), _expr_linear(m, q),
            (-5, 5), (-6, 6),
            "Una funzione lineare con m ≠ 0 ha come immagine tutto ℝ: "
            "la retta si estende all'infinito in entrambe le direzioni.",
        ))

        # Quadratic a > 0: image = [k, +∞)
        a_pos = random.choice([1, 2])
        h_q = random.choice([-2, -1, 0, 1, 2])
        k_q = random.choice([-3, -2, -1, 0, 1, 2, 3])
        yr = max(abs(k_q) + 5, 6)
        catalogue.append((
            f"[{_fmt_num(k_q)}, +∞)",
            _quadratic(a_pos, h_q, k_q), _expr_quadratic(a_pos, h_q, k_q),
            (-5, 5), (-yr, yr),
            f"La parabola si apre verso l'alto con vertice in "
            f"({_fmt_num(h_q)}, {_fmt_num(k_q)}). Il valore minimo è {_fmt_num(k_q)}, "
            f"quindi l'immagine è [{_fmt_num(k_q)}, +∞).",
        ))

        # Quadratic a < 0: image = (-∞, k]
        a_neg = random.choice([-2, -1])
        h_q2 = random.choice([-2, -1, 0, 1, 2])
        k_q2 = random.choice([-3, -2, -1, 0, 1, 2, 3])
        yr2 = max(abs(k_q2) + 5, 6)
        catalogue.append((
            f"(-∞, {_fmt_num(k_q2)}]",
            _quadratic(a_neg, h_q2, k_q2), _expr_quadratic(a_neg, h_q2, k_q2),
            (-5, 5), (-yr2, yr2),
            f"La parabola si apre verso il basso con vertice in "
            f"({_fmt_num(h_q2)}, {_fmt_num(k_q2)}). Il valore massimo è {_fmt_num(k_q2)}, "
            f"quindi l'immagine è (-∞, {_fmt_num(k_q2)}].",
        ))

        # Exponential a > 0: image = (k, +∞)
        b_exp = random.choice([2, 3])
        k_exp = random.choice([-2, -1, 0, 1, 2])
        catalogue.append((
            f"({_fmt_num(k_exp)}, +∞)",
            _exponential(1, b_exp, k_exp), _expr_exponential(1, b_exp, k_exp),
            (-3, 4), (k_exp - 2, k_exp + 10),
            f"La funzione esponenziale con a > 0 ha asintoto orizzontale y = {_fmt_num(k_exp)} "
            f"e cresce verso +∞. L'immagine è ({_fmt_num(k_exp)}, +∞) — "
            f"il valore {_fmt_num(k_exp)} non viene mai raggiunto.",
        ))

        # Exponential a < 0: image = (-∞, k)
        k_exp2 = random.choice([-1, 0, 1, 2])
        catalogue.append((
            f"(-∞, {_fmt_num(k_exp2)})",
            _exponential(-1, 2, k_exp2), _expr_exponential(-1, 2, k_exp2),
            (-3, 4), (k_exp2 - 10, k_exp2 + 2),
            f"La funzione esponenziale con a < 0 ha asintoto orizzontale y = {_fmt_num(k_exp2)} "
            f"e decresce verso -∞. L'immagine è (-∞, {_fmt_num(k_exp2)}).",
        ))

        # Sqrt a > 0: image = [k, +∞)
        a_sq = random.choice([1, 2])
        h_sq = random.choice([0, 1, 2])
        k_sq = random.choice([-1, 0, 1])
        catalogue.append((
            f"[{_fmt_num(k_sq)}, +∞)",
            _sqrt_func(a_sq, h_sq, k_sq), _expr_sqrt(a_sq, h_sq, k_sq),
            (h_sq - 1, h_sq + 8), (-1, 5),
            f"La funzione radice quadrata con a > 0 parte dal valore minimo "
            f"f({_fmt_num(h_sq)}) = {_fmt_num(k_sq)} e cresce. L'immagine è [{_fmt_num(k_sq)}, +∞).",
        ))

        choice = random.choice(catalogue)
        correct, func, expr_str, x_range, y_range, reason = choice

        graph_svg = _build_svg(func, x_range, y_range, label=expr_str)

        # Build plausible distractors
        all_possible = [
            "ℝ (tutti i reali)",
            "[0, +∞)",
            "(0, +∞)",
            "(-∞, 0]",
            "(-∞, 0)",
            "[-1, +∞)",
            "(1, +∞)",
            "(-∞, 1]",
            "(-∞, 1)",
            "[-2, +∞)",
            "(2, +∞)",
            "(-∞, 2]",
            "(-∞, -1)",
            "[-3, +∞)",
            "(3, +∞)",
            "(-∞, 3]",
            "(-∞, -2]",
            "(-∞, -3]",
        ]
        distractors = [d for d in all_possible if d != correct]
        random.shuffle(distractors)
        distractors = distractors[:4]

        options_raw = [correct] + distractors
        correct_index = 0
        options, correct_index = self.shuffle_options(options_raw, correct_index)

        explanation = (
            f"L'immagine (o codominio effettivo) di una funzione è l'insieme di tutti "
            f"i valori y effettivamente assunti da f(x). {reason}"
        )

        return {
            "question": f"Qual è l'immagine (insieme dei valori) di {expr_str}?",
            "graph_data": graph_svg,
            "options": options,
            "correct_index": correct_index,
            "explanation": explanation,
            "did_you_know": (
                "L'immagine di una funzione è un sottoinsieme del codominio: "
                "comprende solo i valori y che la funzione assume effettivamente. "
                "Graficamente, è la proiezione del grafico sull'asse y."
            ),
        }

    def _template_injectivity_intervals(self) -> dict:
        """Su quali intervalli la funzione è iniettiva? (per funzioni non iniettive)."""
        catalogue = []

        # Quadratic
        a = random.choice([-2, -1, 1, 2])
        h = random.choice([-2, -1, 0, 1, 2])
        k = random.choice([-2, -1, 0, 1, 2])
        yr = max(abs(k) + 5, 6)
        catalogue.append((
            f"(-∞, {_fmt_num(h)}] oppure [{_fmt_num(h)}, +∞)",
            _quadratic(a, h, k), _expr_quadratic(a, h, k),
            (-5, 5), (-yr, yr),
            f"La parabola {_expr_quadratic(a, h, k)} ha il vertice in x = {_fmt_num(h)}. "
            f"A sinistra del vertice è strettamente monotona "
            f"({'decrescente' if a > 0 else 'crescente'}), "
            f"a destra è strettamente monotona "
            f"({'crescente' if a > 0 else 'decrescente'}). "
            f"Quindi è iniettiva su (-∞, {_fmt_num(h)}] e su [{_fmt_num(h)}, +∞).",
            h,
        ))

        # Abs value
        a_abs = random.choice([-2, -1, 1, 2])
        h_abs = random.choice([-2, -1, 0, 1, 2])
        k_abs = random.choice([-2, -1, 0, 1, 2])
        catalogue.append((
            f"(-∞, {_fmt_num(h_abs)}] oppure [{_fmt_num(h_abs)}, +∞)",
            _abs_value(a_abs, h_abs, k_abs), _expr_abs(a_abs, h_abs, k_abs),
            (-5, 5), (-5, 6),
            f"La funzione valore assoluto {_expr_abs(a_abs, h_abs, k_abs)} ha il vertice "
            f"in x = {_fmt_num(h_abs)}. A sinistra è strettamente monotona "
            f"({'decrescente' if a_abs > 0 else 'crescente'}), "
            f"a destra è strettamente monotona "
            f"({'crescente' if a_abs > 0 else 'decrescente'}). "
            f"Quindi è iniettiva su (-∞, {_fmt_num(h_abs)}] e su [{_fmt_num(h_abs)}, +∞).",
            h_abs,
        ))

        # Sin
        a_sin = random.choice([1, 2])
        b_sin = random.choice([1, 2])
        half_period = round(math.pi / b_sin, 2)
        catalogue.append((
            f"Intervalli di ampiezza π/{_fmt_num(b_sin)} (es. [-{half_period}, {half_period}])",
            _sin_func(a_sin, b_sin, 0, 0), _expr_sin(a_sin, b_sin, 0, 0),
            (-7, 7), (-4, 4),
            f"La funzione {_expr_sin(a_sin, b_sin, 0, 0)} è periodica con periodo "
            f"2π/{_fmt_num(b_sin)} ≈ {_fmt_num(round(2 * math.pi / b_sin, 2))}. "
            f"È iniettiva su ciascun intervallo di ampiezza pari a mezzo periodo, "
            f"cioè π/{_fmt_num(b_sin)} ≈ {_fmt_num(half_period)}.",
            0,
        ))

        # Cos
        a_cos = random.choice([1, 2])
        b_cos = random.choice([1, 2])
        half_period_cos = round(math.pi / b_cos, 2)
        catalogue.append((
            f"Intervalli di ampiezza π/{_fmt_num(b_cos)} (es. [0, {half_period_cos}])",
            _cos_func(a_cos, b_cos, 0, 0), _expr_cos(a_cos, b_cos, 0, 0),
            (-7, 7), (-4, 4),
            f"La funzione {_expr_cos(a_cos, b_cos, 0, 0)} è periodica con periodo "
            f"2π/{_fmt_num(b_cos)} ≈ {_fmt_num(round(2 * math.pi / b_cos, 2))}. "
            f"È iniettiva su ciascun intervallo di ampiezza pari a mezzo periodo, "
            f"cioè π/{_fmt_num(b_cos)} ≈ {_fmt_num(half_period_cos)}.",
            0,
        ))

        choice = random.choice(catalogue)
        correct, func, expr_str, x_range, y_range, reason, vertex = choice

        graph_svg = _build_svg(func, x_range, y_range, label=expr_str)

        # Build distractors
        v = vertex
        all_possible = [
            f"(-∞, {_fmt_num(v + 1)}] oppure [{_fmt_num(v + 1)}, +∞)",
            f"(-∞, {_fmt_num(v - 1)}] oppure [{_fmt_num(v - 1)}, +∞)",
            "È sempre iniettiva su tutto ℝ",
            "Non è mai iniettiva su alcun intervallo",
            f"Solo su [{_fmt_num(v)}, +∞)",
            f"Solo su (-∞, {_fmt_num(v)}]",
            f"(-∞, {_fmt_num(v + 2)}] oppure [{_fmt_num(v + 2)}, +∞)",
            "Solo per x > 0",
            "Intervalli di ampiezza 2π",
            "Intervalli di ampiezza π",
            f"Intervalli di ampiezza π/2 (es. [0, {_fmt_num(round(math.pi / 2, 2))}])",
        ]
        distractors = [d for d in all_possible if d != correct]
        random.shuffle(distractors)
        distractors = distractors[:4]

        options_raw = [correct] + distractors
        correct_index = 0
        options, correct_index = self.shuffle_options(options_raw, correct_index)

        explanation = (
            f"Una funzione non iniettiva su tutto il dominio può essere iniettiva "
            f"se ci si restringe a intervalli opportuni dove è strettamente monotona. "
            f"{reason}"
        )

        return {
            "question": f"Su quali intervalli la funzione {expr_str} è iniettiva?",
            "graph_data": graph_svg,
            "options": options,
            "correct_index": correct_index,
            "explanation": explanation,
            "did_you_know": (
                "Restringere il dominio di una funzione per renderla iniettiva è il primo "
                "passo per definire la sua funzione inversa. Ad esempio, arcsin è "
                "l'inversa di sin ristretta a [-π/2, π/2]."
            ),
        }

    # ------------------------------------------------------------------
    # Inverse templates: given a graph, answer a question about it
    # ------------------------------------------------------------------

    def _template_inverse_preimage(self) -> dict:
        """Osserva il grafico di f. Trova tutti i valori di x tali che f(x) = f(a)."""
        # Use a quadratic a(x-h)^2 + k with integer vertex
        h = random.choice([-1, 0, 1, 2])
        k = random.choice([-3, -2, -1, 0, 1, 2, 3])
        a_coeff = random.choice([-1, 1])

        func = _quadratic(a_coeff, h, k)
        expr_str = _expr_quadratic(a_coeff, h, k)

        # Pick an x-value that is NOT the vertex so there's a symmetric partner
        offset = random.choice([1, 2, 3])
        x_a = h + offset
        # The symmetric point is h - offset
        x_sym = h - offset
        y_val = func(x_a)

        x_range = (min(x_sym, h) - 3, max(x_a, h) + 3)
        yr = max(abs(k) + 5, abs(y_val) + 2, 6)
        y_range = (-yr, yr)

        graph_svg = _build_svg(func, x_range, y_range, label=expr_str)

        correct = f"x = {_fmt_num(x_sym)} e x = {_fmt_num(x_a)}"

        # Generate distractors
        distractors = [
            f"x = {_fmt_num(x_a)}",
            f"x = {_fmt_num(h)}",
            f"x = {_fmt_num(x_sym)} e x = {_fmt_num(x_a + 1)}",
            f"x = {_fmt_num(x_sym - 1)} e x = {_fmt_num(x_a + 1)}",
            f"x = {_fmt_num(h)} e x = {_fmt_num(x_a)}",
            f"x = {_fmt_num(x_sym)} e x = {_fmt_num(h)}",
        ]
        distractors = [d for d in distractors if d != correct]
        random.shuffle(distractors)
        distractors = distractors[:4]

        options_raw = [correct] + distractors
        correct_index = 0
        options, correct_index = self.shuffle_options(options_raw, correct_index)

        explanation = (
            f"La funzione {expr_str} è una parabola con vertice in ({_fmt_num(h)}, {_fmt_num(k)}). "
            f"f({_fmt_num(x_a)}) = {_fmt_num(y_val)}. Per simmetria rispetto all'asse x = {_fmt_num(h)}, "
            f"anche f({_fmt_num(x_sym)}) = {_fmt_num(y_val)}. "
            f"Quindi f(x) = f({_fmt_num(x_a)}) per x = {_fmt_num(x_sym)} e x = {_fmt_num(x_a)}."
        )

        return {
            "question": (
                f"Osserva il grafico di {expr_str}. "
                f"Trova tutti i valori di x tali che f(x) = f({_fmt_num(x_a)})."
            ),
            "graph_data": graph_svg,
            "options": options,
            "correct_index": correct_index,
            "explanation": explanation,
            "did_you_know": (
                "La preimmagine di un valore y₀ è l'insieme di tutti gli x "
                "tali che f(x) = y₀. Per una parabola, la preimmagine di ogni "
                "valore (tranne il vertice) contiene esattamente due punti simmetrici."
            ),
        }

    def _template_inverse_sign(self) -> dict:
        """Osserva il grafico. In quale intervallo f(x) < 0?"""
        # Quadratic with known integer roots: f(x) = a(x - r1)(x - r2)
        r1 = random.randint(-4, 0)
        r2 = r1 + random.randint(2, 5)
        a_coeff = random.choice([-1, 1])

        def func(x):
            return a_coeff * (x - r1) * (x - r2)

        # Standard form for display
        a_std = a_coeff
        b_std = -a_coeff * (r1 + r2)
        c_std = a_coeff * r1 * r2
        expr_str = _expr_quadratic_standard(a_std, b_std, c_std)

        x_range = (min(r1, r2) - 3, max(r1, r2) + 3)
        # Compute vertex y-value for range
        vertex_x = (r1 + r2) / 2
        vertex_y = func(vertex_x)
        yr = max(abs(vertex_y) + 2, 6)
        y_range = (-yr, yr)

        graph_svg = _build_svg(func, x_range, y_range, label=expr_str)

        if a_coeff > 0:
            # f(x) < 0 between the roots
            correct = f"({_fmt_num(r1)}, {_fmt_num(r2)})"
            distractors = [
                f"(-∞, {_fmt_num(r1)}) ∪ ({_fmt_num(r2)}, +∞)",
                f"[{_fmt_num(r1)}, {_fmt_num(r2)}]",
                f"(-∞, {_fmt_num(r1)})",
                f"({_fmt_num(r2)}, +∞)",
                f"(-∞, {_fmt_num(r1 - 1)}) ∪ ({_fmt_num(r2 + 1)}, +∞)",
                f"({_fmt_num(r1 - 1)}, {_fmt_num(r2 + 1)})",
            ]
        else:
            # f(x) < 0 outside the roots
            correct = f"(-∞, {_fmt_num(r1)}) ∪ ({_fmt_num(r2)}, +∞)"
            distractors = [
                f"({_fmt_num(r1)}, {_fmt_num(r2)})",
                f"[{_fmt_num(r1)}, {_fmt_num(r2)}]",
                f"(-∞, {_fmt_num(r1)})",
                f"({_fmt_num(r2)}, +∞)",
                f"(-∞, {_fmt_num(r1 - 1)}) ∪ ({_fmt_num(r2 + 1)}, +∞)",
                f"({_fmt_num(r1 + 1)}, {_fmt_num(r2 - 1)})",
            ]

        distractors = [d for d in distractors if d != correct]
        random.shuffle(distractors)
        distractors = distractors[:4]

        options_raw = [correct] + distractors
        correct_index = 0
        options, correct_index = self.shuffle_options(options_raw, correct_index)

        direction = "verso l'alto" if a_coeff > 0 else "verso il basso"
        explanation = (
            f"La parabola {expr_str} ha radici x = {_fmt_num(r1)} e x = {_fmt_num(r2)}, "
            f"con apertura {direction}. "
        )
        if a_coeff > 0:
            explanation += (
                f"Una parabola rivolta verso l'alto è negativa tra le radici: "
                f"f(x) < 0 per x ∈ ({_fmt_num(r1)}, {_fmt_num(r2)})."
            )
        else:
            explanation += (
                f"Una parabola rivolta verso il basso è negativa fuori dalle radici: "
                f"f(x) < 0 per x ∈ (-∞, {_fmt_num(r1)}) ∪ ({_fmt_num(r2)}, +∞)."
            )

        return {
            "question": f"Osserva il grafico di {expr_str}. In quale intervallo f(x) < 0?",
            "graph_data": graph_svg,
            "options": options,
            "correct_index": correct_index,
            "explanation": explanation,
            "did_you_know": (
                "Lo studio del segno di una funzione è fondamentale per risolvere "
                "disequazioni. Il grafico rende immediato capire dove la funzione "
                "è positiva (sopra l'asse x) o negativa (sotto l'asse x)."
            ),
        }

    def _template_inverse_increasing(self) -> dict:
        """Osserva il grafico. In quale intervallo f è crescente?"""
        h = random.choice([-2, -1, 0, 1, 2])
        k = random.choice([-3, -2, -1, 0, 1, 2, 3])
        a_coeff = random.choice([-1, 1])

        func = _quadratic(a_coeff, h, k)
        expr_str = _expr_quadratic(a_coeff, h, k)

        x_range = (h - 5, h + 5)
        yr = max(abs(k) + 5, 6)
        y_range = (-yr, yr)

        graph_svg = _build_svg(func, x_range, y_range, label=expr_str)

        if a_coeff > 0:
            # Parabola up: increasing on (h, +∞)
            correct = f"({_fmt_num(h)}, +∞)"
            distractors = [
                f"(-∞, {_fmt_num(h)})",
                f"({_fmt_num(h - 1)}, +∞)",
                f"(-∞, {_fmt_num(h + 1)})",
                "(-∞, +∞)",
                f"[{_fmt_num(h)}, +∞)",
                f"({_fmt_num(h + 1)}, +∞)",
            ]
        else:
            # Parabola down: increasing on (-∞, h)
            correct = f"(-∞, {_fmt_num(h)})"
            distractors = [
                f"({_fmt_num(h)}, +∞)",
                f"(-∞, {_fmt_num(h + 1)})",
                f"(-∞, {_fmt_num(h - 1)})",
                "(-∞, +∞)",
                f"(-∞, {_fmt_num(h)}]",
                f"({_fmt_num(h - 1)}, +∞)",
            ]

        distractors = [d for d in distractors if d != correct]
        random.shuffle(distractors)
        distractors = distractors[:4]

        options_raw = [correct] + distractors
        correct_index = 0
        options, correct_index = self.shuffle_options(options_raw, correct_index)

        direction = "verso l'alto" if a_coeff > 0 else "verso il basso"
        explanation = (
            f"La parabola {expr_str} ha vertice in ({_fmt_num(h)}, {_fmt_num(k)}) "
            f"con apertura {direction}. "
        )
        if a_coeff > 0:
            explanation += (
                f"Una parabola rivolta verso l'alto è crescente a destra del vertice: "
                f"f è crescente per x ∈ ({_fmt_num(h)}, +∞)."
            )
        else:
            explanation += (
                f"Una parabola rivolta verso il basso è crescente a sinistra del vertice: "
                f"f è crescente per x ∈ (-∞, {_fmt_num(h)})."
            )

        return {
            "question": f"Osserva il grafico di {expr_str}. In quale intervallo f è crescente?",
            "graph_data": graph_svg,
            "options": options,
            "correct_index": correct_index,
            "explanation": explanation,
            "did_you_know": (
                "Una funzione è crescente in un intervallo se, presi due punti "
                "qualsiasi x₁ < x₂ nell'intervallo, si ha f(x₁) < f(x₂). "
                "Graficamente, il grafico 'sale' da sinistra a destra."
            ),
        }

    def _template_inverse_max_min(self) -> dict:
        """Osserva il grafico. Qual è il valore massimo (o minimo) di f nell'intervallo [a, b]?"""
        h = random.choice([-2, -1, 0, 1, 2])
        k = random.choice([-3, -2, -1, 0, 1, 2, 3])
        a_coeff = random.choice([-1, 1])

        func = _quadratic(a_coeff, h, k)
        expr_str = _expr_quadratic(a_coeff, h, k)

        # Interval containing the vertex
        margin = random.choice([2, 3, 4])
        interval_a = h - margin
        interval_b = h + margin

        x_range = (interval_a - 2, interval_b + 2)
        # Compute values at interval endpoints and vertex
        val_left = func(interval_a)
        val_right = func(interval_b)
        val_vertex = k

        if a_coeff > 0:
            # Parabola up: min at vertex
            extreme_type = "minimo"
            correct_val = val_vertex
        else:
            # Parabola down: max at vertex
            extreme_type = "massimo"
            correct_val = val_vertex

        yr = max(abs(val_left) + 2, abs(val_right) + 2, abs(val_vertex) + 2, 6)
        y_range = (-yr, yr)

        graph_svg = _build_svg(func, x_range, y_range, label=expr_str)

        correct = _fmt_num(correct_val)

        # Generate numeric distractors
        distractor_vals = set()
        distractor_vals.add(int(val_left))
        distractor_vals.add(int(val_right))
        for delta in [-2, -1, 1, 2]:
            distractor_vals.add(int(correct_val) + delta)
        distractor_vals.discard(int(correct_val))
        distractors = [_fmt_num(v) for v in sorted(distractor_vals)]
        distractors = [d for d in distractors if d != correct]
        random.shuffle(distractors)
        distractors = distractors[:4]

        # Ensure we have 4 distractors
        fallback = -10
        while len(distractors) < 4:
            d = _fmt_num(fallback)
            if d != correct and d not in distractors:
                distractors.append(d)
            fallback += 1

        options_raw = [correct] + distractors
        correct_index = 0
        options, correct_index = self.shuffle_options(options_raw, correct_index)

        explanation = (
            f"La parabola {expr_str} ha vertice in ({_fmt_num(h)}, {_fmt_num(k)}). "
            f"Nell'intervallo [{_fmt_num(interval_a)}, {_fmt_num(interval_b)}], "
            f"il vertice è contenuto, quindi il valore {extreme_type} è {correct}."
        )

        return {
            "question": (
                f"Osserva il grafico di {expr_str}. "
                f"Qual è il valore {extreme_type} di f "
                f"nell'intervallo [{_fmt_num(interval_a)}, {_fmt_num(interval_b)}]?"
            ),
            "graph_data": graph_svg,
            "options": options,
            "correct_index": correct_index,
            "explanation": explanation,
            "did_you_know": (
                "Il teorema di Weierstrass garantisce che una funzione continua "
                "su un intervallo chiuso e limitato [a, b] ammette sempre un "
                "massimo e un minimo assoluti."
            ),
        }

    def _template_inverse_range(self) -> dict:
        """Osserva il grafico. Qual è il codominio (immagine) di f?"""
        variant = random.choice(["quadratic_up", "quadratic_down", "sin"])

        if variant == "quadratic_up":
            h = random.choice([-2, -1, 0, 1, 2])
            k = random.choice([-3, -2, -1, 0, 1, 2, 3])
            func = _quadratic(1, h, k)
            expr_str = _expr_quadratic(1, h, k)
            x_range = (h - 5, h + 5)
            yr = max(abs(k) + 8, 10)
            y_range = (-yr + k, yr + k)
            correct = f"[{_fmt_num(k)}, +∞)"
            distractors = [
                f"({_fmt_num(k)}, +∞)",
                f"(-∞, {_fmt_num(k)}]",
                "(-∞, +∞)",
                f"[{_fmt_num(k - 1)}, +∞)",
                f"[{_fmt_num(k + 1)}, +∞)",
                f"[0, +∞)",
            ]
        elif variant == "quadratic_down":
            h = random.choice([-2, -1, 0, 1, 2])
            k = random.choice([-3, -2, -1, 0, 1, 2, 3])
            func = _quadratic(-1, h, k)
            expr_str = _expr_quadratic(-1, h, k)
            x_range = (h - 5, h + 5)
            yr = max(abs(k) + 8, 10)
            y_range = (-yr + k, yr + k)
            correct = f"(-∞, {_fmt_num(k)}]"
            distractors = [
                f"(-∞, {_fmt_num(k)})",
                f"[{_fmt_num(k)}, +∞)",
                "(-∞, +∞)",
                f"(-∞, {_fmt_num(k + 1)}]",
                f"(-∞, {_fmt_num(k - 1)}]",
                f"(-∞, 0]",
            ]
        else:  # sin
            a_sin = random.choice([1, 2, 3])
            k_sin = random.choice([-2, -1, 0, 1, 2])
            func = _sin_func(a_sin, 1, 0, k_sin)
            expr_str = _expr_sin(a_sin, 1, 0, k_sin)
            x_range = (-7, 7)
            y_range = (-a_sin - abs(k_sin) - 2, a_sin + abs(k_sin) + 2)
            lo = k_sin - a_sin
            hi = k_sin + a_sin
            correct = f"[{_fmt_num(lo)}, {_fmt_num(hi)}]"
            k = k_sin  # for distractors
            distractors = [
                f"({_fmt_num(lo)}, {_fmt_num(hi)})",
                f"[{_fmt_num(lo - 1)}, {_fmt_num(hi + 1)}]",
                "(-∞, +∞)",
                f"[-{_fmt_num(a_sin)}, {_fmt_num(a_sin)}]",
                f"[{_fmt_num(lo + 1)}, {_fmt_num(hi - 1)}]" if a_sin > 1 else f"[0, {_fmt_num(hi)}]",
                f"[{_fmt_num(lo)}, {_fmt_num(hi + 1)}]",
            ]

        graph_svg = _build_svg(func, x_range, y_range, label=expr_str)

        distractors = [d for d in distractors if d != correct]
        random.shuffle(distractors)
        distractors = distractors[:4]

        options_raw = [correct] + distractors
        correct_index = 0
        options, correct_index = self.shuffle_options(options_raw, correct_index)

        explanation = (
            f"L'immagine (codominio effettivo) di {expr_str} è l'insieme di tutti "
            f"i valori y che la funzione assume. "
            f"Osservando il grafico, i valori di y coprono l'intervallo {correct}."
        )

        return {
            "question": f"Osserva il grafico di {expr_str}. Qual è il codominio (immagine) di f?",
            "graph_data": graph_svg,
            "options": options,
            "correct_index": correct_index,
            "explanation": explanation,
            "did_you_know": (
                "L'immagine di una funzione è il sottoinsieme del codominio "
                "effettivamente raggiunto dalla funzione. Per una parabola y = x² "
                "l'immagine è [0, +∞), non tutto ℝ."
            ),
        }

    def _template_inverse_intersections(self) -> dict:
        """Osserva il grafico. Quante soluzioni ha l'equazione f(x) = k?"""
        variant = random.choice(["quadratic", "cubic"])

        if variant == "quadratic":
            h = random.choice([-2, -1, 0, 1, 2])
            v_k = random.choice([-3, -2, -1, 0, 1, 2, 3])
            a_coeff = random.choice([-1, 1])
            func = _quadratic(a_coeff, h, v_k)
            expr_str = _expr_quadratic(a_coeff, h, v_k)

            x_range = (h - 5, h + 5)
            yr = max(abs(v_k) + 6, 8)
            y_range = (-yr, yr)

            # Choose k value to get a known number of intersections
            case = random.choice(["zero", "one", "two"])
            if a_coeff > 0:
                if case == "zero":
                    k_line = v_k - random.randint(1, 3)
                    n_solutions = 0
                elif case == "one":
                    k_line = v_k
                    n_solutions = 1
                else:
                    k_line = v_k + random.randint(1, 4)
                    n_solutions = 2
            else:
                if case == "zero":
                    k_line = v_k + random.randint(1, 3)
                    n_solutions = 0
                elif case == "one":
                    k_line = v_k
                    n_solutions = 1
                else:
                    k_line = v_k - random.randint(1, 4)
                    n_solutions = 2
        else:
            # Cubic: f(x) = (x - r1)(x - r2)(x - r3) for 3 distinct roots
            roots = sorted(random.sample(range(-3, 4), 3))
            r1, r2, r3 = roots

            def func(x):
                return (x - r1) * (x - r2) * (x - r3)

            expr_str = f"f(x) = (x{_fmt_num(-r1, always_sign=True)})(x{_fmt_num(-r2, always_sign=True)})(x{_fmt_num(-r3, always_sign=True)})"

            x_range = (r1 - 2, r3 + 2)
            # Evaluate at some points for y_range
            test_vals = [func(x) for x in range(r1 - 2, r3 + 3)]
            yr = max(abs(min(test_vals)), abs(max(test_vals)), 6) + 2
            y_range = (-yr, yr)

            # Choose k for 1 or 3 intersections
            case = random.choice(["one", "three"])
            if case == "three":
                # k=0 gives exactly 3 solutions (the roots)
                k_line = 0
                n_solutions = 3
            else:
                # k large enough to have only 1 intersection
                k_line = int(yr) - 1
                if k_line == 0:
                    k_line = int(yr)
                n_solutions = 1

        graph_svg = _build_svg(func, x_range, y_range, label=expr_str)

        # Add horizontal line for y=k
        ox_start, oy_k = _world_to_svg(x_range[0], k_line, x_range, y_range)
        ox_end, _ = _world_to_svg(x_range[1], k_line, x_range, y_range)
        line_svg = (
            f'<line x1="{ox_start:.1f}" y1="{oy_k:.1f}" '
            f'x2="{ox_end:.1f}" y2="{oy_k:.1f}" '
            f'stroke="#dc2626" stroke-width="1" stroke-dasharray="4,4"/>'
        )
        label_svg = (
            f'<text x="{ox_end - 5:.1f}" y="{oy_k - 5:.1f}" '
            f'font-size="9" fill="#dc2626" text-anchor="end">y = {_fmt_num(k_line)}</text>'
        )
        graph_svg = graph_svg.replace("</svg>", f"{line_svg}{label_svg}</svg>")

        correct = str(n_solutions)
        all_options = ["0", "1", "2", "3", "4"]
        distractors = [o for o in all_options if o != correct]
        random.shuffle(distractors)
        distractors = distractors[:4]

        options_raw = [correct] + distractors
        correct_index = 0
        options, correct_index = self.shuffle_options(options_raw, correct_index)

        explanation = (
            f"Per trovare le soluzioni di f(x) = {_fmt_num(k_line)}, si traccia la retta "
            f"orizzontale y = {_fmt_num(k_line)} e si contano le intersezioni con il grafico. "
            f"In questo caso le intersezioni sono {n_solutions}."
        )

        return {
            "question": (
                f"Osserva il grafico di {expr_str}. "
                f"Quante soluzioni ha l'equazione f(x) = {_fmt_num(k_line)}?"
            ),
            "graph_data": graph_svg,
            "options": options,
            "correct_index": correct_index,
            "explanation": explanation,
            "did_you_know": (
                "Il numero di soluzioni di f(x) = k corrisponde al numero di "
                "intersezioni tra il grafico di f e la retta orizzontale y = k. "
                "Questo è il principio alla base del test della retta orizzontale "
                "per l'iniettività."
            ),
        }

    # ------------------------------------------------------------------
    # Multiple-representation templates
    # ------------------------------------------------------------------

    # -- Table → Formula ---------------------------------------------------

    def _template_table_to_formula_L1(self) -> dict:
        """L1: linear/quadratic table → identify the formula."""
        variant = random.choice(["linear", "quadratic"])

        if variant == "linear":
            m = random.choice([-3, -2, -1, 1, 2, 3])
            q = random.choice([-4, -3, -2, -1, 0, 1, 2, 3, 4])
            xs = list(range(-2, 4))
            ys = [m * x + q for x in xs]
            correct_expr = _expr_linear(m, q)
            family = "linear"
            hint = f"La tabella mostra una relazione lineare con pendenza {_fmt_num(m)} e intercetta {_fmt_num(q)}."
            distractor_params = [
                _expr_linear(-m, q),
                _expr_linear(m, -q),
                _expr_linear(m + 1, q),
                _expr_linear(m, q + 1),
                _expr_linear(m - 1, q - 1),
                _expr_quadratic(1, 0, q),
            ]
        else:
            a = random.choice([-2, -1, 1, 2])
            c = random.choice([-3, -2, -1, 0, 1, 2, 3])
            xs = list(range(-2, 4))
            ys = [a * x * x + c for x in xs]
            correct_expr = _expr_quadratic_standard(a, 0, c)
            family = "quadratic"
            hint = f"La tabella corrisponde a una parabola f(x) = {_fmt_num(a)}x² {_fmt_num(c, always_sign=True)}."
            distractor_params = [
                _expr_quadratic_standard(-a, 0, c),
                _expr_quadratic_standard(a, 0, -c),
                _expr_quadratic_standard(a, 1, c),
                _expr_quadratic_standard(a + 1, 0, c),
                _expr_linear(a, c),
                _expr_quadratic_standard(a, -1, c),
            ]

        # Build table HTML
        header = "".join(f"<th>{x}</th>" for x in xs)
        values = "".join(f"<td>{_fmt_num(y)}</td>" for y in ys)
        table_html = (
            f'<table class="exercise-table" style="border-collapse:collapse;text-align:center;margin:10px auto">'
            f'<tr style="border-bottom:2px solid #333"><th>x</th>{header}</tr>'
            f'<tr><th>f(x)</th>{values}</tr></table>'
        )

        distractors = [d for d in distractor_params if d != correct_expr]
        seen = {correct_expr}
        unique_distractors = []
        for d in distractors:
            if d not in seen:
                seen.add(d)
                unique_distractors.append(d)
        while len(unique_distractors) < 4:
            fam = random.choice(["linear", "quadratic"])
            spec = _make_spec(fam, transformed=True)
            expr_cand = spec[1]
            if expr_cand not in seen:
                seen.add(expr_cand)
                unique_distractors.append(expr_cand)
        unique_distractors = unique_distractors[:4]

        options_raw = [correct_expr] + unique_distractors
        correct_index = 0
        options, correct_index = self.shuffle_options(options_raw, correct_index)

        explanation = (
            f"{hint} Sostituendo i valori di x nella formula {correct_expr} "
            f"si ottengono esattamente i valori della tabella."
        )
        return {
            "question": f"Osserva la tabella seguente:\n{table_html}\nQuale funzione genera questa tabella?",
            "graph_data": "",
            "options": options,
            "correct_index": correct_index,
            "explanation": explanation,
            "did_you_know": "Per riconoscere una funzione da una tabella, controlla se le differenze prime (lineare) o le differenze seconde (quadratica) sono costanti.",
            "difficulty": 1,
        }

    def _template_table_to_formula_L2(self) -> dict:
        """L2: exponential/logarithmic table → identify the formula."""
        variant = random.choice(["exponential", "logarithmic"])

        if variant == "exponential":
            b = random.choice([2, 3])
            a = random.choice([-1, 1])
            k = random.choice([-1, 0, 1])
            xs = list(range(-1, 5))
            func = _exponential(a, b, k)
            ys = [func(x) for x in xs]
            correct_expr = _expr_exponential(a, b, k)
            hint = f"I valori crescono (o decrescono) in modo esponenziale con base {_fmt_num(b)}."
            distractor_params = [
                _expr_exponential(a, b + 1, k),
                _expr_exponential(-a, b, k),
                _expr_exponential(a, b, k + 1),
                _expr_linear(b, k),
                _expr_exponential(a, b, -k) if k != 0 else _expr_exponential(a, b, 2),
                _expr_quadratic_standard(a, 0, k),
            ]
        else:
            a = random.choice([-1, 1])
            k = random.choice([-1, 0, 1])
            xs = [1, 2, 3, 4, 5, 6]
            func = _logarithmic(a, 0, k)
            ys = [round(func(x), 2) for x in xs]
            correct_expr = _expr_logarithmic(a, 0, k)
            hint = f"I valori crescono logaritmicamente."
            distractor_params = [
                _expr_logarithmic(-a, 0, k),
                _expr_logarithmic(a, 0, k + 1),
                _expr_logarithmic(a, 1, k),
                _expr_exponential(1, 2, k),
                _expr_linear(1, k),
                _expr_logarithmic(a, 0, -k) if k != 0 else _expr_logarithmic(a, 0, 2),
            ]

        # format y values for display
        y_strs = []
        for y in ys:
            if y is not None and y == int(y):
                y_strs.append(str(int(y)))
            elif y is not None:
                y_strs.append(f"{y:.2f}")
            else:
                y_strs.append("N/D")

        header = "".join(f"<th>{x}</th>" for x in xs)
        values = "".join(f"<td>{ys}</td>" for ys in y_strs)
        table_html = (
            f'<table class="exercise-table" style="border-collapse:collapse;text-align:center;margin:10px auto">'
            f'<tr style="border-bottom:2px solid #333"><th>x</th>{header}</tr>'
            f'<tr><th>f(x)</th>{values}</tr></table>'
        )

        distractors = [d for d in distractor_params if d != correct_expr]
        seen = {correct_expr}
        unique_distractors = []
        for d in distractors:
            if d not in seen:
                seen.add(d)
                unique_distractors.append(d)
        while len(unique_distractors) < 4:
            fam = random.choice(_ALL_FAMILIES)
            spec = _make_spec(fam, transformed=True)
            if spec[1] not in seen:
                seen.add(spec[1])
                unique_distractors.append(spec[1])
        unique_distractors = unique_distractors[:4]

        options_raw = [correct_expr] + unique_distractors
        correct_index = 0
        options, correct_index = self.shuffle_options(options_raw, correct_index)

        explanation = (
            f"{hint} La formula corretta è {correct_expr}. "
            f"Verificando: sostituendo i valori di x si ottengono i valori della tabella."
        )
        return {
            "question": f"Osserva la tabella seguente:\n{table_html}\nQuale funzione genera questa tabella?",
            "graph_data": "",
            "options": options,
            "correct_index": correct_index,
            "explanation": explanation,
            "did_you_know": "Per le funzioni esponenziali, il rapporto tra valori consecutivi è costante. Per quelle logaritmiche, i valori crescono sempre più lentamente.",
            "difficulty": 2,
        }

    def _template_table_to_formula_L3(self) -> dict:
        """L3: ambiguous tables requiring reasoning to distinguish families."""
        # Use functions that look similar over small ranges
        variant = random.choice(["quad_vs_exp", "linear_vs_log"])

        if variant == "quad_vs_exp":
            # Quadratic that looks like exponential for small positive x
            a = random.choice([1, 2])
            c = random.choice([0, 1])
            xs = [0, 1, 2, 3, 4, 5]
            quad_func = lambda x, _a=a, _c=c: _a * x * x + _c
            ys = [quad_func(x) for x in xs]
            correct_expr = _expr_quadratic_standard(a, 0, c)

            # Exponential distractor that fits first few points approximately
            b_exp = 2
            distractor_params = [
                _expr_exponential(1, b_exp, 0),
                _expr_quadratic_standard(-a, 0, c),
                _expr_quadratic_standard(a, 1, c),
                _expr_linear(a * 5, c),
                _expr_exponential(1, 3, 0),
                _expr_quadratic_standard(a + 1, 0, c),
            ]
            hint = (
                f"Attenzione: per x piccoli, x² e 2^x danno valori simili. "
                f"La differenza seconda costante (= {_fmt_num(2 * a)}) conferma che è quadratica."
            )
        else:
            # Linear vs log: use points where ln(x) is close to linear
            m = 1
            q = 0
            xs = [1, 2, 3, 4, 5, 6]
            lin_func = lambda x, _m=m, _q=q: _m * x + _q
            ys = [lin_func(x) for x in xs]
            correct_expr = _expr_linear(m, q)

            distractor_params = [
                _expr_logarithmic(1, 0, 0),
                _expr_linear(-m, q),
                _expr_linear(m, q + 1),
                _expr_exponential(1, 2, 0),
                _expr_linear(m + 1, q),
                _expr_quadratic_standard(1, 0, 0),
            ]
            hint = (
                f"Le differenze prime costanti confermano che si tratta di una funzione lineare, "
                f"non logaritmica."
            )

        header = "".join(f"<th>{x}</th>" for x in xs)
        values_row = "".join(f"<td>{_fmt_num(y)}</td>" for y in ys)
        table_html = (
            f'<table class="exercise-table" style="border-collapse:collapse;text-align:center;margin:10px auto">'
            f'<tr style="border-bottom:2px solid #333"><th>x</th>{header}</tr>'
            f'<tr><th>f(x)</th>{values_row}</tr></table>'
        )

        distractors = [d for d in distractor_params if d != correct_expr]
        seen = {correct_expr}
        unique_distractors = []
        for d in distractors:
            if d not in seen:
                seen.add(d)
                unique_distractors.append(d)
        while len(unique_distractors) < 4:
            fam = random.choice(_ALL_FAMILIES)
            spec = _make_spec(fam, transformed=True, complex_transforms=True)
            if spec[1] not in seen:
                seen.add(spec[1])
                unique_distractors.append(spec[1])
        unique_distractors = unique_distractors[:4]

        options_raw = [correct_expr] + unique_distractors
        correct_index = 0
        options, correct_index = self.shuffle_options(options_raw, correct_index)

        explanation = (
            f"{hint} La formula corretta è {correct_expr}."
        )
        return {
            "question": f"Osserva attentamente la tabella:\n{table_html}\nQuale funzione genera esattamente questa tabella?",
            "graph_data": "",
            "options": options,
            "correct_index": correct_index,
            "explanation": explanation,
            "did_you_know": "Per distinguere famiglie di funzioni da una tabella: differenze prime costanti → lineare; differenze seconde costanti → quadratica; rapporti costanti → esponenziale.",
            "difficulty": 3,
        }

    # -- Table → Graph -----------------------------------------------------

    def _template_table_to_graph_L2(self) -> dict:
        """L2: given a table, pick the correct graph among 5."""
        family = random.choice(["linear", "quadratic"])

        if family == "linear":
            m = random.choice([-2, -1, 1, 2, 3])
            q = random.choice([-3, -2, -1, 0, 1, 2, 3])
            xs = list(range(-2, 4))
            func = _linear(m, q)
            ys = [func(x) for x in xs]
            correct_spec = (func, _expr_linear(m, q), "lineare", "", (-5, 5), (-8, 8))
            distractor_families = [
                lambda: _make_spec("linear", transformed=True),
                lambda: _make_spec("quadratic", transformed=False),
                lambda: _make_spec("linear", transformed=True),
                lambda: _make_spec("abs", transformed=False),
            ]
        else:
            a = random.choice([-1, 1, 2])
            h = random.choice([-1, 0, 1])
            k = random.choice([-2, -1, 0, 1, 2])
            xs = list(range(-2, 4))
            func = _quadratic(a, h, k)
            ys = [func(x) for x in xs]
            yr = max(abs(k) + 5, 6)
            correct_spec = (func, _expr_quadratic(a, h, k), "quadratica", "", (-5, 5), (-yr, yr))
            distractor_families = [
                lambda: _make_spec("quadratic", transformed=True),
                lambda: _make_spec("abs", transformed=False),
                lambda: _make_spec("quadratic", transformed=True),
                lambda: _make_spec("linear", transformed=True),
            ]

        y_strs = [_fmt_num(y) for y in ys]
        header = "".join(f"<th>{x}</th>" for x in xs)
        values_row = "".join(f"<td>{ys}</td>" for ys in y_strs)
        table_html = (
            f'<table class="exercise-table" style="border-collapse:collapse;text-align:center;margin:10px auto">'
            f'<tr style="border-bottom:2px solid #333"><th>x</th>{header}</tr>'
            f'<tr><th>f(x)</th>{values_row}</tr></table>'
        )

        colors = ["#2563eb", "#dc2626", "#16a34a", "#9333ea", "#f59e0b"]
        random.shuffle(colors)

        correct_svg = _build_svg(correct_spec[0], correct_spec[4], correct_spec[5], color=colors[0])

        distractor_svgs = []
        seen_exprs = {correct_spec[1]}
        for i, gen in enumerate(distractor_families):
            attempts = 0
            while attempts < 10:
                spec = gen()
                if spec[1] not in seen_exprs:
                    seen_exprs.add(spec[1])
                    svg = _build_svg(spec[0], spec[4], spec[5], color=colors[(i + 1) % len(colors)])
                    distractor_svgs.append(svg)
                    break
                attempts += 1
            else:
                spec = _make_spec(random.choice(_ALL_FAMILIES), transformed=True)
                svg = _build_svg(spec[0], spec[4], spec[5], color=colors[(i + 1) % len(colors)])
                distractor_svgs.append(svg)

        options_raw = [correct_svg] + distractor_svgs[:4]
        correct_index = 0
        options, correct_index = self.shuffle_options(options_raw, correct_index)

        explanation = (
            f"Sostituendo i valori dalla tabella nel grafico corretto, "
            f"i punti ({', '.join(f'({x},{y})' for x, y in zip(xs, y_strs))}) "
            f"devono giacere sulla curva."
        )
        return {
            "question": f"Osserva la tabella:\n{table_html}\nQuale grafico corrisponde a questi valori?",
            "graph_data": "",
            "options": options,
            "correct_index": correct_index,
            "explanation": explanation,
            "did_you_know": "Per verificare se un grafico corrisponde a una tabella, controlla che tutti i punti (x, f(x)) della tabella giacciano sulla curva.",
            "difficulty": 2,
        }

    def _template_table_to_graph_L3(self) -> dict:
        """L3: harder table-to-graph with exponential/log families."""
        family = random.choice(["exponential", "logarithmic"])

        if family == "exponential":
            a = random.choice([1, -1])
            b = random.choice([2, 3])
            k = random.choice([-1, 0, 1])
            xs = list(range(-1, 5))
            func = _exponential(a, b, k)
            ys = [func(x) for x in xs]
            correct_spec = (func, _expr_exponential(a, b, k), "esponenziale", "", (-3, 5), (-5, 15))
            distractor_gens = [
                lambda: _make_spec("exponential", transformed=True),
                lambda: _make_spec("quadratic", transformed=True),
                lambda: _make_spec("logarithmic", transformed=False),
                lambda: _make_spec("exponential", transformed=True),
            ]
        else:
            a = random.choice([1, -1])
            k = random.choice([-1, 0, 1])
            xs = [1, 2, 3, 4, 5, 6]
            func = _logarithmic(a, 0, k)
            ys = [round(func(x), 2) for x in xs]
            correct_spec = (func, _expr_logarithmic(a, 0, k), "logaritmica", "", (-1, 8), (-5, 5))
            distractor_gens = [
                lambda: _make_spec("logarithmic", transformed=True),
                lambda: _make_spec("exponential", transformed=False),
                lambda: _make_spec("sqrt", transformed=False) if hasattr(_make_spec, '__call__') else _make_spec("linear", transformed=True),
                lambda: _make_spec("logarithmic", transformed=True),
            ]

        y_strs = []
        for y in ys:
            if y is not None and y == int(y):
                y_strs.append(str(int(y)))
            elif y is not None:
                y_strs.append(f"{y:.2f}")
            else:
                y_strs.append("N/D")

        header = "".join(f"<th>{x}</th>" for x in xs)
        values_row = "".join(f"<td>{ys}</td>" for ys in y_strs)
        table_html = (
            f'<table class="exercise-table" style="border-collapse:collapse;text-align:center;margin:10px auto">'
            f'<tr style="border-bottom:2px solid #333"><th>x</th>{header}</tr>'
            f'<tr><th>f(x)</th>{values_row}</tr></table>'
        )

        colors = ["#2563eb", "#dc2626", "#16a34a", "#9333ea", "#f59e0b"]
        random.shuffle(colors)

        correct_svg = _build_svg(correct_spec[0], correct_spec[4], correct_spec[5], color=colors[0])

        distractor_svgs = []
        seen_exprs = {correct_spec[1]}
        for i, gen in enumerate(distractor_gens):
            attempts = 0
            while attempts < 10:
                spec = gen()
                if spec[1] not in seen_exprs:
                    seen_exprs.add(spec[1])
                    svg = _build_svg(spec[0], spec[4], spec[5], color=colors[(i + 1) % len(colors)])
                    distractor_svgs.append(svg)
                    break
                attempts += 1
            else:
                spec = _make_spec(random.choice(_ALL_FAMILIES), transformed=True)
                svg = _build_svg(spec[0], spec[4], spec[5], color=colors[(i + 1) % len(colors)])
                distractor_svgs.append(svg)

        options_raw = [correct_svg] + distractor_svgs[:4]
        correct_index = 0
        options, correct_index = self.shuffle_options(options_raw, correct_index)

        explanation = (
            f"I punti della tabella corrispondono alla funzione {correct_spec[1]}. "
            f"Il grafico corretto deve passare per tutti i punti indicati."
        )
        return {
            "question": f"Osserva la tabella:\n{table_html}\nQuale grafico corrisponde a questi valori?",
            "graph_data": "",
            "options": options,
            "correct_index": correct_index,
            "explanation": explanation,
            "did_you_know": "Le funzioni esponenziali crescono molto più rapidamente delle quadratiche per x grande, mentre le logaritmiche crescono molto più lentamente delle lineari.",
            "difficulty": 3,
        }

    # -- Verbal → Formula --------------------------------------------------

    def _template_verbal_to_formula_L1(self) -> dict:
        """L1: simple verbal descriptions → identify the formula."""
        descriptions = [
            {
                "text": "Una funzione che raddoppia il suo valore ogni volta che x aumenta di 1",
                "correct": _expr_exponential(1, 2, 0),
                "distractors": [
                    _expr_linear(2, 0),
                    _expr_quadratic_standard(2, 0, 0),
                    _expr_exponential(1, 3, 0),
                    _expr_exponential(2, 2, 0),
                    _expr_linear(1, 2),
                ],
                "hint": "Se f(x+1) = 2·f(x) e f(0)=1, allora f(x) = 2^x.",
            },
            {
                "text": "Una funzione che triplica il suo valore ogni volta che x aumenta di 1",
                "correct": _expr_exponential(1, 3, 0),
                "distractors": [
                    _expr_linear(3, 0),
                    _expr_quadratic_standard(3, 0, 0),
                    _expr_exponential(1, 2, 0),
                    _expr_exponential(3, 3, 0),
                    _expr_linear(1, 3),
                ],
                "hint": "Se f(x+1) = 3·f(x) e f(0)=1, allora f(x) = 3^x.",
            },
            {
                "text": "Una funzione il cui valore aumenta di 3 unità per ogni aumento unitario di x",
                "correct": _expr_linear(3, 0),
                "distractors": [
                    _expr_linear(2, 0),
                    _expr_exponential(1, 3, 0),
                    _expr_linear(3, 1),
                    _expr_linear(-3, 0),
                    _expr_quadratic_standard(3, 0, 0),
                ],
                "hint": "Un tasso di variazione costante indica una funzione lineare: f(x) = 3x.",
            },
            {
                "text": "Una funzione il cui valore diminuisce di 2 unità per ogni aumento unitario di x",
                "correct": _expr_linear(-2, 0),
                "distractors": [
                    _expr_linear(2, 0),
                    _expr_linear(-1, 0),
                    _expr_exponential(1, 2, 0),
                    _expr_linear(-2, 1),
                    _expr_quadratic_standard(-2, 0, 0),
                ],
                "hint": "Un tasso di variazione costante negativo: f(x) = -2x.",
            },
            {
                "text": "Una funzione che vale 0 in x = 0 e il cui quadrato di x",
                "correct": _expr_quadratic_standard(1, 0, 0),
                "distractors": [
                    _expr_quadratic_standard(-1, 0, 0),
                    _expr_quadratic_standard(2, 0, 0),
                    _expr_linear(1, 0),
                    _expr_abs(1, 0, 0),
                    _expr_quadratic_standard(1, 0, 1),
                ],
                "hint": "f(0) = 0 e f(x) = x² soddisfa la descrizione.",
            },
            {
                "text": "Una funzione che dimezza il suo valore ogni volta che x aumenta di 1",
                "correct": "y = (1/2)^x",
                "correct_alt": _expr_exponential(1, 0.5, 0),
                "distractors": [
                    _expr_linear(-0.5, 0),
                    _expr_exponential(1, 2, 0),
                    _expr_exponential(-1, 2, 0),
                    _expr_linear(0.5, 0),
                    _expr_exponential(1, 3, 0),
                ],
                "hint": "Se f(x+1) = f(x)/2, allora f(x) = (1/2)^x = 0.5^x.",
            },
            {
                "text": "Una funzione sempre positiva che si avvicina a zero quando x cresce",
                "correct": _expr_exponential(1, 0.5, 0),
                "distractors": [
                    _expr_exponential(1, 2, 0),
                    _expr_linear(-1, 0),
                    _expr_logarithmic(1, 0, 0),
                    _expr_reciprocal(1, 0, 0),
                    _expr_exponential(-1, 2, 0),
                ],
                "hint": "Una funzione esponenziale con base 0 < b < 1 decresce verso 0.",
            },
            {
                "text": "Una funzione che passa per (0, 1) e cresce sempre più rapidamente",
                "correct": _expr_exponential(1, 2, 0),
                "distractors": [
                    _expr_quadratic_standard(1, 0, 1),
                    _expr_linear(2, 1),
                    _expr_exponential(1, 3, 0),
                    _expr_logarithmic(1, 0, 1),
                    _expr_exponential(1, 2, 1),
                ],
                "hint": "f(0) = 1 e crescita sempre più rapida → esponenziale: f(x) = 2^x.",
            },
            {
                "text": "Una funzione simmetrica rispetto all'asse y che vale 0 nell'origine",
                "correct": _expr_quadratic_standard(1, 0, 0),
                "distractors": [
                    _expr_linear(1, 0),
                    _expr_abs(1, 0, 0),
                    _expr_quadratic_standard(1, 0, 1),
                    _expr_quadratic_standard(-1, 0, 0),
                    _expr_exponential(1, 2, 0),
                ],
                "hint": "f(-x) = f(x) e f(0) = 0 → f(x) = x².",
            },
            {
                "text": "Una funzione che cresce molto lentamente e non è definita per x ≤ 0",
                "correct": _expr_logarithmic(1, 0, 0),
                "distractors": [
                    _expr_exponential(1, 2, 0),
                    _expr_linear(0.5, 0),
                    _expr_logarithmic(-1, 0, 0),
                    _expr_reciprocal(1, 0, 0),
                    _expr_sqrt(1, 0, 0),
                ],
                "hint": "Dominio x > 0 e crescita lenta → f(x) = ln(x).",
            },
        ]

        choice = random.choice(descriptions)
        correct_expr = choice.get("correct_alt", choice["correct"])
        # Use the display form
        correct_display = choice["correct"]

        dist_raw = [d for d in choice["distractors"] if d != correct_display]
        seen = {correct_display}
        unique_dist = []
        for d in dist_raw:
            if d not in seen:
                seen.add(d)
                unique_dist.append(d)
        while len(unique_dist) < 4:
            spec = _make_spec(random.choice(_ALL_FAMILIES), transformed=False)
            if spec[1] not in seen:
                seen.add(spec[1])
                unique_dist.append(spec[1])
        unique_dist = unique_dist[:4]

        options_raw = [correct_display] + unique_dist
        correct_index = 0
        options, correct_index = self.shuffle_options(options_raw, correct_index)

        explanation = choice["hint"]
        return {
            "question": f"{choice['text']}. Quale formula la descrive?",
            "graph_data": "",
            "options": options,
            "correct_index": correct_index,
            "explanation": explanation,
            "did_you_know": "Tradurre una descrizione verbale in formula è una competenza chiave: cerca parole come 'raddoppia' (esponenziale), 'costante' (lineare), 'rallenta' (logaritmica).",
            "difficulty": 1,
        }

    def _template_verbal_to_formula_L2(self) -> dict:
        """L2: more complex verbal descriptions with constraints."""
        descriptions = [
            {
                "text": "Una funzione che parte da 5 e raddoppia ad ogni passo: f(0)=5, f(1)=10, f(2)=20, ...",
                "correct": "y = 5·2^x",
                "distractors": [
                    _expr_exponential(1, 2, 5),
                    _expr_linear(5, 5),
                    _expr_exponential(10, 2, 0),
                    _expr_exponential(5, 3, 0),
                    "y = 2·5^x",
                ],
                "hint": "f(0)=5 e f(x+1)=2·f(x), quindi f(x) = 5·2^x.",
            },
            {
                "text": "Una funzione quadratica con vertice in (2, -3) che si apre verso l'alto",
                "correct": _expr_quadratic(1, 2, -3),
                "distractors": [
                    _expr_quadratic(-1, 2, -3),
                    _expr_quadratic(1, -2, -3),
                    _expr_quadratic(1, 2, 3),
                    _expr_quadratic(2, 2, -3),
                    _expr_quadratic(1, -2, 3),
                ],
                "hint": "Vertice (h, k) = (2, -3) e a > 0 → f(x) = (x-2)² - 3.",
            },
            {
                "text": "Una funzione definita solo per x > 2 che cresce lentamente e vale 0 in x = 3",
                "correct": _expr_logarithmic(1, 2, 0),
                "distractors": [
                    _expr_logarithmic(1, 0, 0),
                    _expr_logarithmic(1, 3, 0),
                    _expr_logarithmic(-1, 2, 0),
                    _expr_logarithmic(1, 2, 1),
                    _expr_reciprocal(1, 2, 0),
                ],
                "hint": "Dominio x > 2, crescita lenta, f(3)=ln(1)=0 → f(x) = ln(x-2).",
            },
            {
                "text": "Una funzione lineare che passa per i punti (0, 3) e (2, 7)",
                "correct": _expr_linear(2, 3),
                "distractors": [
                    _expr_linear(3, 2),
                    _expr_linear(2, -3),
                    _expr_linear(7, 3),
                    _expr_linear(1, 3),
                    _expr_linear(2, 7),
                ],
                "hint": "Pendenza = (7-3)/(2-0) = 2, intercetta = 3 → y = 2x + 3.",
            },
            {
                "text": "Una funzione esponenziale che vale 1 in x = 0 e 8 in x = 3",
                "correct": _expr_exponential(1, 2, 0),
                "distractors": [
                    _expr_exponential(1, 3, 0),
                    _expr_exponential(1, 8, 0),
                    _expr_exponential(8, 2, 0),
                    _expr_linear(8, 1),
                    _expr_exponential(1, 2, 1),
                ],
                "hint": "f(0)=1 e f(3)=8 → 1·b³ = 8 → b = 2 → f(x) = 2^x.",
            },
            {
                "text": "Una funzione che ha un asintoto orizzontale y = -1 e passa per (0, 0)",
                "correct": _expr_exponential(1, 2, -1),
                "distractors": [
                    _expr_exponential(1, 2, 0),
                    _expr_exponential(1, 2, 1),
                    _expr_linear(1, -1),
                    _expr_logarithmic(1, 0, -1),
                    _expr_exponential(-1, 2, -1),
                ],
                "hint": "Asintoto y = -1 → k = -1. f(0) = b⁰ + (-1) = 0 → a = 1. f(x) = 2^x - 1.",
            },
            {
                "text": "Una parabola con zeri in x = -1 e x = 3 che passa per (0, -3)",
                "correct": _expr_quadratic_standard(1, -2, -3),
                "distractors": [
                    _expr_quadratic_standard(1, 2, -3),
                    _expr_quadratic_standard(-1, -2, -3),
                    _expr_quadratic_standard(1, -2, 3),
                    _expr_quadratic(1, 1, -4),
                    _expr_quadratic_standard(2, -2, -3),
                ],
                "hint": "Zeri -1 e 3 → f(x) = a(x+1)(x-3). f(0) = a·1·(-3) = -3a = -3 → a = 1. f(x) = x² - 2x - 3.",
            },
            {
                "text": "Una funzione che è l'inversa di y = e^x",
                "correct": _expr_logarithmic(1, 0, 0),
                "distractors": [
                    _expr_exponential(1, math.e, 0) if False else "y = e^x",
                    _expr_exponential(-1, 2, 0),
                    _expr_reciprocal(1, 0, 0),
                    _expr_logarithmic(-1, 0, 0),
                    _expr_logarithmic(1, 1, 0),
                ],
                "hint": "L'inversa di e^x è ln(x): se y = e^x allora x = ln(y).",
            },
            {
                "text": "Una funzione con un asintoto verticale in x = 1 e un asintoto orizzontale in y = 2",
                "correct": _expr_reciprocal(1, 1, 2),
                "distractors": [
                    _expr_reciprocal(1, 2, 1),
                    _expr_reciprocal(1, 1, 0),
                    _expr_reciprocal(1, 0, 2),
                    _expr_logarithmic(1, 1, 2),
                    _expr_reciprocal(-1, 1, 2),
                ],
                "hint": "Asintoto verticale x = 1 → h = 1; asintoto orizzontale y = 2 → k = 2. f(x) = 1/(x-1) + 2.",
            },
            {
                "text": "Una funzione che oscilla tra -2 e 2 con periodo π",
                "correct": _expr_sin(2, 2, 0, 0),
                "distractors": [
                    _expr_sin(2, 1, 0, 0),
                    _expr_sin(1, 2, 0, 0),
                    _expr_cos(2, 2, 0, 0),
                    _expr_sin(2, 2, 0, 1),
                    _expr_sin(2, 3, 0, 0),
                ],
                "hint": "Ampiezza 2 e periodo π (b = 2π/π = 2) → f(x) = 2sin(2x).",
            },
        ]

        choice = random.choice(descriptions)
        correct_display = choice["correct"]

        dist_raw = [d for d in choice["distractors"] if d != correct_display]
        seen = {correct_display}
        unique_dist = []
        for d in dist_raw:
            if d not in seen:
                seen.add(d)
                unique_dist.append(d)
        while len(unique_dist) < 4:
            spec = _make_spec(random.choice(_ALL_FAMILIES), transformed=True)
            if spec[1] not in seen:
                seen.add(spec[1])
                unique_dist.append(spec[1])
        unique_dist = unique_dist[:4]

        options_raw = [correct_display] + unique_dist
        correct_index = 0
        options, correct_index = self.shuffle_options(options_raw, correct_index)

        explanation = choice["hint"]
        return {
            "question": f"{choice['text']}. Quale formula descrive questa funzione?",
            "graph_data": "",
            "options": options,
            "correct_index": correct_index,
            "explanation": explanation,
            "did_you_know": "Tradurre vincoli verbali in equazioni è fondamentale: 'passa per (a,b)' significa f(a)=b; 'asintoto y=k' significa che la funzione tende a k.",
            "difficulty": 2,
        }

    # -- Formula-form conversion --------------------------------------------

    def _template_formula_form_conversion_L2(self) -> dict:
        """L2: standard form → vertex form for quadratics."""
        # Generate a quadratic in vertex form a(x-h)^2 + k
        a = random.choice([-2, -1, 1, 2])
        h = random.choice([-3, -2, -1, 0, 1, 2, 3])
        k = random.choice([-4, -3, -2, -1, 0, 1, 2, 3, 4])

        # Expand to standard: a*x^2 - 2ah*x + a*h^2 + k
        std_a = a
        std_b = -2 * a * h
        std_c = a * h * h + k

        standard_expr = _expr_quadratic_standard(std_a, std_b, std_c)
        vertex_expr = _expr_quadratic(a, h, k)

        # Distractors: common mistakes in completing the square
        distractor_params = [
            _expr_quadratic(a, -h, k),            # wrong sign of h
            _expr_quadratic(a, h, -k),             # wrong sign of k
            _expr_quadratic(-a, h, k),             # wrong sign of a
            _expr_quadratic(a, h, k + a * h * h),  # forgot to subtract ah²
            _expr_quadratic(a, h + 1, k),          # off-by-one h
            _expr_quadratic(a, h, k + 1),          # off-by-one k
            _expr_quadratic(a, 2 * h, k),          # forgot to halve b/2a
        ]

        distractors = [d for d in distractor_params if d != vertex_expr]
        seen = {vertex_expr}
        unique_dist = []
        for d in distractors:
            if d not in seen:
                seen.add(d)
                unique_dist.append(d)
        while len(unique_dist) < 4:
            new_h = h + random.choice([-2, -1, 1, 2])
            new_k = k + random.choice([-2, -1, 1, 2])
            cand = _expr_quadratic(a, new_h, new_k)
            if cand not in seen:
                seen.add(cand)
                unique_dist.append(cand)
        unique_dist = unique_dist[:4]

        options_raw = [vertex_expr] + unique_dist
        correct_index = 0
        options, correct_index = self.shuffle_options(options_raw, correct_index)

        explanation = (
            f"Completando il quadrato: {standard_expr} → "
            f"{_fmt_num(std_a)}(x² {_fmt_num(-2 * h, always_sign=True)}x) {_fmt_num(std_c, always_sign=True)} → "
            f"{_fmt_num(std_a)}(x {_fmt_num(-h, always_sign=True)})² {_fmt_num(k, always_sign=True)} → "
            f"{vertex_expr}."
        )

        return {
            "question": f"Riscrivi {standard_expr} nella forma a(x - h)² + k (forma del vertice).",
            "graph_data": "",
            "options": options,
            "correct_index": correct_index,
            "explanation": explanation,
            "did_you_know": "La forma del vertice y = a(x-h)² + k rivela immediatamente il vertice (h, k) della parabola e la direzione di apertura (segno di a).",
            "difficulty": 2,
        }

    def _template_formula_form_conversion_L3(self) -> dict:
        """L3: vertex form → factored form, or standard → factored."""
        # Generate quadratic with integer roots
        r1 = random.randint(-4, 0)
        r2 = random.randint(r1 + 1, 4)
        a = random.choice([-2, -1, 1, 2])

        # Factored form
        r1_part = f"x{_fmt_num(-r1, always_sign=True)}" if r1 != 0 else "x"
        r2_part = f"x{_fmt_num(-r2, always_sign=True)}" if r2 != 0 else "x"
        if a == 1:
            factored_expr = f"f(x) = ({r1_part})({r2_part})"
        elif a == -1:
            factored_expr = f"f(x) = -({r1_part})({r2_part})"
        else:
            factored_expr = f"f(x) = {_fmt_num(a)}({r1_part})({r2_part})"

        # Standard form
        std_a = a
        std_b = -a * (r1 + r2)
        std_c = a * r1 * r2
        standard_expr = _expr_quadratic_standard(std_a, std_b, std_c)

        # Distractors: common factoring mistakes
        distractor_list = []

        # Wrong roots
        wrong_pairs = [
            (r1 + 1, r2), (r1, r2 - 1), (-r1, r2), (r1, -r2),
            (r1 - 1, r2 + 1), (r2, r1 + 2),
        ]
        for wr1, wr2 in wrong_pairs:
            wr1_part = f"x{_fmt_num(-wr1, always_sign=True)}" if wr1 != 0 else "x"
            wr2_part = f"x{_fmt_num(-wr2, always_sign=True)}" if wr2 != 0 else "x"
            if a == 1:
                d = f"f(x) = ({wr1_part})({wr2_part})"
            elif a == -1:
                d = f"f(x) = -({wr1_part})({wr2_part})"
            else:
                d = f"f(x) = {_fmt_num(a)}({wr1_part})({wr2_part})"
            distractor_list.append(d)

        distractors = [d for d in distractor_list if d != factored_expr]
        seen = {factored_expr}
        unique_dist = []
        for d in distractors:
            if d not in seen:
                seen.add(d)
                unique_dist.append(d)
        while len(unique_dist) < 4:
            wr1 = r1 + random.choice([-3, -2, 2, 3])
            wr2 = r2 + random.choice([-3, -2, 2, 3])
            wr1_part = f"x{_fmt_num(-wr1, always_sign=True)}" if wr1 != 0 else "x"
            wr2_part = f"x{_fmt_num(-wr2, always_sign=True)}" if wr2 != 0 else "x"
            if a == 1:
                cand = f"f(x) = ({wr1_part})({wr2_part})"
            elif a == -1:
                cand = f"f(x) = -({wr1_part})({wr2_part})"
            else:
                cand = f"f(x) = {_fmt_num(a)}({wr1_part})({wr2_part})"
            if cand not in seen:
                seen.add(cand)
                unique_dist.append(cand)
        unique_dist = unique_dist[:4]

        options_raw = [factored_expr] + unique_dist
        correct_index = 0
        options, correct_index = self.shuffle_options(options_raw, correct_index)

        explanation = (
            f"Da {standard_expr}: troviamo le radici con la formula quadratica o scomposizione. "
            f"Le radici sono x = {_fmt_num(r1)} e x = {_fmt_num(r2)}, "
            f"quindi la forma fattorizzata è {factored_expr}."
        )

        return {
            "question": f"Riscrivi {standard_expr} in forma fattorizzata a(x - r₁)(x - r₂).",
            "graph_data": "",
            "options": options,
            "correct_index": correct_index,
            "explanation": explanation,
            "did_you_know": "La forma fattorizzata rivela immediatamente gli zeri della funzione. Utile per risolvere disequazioni e per lo studio del segno.",
            "difficulty": 3,
        }

    # ------------------------------------------------------------------

    def generate(self, difficulty: int) -> dict:
        difficulty = max(1, min(3, difficulty))

        # ~17% chance of a multiple-representation template (all levels)
        if random.random() < 0.17:
            repr_templates = []
            if difficulty == 1:
                repr_templates = [
                    self._template_table_to_formula_L1,
                    self._template_verbal_to_formula_L1,
                ]
            elif difficulty == 2:
                repr_templates = [
                    self._template_table_to_formula_L1,
                    self._template_table_to_formula_L2,
                    self._template_table_to_graph_L2,
                    self._template_verbal_to_formula_L1,
                    self._template_verbal_to_formula_L2,
                    self._template_formula_form_conversion_L2,
                ]
            else:  # difficulty == 3
                repr_templates = [
                    self._template_table_to_formula_L2,
                    self._template_table_to_formula_L3,
                    self._template_table_to_graph_L2,
                    self._template_table_to_graph_L3,
                    self._template_verbal_to_formula_L2,
                    self._template_formula_form_conversion_L2,
                    self._template_formula_form_conversion_L3,
                ]
            template_fn = random.choice(repr_templates)
            return template_fn()

        # At L2/L3, mix in domain/evaluation/sign/injectivity templates
        if difficulty >= 2:
            domain_templates = [
                self._template_domain_logarithmic,
                self._template_domain_rational,
                self._template_domain_sqrt,
                self._template_function_evaluation,
                self._template_injectivity,
                self._template_invertibility,
                self._template_codomain,
                self._template_inverse_sign,
                self._template_inverse_increasing,
                self._template_inverse_max_min,
                self._template_inverse_intersections,
            ]
            if difficulty == 3:
                domain_templates.append(self._template_sign_of_function)
                domain_templates.append(self._template_injectivity_intervals)
                domain_templates.append(self._template_inverse_preimage)
                domain_templates.append(self._template_inverse_range)

            # ~45% chance of a domain/evaluation/sign/inverse template at L2+
            if random.random() < 0.45:
                template_fn = random.choice(domain_templates)
                return template_fn()

        # pick correct function
        if difficulty == 1:
            correct_spec = _random_spec_level1()
        elif difficulty == 2:
            correct_spec = _random_spec_level2()
        else:
            correct_spec = _random_spec_level3()

        func, expr, family_it, hint, x_range, y_range = correct_spec
        correct_family = _family_from_name(family_it)

        # choose mode
        mode = random.choice(["graph_to_func", "func_to_graph"])

        # generate distractors
        distractor_specs = _generate_distractors(correct_family, difficulty, count=4)

        # ensure no duplicate expressions
        distractor_exprs = set()
        unique_distractors = []
        for spec in distractor_specs:
            d_expr = spec[1]
            if d_expr != expr and d_expr not in distractor_exprs:
                distractor_exprs.add(d_expr)
                unique_distractors.append(spec)
        # fill if we lost some to dedup
        attempts = 0
        while len(unique_distractors) < 4 and attempts < 20:
            attempts += 1
            fam = random.choice(_ALL_FAMILIES)
            spec = _make_spec(fam, transformed=(difficulty > 1), complex_transforms=(difficulty == 3))
            if spec[1] != expr and spec[1] not in distractor_exprs:
                distractor_exprs.add(spec[1])
                unique_distractors.append(spec)
        distractor_specs = unique_distractors[:4]

        if mode == "graph_to_func":
            # show graph, choose among expressions
            graph_svg = _build_svg(func, x_range, y_range, color="#2563eb")
            options_raw = [expr] + [s[1] for s in distractor_specs]
            correct_index = 0
            options, correct_index = self.shuffle_options(options_raw, correct_index)
            question = "Osserva il grafico. Quale funzione corrisponde alla curva mostrata?"
        else:
            # show expression, choose among graphs
            colors = ["#2563eb", "#dc2626", "#16a34a", "#9333ea", "#f59e0b"]
            random.shuffle(colors)
            all_specs = [correct_spec] + distractor_specs
            graph_svgs = []
            for i, spec in enumerate(all_specs):
                s_func, _, _, _, s_xr, s_yr = spec
                svg = _build_svg(s_func, s_xr, s_yr, color=colors[i % len(colors)])
                graph_svgs.append(svg)
            graph_svg = ""  # no main graph in this mode; expression is the prompt
            options_raw = graph_svgs
            correct_index = 0
            options, correct_index = self.shuffle_options(options_raw, correct_index)
            question = f"Data la funzione {expr}, quale grafico la rappresenta?"

        explanation = f"{hint}. La famiglia di funzione è: {family_it}. "
        if difficulty >= 2:
            explanation += f"L'espressione corretta è {expr}."

        did_you_know = random.choice(_DID_YOU_KNOW)

        result = {
            "question": question,
            "graph_data": graph_svg,
            "options": options,
            "correct_index": correct_index,
            "explanation": explanation,
            "did_you_know": did_you_know,
        }
        return result
