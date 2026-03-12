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


def _interval_str(intervals):
    """Convert a list of interval tuples to proper mathematical notation.

    Each tuple: (low, high, low_inclusive, high_inclusive)
    Special values: math.inf / -math.inf for unbounded.
    Empty list means no solution. None means all reals.
    """
    if intervals is None:
        return "\u2200x \u2208 \u211d"  # ∀x ∈ ℝ
    if len(intervals) == 0:
        return "Nessuna soluzione"

    parts = []
    for low, high, low_inc, high_inc in intervals:
        left_bracket = "[" if low_inc else "("
        right_bracket = "]" if high_inc else ")"
        low_str = "-\u221e" if low == -math.inf else _fmt(low)
        high_str = "+\u221e" if high == math.inf else _fmt(high)
        # Infinities are never inclusive
        if low == -math.inf:
            left_bracket = "("
        if high == math.inf:
            right_bracket = ")"
        parts.append(f"x \u2208 {left_bracket}{low_str}, {high_str}{right_bracket}")

    return " \u222a ".join(parts)


def _interval_str_exclude(value):
    """Return notation for all reals except a single point: x ∈ ℝ \\ {value}."""
    return f"x \u2208 \u211d \\ {{{_fmt(value)}}}"


def _make_interval_distractors(correct_str, boundaries=None, count=4):
    """Generate plausible wrong interval answers.

    Args:
        correct_str: The correct interval string.
        boundaries: List of numeric boundary values used in the correct answer.
        count: Number of distractors to generate.
    """
    distractors = set()

    if boundaries is None:
        boundaries = []

    # Strategy 1: Flip open/closed brackets
    flipped = correct_str
    replacements = [("[", "("), ("]", ")"), ("(", "["), (")", "]")]
    for old, new in replacements:
        candidate = correct_str.replace(old, new, 1)
        if candidate != correct_str:
            distractors.add(candidate)

    # Strategy 2: Shift boundaries by +-1
    for b in boundaries:
        for offset in [-1, 1]:
            shifted = correct_str.replace(_fmt(b), _fmt(b + offset))
            if shifted != correct_str:
                distractors.add(shifted)

    # Strategy 3: Swap direction (complement-like)
    if "\u222a" not in correct_str and "Nessuna" not in correct_str and "\u2200" not in correct_str:
        # Single interval - try to create complementary intervals
        for b in boundaries:
            # If correct is (b, +inf), try (-inf, b)
            distractors.add(_interval_str([(-math.inf, b, False, False)]))
            distractors.add(_interval_str([(b, math.inf, False, False)]))
            distractors.add(_interval_str([(-math.inf, b, False, True)]))
            distractors.add(_interval_str([(b, math.inf, True, False)]))

    # Strategy 4: Use special answers as distractors
    specials = ["\u2200x \u2208 \u211d", "Nessuna soluzione"]
    for s in specials:
        if s != correct_str:
            distractors.add(s)

    # Strategy 5: For union intervals, offer individual parts
    if "\u222a" in correct_str and len(boundaries) >= 2:
        b_sorted = sorted(boundaries)
        distractors.add(_interval_str([(b_sorted[0], b_sorted[1], False, False)]))
        distractors.add(_interval_str([(b_sorted[0], b_sorted[1], True, True)]))

    # Strategy 6: If single interval with two boundaries, offer union of complement
    if "\u222a" not in correct_str and len(boundaries) >= 2:
        b_sorted = sorted(boundaries)
        distractors.add(
            _interval_str([
                (-math.inf, b_sorted[0], False, False),
                (b_sorted[1], math.inf, False, False),
            ])
        )

    distractors.discard(correct_str)

    result = list(distractors)
    random.shuffle(result)

    # If still need more, generate with shifted boundaries
    attempts = 0
    while len(result) < count and attempts < 50:
        attempts += 1
        if boundaries:
            b = random.choice(boundaries)
            offset = random.choice([-2, -1, 1, 2, 3])
            inc = random.choice([True, False])
            candidate = _interval_str([(b + offset, math.inf, inc, False)])
            if candidate != correct_str and candidate not in result:
                result.append(candidate)
            candidate = _interval_str([(-math.inf, b + offset, False, inc)])
            if candidate != correct_str and candidate not in result:
                result.append(candidate)
        else:
            v = random.randint(-5, 5)
            candidate = _interval_str([(-math.inf, v, False, False)])
            if candidate != correct_str and candidate not in result:
                result.append(candidate)

    return result[:count]


