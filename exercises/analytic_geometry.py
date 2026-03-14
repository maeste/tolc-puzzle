import math
import random

from exercises.base import Exercise


def _fmt(value, decimals=2):
    """Format a numeric value: show as int if whole, otherwise round."""
    if isinstance(value, str):
        return value
    if abs(value - round(value)) < 1e-9:
        return str(int(round(value)))
    return str(round(value, decimals))


def _make_distractors(correct_value, count=4):
    """Generate plausible wrong numeric answers."""
    distractors = set()
    correct_str = _fmt(correct_value)

    if correct_value != 0:
        distractors.add(_fmt(-correct_value))

    distractors.add(_fmt(correct_value + 1))
    distractors.add(_fmt(correct_value - 1))
    distractors.add(_fmt(correct_value + 2))
    distractors.add(_fmt(correct_value - 2))

    if correct_value != 0:
        distractors.add(_fmt(correct_value * 2))
        if abs(correct_value) >= 2:
            distractors.add(_fmt(correct_value / 2))

    distractors.add(_fmt(correct_value + 3))
    distractors.add(_fmt(correct_value - 3))

    distractors.discard(correct_str)

    attempts = 0
    while len(distractors) < count and attempts < 100:
        attempts += 1
        spread = max(3, abs(correct_value) * 0.3)
        offset = random.uniform(-spread, spread)
        d = round(correct_value + offset, 2)
        d_str = _fmt(d)
        if d_str != correct_str:
            distractors.add(d_str)

    return list(distractors)[:count]


def _fmt_eq(m, q):
    """Format a line equation y = mx + q as a readable string."""
    if m == 0:
        return f"y = {_fmt(q)}"
    if m == 1:
        m_part = "x"
    elif m == -1:
        m_part = "-x"
    else:
        m_part = f"{_fmt(m)}x"
    if q == 0:
        return f"y = {m_part}"
    sign = "+" if q > 0 else "-"
    return f"y = {m_part} {sign} {_fmt(abs(q))}"


def _make_equation_distractors(m, q, count=3):
    """Generate plausible wrong line equations by tweaking slope and intercept."""
    correct = _fmt_eq(m, q)
    distractors = set()

    # Tweak intercept
    for delta in [-2, -1, 1, 2]:
        distractors.add(_fmt_eq(m, q + delta))

    # Tweak slope
    for delta in [-1, 1]:
        distractors.add(_fmt_eq(m + delta, q))

    # Sign errors
    distractors.add(_fmt_eq(-m, q))
    distractors.add(_fmt_eq(m, -q))
    distractors.add(_fmt_eq(-m, -q))

    # Swap slope and intercept
    if m != q:
        distractors.add(_fmt_eq(q, m))

    distractors.discard(correct)
    result = list(distractors)

    # Fill with random offsets if needed
    attempts = 0
    while len(result) < count and attempts < 50:
        attempts += 1
        dm = random.choice([-3, -2, 2, 3])
        dq = random.choice([-3, -2, 2, 3])
        candidate = _fmt_eq(m + dm, q + dq)
        if candidate != correct and candidate not in result:
            result.append(candidate)

    return result[:count]


def _fmt_circle_eq(h, k, r):
    """Format a circle equation (x - h)^2 + (y - k)^2 = r^2."""
    def _term(var, center):
        if center == 0:
            return f"{var}^2"
        elif center > 0:
            return f"({var} - {_fmt(center)})^2"
        else:
            return f"({var} + {_fmt(abs(center))})^2"

    return f"{_term('x', h)} + {_term('y', k)} = {_fmt(r * r)}"


def _make_circle_distractors(h, k, r, count=3):
    """Generate plausible wrong circle equations."""
    correct = _fmt_circle_eq(h, k, r)
    distractors = set()

    # Wrong radius
    for delta in [-1, 1, 2]:
        if r + delta > 0:
            distractors.add(_fmt_circle_eq(h, k, r + delta))

    # Forgot to square radius
    distractors.add(f"{_fmt_circle_eq(h, k, r).rsplit('=', 1)[0]}= {_fmt(r)}")

    # Sign errors on center
    distractors.add(_fmt_circle_eq(-h, k, r))
    distractors.add(_fmt_circle_eq(h, -k, r))
    distractors.add(_fmt_circle_eq(-h, -k, r))

    # Swapped center coordinates
    if h != k:
        distractors.add(_fmt_circle_eq(k, h, r))

    distractors.discard(correct)
    result = list(distractors)

    attempts = 0
    while len(result) < count and attempts < 50:
        attempts += 1
        dh = random.choice([-2, -1, 1, 2])
        dk = random.choice([-2, -1, 1, 2])
        candidate = _fmt_circle_eq(h + dh, k + dk, r)
        if candidate != correct and candidate not in result:
            result.append(candidate)

    return result[:count]


