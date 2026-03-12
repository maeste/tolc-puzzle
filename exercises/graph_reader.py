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

    def generate(self, difficulty: int) -> dict:
        difficulty = max(1, min(3, difficulty))

        # At L2/L3, mix in domain/evaluation/sign templates
        if difficulty >= 2:
            domain_templates = [
                self._template_domain_logarithmic,
                self._template_domain_rational,
                self._template_domain_sqrt,
                self._template_function_evaluation,
            ]
            if difficulty == 3:
                domain_templates.append(self._template_sign_of_function)

            # ~35% chance of a domain/evaluation/sign template at L2+
            if random.random() < 0.35:
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