# ---------------------------------------------------------------------------
# LEVEL 1 Templates -- First degree inequalities
# ---------------------------------------------------------------------------

def _t1_linear_inequality_with_fractions():
    """Inequality like (ax + b)/c > d or (ax + b)/c <= d."""
    # Construct from boundary to guarantee integer d:
    # (ax + b)/c = d when x = boundary  =>  d = (a*boundary + b) / c
    # Pick a, c first, then boundary, then compute b so that d is integer.
    a = random.choice([i for i in range(-6, 7) if i != 0])
    c = random.choice([i for i in range(-6, 7) if i != 0])
    boundary = random.randint(-8, 8)
    # d = (a*boundary + b) / c must be integer, so pick d first and derive b
    d = random.randint(-8, 8)
    # b = c*d - a*boundary
    b = c * d - a * boundary

    op_symbol = random.choice([">", "<", "\u2265", "\u2264"])
    op_name = {">" : "maggiore", "<": "minore", "\u2265": "maggiore o uguale", "\u2264": "minore o uguale"}

    # Solve: (ax + b)/c op d
    # ax + b op*sign(c) cd
    # ax op*sign(c) cd - b
    # x op*sign(c)*sign(a) (cd - b)/a = boundary
    # Determine effective comparison after dividing by a and c
    flips = 0
    if c < 0:
        flips += 1
    if a < 0:
        flips += 1

    # Map original operator through flips
    effective_op = op_symbol
    if flips == 1:
        flip_map = {">": "<", "<": ">", "\u2265": "\u2264", "\u2264": "\u2265"}
        effective_op = flip_map[op_symbol]

    # Build solution intervals
    if effective_op == ">":
        intervals = [(boundary, math.inf, False, False)]
    elif effective_op == "<":
        intervals = [(-math.inf, boundary, False, False)]
    elif effective_op == "\u2265":
        intervals = [(boundary, math.inf, True, False)]
    else:  # ≤
        intervals = [(-math.inf, boundary, False, True)]

    correct_str = _interval_str(intervals)

    sign_b = f"+ {b}" if b >= 0 else f"- {abs(b)}"
    question = f"Risolvi la disequazione ({a}x {sign_b}) / {c} {op_symbol} {d}."

    explanation = (
        f"Moltiplichiamo entrambi i membri per {c}"
        f"{' (negativo, il verso cambia)' if c < 0 else ''}:\n"
        f"{a}x {sign_b} {'<' if c < 0 else '>'} {c * d} (se op era {op_symbol})\n"
        f"Isoliamo x: {a}x {'>' if (c > 0) == (op_symbol in ['>', '\u2265']) else '<'} {c * d - b}\n"
        f"x = {_fmt(boundary)} con verso "
        f"{'invertito' if flips == 1 else 'conservato'}.\n"
        f"Soluzione: {correct_str}."
    )

    tip = ("Quando moltiplichi o dividi una disequazione per un numero negativo, "
           "il verso della disuguaglianza si inverte.")

    distractors = _make_interval_distractors(correct_str, boundaries=[boundary])
    return question, correct_str, distractors, explanation, tip