def _fmt_parabola_eq(a, b, c):
    """Format a vertical parabola equation y = ax^2 + bx + c."""
    parts = []
    # ax^2 term
    if a == 1:
        parts.append("x²")
    elif a == -1:
        parts.append("-x²")
    else:
        parts.append(f"{_fmt(a)}x²")
    # bx term
    if b != 0:
        if b > 0:
            if b == 1:
                parts.append("+ x")
            else:
                parts.append(f"+ {_fmt(b)}x")
        else:
            if b == -1:
                parts.append("- x")
            else:
                parts.append(f"- {_fmt(abs(b))}x")
    # c term
    if c != 0:
        if c > 0:
            parts.append(f"+ {_fmt(c)}")
        else:
            parts.append(f"- {_fmt(abs(c))}")
    return "y = " + " ".join(parts)


def _fmt_parabola_eq_horizontal(a, b, c):
    """Format a horizontal parabola equation x = ay^2 + by + c."""
    parts = []
    if a == 1:
        parts.append("y²")
    elif a == -1:
        parts.append("-y²")
    else:
        parts.append(f"{_fmt(a)}y²")
    if b != 0:
        if b > 0:
            if b == 1:
                parts.append("+ y")
            else:
                parts.append(f"+ {_fmt(b)}y")
        else:
            if b == -1:
                parts.append("- y")
            else:
                parts.append(f"- {_fmt(abs(b))}y")
    if c != 0:
        if c > 0:
            parts.append(f"+ {_fmt(c)}")
        else:
            parts.append(f"- {_fmt(abs(c))}")
    return "x = " + " ".join(parts)


# ---------------------------------------------------------------------------
# LEVEL 1 Templates -- Basic analytic geometry
# ---------------------------------------------------------------------------

def _t1_line_from_point_slope():
    """Given point (x0, y0) and slope m, find the equation y = mx + q."""
    x0 = random.randint(-5, 5)
    y0 = random.randint(-5, 5)
    m = random.choice([i for i in range(-4, 5) if i != 0])

    q = y0 - m * x0

    correct_eq = _fmt_eq(m, q)
    distractors = _make_equation_distractors(m, q)

    question = (
        f"Trova l'equazione della retta passante per il punto ({x0}, {y0}) "
        f"con coefficiente angolare m = {m}."
    )
    explanation = (
        f"Usiamo la formula punto-pendenza: y - y0 = m(x - x0).\n"
        f"y - {y0} = {m}(x - {x0})\n"
        f"y = {m}x - {m * x0} + {y0}\n"
        f"y = {m}x + {_fmt(q)}\n"
        f"L'equazione è: {correct_eq}."
    )
    tip = (
        "La formula punto-pendenza y - y0 = m(x - x0) permette di trovare "
        "l'equazione di una retta noti un punto e il coefficiente angolare."
    )
    return question, correct_eq, distractors, explanation, tip


def _t1_distance_two_points():
    """Given two points, compute the distance."""
    x1 = random.randint(-6, 6)
    y1 = random.randint(-6, 6)
    x2 = random.randint(-6, 6)
    y2 = random.randint(-6, 6)
    while x1 == x2 and y1 == y2:
        x2 = random.randint(-6, 6)
        y2 = random.randint(-6, 6)

    dist_sq = (x2 - x1) ** 2 + (y2 - y1) ** 2
    dist = math.sqrt(dist_sq)

    question = (
        f"Calcola la distanza tra i punti A({x1}, {y1}) e B({x2}, {y2}). "
        f"Arrotonda a due decimali se necessario."
    )
    explanation = (
        f"d = sqrt((x2 - x1)^2 + (y2 - y1)^2)\n"
        f"d = sqrt(({x2} - {x1})^2 + ({y2} - {y1})^2)\n"
        f"d = sqrt({(x2 - x1)}^2 + {(y2 - y1)}^2)\n"
        f"d = sqrt({(x2 - x1) ** 2} + {(y2 - y1) ** 2})\n"
        f"d = sqrt({dist_sq}) = {_fmt(dist)}."
    )
    tip = (
        "La distanza tra due punti nel piano si calcola con la formula: "
        "d = sqrt((x2-x1)^2 + (y2-y1)^2), derivata dal teorema di Pitagora."
    )
    return question, dist, explanation, tip


def _t1_midpoint():
    """Given two points, find the midpoint and ask for x_m + y_m."""
    x1 = random.randint(-8, 8)
    y1 = random.randint(-8, 8)
    x2 = random.randint(-8, 8)
    y2 = random.randint(-8, 8)
    while x1 == x2 and y1 == y2:
        x2 = random.randint(-8, 8)
        y2 = random.randint(-8, 8)

    # Ensure integer midpoint coordinates
    while (x1 + x2) % 2 != 0 or (y1 + y2) % 2 != 0:
        x2 = random.randint(-8, 8)
        y2 = random.randint(-8, 8)
        if x1 == x2 and y1 == y2:
            x2 += 2

    xm = (x1 + x2) // 2
    ym = (y1 + y2) // 2
    result = float(xm + ym)

    question = (
        f"Trova il punto medio M del segmento con estremi A({x1}, {y1}) e B({x2}, {y2}). "
        f"Quanto vale x_M + y_M?"
    )
    explanation = (
        f"Il punto medio ha coordinate: M = ((x1+x2)/2, (y1+y2)/2)\n"
        f"x_M = ({x1} + {x2}) / 2 = {_fmt(xm)}\n"
        f"y_M = ({y1} + {y2}) / 2 = {_fmt(ym)}\n"
        f"x_M + y_M = {_fmt(xm)} + {_fmt(ym)} = {_fmt(result)}."
    )
    tip = (
        "Il punto medio di un segmento si calcola facendo la media aritmetica "
        "delle coordinate: M = ((x1+x2)/2, (y1+y2)/2)."
    )
    return question, result, explanation, tip


