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


def _fmt_fraction(num, den):
    """Format a fraction, simplifying it first."""
    g = math.gcd(abs(int(num)), abs(int(den)))
    num = int(num) // g
    den = int(den) // g
    if den < 0:
        num, den = -num, -den
    if den == 1:
        return str(num)
    return f"{num}/{den}"


def _ensure_distinct_distractors(correct_str, distractors, count=4):
    """Ensure we have exactly `count` distractors all distinct from correct and each other."""
    seen = {correct_str}
    result = []
    for d in distractors:
        ds = str(d)
        if ds not in seen:
            seen.add(ds)
            result.append(ds)
        if len(result) == count:
            return result
    # Fallback: generate numeric offsets
    try:
        cv = float(correct_str.replace("/", "÷"))
    except (ValueError, ZeroDivisionError):
        cv = 10
    offset = 1
    while len(result) < count:
        candidate = _fmt(cv + offset)
        if candidate not in seen:
            seen.add(candidate)
            result.append(candidate)
        candidate = _fmt(cv - offset)
        if candidate not in seen:
            seen.add(candidate)
            result.append(candidate)
        offset += 1
    return result[:count]


# ---------------------------------------------------------------------------
# Template functions
# Each returns (question, correct_str, distractors_list, explanation, tip)
# ---------------------------------------------------------------------------

# ============ LEVEL 1 ============

def _t1_algebra_geometry_area():
    """Algebra + Geometria: rettangolo con lati espressi in x, dato il perimetro, trovare l'area."""
    # Generate coefficients for sides: (ax + b) and (cx + d)
    a = random.randint(1, 3)
    b = random.randint(1, 6)
    c = random.randint(1, 3)
    d = random.randint(-3, 5)

    # Choose x such that both sides are positive and give integer results
    x = random.randint(2, 6)
    side1 = a * x + b
    side2 = c * x + d

    # Ensure both sides are positive
    while side1 <= 0 or side2 <= 0:
        x += 1
        side1 = a * x + b
        side2 = c * x + d

    perimeter = 2 * (side1 + side2)
    area = side1 * side2

    # Format side expressions
    def _fmt_expr(coeff, const):
        if coeff == 1:
            expr = "x"
        else:
            expr = f"{coeff}x"
        if const > 0:
            expr += f" + {const}"
        elif const < 0:
            expr += f" - {abs(const)}"
        return expr

    expr1 = _fmt_expr(a, b)
    expr2 = _fmt_expr(c, d)

    question = (
        f"Un rettangolo ha lati di lunghezza ({expr1}) e ({expr2}). "
        f"Se il perimetro vale {perimeter}, qual e' l'area del rettangolo?"
    )

    correct_str = _fmt(area)

    # Distractors: common mistakes
    distractors = [
        _fmt(perimeter),                          # confuse perimeter with area
        _fmt(side1 + side2),                       # forgot to multiply, just sum
        _fmt(side1 * side2 + side1),               # arithmetic error
        _fmt(2 * side1 * side2),                   # doubled the area
        _fmt(abs(side1 - side2) * max(side1, side2)),  # wrong sides
    ]
    distractors = _ensure_distinct_distractors(correct_str, distractors)

    explanation = (
        f"Passaggio 1 (Algebra): Dal perimetro P = 2*(lato1 + lato2) = {perimeter}, "
        f"otteniamo ({expr1}) + ({expr2}) = {perimeter // 2}. "
        f"Semplificando: {a + c}x + {b + d} = {perimeter // 2}, "
        f"quindi x = {x}.\n"
        f"Passaggio 2 (Geometria): Con x = {x}, "
        f"lato1 = {a}*{x} + {b} = {side1} e lato2 = {c}*{x} + {d} = {side2}. "
        f"Area = {side1} * {side2} = {area}."
    )

    tip = (
        "Questo tipo di domanda combina algebra (risoluzione di equazioni lineari) "
        "e geometria (calcolo dell'area del rettangolo). "
        "Prima risolvi per la variabile, poi calcola la misura geometrica."
    )

    return question, correct_str, distractors, explanation, tip


# ============ LEVEL 2 ============