def _t1_linear_inequality_with_parentheses():
    """Inequality like a(bx + c) - d > ex + f."""
    a = random.choice([i for i in range(-5, 6) if i != 0])
    b_coeff = random.choice([i for i in range(-4, 5) if i != 0])
    c = random.randint(-8, 8)
    d = random.randint(-10, 10)
    e = random.choice([i for i in range(-5, 6) if i != 0])

    # a(bx + c) - d > ex + f
    # abx + ac - d > ex + f
    # (ab - e)x > f - ac + d
    coeff_x = a * b_coeff - e
    # Ensure non-zero coefficient for x
    while coeff_x == 0:
        e = random.choice([i for i in range(-5, 6) if i != 0])
        coeff_x = a * b_coeff - e

    # Pick boundary first, derive f to guarantee integer boundary
    # boundary = (f - a*c + d) / coeff_x  =>  f = coeff_x * boundary + a*c - d
    boundary = random.randint(-8, 8)
    f = coeff_x * boundary + a * c - d
    rhs = f - a * c + d

    op_symbol = random.choice([">", "<", "\u2265", "\u2264"])

    effective_op = op_symbol
    if coeff_x < 0:
        flip_map = {">": "<", "<": ">", "\u2265": "\u2264", "\u2264": "\u2265"}
        effective_op = flip_map[op_symbol]

    if effective_op == ">":
        intervals = [(boundary, math.inf, False, False)]
    elif effective_op == "<":
        intervals = [(-math.inf, boundary, False, False)]
    elif effective_op == "\u2265":
        intervals = [(boundary, math.inf, True, False)]
    else:
        intervals = [(-math.inf, boundary, False, True)]

    correct_str = _interval_str(intervals)

    sign_c = f"+ {c}" if c >= 0 else f"- {abs(c)}"
    sign_d = f"- {d}" if d >= 0 else f"+ {abs(d)}"
    sign_f = f"+ {f}" if f >= 0 else f"- {abs(f)}"

    question = (
        f"Risolvi la disequazione "
        f"{a}({b_coeff}x {sign_c}) {sign_d} {op_symbol} {e}x {sign_f}."
    )

    explanation = (
        f"Espandiamo: {a * b_coeff}x + {a * c} - {d} {op_symbol} {e}x + {f}\n"
        f"Raccogliamo x: ({a * b_coeff} - {e})x {op_symbol} {f} - {a * c} + {d}\n"
        f"{coeff_x}x {op_symbol} {rhs}\n"
        f"x {effective_op} {_fmt(boundary)}"
        f"{' (verso invertito perche dividiamo per negativo)' if coeff_x < 0 else ''}.\n"
        f"Soluzione: {correct_str}."
    )

    tip = ("Per risolvere disequazioni con parentesi, prima espandi, "
           "poi raccogli i termini con x da un lato e i numeri dall'altro.")

    distractors = _make_interval_distractors(correct_str, boundaries=[boundary])
    return question, correct_str, distractors, explanation, tip


# ---------------------------------------------------------------------------
# LEVEL 2 Templates -- Second degree inequalities
# ---------------------------------------------------------------------------