# ---------------------------------------------------------------------------
# LEVEL 2 Templates -- Intermediate analytic geometry
# ---------------------------------------------------------------------------

def _t2_parallel_perpendicular():
    """Given line y = mx + q and a point, find parallel or perpendicular through that point."""
    m = random.choice([i for i in range(-4, 5) if i != 0])
    q_orig = random.randint(-5, 5)
    px = random.randint(-4, 4)
    py = random.randint(-4, 4)

    variant = random.choice(["parallela", "perpendicolare"])

    if variant == "parallela":
        m_new = m
        q_new = py - m_new * px
        relation_text = "parallela"
        slope_explanation = f"La retta parallela ha lo stesso coefficiente angolare m = {m}."
    else:
        # Perpendicular slope is -1/m. To keep integer results, pick m from {1, -1, 2, -2}
        # and ensure the perpendicular slope works cleanly
        m = random.choice([1, -1, 2, -2])
        q_orig = random.randint(-5, 5)
        if abs(m) == 2:
            # m_perp = -1/2, force py and px so q_new is rational
            # q_new = py - (-1/m)*px = py + px/m
            # Pick px as multiple of m for integer q_new
            px = random.choice([i for i in range(-4, 5) if i % m == 0 and i != 0])
            if px == 0:
                px = m
            py = random.randint(-4, 4)
        else:
            px = random.randint(-4, 4)
            py = random.randint(-4, 4)

        m_perp = -1 / m
        m_new = m_perp
        q_new = py - m_new * px
        relation_text = "perpendicolare"
        slope_explanation = (
            f"Il coefficiente angolare della retta perpendicolare è m' = -1/m = -1/{m} = {_fmt(m_perp)}."
        )

    # Round q_new if it should be integer
    if abs(q_new - round(q_new)) < 1e-9:
        q_new = int(round(q_new))

    correct_eq = _fmt_eq(m_new, q_new)
    distractors = _make_equation_distractors(m_new, q_new)

    orig_eq = _fmt_eq(m, q_orig)

    question = (
        f"Trova l'equazione della retta {relation_text} alla retta {orig_eq} "
        f"e passante per il punto ({px}, {py})."
    )
    explanation = (
        f"{slope_explanation}\n"
        f"Usiamo il punto ({px}, {py}): y - {py} = {_fmt(m_new)}(x - {px})\n"
        f"y = {_fmt(m_new)}x + {_fmt(q_new)}\n"
        f"L'equazione è: {correct_eq}."
    )
    tip = (
        "Due rette sono parallele se hanno lo stesso coefficiente angolare. "
        "Sono perpendicolari se il prodotto dei coefficienti angolari è -1: m1 * m2 = -1."
    )
    return question, correct_eq, distractors, explanation, tip


def _t2_line_through_two_points():
    """Given two points, find the equation of the line through them."""
    x1 = random.randint(-5, 5)
    y1 = random.randint(-5, 5)
    x2 = random.randint(-5, 5)
    y2 = random.randint(-5, 5)
    while x1 == x2:
        x2 = random.randint(-5, 5)

    # Ensure integer slope: pick points so (y2-y1) is divisible by (x2-x1)
    dx = x2 - x1
    dy_candidates = [i * dx for i in range(-4, 5) if i != 0]
    if not dy_candidates:
        dy_candidates = [dx, -dx]
    dy = random.choice(dy_candidates)
    y2 = y1 + dy

    m = dy // dx
    q = y1 - m * x1

    correct_eq = _fmt_eq(m, q)
    distractors = _make_equation_distractors(m, q)

    question = (
        f"Trova l'equazione della retta passante per i punti A({x1}, {y1}) e B({x2}, {y2})."
    )
    explanation = (
        f"Il coefficiente angolare è m = (y2 - y1) / (x2 - x1) = ({y2} - {y1}) / ({x2} - {x1}) = {dy}/{dx} = {_fmt(m)}.\n"
        f"Usando il punto A: y - {y1} = {m}(x - {x1})\n"
        f"y = {m}x - {m * x1} + {y1} = {m}x + {_fmt(q)}\n"
        f"L'equazione è: {correct_eq}."
    )
    tip = (
        "Per trovare l'equazione della retta per due punti, calcola prima il coefficiente "
        "angolare m = (y2-y1)/(x2-x1), poi usa la formula punto-pendenza."
    )
    return question, correct_eq, distractors, explanation, tip