def _t2_quadratic_analytic_geo():
    """Algebra + Geometria Analitica: parabola passante per due punti, trovare il vertice."""
    # y = x^2 - a*x + b, passing through two symmetric points
    # Choose vertex x_v, then pick two points symmetric around it
    x_v = random.randint(1, 5)
    # Pick two x-values symmetric around x_v
    delta = random.randint(1, 3)
    x1 = x_v - delta
    x2 = x_v + delta

    # Choose a y-value for both points (they'll be equal since symmetric)
    # a = 2*x_v (from vertex formula x_v = a/2 for y = x^2 - ax + b)
    a_coeff = 2 * x_v
    # Choose b so that points have nice y-values
    b_coeff = random.randint(0, 8)
    y1 = x1 * x1 - a_coeff * x1 + b_coeff
    y2 = x2 * x2 - a_coeff * x2 + b_coeff
    # y1 should equal y2 by symmetry
    assert y1 == y2, f"Symmetry broken: y1={y1}, y2={y2}"

    y_v = x_v * x_v - a_coeff * x_v + b_coeff

    question = (
        f"La parabola y = x² - {a_coeff}x + {b_coeff} passa per i punti "
        f"({x1}, {y1}) e ({x2}, {y2}). Qual e' il vertice della parabola?"
    )

    correct_str = f"({x_v}, {y_v})"

    # Distractors
    distractors = [
        f"({x_v}, {y_v + delta})",         # wrong y_v
        f"({x_v + 1}, {y_v})",             # wrong x_v
        f"({a_coeff}, {y_v})",              # used a instead of a/2
        f"({x_v}, {-y_v})" if y_v != 0 else f"({x_v}, {y_v + 2})",  # sign error
        f"({x_v - 1}, {y_v + 1})",          # both wrong
    ]
    distractors = _ensure_distinct_distractors(correct_str, distractors)

    explanation = (
        f"Passaggio 1 (Algebra - Sistema di equazioni): "
        f"Dalla parabola y = x² - {a_coeff}x + {b_coeff}, sostituendo i punti "
        f"({x1}, {y1}) e ({x2}, {y2}) si verifica che l'equazione e' soddisfatta.\n"
        f"Passaggio 2 (Geometria Analitica - Vertice): "
        f"Per la parabola y = x² - ax + b, il vertice ha ascissa x_v = a/2 = {a_coeff}/2 = {x_v}. "
        f"Sostituendo: y_v = {x_v}² - {a_coeff}*{x_v} + {b_coeff} = "
        f"{x_v*x_v} - {a_coeff*x_v} + {b_coeff} = {y_v}. "
        f"Il vertice e' ({x_v}, {y_v})."
    )

    tip = (
        "Questo tipo di domanda combina algebra (sistemi di equazioni) "
        "e geometria analitica (formula del vertice di una parabola). "
        "Ricorda: per y = x² - ax + b, x_v = a/2."
    )

    return question, correct_str, distractors, explanation, tip