def _t2_quadratic_positive_delta():
    """ax^2 + bx + c > 0 (or <, >=, <=) with delta > 0, two real roots."""
    x1 = random.randint(-6, 6)
    x2 = random.randint(-6, 6)
    while x1 == x2:
        x2 = random.randint(-6, 6)
    if x1 > x2:
        x1, x2 = x2, x1

    a = random.choice([1, 1, 1, -1, 2, -2])
    # a(x - x1)(x - x2) = ax^2 - a(x1+x2)x + a*x1*x2
    b_coeff = -a * (x1 + x2)
    c_coeff = a * x1 * x2

    op_symbol = random.choice([">", "<", "\u2265", "\u2264"])
    strict = op_symbol in [">", "<"]

    # For a > 0: parabola opens up, ax^2+bx+c < 0 between roots, > 0 outside
    # For a < 0: parabola opens down, opposite
    if a > 0:
        if op_symbol == ">":
            intervals = [(-math.inf, x1, False, False), (x2, math.inf, False, False)]
        elif op_symbol == "\u2265":
            intervals = [(-math.inf, x1, False, True), (x2, math.inf, True, False)]
        elif op_symbol == "<":
            intervals = [(x1, x2, False, False)]
        else:  # ≤
            intervals = [(x1, x2, True, True)]
    else:  # a < 0
        if op_symbol == ">":
            intervals = [(x1, x2, False, False)]
        elif op_symbol == "\u2265":
            intervals = [(x1, x2, True, True)]
        elif op_symbol == "<":
            intervals = [(-math.inf, x1, False, False), (x2, math.inf, False, False)]
        else:  # ≤
            intervals = [(-math.inf, x1, False, True), (x2, math.inf, True, False)]

    correct_str = _interval_str(intervals)

    sign_b = f"+ {b_coeff}" if b_coeff >= 0 else f"- {abs(b_coeff)}"
    sign_c = f"+ {c_coeff}" if c_coeff >= 0 else f"- {abs(c_coeff)}"
    a_str = "" if a == 1 else ("-" if a == -1 else f"{a}")

    question = (
        f"Risolvi la disequazione {a_str}x\u00b2 {sign_b}x {sign_c} {op_symbol} 0."
    )

    explanation = (
        f"Troviamo le radici: {a_str}x\u00b2 {sign_b}x {sign_c} = 0\n"
        f"Le radici sono x\u2081 = {x1} e x\u2082 = {x2}.\n"
        f"Il coefficiente di x\u00b2 e' {'positivo' if a > 0 else 'negativo'}, "
        f"quindi la parabola apre verso {'l alto' if a > 0 else 'il basso'}.\n"
        f"Studiando il segno: {correct_str}."
    )

    tip = ("Per le disequazioni di 2\u00b0 grado, trova le radici e studia il segno "
           "del polinomio considerando la concavita' della parabola.")

    distractors = _make_interval_distractors(correct_str, boundaries=[x1, x2])
    return question, correct_str, distractors, explanation, tip


def _t2_quadratic_zero_delta():
    """ax^2 + bx + c >= 0 (or >, <, <=) with delta = 0, double root."""
    x0 = random.randint(-6, 6)
    a = random.choice([1, 1, -1, 2, -2])
    # a(x - x0)^2 = ax^2 - 2a*x0*x + a*x0^2
    b_coeff = -2 * a * x0
    c_coeff = a * x0 * x0

    op_symbol = random.choice([">", "<", "\u2265", "\u2264"])

    # a(x-x0)^2 is always >= 0 if a > 0, always <= 0 if a < 0
    # Equals zero only at x = x0
    if a > 0:
        # Expression >= 0 always, = 0 only at x0
        if op_symbol == ">":
            # > 0: all reals except x0
            correct_str = _interval_str_exclude(x0)
        elif op_symbol == "\u2265":
            # >= 0: all reals
            correct_str = _interval_str(None)
        elif op_symbol == "<":
            # < 0: never
            correct_str = _interval_str([])
        else:  # ≤
            # <= 0: only at x0
            correct_str = f"x = {_fmt(x0)}"
    else:  # a < 0
        # Expression <= 0 always, = 0 only at x0
        if op_symbol == ">":
            correct_str = _interval_str([])
        elif op_symbol == "\u2265":
            correct_str = f"x = {_fmt(x0)}"
        elif op_symbol == "<":
            correct_str = _interval_str_exclude(x0)
        else:  # ≤
            correct_str = _interval_str(None)

    sign_b = f"+ {b_coeff}" if b_coeff >= 0 else f"- {abs(b_coeff)}"
    sign_c = f"+ {c_coeff}" if c_coeff >= 0 else f"- {abs(c_coeff)}"
    a_str = "" if a == 1 else ("-" if a == -1 else f"{a}")

    question = (
        f"Risolvi la disequazione {a_str}x\u00b2 {sign_b}x {sign_c} {op_symbol} 0."
    )

    explanation = (
        f"Il discriminante e' \u0394 = 0, con radice doppia x\u2080 = {x0}.\n"
        f"L'espressione si riscrive come {a_str}(x - {x0})\u00b2.\n"
        f"Poiche' a {'> 0' if a > 0 else '< 0'}, "
        f"l'espressione e' sempre {'\u2265 0' if a > 0 else '\u2264 0'} "
        f"e si annulla solo per x = {x0}.\n"
        f"Soluzione: {correct_str}."
    )

    tip = ("Quando il discriminante e' zero, il trinomio e' un quadrato perfetto: "
           "a(x - x\u2080)\u00b2. Il suo segno dipende solo dal segno di a.")

    distractors = _make_interval_distractors(
        correct_str, boundaries=[x0],
    )
    # Add specific distractors for zero-delta cases
    extra = []
    if correct_str == _interval_str(None):
        extra.append(_interval_str([]))
        extra.append(f"x = {_fmt(x0)}")
    elif correct_str == _interval_str([]):
        extra.append(_interval_str(None))
        extra.append(f"x = {_fmt(x0)}")
    elif correct_str.startswith("x ="):
        extra.append(_interval_str(None))
        extra.append(_interval_str([]))
    elif "\\\\" in correct_str:  # exclude point notation
        extra.append(_interval_str(None))
        extra.append(f"x = {_fmt(x0)}")

    for e in extra:
        if e != correct_str and e not in distractors:
            distractors.append(e)

    return question, correct_str, distractors, explanation, tip