def _t2_segment_bisector():
    """Given endpoints of a segment, find equation of the perpendicular bisector."""
    x1 = random.randint(-4, 4)
    y1 = random.randint(-4, 4)
    # Ensure even sums for integer midpoint and nice perpendicular slope
    x2 = x1 + random.choice([2, -2, 4, -4])
    y2 = y1 + random.choice([2, -2, 4, -4])
    while x1 == x2 and y1 == y2:
        x2 = x1 + random.choice([2, -2, 4, -4])

    xm = (x1 + x2) / 2
    ym = (y1 + y2) / 2

    dx = x2 - x1
    dy = y2 - y1

    if dx == 0:
        # Vertical segment, bisector is horizontal: y = ym
        m_bisector = 0
        q_bisector = ym
    elif dy == 0:
        # Horizontal segment, bisector is vertical. Represent as special case.
        # For simplicity, regenerate to avoid vertical line.
        # Force non-zero dy
        y2 = y1 + random.choice([2, -2, 4, -4])
        dy = y2 - y1
        xm = (x1 + x2) / 2
        ym = (y1 + y2) / 2
        m_seg = dy / dx
        m_bisector = -dx / dy
        q_bisector = ym - m_bisector * xm
    else:
        m_seg = dy / dx
        m_bisector = -dx / dy
        q_bisector = ym - m_bisector * xm

    # Round if close to integer
    if abs(m_bisector - round(m_bisector)) < 1e-9:
        m_bisector = int(round(m_bisector))
    if abs(q_bisector - round(q_bisector)) < 1e-9:
        q_bisector = int(round(q_bisector))

    correct_eq = _fmt_eq(m_bisector, q_bisector)
    distractors = _make_equation_distractors(m_bisector, q_bisector)

    question = (
        f"Trova l'equazione dell'asse del segmento con estremi A({x1}, {y1}) e B({x2}, {y2})."
    )
    explanation = (
        f"Il punto medio è M = (({x1}+{x2})/2, ({y1}+{y2})/2) = ({_fmt(xm)}, {_fmt(ym)}).\n"
        f"Il coefficiente angolare del segmento è m = ({y2}-{y1})/({x2}-{x1}) = {dy}/{dx}.\n"
        f"L'asse è perpendicolare: m_asse = -{dx}/{dy} = {_fmt(m_bisector)}.\n"
        f"Passando per M: y - {_fmt(ym)} = {_fmt(m_bisector)}(x - {_fmt(xm)})\n"
        f"L'equazione è: {correct_eq}."
    )
    tip = (
        "L'asse di un segmento è la retta perpendicolare al segmento passante per il suo punto medio. "
        "Ha coefficiente angolare -1/m rispetto al segmento."
    )
    return question, correct_eq, distractors, explanation, tip


# ---------------------------------------------------------------------------
# LEVEL 3 Templates -- Advanced analytic geometry
# ---------------------------------------------------------------------------

def _t3_circle_equation():
    """Given center and radius (or center and point on circle), find the equation."""
    h = random.randint(-4, 4)
    k = random.randint(-4, 4)

    variant = random.choice(["radius", "point"])

    if variant == "radius":
        r = random.randint(1, 6)
        question = (
            f"Scrivi l'equazione della circonferenza con centro C({h}, {k}) e raggio r = {r}."
        )
        explanation = (
            f"L'equazione della circonferenza con centro ({h}, {k}) e raggio {r} è:\n"
            f"(x - {h})^2 + (y - {k})^2 = {r}^2\n"
            f"{_fmt_circle_eq(h, k, r)}."
        )
    else:
        # Point on the circle
        angle_idx = random.randint(0, 3)
        offsets = [(3, 4), (4, 3), (5, 0), (0, 5), (1, 2), (2, 1)]
        dx, dy = random.choice(offsets)
        sign_x = random.choice([1, -1])
        sign_y = random.choice([1, -1])
        px = h + sign_x * dx
        py = k + sign_y * dy
        r_sq = (px - h) ** 2 + (py - k) ** 2
        r = math.sqrt(r_sq)
        # r may not be integer, but r^2 is
        question = (
            f"Scrivi l'equazione della circonferenza con centro C({h}, {k}) "
            f"passante per il punto P({px}, {py})."
        )
        explanation = (
            f"Il raggio è la distanza CP:\n"
            f"r = sqrt(({px}-{h})^2 + ({py}-{k})^2) = sqrt({(px - h) ** 2} + {(py - k) ** 2}) = sqrt({r_sq}).\n"
            f"r^2 = {r_sq}\n"
            f"L'equazione è: {_fmt_circle_eq(h, k, r)}."
        )

    correct_eq = _fmt_circle_eq(h, k, r)
    distractors = _make_circle_distractors(h, k, r)

    tip = (
        "L'equazione della circonferenza con centro (h, k) e raggio r è: "
        "(x - h)^2 + (y - k)^2 = r^2."
    )
    return question, correct_eq, distractors, explanation, tip