def _t2_probability_combinatorics():
    """Probabilita' + Combinatorica: estrazioni senza rimpiazzo da un mazzo."""
    # Parametrize: deck_size, suit_size, cards_drawn
    suit_options = [
        (40, 10, 3, "napoletane", "bastoni"),
        (40, 10, 2, "napoletane", "coppe"),
        (52, 13, 3, "francesi", "cuori"),
        (52, 13, 2, "francesi", "picche"),
    ]
    deck_size, suit_size, draw, deck_name, suit_name = random.choice(suit_options)

    # P = C(suit_size, draw) / C(deck_size, draw)
    numerator = math.comb(suit_size, draw)
    denominator = math.comb(deck_size, draw)

    g = math.gcd(numerator, denominator)
    frac_num = numerator // g
    frac_den = denominator // g

    correct_str = _fmt_fraction(frac_num, frac_den)

    # Wrong answer: with replacement
    wrong_replacement = f"{_fmt_fraction(suit_size**draw, deck_size**draw)}"

    # Wrong answer: wrong combinatorics (permutations instead of combinations)
    wrong_perm_num = math.perm(suit_size, draw)
    wrong_perm_den = math.perm(deck_size, draw)
    g2 = math.gcd(wrong_perm_num, wrong_perm_den)
    wrong_perm = _fmt_fraction(wrong_perm_num // g2, wrong_perm_den // g2)

    # Wrong: forgot "without replacement" -- used suit_size/deck_size for each
    wrong_simple = _fmt_fraction(suit_size, deck_size)

    # Wrong: inverted fraction
    wrong_inverted = _fmt_fraction(frac_den, frac_num)

    distractors = [wrong_replacement, wrong_perm, wrong_simple, wrong_inverted]
    distractors = _ensure_distinct_distractors(correct_str, distractors)

    question = (
        f"Da un mazzo di {deck_size} carte {deck_name}, si estraggono {draw} carte "
        f"senza rimpiazzo. Qual e' la probabilita' che siano tutte di {suit_name}?"
    )

    explanation = (
        f"Passaggio 1 (Combinatorica): Il numero di modi per scegliere {draw} carte "
        f"di {suit_name} da {suit_size} e' C({suit_size},{draw}) = {numerator}. "
        f"Il numero totale di modi per scegliere {draw} carte da {deck_size} "
        f"e' C({deck_size},{draw}) = {denominator}.\n"
        f"Passaggio 2 (Probabilita'): P = C({suit_size},{draw}) / C({deck_size},{draw}) "
        f"= {numerator}/{denominator} = {correct_str}."
    )

    tip = (
        "Questo tipo di domanda combina combinatorica (combinazioni C(n,k)) "
        "e probabilita' (rapporto casi favorevoli / casi possibili). "
        "Attenzione: senza rimpiazzo si usano le combinazioni, non le potenze!"
    )

    return question, correct_str, distractors, explanation, tip


# ============ LEVEL 3 ============

def _t3_trig_geometry():
    """Trigonometria + Geometria: area di un triangolo rettangolo dati ipotenusa e angolo."""
    # Choose angle from special angles
    angle_options = [
        (30, math.sin(math.radians(30)), math.cos(math.radians(30))),
        (45, math.sin(math.radians(45)), math.cos(math.radians(45))),
        (60, math.sin(math.radians(60)), math.cos(math.radians(60))),
    ]
    angle_deg, sin_val, cos_val = random.choice(angle_options)

    # Choose hypotenuse that gives clean results for common angles
    if angle_deg == 30:
        hyp = random.choice([10, 12, 14, 16, 20])
    elif angle_deg == 45:
        hyp = random.choice([10, 12, 14, 16, 20])
    else:
        hyp = random.choice([10, 12, 14, 16, 20])

    # cathetus opposite to angle = hyp * sin(angle)
    # cathetus adjacent to angle = hyp * cos(angle)
    cat_opp = hyp * sin_val
    cat_adj = hyp * cos_val

    area = cat_opp * cat_adj / 2

    # Format: round to 2 decimals for clean display
    correct_str = _fmt(area)

    # Distractors
    wrong_no_half = _fmt(cat_opp * cat_adj)                 # forgot /2
    wrong_swap = _fmt(hyp * sin_val * hyp * cos_val / 2)    # used hyp twice
    wrong_sin_cos_swap = _fmt(hyp * cos_val * hyp * sin_val / 2)  # same as above for these
    wrong_just_catheti = _fmt(cat_opp + cat_adj)             # sum instead of product
    wrong_hyp_cat = _fmt(hyp * cat_opp / 2)                  # used hyp as base

    distractors = [wrong_no_half, wrong_just_catheti, wrong_hyp_cat,
                   _fmt(area + hyp), _fmt(area * 2)]
    distractors = _ensure_distinct_distractors(correct_str, distractors)

    cat_opp_str = _fmt(cat_opp)
    cat_adj_str = _fmt(cat_adj)

    question = (
        f"In un triangolo rettangolo, l'ipotenusa misura {hyp} e un angolo acuto "
        f"e' di {angle_deg} gradi. Calcola l'area del triangolo."
    )

    explanation = (
        f"Passaggio 1 (Trigonometria): "
        f"Cateto opposto = ipotenusa * sin({angle_deg}°) = {hyp} * {_fmt(sin_val, 4)} = {cat_opp_str}. "
        f"Cateto adiacente = ipotenusa * cos({angle_deg}°) = {hyp} * {_fmt(cos_val, 4)} = {cat_adj_str}.\n"
        f"Passaggio 2 (Geometria): "
        f"Area = (base * altezza) / 2 = ({cat_opp_str} * {cat_adj_str}) / 2 = {correct_str}."
    )

    tip = (
        "Questo tipo di domanda combina trigonometria (sin e cos per trovare i cateti) "
        "e geometria (formula dell'area del triangolo). "
        "Ricorda: area = base * altezza / 2, e non dimenticare di dividere per 2!"
    )

    return question, correct_str, distractors, explanation, tip


def _t3_functions_statistics():
    """Funzioni + Statistica: calcolare la media dei valori di una funzione."""
    # Choose function type
    func_type = random.choice(["linear", "quadratic"])

    if func_type == "linear":
        a_coeff = random.randint(1, 5)
        b_coeff = random.randint(-3, 7)
        n = random.randint(4, 7)

        def f(x):
            return a_coeff * x + b_coeff

        if a_coeff == 1:
            func_str = f"f(x) = x + {b_coeff}" if b_coeff >= 0 else f"f(x) = x - {abs(b_coeff)}"
        else:
            func_str = f"f(x) = {a_coeff}x + {b_coeff}" if b_coeff >= 0 else f"f(x) = {a_coeff}x - {abs(b_coeff)}"
    else:
        a_coeff = random.choice([1, 2])
        b_coeff = random.randint(-2, 3)
        n = random.randint(4, 6)

        def f(x):
            return a_coeff * x * x + b_coeff

        if a_coeff == 1:
            func_str = f"f(x) = x² + {b_coeff}" if b_coeff >= 0 else f"f(x) = x² - {abs(b_coeff)}"
        else:
            func_str = f"f(x) = {a_coeff}x² + {b_coeff}" if b_coeff >= 0 else f"f(x) = {a_coeff}x² - {abs(b_coeff)}"

    values = [f(i) for i in range(1, n + 1)]
    total = sum(values)
    mean = total / n

    correct_str = _fmt(mean)

    # Distractors
    # Median
    sorted_vals = sorted(values)
    if n % 2 == 0:
        median = (sorted_vals[n // 2 - 1] + sorted_vals[n // 2]) / 2
    else:
        median = sorted_vals[n // 2]
    wrong_median = _fmt(median)

    # Forgot to divide
    wrong_no_div = _fmt(total)

    # Wrong evaluation (off by one in range)
    values_wrong = [f(i) for i in range(0, n)]
    wrong_eval = _fmt(sum(values_wrong) / n)

    # Divided by wrong n
    wrong_n = _fmt(total / (n + 1))

    distractors = [wrong_median, wrong_no_div, wrong_eval, wrong_n,
                   _fmt(mean + 1), _fmt(mean - 1)]
    distractors = _ensure_distinct_distractors(correct_str, distractors)

    values_str = ", ".join(str(v) for v in values)
    eval_steps = ", ".join(f"f({i}) = {values[i-1]}" for i in range(1, n + 1))

    question = (
        f"I voti di {n} studenti sono f(1), f(2), ..., f({n}) dove {func_str}. "
        f"Qual e' la media dei voti?"
    )

    explanation = (
        f"Passaggio 1 (Funzioni - Valutazione): Calcoliamo {eval_steps}. "
        f"I voti sono: {values_str}.\n"
        f"Passaggio 2 (Statistica - Media): "
        f"Media = ({' + '.join(str(v) for v in values)}) / {n} = {total} / {n} = {correct_str}."
    )

    tip = (
        "Questo tipo di domanda combina funzioni (valutazione in piu' punti) "
        "e statistica (calcolo della media aritmetica). "
        "Prima valuta la funzione in ogni punto, poi calcola la media dividendo la somma per il numero di valori."
    )

    return question, correct_str, distractors, explanation, tip


# ---------------------------------------------------------------------------
# Exercise class
# ---------------------------------------------------------------------------

_TEMPLATES_L1 = [
    _t1_algebra_geometry_area,
]

_TEMPLATES_L2 = [
    _t2_quadratic_analytic_geo,
    _t2_probability_combinatorics,
]

_TEMPLATES_L3 = [
    _t3_trig_geometry,
    _t3_functions_statistics,
]


class CrossTopicExercise(Exercise):
    """Domande Trasversali -- cross-topic questions combining 2+ math areas."""

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