def _t2_quadratic_negative_delta():
    """ax^2 + bx + c > 0 (or <, >=, <=) with delta < 0."""
    a = random.choice([1, 1, 2, -1, -2])
    # Need b^2 - 4ac < 0. Pick small b, large enough |c| with same sign as a.
    b_coeff = random.randint(-3, 3)
    # Need 4ac > b^2, so c > b^2/(4a) if a > 0, or c < b^2/(4a) if a < 0
    min_c = (b_coeff * b_coeff) // (4 * abs(a)) + 1
    if a > 0:
        c_coeff = random.randint(min_c, min_c + 5)
    else:
        c_coeff = random.randint(-min_c - 5, -min_c)

    # Verify delta < 0
    delta = b_coeff * b_coeff - 4 * a * c_coeff
    while delta >= 0:
        if a > 0:
            c_coeff += 1
        else:
            c_coeff -= 1
        delta = b_coeff * b_coeff - 4 * a * c_coeff

    op_symbol = random.choice([">", "<", "\u2265", "\u2264"])

    # No real roots. Expression has same sign as a everywhere.
    if a > 0:
        # Always positive
        if op_symbol in [">", "\u2265"]:
            correct_str = _interval_str(None)  # ∀x ∈ ℝ
        else:
            correct_str = _interval_str([])  # Nessuna soluzione
    else:
        # Always negative
        if op_symbol in ["<", "\u2264"]:
            correct_str = _interval_str(None)
        else:
            correct_str = _interval_str([])

    sign_b = f"+ {b_coeff}" if b_coeff >= 0 else f"- {abs(b_coeff)}"
    sign_c = f"+ {c_coeff}" if c_coeff >= 0 else f"- {abs(c_coeff)}"
    a_str = "" if a == 1 else ("-" if a == -1 else f"{a}")

    question = (
        f"Risolvi la disequazione {a_str}x\u00b2 {sign_b}x {sign_c} {op_symbol} 0."
    )

    explanation = (
        f"Calcoliamo il discriminante: \u0394 = ({b_coeff})\u00b2 - 4\u00b7{a}\u00b7{c_coeff} = {delta}.\n"
        f"Poiche' \u0394 < 0, non ci sono radici reali.\n"
        f"Il coefficiente di x\u00b2 e' {'positivo' if a > 0 else 'negativo'}, "
        f"quindi l'espressione e' sempre {'positiva' if a > 0 else 'negativa'}.\n"
        f"Soluzione: {correct_str}."
    )

    tip = ("Quando \u0394 < 0, il trinomio non ha radici reali e mantiene "
           "sempre lo stesso segno, determinato dal coefficiente di x\u00b2.")

    # Distractors: the other special answer plus some fake intervals
    distractors = []
    if correct_str == _interval_str(None):
        distractors.append(_interval_str([]))
    else:
        distractors.append(_interval_str(None))

    # Add some plausible-looking intervals as distractors
    fake_root = random.randint(-4, 4)
    distractors.append(_interval_str([(-math.inf, fake_root, False, False)]))
    distractors.append(_interval_str([(fake_root, math.inf, False, False)]))
    distractors.append(
        _interval_str([(-math.inf, fake_root, False, False), (fake_root + 2, math.inf, False, False)])
    )

    return question, correct_str, distractors, explanation, tip