def _t3_line_circle_intersection():
    """Given line and circle, find number of intersection points."""
    # Circle centered at origin for simplicity
    r = random.randint(2, 5)

    # Line y = mx + q
    m = random.choice([0, 1, -1, 2, -2])
    # Choose q to control the number of intersections
    variant = random.choice(["secante", "tangente", "esterna"])

    # Distance from origin to line y = mx + q is |q| / sqrt(1 + m^2)
    denom = math.sqrt(1 + m * m)

    if variant == "secante":
        # d < r => |q| < r * sqrt(1+m^2)
        max_q = int(r * denom) - 1
        if max_q < 0:
            max_q = 0
        q = random.randint(-max_q, max_q) if max_q > 0 else 0
        n_intersections = 2
    elif variant == "tangente":
        # d = r => |q| = r * sqrt(1+m^2)
        # This only works cleanly for specific cases
        # For m=0: q = +/- r
        if m == 0:
            q = random.choice([r, -r])
        else:
            # Use m=1: q = +/- r*sqrt(2), not integer. Use m=0 instead.
            m = 0
            q = random.choice([r, -r])
        n_intersections = 1
    else:
        # d > r => |q| > r * sqrt(1+m^2)
        min_q = int(r * denom) + 1
        q = random.choice([min_q, -min_q, min_q + 1, -min_q - 1])
        n_intersections = 0

    result = float(n_intersections)
    line_eq = _fmt_eq(m, q)
    circle_eq = _fmt_circle_eq(0, 0, r)

    question = (
        f"Quanti punti di intersezione hanno la retta {line_eq} e la circonferenza {circle_eq}?"
    )
    d = abs(q) / denom
    explanation = (
        f"La distanza dal centro (0, 0) alla retta è d = |{q}| / sqrt(1 + {m}^2) = {_fmt(d)}.\n"
        f"Il raggio è r = {r}.\n"
    )
    if n_intersections == 2:
        explanation += f"Poiché d = {_fmt(d)} < r = {r}, la retta è secante: 2 punti di intersezione."
    elif n_intersections == 1:
        explanation += f"Poiché d = {_fmt(d)} = r = {r}, la retta è tangente: 1 punto di intersezione."
    else:
        explanation += f"Poiché d = {_fmt(d)} > r = {r}, la retta è esterna: 0 punti di intersezione."

    tip = (
        "Per determinare la posizione reciproca di retta e circonferenza, confronta la distanza "
        "del centro dalla retta con il raggio: d < r (secante, 2 punti), d = r (tangente, 1 punto), d > r (esterna, 0 punti)."
    )
    return question, result, explanation, tip


def _t1_parabola_vertex():
    """Given y = ax^2 + bx + c, find the vertex."""
    a = random.choice([i for i in range(-3, 4) if i != 0])
    h = random.randint(-4, 4)
    k = random.randint(-5, 5)
    # From vertex form y = a(x-h)^2 + k => y = ax^2 - 2ahx + ah^2 + k
    b = -2 * a * h
    c = a * h * h + k

    # Format the equation
    eq = _fmt_parabola_eq(a, b, c)

    correct_str = f"({h}, {k})"

    # Distractors: common sign/formula errors
    dists = set()
    dists.add(f"({-h}, {k})")
    dists.add(f"({h}, {-k})")
    if a != 0:
        wrong_x = b // (2 * a) if (2 * a) != 0 else h + 1
        dists.add(f"({wrong_x}, {k})")
    dists.add(f"({h}, {c})")
    dists.add(f"({-h}, {-k})")
    dists.add(f"({b}, {c})")
    dists.discard(correct_str)
    distractors = list(dists)[:4]
    while len(distractors) < 4:
        distractors.append(f"({h + len(distractors) + 1}, {k - len(distractors)})")

    question = f"Qual è il vertice della parabola {eq}?"
    explanation = (
        f"Per la parabola y = ax² + bx + c, il vertice ha coordinate:\n"
        f"x_V = -b/(2a) = -({b})/(2·{a}) = {h}\n"
        f"y_V = c - b²/(4a) = {c} - ({b})²/(4·{a}) = {c} - {b * b}/({4 * a}) = {k}\n"
        f"Vertice V = ({h}, {k})."
    )
    tip = (
        "Il vertice di una parabola y = ax² + bx + c ha coordinate "
        "V = (-b/(2a), c - b²/(4a))."
    )
    return question, correct_str, distractors, explanation, tip


def _t1_parabola_intersections_x():
    """Find x-axis intersections of y = a(x - r1)(x - r2)."""
    a = random.choice([i for i in range(-3, 4) if i != 0])
    r1 = random.randint(-5, 5)
    r2 = random.randint(-5, 5)
    while r1 == r2:
        r2 = random.randint(-5, 5)
    # Order roots
    if r1 > r2:
        r1, r2 = r2, r1

    # Expand: y = a(x^2 - (r1+r2)x + r1*r2) = ax^2 + bx + c
    b_coeff = -a * (r1 + r2)
    c_coeff = a * r1 * r2
    eq = _fmt_parabola_eq(a, b_coeff, c_coeff)

    correct_str = f"({r1}, 0) e ({r2}, 0)"

    dists = set()
    dists.add(f"({-r1}, 0) e ({-r2}, 0)")
    xv = (r1 + r2) / 2
    if abs(xv - round(xv)) < 1e-9:
        dists.add(f"({int(round(xv))}, 0)")
    dists.add(f"({r1}, 0)")
    dists.add(f"(0, {c_coeff})")
    dists.add(f"({-r2}, 0) e ({-r1}, 0)")
    dists.add(f"({r1 + 1}, 0) e ({r2 - 1}, 0)")
    dists.discard(correct_str)
    distractors = list(dists)[:4]
    while len(distractors) < 4:
        distractors.append(f"({r1 - len(distractors)}, 0) e ({r2 + len(distractors)}, 0)")

    question = f"Quali sono le intersezioni con l'asse x della parabola {eq}?"
    explanation = (
        f"Poniamo y = 0: {a}(x - {r1})(x - {r2}) = 0\n"
        f"Le soluzioni sono x = {r1} e x = {r2}.\n"
        f"Le intersezioni sono ({r1}, 0) e ({r2}, 0)."
    )
    tip = (
        "Per trovare le intersezioni con l'asse x, si pone y = 0 e si risolvono "
        "le soluzioni dell'equazione di secondo grado."
    )
    return question, correct_str, distractors, explanation, tip