# ---------------------------------------------------------------------------
# LEVEL 3 Templates -- Rational and systems
# ---------------------------------------------------------------------------

def _t3_rational_inequality():
    """(ax + b)/(cx + d) > 0 (or >=, <, <=). Study sign of numerator and denominator."""
    # Construct from zeros to guarantee integer roots:
    # numerator zero: x_n, so b = -a * x_n
    # denominator zero: x_d, so d = -c * x_d
    a = random.choice([i for i in range(-5, 6) if i != 0])
    c_val = random.choice([i for i in range(-5, 6) if i != 0])
    x_n = random.randint(-8, 8)
    x_d = random.randint(-8, 8)
    while x_n == x_d:
        x_d = random.randint(-8, 8)
    b = -a * x_n
    d = -c_val * x_d

    op_symbol = random.choice([">", "<", "\u2265", "\u2264"])
    strict = op_symbol in [">", "<"]
    want_positive = op_symbol in [">", "\u2265"]

    # Sign study: the expression changes sign at x_n and x_d
    # Need to determine sign in each interval
    points = sorted([x_n, x_d])
    p1, p2 = points

    # Test sign in interval (-inf, p1): pick test point p1 - 1
    def sign_at(x):
        num = a * x + b
        den = c_val * x + d
        if den == 0:
            return 0
        return 1 if (num * den) > 0 else -1

    sign_left = sign_at(p1 - 1)
    sign_mid = sign_at((p1 + p2) / 2) if p1 != p2 else 0
    sign_right = sign_at(p2 + 1)

    # Determine which point is the numerator zero and which is denominator zero
    # x_d is excluded (denominator = 0), x_n may be included for non-strict
    intervals = []
    if want_positive:
        # We want expression > 0 or >= 0
        if sign_left > 0:
            intervals.append((-math.inf, p1, False, False))
        if sign_mid > 0 and p1 != p2:
            intervals.append((p1, p2, False, False))
        if sign_right > 0:
            intervals.append((p2, math.inf, False, False))
    else:
        # We want expression < 0 or <= 0
        if sign_left < 0:
            intervals.append((-math.inf, p1, False, False))
        if sign_mid < 0 and p1 != p2:
            intervals.append((p1, p2, False, False))
        if sign_right < 0:
            intervals.append((p2, math.inf, False, False))

    # Adjust inclusivity: x_n can be included for non-strict, x_d never
    if not strict:
        for i, (lo, hi, lo_inc, hi_inc) in enumerate(intervals):
            if lo == x_n:
                intervals[i] = (lo, hi, True, hi_inc)
            if hi == x_n:
                intervals[i] = (lo, hi, lo_inc, True)
    # x_d is never included (denominator zero)
    for i, (lo, hi, lo_inc, hi_inc) in enumerate(intervals):
        if lo == x_d:
            intervals[i] = (lo, hi, False, hi_inc)
        if hi == x_d:
            intervals[i] = (lo, hi, lo_inc, False)

    if len(intervals) == 0:
        # Check if x_n should be a point solution for >= or <=
        if not strict and sign_at(x_n) == 0:
            # The expression equals 0 at x_n, which satisfies >= 0 or <= 0
            correct_str = f"x = {_fmt(x_n)}"
        else:
            correct_str = _interval_str([])
    else:
        correct_str = _interval_str(intervals)

    sign_b = f"+ {b}" if b >= 0 else f"- {abs(b)}"
    sign_d = f"+ {d}" if d >= 0 else f"- {abs(d)}"

    question = (
        f"Risolvi la disequazione ({a}x {sign_b}) / ({c_val}x {sign_d}) {op_symbol} 0."
    )

    explanation = (
        f"Numeratore = 0: {a}x {sign_b} = 0 \u21d2 x = {x_n}\n"
        f"Denominatore = 0: {c_val}x {sign_d} = 0 \u21d2 x = {x_d} (escluso!)\n"
        f"Studiamo il segno nei tre intervalli:\n"
        f"  x < {p1}: segno {'positivo' if sign_left > 0 else 'negativo'}\n"
        f"  {p1} < x < {p2}: segno {'positivo' if sign_mid > 0 else 'negativo'}\n"
        f"  x > {p2}: segno {'positivo' if sign_right > 0 else 'negativo'}\n"
        f"Soluzione: {correct_str}."
    )

    tip = ("Per le disequazioni fratte, studia separatamente il segno del numeratore e "
           "del denominatore, poi combina i risultati. Il denominatore non puo' mai essere zero.")

    distractors = _make_interval_distractors(correct_str, boundaries=[x_n, x_d])
    return question, correct_str, distractors, explanation, tip


def _t3_system_of_inequalities():
    """System of two linear inequalities. Find intersection of solution sets."""
    # Construct from bounds to guarantee integer boundaries:
    # a*x + b = 0  =>  x = -b/a  =>  b = -a * bound
    a1 = random.choice([i for i in range(-5, 6) if i != 0])
    bound1 = random.randint(-8, 8)
    b1 = -a1 * bound1

    a2 = random.choice([i for i in range(-5, 6) if i != 0])
    bound2 = random.randint(-8, 8)
    while bound1 == bound2:
        bound2 = random.randint(-8, 8)
    b2 = -a2 * bound2

    op1 = random.choice([">", "\u2265"])
    op2 = random.choice(["<", "\u2264"])

    # Solve first: a1*x + b1 op1 0
    if a1 > 0:
        # x op1 -b1/a1
        if op1 == ">":
            sol1 = (bound1, math.inf, False, False)
        else:
            sol1 = (bound1, math.inf, True, False)
    else:
        flip = {">": "<", "\u2265": "\u2264"}
        flipped1 = flip[op1]
        if flipped1 == "<":
            sol1 = (-math.inf, bound1, False, False)
        else:
            sol1 = (-math.inf, bound1, False, True)

    # Solve second: a2*x + b2 op2 0
    if a2 > 0:
        if op2 == "<":
            sol2 = (-math.inf, bound2, False, False)
        else:
            sol2 = (-math.inf, bound2, False, True)
    else:
        flip = {"<": ">", "\u2264": "\u2265"}
        flipped2 = flip[op2]
        if flipped2 == ">":
            sol2 = (bound2, math.inf, False, False)
        else:
            sol2 = (bound2, math.inf, True, False)

    # Intersection of sol1 and sol2
    lo = max(sol1[0], sol2[0])
    hi = min(sol1[1], sol2[1])

    if sol1[0] == lo:
        lo_inc = sol1[2]
    elif sol2[0] == lo:
        lo_inc = sol2[2]
    else:
        lo_inc = sol1[2] and sol2[2]

    if sol1[0] == sol2[0]:
        lo_inc = sol1[2] and sol2[2]

    if sol1[1] == hi:
        hi_inc = sol1[3]
    elif sol2[1] == hi:
        hi_inc = sol2[3]
    else:
        hi_inc = sol1[3] and sol2[3]

    if sol1[1] == sol2[1]:
        hi_inc = sol1[3] and sol2[3]

    if lo > hi or (lo == hi and not (lo_inc and hi_inc)):
        correct_str = _interval_str([])
    else:
        correct_str = _interval_str([(lo, hi, lo_inc, hi_inc)])

    sign_b1 = f"+ {b1}" if b1 >= 0 else f"- {abs(b1)}"
    sign_b2 = f"+ {b2}" if b2 >= 0 else f"- {abs(b2)}"

    question = (
        f"Risolvi il sistema di disequazioni:\n"
        f"  {a1}x {sign_b1} {op1} 0\n"
        f"  {a2}x {sign_b2} {op2} 0"
    )

    # Describe individual solutions
    def _describe_sol(sol_tuple):
        lo_s, hi_s, li, hi_i = sol_tuple
        return _interval_str([(lo_s, hi_s, li, hi_i)])

    explanation = (
        f"Prima disequazione: {a1}x {sign_b1} {op1} 0\n"
        f"  Soluzione: {_describe_sol(sol1)}\n"
        f"Seconda disequazione: {a2}x {sign_b2} {op2} 0\n"
        f"  Soluzione: {_describe_sol(sol2)}\n"
        f"Intersezione delle soluzioni: {correct_str}."
    )

    tip = ("Per risolvere un sistema di disequazioni, risolvi ciascuna separatamente "
           "e poi trova l'intersezione delle soluzioni.")

    boundaries = [bound1, bound2]
    distractors = _make_interval_distractors(correct_str, boundaries=boundaries)

    # Also add union as distractor (common mistake)
    lo_union = min(sol1[0], sol2[0])
    hi_union = max(sol1[1], sol2[1])
    lo_union_inc = sol1[2] if sol1[0] <= sol2[0] else sol2[2]
    hi_union_inc = sol1[3] if sol1[1] >= sol2[1] else sol2[3]
    union_str = _interval_str([(lo_union, hi_union, lo_union_inc, hi_union_inc)])
    if union_str != correct_str and union_str not in distractors:
        distractors.append(union_str)

    return question, correct_str, distractors, explanation, tip