def _t2_parabola_equation_from_vertex():
    """Given vertex and a point, find the parabola equation."""
    h = random.randint(-4, 4)
    k = random.randint(-4, 4)
    # Pick a point (x0, y0) such that a = (y0 - k) / (x0 - h)^2 is integer
    x0 = h + random.choice([i for i in range(-3, 4) if i != 0])
    dx_sq = (x0 - h) ** 2
    a = random.choice([i for i in range(-3, 4) if i != 0])
    y0 = a * dx_sq + k

    # Build correct equation string in vertex form and expanded form
    b = -2 * a * h
    c = a * h * h + k
    correct_str = _fmt_parabola_eq(a, b, c)

    dists = set()
    # Wrong sign of a
    dists.add(_fmt_parabola_eq(-a, 2 * a * h, -a * h * h + k))
    # Wrong a value
    for da in [-1, 1, 2]:
        if a + da != 0:
            wrong_b = -2 * (a + da) * h
            wrong_c = (a + da) * h * h + k
            dists.add(_fmt_parabola_eq(a + da, wrong_b, wrong_c))
    # Forgot vertex shift
    dists.add(_fmt_parabola_eq(a, 0, k))
    dists.discard(correct_str)
    distractors = list(dists)[:4]
    while len(distractors) < 4:
        filler_a = a + len(distractors) + 1
        distractors.append(_fmt_parabola_eq(filler_a, -2 * filler_a * h, filler_a * h * h + k))

    question = (
        f"Trova l'equazione della parabola con vertice V({h}, {k}) "
        f"passante per P({x0}, {y0})."
    )
    explanation = (
        f"Forma del vertice: y = a(x - {h})² + {k}\n"
        f"Sostituiamo P({x0}, {y0}): {y0} = a({x0} - {h})² + {k}\n"
        f"{y0} = a·{dx_sq} + {k}\n"
        f"a = ({y0} - {k}) / {dx_sq} = {y0 - k}/{dx_sq} = {a}\n"
        f"L'equazione è: {correct_str}."
    )
    tip = (
        "Dalla forma del vertice y = a(x - h)² + k, sostituisci le coordinate "
        "di un punto noto per trovare il valore di a, poi espandi."
    )
    return question, correct_str, distractors, explanation, tip


def _t2_parabola_axis_direction():
    """Identify axis of symmetry and opening direction of a parabola."""
    variant = random.choice(["vertical", "horizontal"])

    if variant == "vertical":
        # y = ax^2 + bx + c
        a = random.choice([i for i in range(-3, 4) if i != 0])
        h = random.randint(-4, 4)
        k = random.randint(-4, 4)
        b = -2 * a * h
        c = a * h * h + k
        eq = _fmt_parabola_eq(a, b, c)
        direction = "alto" if a > 0 else "basso"
        correct_str = f"Asse x = {h}, aperta verso l'{direction}"
        wrong_dir = "basso" if a > 0 else "alto"
        dists = set()
        dists.add(f"Asse x = {h}, aperta verso l'{wrong_dir}")
        dists.add(f"Asse y = {k}, aperta verso destra")
        dists.add(f"Asse y = {k}, aperta verso sinistra")
        dists.add(f"Asse x = {-h}, aperta verso l'{direction}")
        dists.add(f"Asse x = {b}, aperta verso l'{direction}")
    else:
        # x = ay^2 + by + c
        a = random.choice([i for i in range(-3, 4) if i != 0])
        k = random.randint(-4, 4)
        h = random.randint(-4, 4)
        b = -2 * a * k
        c = a * k * k + h
        # Format: x = ay² + by + c
        eq = _fmt_parabola_eq_horizontal(a, b, c)
        direction = "destra" if a > 0 else "sinistra"
        correct_str = f"Asse y = {k}, aperta verso {direction}"
        wrong_dir = "sinistra" if a > 0 else "destra"
        dists = set()
        dists.add(f"Asse y = {k}, aperta verso {wrong_dir}")
        dists.add(f"Asse x = {h}, aperta verso l'alto")
        dists.add(f"Asse x = {h}, aperta verso il basso")
        dists.add(f"Asse y = {-k}, aperta verso {direction}")
        dists.add(f"Asse y = {b}, aperta verso {direction}")

    dists.discard(correct_str)
    distractors = list(dists)[:4]
    while len(distractors) < 4:
        distractors.append(f"Asse x = {h + len(distractors)}, aperta verso l'alto")

    question = (
        f"Qual è l'asse di simmetria e la direzione di apertura della parabola {eq}?"
    )
    explanation = (
        f"L'equazione è {eq}.\n"
        f"La risposta corretta è: {correct_str}."
    )
    tip = (
        "Per y = ax² + bx + c l'asse è verticale x = -b/(2a) e si apre verso l'alto (a>0) "
        "o il basso (a<0). Per x = ay² + by + c l'asse è orizzontale y = -b/(2a) e si apre "
        "verso destra (a>0) o sinistra (a<0)."
    )
    return question, correct_str, distractors, explanation, tip