# ---------------------------------------------------------------------------
# Template registries
# ---------------------------------------------------------------------------

_TEMPLATES_L1 = [
    _t1_linear_inequality_with_fractions,
    _t1_linear_inequality_with_parentheses,
]

_TEMPLATES_L2 = [
    _t2_quadratic_positive_delta,
    _t2_quadratic_zero_delta,
    _t2_quadratic_negative_delta,
]

_TEMPLATES_L3 = [
    _t3_rational_inequality,
    _t3_system_of_inequalities,
]


class InequalitiesExercise(Exercise):
    """Disequazioni -- di 1 e 2 grado, razionali e sistemi."""

    TEMPLATES_L1 = _TEMPLATES_L1
    TEMPLATES_L2 = _TEMPLATES_L2
    TEMPLATES_L3 = _TEMPLATES_L3

    def generate(self, difficulty: int) -> dict:
        difficulty = max(1, min(3, difficulty))

        if difficulty == 1:
            templates = self.TEMPLATES_L1
        elif difficulty == 2:
            templates = self.TEMPLATES_L2
        else:
            templates = self.TEMPLATES_L3

        template_fn = random.choice(templates)
        question, correct_str, distractors, explanation, tip = template_fn()

        options = [correct_str] + distractors[:4]
        # Deduplicate while preserving order
        seen = set()
        unique_options = []
        for opt in options:
            if opt not in seen:
                seen.add(opt)
                unique_options.append(opt)
        options = unique_options

        # Ensure at least 4 options
        attempts = 0
        while len(options) < 4 and attempts < 50:
            attempts += 1
            filler = _interval_str([
                (random.randint(-8, 8), math.inf, random.choice([True, False]), False)
            ])
            if filler not in seen:
                options.append(filler)
                seen.add(filler)

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