def _t3_parabola_line_intersection():
    """Find the sum of x-coordinates of intersection points between parabola and line."""
    a = random.choice([i for i in range(-3, 4) if i != 0])
    # Pick integer roots for the resulting quadratic
    s1 = random.randint(-4, 4)
    s2 = random.randint(-4, 4)
    while s1 == s2:
        s2 = random.randint(-4, 4)

    # The quadratic a*x^2 + (b-m)*x + (c-q) = 0 has roots s1, s2
    # So (b-m) = -a*(s1+s2) and (c-q) = a*s1*s2
    # Pick m and derive b, pick q and derive c
    m = random.randint(-3, 3)
    b = -a * (s1 + s2) + m
    q = random.randint(-5, 5)
    c = a * s1 * s2 + q

    parabola_eq = _fmt_parabola_eq(a, b, c)
    line_eq = _fmt_eq(m, q)

    sum_x = s1 + s2
    correct_value = float(sum_x)

    question = (
        f"Trova la somma delle ascisse dei punti di intersezione tra la parabola "
        f"{parabola_eq} e la retta {line_eq}."
    )
    explanation = (
        f"Poniamo {a}x² + {b}x + {c} = {m}x + {q}\n"
        f"{a}x² + ({b}-{m})x + ({c}-{q}) = 0\n"
        f"{a}x² + {b - m}x + {c - q} = 0\n"
        f"Per Vieta, la somma delle radici = -{b - m}/{a} = {sum_x}.\n"
        f"Le radici sono x = {s1} e x = {s2}, somma = {sum_x}."
    )
    tip = (
        "Per trovare le intersezioni tra parabola e retta, metti a sistema le equazioni. "
        "La somma delle radici si può calcolare con la formula di Vieta: x1 + x2 = -B/A."
    )
    return question, correct_value, explanation, tip


def _t3_parabola_tangent():
    """Find the tangent line to y = ax^2 + bx + c at a given x0."""
    a = random.choice([i for i in range(-3, 4) if i != 0])
    b = random.randint(-4, 4)
    c = random.randint(-4, 4)
    x0 = random.randint(-3, 3)

    # Tangent slope: y' = 2ax0 + b
    m_tan = 2 * a * x0 + b
    # y-value at x0
    y0 = a * x0 * x0 + b * x0 + c
    # Tangent: y = m_tan * (x - x0) + y0 = m_tan * x + (y0 - m_tan * x0)
    q_tan = y0 - m_tan * x0

    parabola_eq = _fmt_parabola_eq(a, b, c)
    correct_str = _fmt_eq(m_tan, q_tan)

    dists = set()
    # Common error: using ax0 + b instead of 2ax0 + b
    wrong_m1 = a * x0 + b
    dists.add(_fmt_eq(wrong_m1, y0 - wrong_m1 * x0))
    # Wrong intercept
    dists.add(_fmt_eq(m_tan, q_tan + 1))
    dists.add(_fmt_eq(m_tan, q_tan - 1))
    # Secant-like error
    dists.add(_fmt_eq(m_tan + a, q_tan - a))
    dists.add(_fmt_eq(-m_tan, -q_tan))
    dists.discard(correct_str)
    distractors = list(dists)[:4]
    while len(distractors) < 4:
        distractors.append(_fmt_eq(m_tan + len(distractors) + 1, q_tan))

    question = (
        f"Trova l'equazione della retta tangente alla parabola {parabola_eq} "
        f"nel punto di ascissa x = {x0}."
    )
    explanation = (
        f"La derivata di y = {a}x² + {b}x + {c} è y' = {2 * a}x + {b}.\n"
        f"Nel punto x = {x0}: y'({x0}) = {2 * a}·{x0} + {b} = {m_tan}.\n"
        f"Il punto è ({x0}, {y0}).\n"
        f"La tangente è: y - {y0} = {m_tan}(x - {x0})\n"
        f"y = {m_tan}x + {_fmt(q_tan)}\n"
        f"L'equazione è: {correct_str}."
    )
    tip = (
        "La tangente alla parabola y = ax² + bx + c nel punto x₀ ha pendenza "
        "m = 2ax₀ + b (derivata). Poi si usa la formula punto-pendenza."
    )
    return question, correct_str, distractors, explanation, tip


def _t3_combined_problem():
    """Given two lines, find their intersection, then compute distance to a given point."""
    # Line 1: y = m1*x + q1
    m1 = random.choice([1, -1, 2, -2])
    q1 = random.randint(-4, 4)

    # Line 2: y = m2*x + q2, with m2 != m1 for unique intersection
    m2 = random.choice([i for i in [1, -1, 2, -2, 3, -3] if i != m1])
    q2 = random.randint(-4, 4)

    # Intersection: m1*x + q1 = m2*x + q2 => x = (q2 - q1) / (m1 - m2)
    x_int_num = q2 - q1
    x_int_den = m1 - m2
    # Ensure integer intersection
    while x_int_num % x_int_den != 0:
        q2 = random.randint(-4, 4)
        x_int_num = q2 - q1
        if m1 - m2 == 0:
            m2 = random.choice([i for i in [1, -1, 2, -2, 3, -3] if i != m1])
        x_int_den = m1 - m2

    xi = x_int_num // x_int_den
    yi = m1 * xi + q1

    # Target point
    px = random.randint(-5, 5)
    py = random.randint(-5, 5)
    while px == xi and py == yi:
        px = random.randint(-5, 5)

    dist_sq = (px - xi) ** 2 + (py - yi) ** 2
    dist = math.sqrt(dist_sq)

    line1_eq = _fmt_eq(m1, q1)
    line2_eq = _fmt_eq(m2, q2)

    question = (
        f"Le rette {line1_eq} e {line2_eq} si intersecano nel punto P. "
        f"Calcola la distanza da P al punto Q({px}, {py}). Arrotonda a due decimali."
    )
    explanation = (
        f"Troviamo l'intersezione:\n"
        f"{m1}x + {q1} = {m2}x + {q2}\n"
        f"({m1} - {m2})x = {q2} - {q1}\n"
        f"x = {x_int_num}/{x_int_den} = {_fmt(xi)}\n"
        f"y = {m1} * {xi} + {q1} = {_fmt(yi)}\n"
        f"P = ({_fmt(xi)}, {_fmt(yi)})\n"
        f"Distanza PQ = sqrt(({px} - {xi})^2 + ({py} - {yi})^2)\n"
        f"= sqrt({(px - xi) ** 2} + {(py - yi) ** 2}) = sqrt({dist_sq}) = {_fmt(dist)}."
    )
    tip = (
        "Per trovare l'intersezione di due rette, metti a sistema le due equazioni. "
        "Poi usa la formula della distanza tra due punti."
    )
    return question, dist, explanation, tip


# ---------------------------------------------------------------------------
# Template registries
# ---------------------------------------------------------------------------

# String templates: return (question, correct_str, distractors_list, explanation, tip)
_STRING_TEMPLATES_L1 = [
    _t1_line_from_point_slope,
    _t1_parabola_vertex,
    _t1_parabola_intersections_x,
]

# Numeric templates: return (question, correct_value, explanation, tip)
_NUMERIC_TEMPLATES_L1 = [
    _t1_distance_two_points,
    _t1_midpoint,
]

_STRING_TEMPLATES_L2 = [
    _t2_parallel_perpendicular,
    _t2_line_through_two_points,
    _t2_segment_bisector,
    _t2_parabola_equation_from_vertex,
    _t2_parabola_axis_direction,
]

_NUMERIC_TEMPLATES_L2 = []

_STRING_TEMPLATES_L3 = [
    _t3_circle_equation,
    _t3_parabola_tangent,
]

_NUMERIC_TEMPLATES_L3 = [
    _t3_line_circle_intersection,
    _t3_combined_problem,
    _t3_parabola_line_intersection,
]


class AnalyticGeometry(Exercise):
    """Geometria Analitica -- rette, distanze e circonferenze nel piano."""

    TEMPLATES_L1_STRING = _STRING_TEMPLATES_L1
    TEMPLATES_L1_NUMERIC = _NUMERIC_TEMPLATES_L1
    TEMPLATES_L2_STRING = _STRING_TEMPLATES_L2
    TEMPLATES_L2_NUMERIC = _NUMERIC_TEMPLATES_L2
    TEMPLATES_L3_STRING = _STRING_TEMPLATES_L3
    TEMPLATES_L3_NUMERIC = _NUMERIC_TEMPLATES_L3

    def generate(self, difficulty: int) -> dict:
        difficulty = max(1, min(3, difficulty))

        if difficulty == 1:
            all_templates = (
                [(t, "string") for t in self.TEMPLATES_L1_STRING]
                + [(t, "numeric") for t in self.TEMPLATES_L1_NUMERIC]
            )
        elif difficulty == 2:
            all_templates = (
                [(t, "string") for t in self.TEMPLATES_L2_STRING]
                + [(t, "numeric") for t in self.TEMPLATES_L2_NUMERIC]
            )
        else:
            all_templates = (
                [(t, "string") for t in self.TEMPLATES_L3_STRING]
                + [(t, "numeric") for t in self.TEMPLATES_L3_NUMERIC]
            )

        template_fn, ttype = random.choice(all_templates)

        if ttype == "string":
            question, correct_str, distractors, explanation, tip = template_fn()
            options = [correct_str] + distractors[:4]
            correct_index = 0
            options, correct_index = Exercise.shuffle_options(options, correct_index)
        else:
            question, correct_value, explanation, tip = template_fn()
            correct_str = _fmt(correct_value)
            distractors = _make_distractors(correct_value)
            options = [correct_str] + distractors[:4]
            correct_index = 0
            options, correct_index = Exercise.shuffle_options(options, correct_index)

        return {
            "question": question,
            "options": options,
            "correct_index": correct_index,
            "explanation": explanation,
            "did_you_know": tip,
            "difficulty": difficulty,
        }
