import math
import random
from fractions import Fraction

from exercises.base import Exercise


# --- Helper utilities ---

def _fmt_fraction(num: int, den: int) -> str:
    """Format a fraction as a string like '7/9'."""
    return f"{num}/{den}"


def _log_value(base: float, arg: float) -> float:
    """Compute log_base(arg)."""
    return math.log(arg) / math.log(base)


def _fmt_log(base_str: str, arg: int) -> str:
    """Format a logarithm expression with subscript base."""
    subscript_map = {
        "2": "\u2082", "3": "\u2083", "4": "\u2084", "5": "\u2085",
        "6": "\u2086", "7": "\u2087", "8": "\u2088", "9": "\u2089",
        "10": "\u2081\u2080",
    }
    sub = subscript_map.get(str(base_str), f"_{base_str}")
    return f"log{sub}({arg})"


def _fmt_ln(arg: int) -> str:
    """Format natural log."""
    return f"ln({arg})"


# ================================================================
#  LEVEL 1 - Basic Property Testing
# ================================================================

def _which_log_between() -> dict:
    """Quale dei seguenti logaritmi e' compreso tra a e b?"""
    # Pick a target range
    ranges = [
        (1, 2), (2, 3), (3, 4), (0, 1), (1, 3),
    ]
    lo, hi = random.choice(ranges)

    # Pool of (display_string, numeric_value, base_num, arg_num) candidates
    candidates_pool = []
    base_arg_pairs = [
        (2, 3), (2, 5), (2, 7), (2, 8), (2, 9), (2, 10), (2, 12), (2, 15),
        (2, 16), (2, 20), (2, 32), (2, 50), (2, 64),
        (3, 5), (3, 9), (3, 10), (3, 27), (3, 30), (3, 81),
        (10, 2), (10, 5), (10, 50), (10, 100), (10, 500), (10, 1000),
        (5, 10), (5, 20), (5, 25), (5, 100), (5, 125),
    ]
    for base, arg in base_arg_pairs:
        val = _log_value(base, arg)
        label = _fmt_log(str(base), arg)
        candidates_pool.append((label, val, base, arg))

    # Also add some ln candidates
    for arg in [2, 3, 5, 7, 10, 15, 20, 50]:
        val = math.log(arg)
        label = _fmt_ln(arg)
        candidates_pool.append((label, val, math.e, arg))

    # Separate into "in range" and "out of range"
    in_range = [(l, v, b, a) for l, v, b, a in candidates_pool if lo < v < hi]
    out_range = [(l, v, b, a) for l, v, b, a in candidates_pool if not (lo < v < hi)]

    if len(in_range) < 1 or len(out_range) < 4:
        # Fallback: guaranteed case
        lo, hi = 2, 3
        in_range = [(l, v, b, a) for l, v, b, a in candidates_pool if lo < v < hi]
        out_range = [(l, v, b, a) for l, v, b, a in candidates_pool if not (lo < v < hi)]

    correct_item = random.choice(in_range)
    wrong_items = random.sample(out_range, min(4, len(out_range)))

    options = [correct_item[0]] + [w[0] for w in wrong_items]
    correct_index = 0

    question = f"Quale dei seguenti logaritmi ha un valore compreso tra {lo} e {hi}?"

    correct_val = correct_item[1]
    explanation = (
        f"La risposta corretta e' {correct_item[0]} ≈ {correct_val:.4f}, "
        f"che e' compreso nell'intervallo ({lo}, {hi}). "
        f"Per verificare, basta calcolare ciascun logaritmo: "
    )
    details = []
    for item in [correct_item] + wrong_items:
        details.append(f"{item[0]} ≈ {item[1]:.4f}")
    explanation += "; ".join(details) + "."

    tip = (
        "Per stimare un logaritmo log_b(x), chiediti: "
        "b elevato a quale potenza da' x? "
        "Ad esempio, log\u2082(5) e' tra 2 e 3 perche' 2\u00b2 = 4 < 5 < 8 = 2\u00b3."
    )

    return {
        "question": question,
        "options": options,
        "correct_index": correct_index,
        "explanation": explanation,
        "did_you_know": tip,
    }


def _which_is_even() -> dict:
    """Quale delle seguenti espressioni da' sempre un risultato pari?"""
    # Each entry: (expression_string, is_always_even, reason)
    always_even_pool = [
        ("n(n + 1)", True, "prodotto di due interi consecutivi, uno dei quali e' sempre pari"),
        ("n\u00b2 + n", True, "equivale a n(n + 1), prodotto di consecutivi"),
        ("n\u00b2 - n", True, "equivale a n(n - 1), prodotto di consecutivi"),
        ("2n + 4", True, "2(n + 2), sempre pari"),
        ("2n\u00b2", True, "multiplo di 2, sempre pari"),
        ("n(n + 1)(n + 2)", True, "prodotto di tre consecutivi, sempre divisibile per 6"),
        ("6n + 2", True, "2(3n + 1), sempre pari"),
        ("4n - 2", True, "2(2n - 1), sempre pari"),
    ]

    not_even_pool = [
        ("2n + 1", False, "dispari per ogni n intero"),
        ("n\u00b2 + 1", False, "pari solo quando n e' dispari"),
        ("3n + 2", False, "pari solo quando n e' pari"),
        ("n\u00b2 + 3", False, "pari solo quando n e' dispari"),
        ("n\u00b3 + 1", False, "pari solo quando n e' dispari"),
        ("5n", False, "pari solo quando n e' pari"),
        ("n + 3", False, "pari solo quando n e' dispari"),
        ("3n\u00b2 + 1", False, "pari solo quando n e' dispari"),
        ("n\u00b2 + 2n + 3", False, "equivale a (n+1)\u00b2 + 2, pari solo se n e' dispari"),
        ("7n - 1", False, "pari solo quando n e' dispari"),
    ]

    correct_item = random.choice(always_even_pool)
    wrong_items = random.sample(not_even_pool, 4)

    options = [correct_item[0]] + [w[0] for w in wrong_items]
    correct_index = 0

    question = (
        "Quale delle seguenti espressioni da' sempre un risultato pari, "
        "per ogni valore intero di n?"
    )

    explanation = (
        f"L'espressione {correct_item[0]} e' sempre pari perche' e' il "
        f"{correct_item[2]}. "
        f"Le altre espressioni non sono sempre pari: "
    )
    wrong_reasons = [f"{w[0]} e' {w[2]}" for w in wrong_items]
    explanation += "; ".join(wrong_reasons) + "."

    tip = (
        "Per verificare se un'espressione e' sempre pari, "
        "prova con n = 0 e n = 1. Se il risultato e' pari in entrambi i casi, "
        "cerca di dimostrare che si puo' fattorizzare un 2."
    )

    return {
        "question": question,
        "options": options,
        "correct_index": correct_index,
        "explanation": explanation,
        "did_you_know": tip,
    }


def _which_fraction_largest() -> dict:
    """Quale delle seguenti frazioni e' la piu' grande?"""
    # Generate fractions that are close in value
    fraction_pools = [
        # Pool of fractions roughly in [0.6, 0.85]
        [(7, 9), (5, 7), (3, 4), (11, 15), (8, 11), (9, 13), (6, 8), (13, 17),
         (10, 13), (7, 10), (4, 5), (5, 8), (9, 11), (11, 14), (12, 17)],
        # Pool of fractions roughly in [0.3, 0.5]
        [(3, 7), (2, 5), (3, 8), (4, 9), (5, 11), (4, 11), (3, 10), (5, 13),
         (7, 15), (2, 7), (6, 13), (5, 12), (7, 17), (3, 9)],
    ]

    pool = random.choice(fraction_pools)
    selected = random.sample(pool, 5)

    # Compute values and find the largest
    values = [Fraction(n, d) for n, d in selected]
    max_idx = max(range(5), key=lambda i: values[i])

    options = [_fmt_fraction(n, d) for n, d in selected]
    correct_index = max_idx

    question = "Quale delle seguenti frazioni e' la piu' grande?"

    correct_frac = selected[correct_index]
    correct_val = values[correct_index]
    explanation = (
        f"La frazione piu' grande e' {options[correct_index]} = "
        f"{float(correct_val):.4f}. "
        f"Per confrontare le frazioni, si possono ridurre allo stesso denominatore "
        f"oppure calcolare il valore decimale: "
    )
    details = [f"{options[i]} = {float(values[i]):.4f}" for i in range(5)]
    explanation += "; ".join(details) + "."

    tip = (
        "Per confrontare frazioni con denominatori diversi, "
        "puoi usare il prodotto incrociato: a/b > c/d se e solo se ad > bc. "
        "E' piu' veloce che ridurre allo stesso denominatore!"
    )

    return {
        "question": question,
        "options": options,
        "correct_index": correct_index,
        "explanation": explanation,
        "did_you_know": tip,
    }


# ================================================================
#  LEVEL 2 - Equation/Function Properties
# ================================================================

def _which_equation_has_solution() -> dict:
    """Quale delle seguenti equazioni ammette soluzione reale?"""
    # Equations that HAVE a real solution
    has_solution_pool = [
        ("log(x) = -2", "x = 10\u207b\u00b2 = 0.01", "il logaritmo puo' assumere qualsiasi valore reale"),
        ("2\u02e3 = 8", "x = 3", "2\u00b3 = 8"),
        ("x\u00b2 - 5x + 6 = 0", "x = 2 oppure x = 3", "il discriminante e' positivo: 25 - 24 = 1"),
        ("\u221ax = 3", "x = 9", "basta elevare al quadrato: x = 9"),
        ("3\u02e3 = 27", "x = 3", "3\u00b3 = 27"),
        ("e\u02e3 = 1", "x = 0", "e\u2070 = 1"),
        ("log\u2082(x) = 5", "x = 32", "2\u2075 = 32"),
        ("|x - 3| = 5", "x = 8 oppure x = -2", "valore assoluto uguale a un numero positivo"),
        ("x\u00b3 = -8", "x = -2", "(-2)\u00b3 = -8"),
    ]

    # Equations that have NO real solution
    no_solution_pool = [
        ("2\u02e3 = -1", "l'esponenziale e' sempre positivo"),
        ("x\u00b2 = -4", "il quadrato di un reale e' sempre \u2265 0"),
        ("\u221ax = -3", "la radice quadrata e' sempre \u2265 0"),
        ("3\u02e3 = 0", "l'esponenziale non si annulla mai"),
        ("e\u02e3 = -5", "l'esponenziale e' sempre positivo"),
        ("x\u00b2 + 1 = 0", "x\u00b2 + 1 \u2265 1 > 0 per ogni x reale"),
        ("log(x) + x\u00b2 + 1 = 0", "log(x) e' definito per x > 0 e log(x) + x\u00b2 + 1 > 0"),
        ("|x| = -2", "il valore assoluto e' sempre \u2265 0"),
        ("x\u00b2 + x + 1 = 0", "il discriminante e' negativo: 1 - 4 = -3"),
        ("\u221a(x\u00b2 + 1) = 0", "x\u00b2 + 1 \u2265 1 > 0, quindi la radice e' sempre > 0"),
    ]

    correct_item = random.choice(has_solution_pool)
    wrong_items = random.sample(no_solution_pool, 4)

    options = [correct_item[0]] + [w[0] for w in wrong_items]
    correct_index = 0

    question = "Quale delle seguenti equazioni ammette almeno una soluzione reale?"

    explanation = (
        f"L'equazione {correct_item[0]} ammette soluzione reale: {correct_item[1]}, "
        f"perche' {correct_item[2]}. Le altre equazioni non hanno soluzioni reali: "
    )
    wrong_reasons = [f"{w[0]}: {w[1]}" for w in wrong_items]
    explanation += "; ".join(wrong_reasons) + "."

    tip = (
        "Per capire se un'equazione ha soluzioni reali, "
        "analizza il dominio e il codominio delle funzioni coinvolte. "
        "Ad esempio, e\u02e3 > 0 sempre, quindi e\u02e3 = -1 non ha soluzione."
    )

    return {
        "question": question,
        "options": options,
        "correct_index": correct_index,
        "explanation": explanation,
        "did_you_know": tip,
    }


def _which_not_injective() -> dict:
    """Per quale funzione esistono p != q tali che f(p) = f(q)?"""
    # Non-injective functions (correct answers)
    non_injective_pool = [
        ("f(x) = x\u00b2", "f(-1) = f(1) = 1", "non e' iniettiva perche' f(-a) = f(a) per ogni a"),
        ("f(x) = |x|", "f(-2) = f(2) = 2", "non e' iniettiva perche' f(-a) = f(a) per ogni a"),
        ("f(x) = x\u00b2 - 4", "f(-2) = f(2) = 0", "non e' iniettiva perche' f(-a) = f(a) per ogni a"),
        ("f(x) = cos(x)", "f(0) = f(2\u03c0) = 1", "non e' iniettiva perche' e' periodica"),
        ("f(x) = sin(x)", "f(0) = f(\u03c0) = 0", "non e' iniettiva perche' e' periodica"),
        ("f(x) = x\u00b4", "f(-1) = f(1) = 1", "non e' iniettiva perche' f(-a) = f(a) per ogni a"),
        ("f(x) = x\u00b2 + 1", "f(-1) = f(1) = 2", "non e' iniettiva perche' f(-a) = f(a) per ogni a"),
    ]

    # Injective functions (wrong answers)
    injective_pool = [
        ("f(x) = 2x + 1", "funzione lineare con pendenza non nulla"),
        ("f(x) = e\u02e3", "esponenziale, strettamente crescente"),
        ("f(x) = ln(x)", "logaritmo naturale, strettamente crescente"),
        ("f(x) = x\u00b3", "funzione cubica, strettamente crescente"),
        ("f(x) = 3x - 5", "funzione lineare con pendenza non nulla"),
        ("f(x) = \u221ax", "radice quadrata, strettamente crescente per x \u2265 0"),
        ("f(x) = x\u00b3 + x", "derivata 3x\u00b2 + 1 > 0, sempre crescente"),
        ("f(x) = 2\u02e3", "esponenziale, strettamente crescente"),
        ("f(x) = -x + 7", "funzione lineare con pendenza non nulla"),
        ("f(x) = x\u2075", "funzione dispari, strettamente crescente"),
    ]

    correct_item = random.choice(non_injective_pool)
    wrong_items = random.sample(injective_pool, 4)

    options = [correct_item[0]] + [w[0] for w in wrong_items]
    correct_index = 0

    question = (
        "Per quale delle seguenti funzioni esistono due valori distinti "
        "p \u2260 q tali che f(p) = f(q)?"
    )

    explanation = (
        f"La funzione {correct_item[0]} {correct_item[2]}. "
        f"Ad esempio, {correct_item[1]}. "
        f"Le altre funzioni sono iniettive (strettamente monotone): "
    )
    wrong_reasons = [f"{w[0]} e' {w[1]}" for w in wrong_items]
    explanation += "; ".join(wrong_reasons) + "."

    tip = (
        "Una funzione e' iniettiva se f(a) = f(b) implica a = b. "
        "Le funzioni strettamente monotone (sempre crescenti o decrescenti) "
        "sono sempre iniettive. Le funzioni pari come x\u00b2 non sono mai iniettive su tutto R."
    )

    return {
        "question": question,
        "options": options,
        "correct_index": correct_index,
        "explanation": explanation,
        "did_you_know": tip,
    }


def _which_inequality_has_interval() -> dict:
    """Quale disequazione ha come insieme soluzione l'intervallo (a, b)?"""
    # Pick target interval endpoints
    a = random.randint(-3, 1)
    b = a + random.randint(2, 5)

    # The correct inequality: (x - a)(x - b) < 0 has solution (a, b)
    # Format the inequality
    def _fmt_term(val: int) -> str:
        if val == 0:
            return "x"
        elif val > 0:
            return f"(x - {val})"
        else:
            return f"(x + {-val})"

    correct_expr = f"{_fmt_term(a)} \u00b7 {_fmt_term(b)} < 0"

    # Wrong inequalities with different solution sets
    wrong_exprs = []

    # (x - a)(x - b) > 0 has solution (-inf, a) U (b, +inf)
    wrong_exprs.append(
        (f"{_fmt_term(a)} \u00b7 {_fmt_term(b)} > 0",
         f"(-\u221e, {a}) \u222a ({b}, +\u221e)")
    )

    # (x - a)(x - b) <= 0 has solution [a, b] (closed)
    wrong_exprs.append(
        (f"{_fmt_term(a)} \u00b7 {_fmt_term(b)} \u2264 0",
         f"[{a}, {b}]")
    )

    # (x - c)(x - d) < 0 with different roots
    c = a - random.randint(1, 3)
    d = b + random.randint(1, 3)
    wrong_exprs.append(
        (f"{_fmt_term(c)} \u00b7 {_fmt_term(d)} < 0",
         f"({c}, {d})")
    )

    # x - a < 0 has solution (-inf, a)
    wrong_exprs.append(
        (f"x - {a} < 0" if a >= 0 else f"x + {-a} < 0",
         f"(-\u221e, {a})")
    )

    options = [correct_expr] + [w[0] for w in wrong_exprs]
    correct_index = 0

    question = (
        f"Quale delle seguenti disequazioni ha come insieme soluzione "
        f"esattamente l'intervallo ({a}, {b})?"
    )

    explanation = (
        f"La disequazione {correct_expr} ha soluzione ({a}, {b}) perche' "
        f"il prodotto di due fattori e' negativo quando i fattori hanno segno opposto, "
        f"cioe' quando {a} < x < {b}. "
        f"Le altre disequazioni hanno insiemi soluzione diversi: "
    )
    wrong_details = [f"{w[0]} ha soluzione {w[1]}" for w in wrong_exprs]
    explanation += "; ".join(wrong_details) + "."

    tip = (
        "Per risolvere (x - a)(x - b) < 0, ricorda: il prodotto e' negativo "
        "quando i fattori hanno segno opposto. Se a < b, la soluzione e' (a, b). "
        "Per > 0, la soluzione e' (-\u221e, a) \u222a (b, +\u221e)."
    )

    return {
        "question": question,
        "options": options,
        "correct_index": correct_index,
        "explanation": explanation,
        "did_you_know": tip,
    }


def _which_expression_equals() -> dict:
    """Quale espressione e' equivalente a un'espressione target?"""
    # Pool of (target_display, correct_equivalent, wrong_alternatives)
    expression_pairs = [
        (
            "4x\u00b2 - 9",
            "(2x - 3)(2x + 3)",
            ["(2x - 3)\u00b2", "(4x - 3)(x + 3)", "(2x - 9)(2x + 1)", "4(x\u00b2 - 9)"],
        ),
        (
            "x\u00b2 - 6x + 9",
            "(x - 3)\u00b2",
            ["(x - 3)(x + 3)", "(x - 9)\u00b2", "x(x - 6) + 9", "(x + 3)\u00b2"],
        ),
        (
            "x\u00b2 + 2x + 1",
            "(x + 1)\u00b2",
            ["(x + 1)(x - 1)", "x(x + 2) + 2", "(x - 1)\u00b2", "x\u00b2 + 1"],
        ),
        (
            "9x\u00b2 - 1",
            "(3x - 1)(3x + 1)",
            ["(3x - 1)\u00b2", "(9x - 1)(x + 1)", "3(3x\u00b2 - 1)", "9(x\u00b2 - 1)"],
        ),
        (
            "x\u00b3 - 1",
            "(x - 1)(x\u00b2 + x + 1)",
            ["(x - 1)\u00b3", "(x - 1)(x\u00b2 - x + 1)", "(x - 1)(x + 1)\u00b2", "x(x\u00b2 - 1)"],
        ),
        (
            "x\u00b2 - 4",
            "(x - 2)(x + 2)",
            ["(x - 2)\u00b2", "(x - 4)(x + 1)", "x(x - 4)", "(x + 2)\u00b2 - 8"],
        ),
        (
            "x\u00b3 + 8",
            "(x + 2)(x\u00b2 - 2x + 4)",
            ["(x + 2)\u00b3", "(x + 2)(x\u00b2 + 2x + 4)", "(x + 8)(x\u00b2 - 1)", "x\u00b3 + 2\u00b3"],
        ),
        (
            "x\u00b2 + 4x + 4",
            "(x + 2)\u00b2",
            ["(x + 2)(x - 2)", "(x + 4)\u00b2", "x(x + 4) + 2", "(x - 2)\u00b2 + 8x"],
        ),
        (
            "25x\u00b2 - 16",
            "(5x - 4)(5x + 4)",
            ["(5x - 4)\u00b2", "(25x - 4)(x + 4)", "5(5x\u00b2 - 16)", "(5x - 16)(5x + 1)"],
        ),
    ]

    target_display, correct_eq, wrong_alts = random.choice(expression_pairs)

    options = [correct_eq] + wrong_alts
    correct_index = 0

    question = f"Quale delle seguenti espressioni e' equivalente a {target_display}?"

    explanation = (
        f"L'espressione {target_display} puo' essere fattorizzata (o espansa) come "
        f"{correct_eq}. Si verifica sviluppando il prodotto e ottenendo l'espressione originale. "
        f"Le altre opzioni sono algebricamente diverse."
    )

    tip = (
        "Per verificare un'equivalenza algebrica, puoi espandere l'espressione "
        "fattorizzata e confrontare termine per termine con l'originale. "
        "Ricorda le identita' notevoli: a\u00b2 - b\u00b2 = (a-b)(a+b), "
        "(a\u00b1b)\u00b2 = a\u00b2 \u00b1 2ab + b\u00b2."
    )

    return {
        "question": question,
        "options": options,
        "correct_index": correct_index,
        "explanation": explanation,
        "did_you_know": tip,
    }


# ================================================================
#  LEVEL 3 - Advanced Reasoning
# ================================================================

def _which_system_consistent() -> dict:
    """Quale sistema lineare ha una e una sola soluzione?"""
    def _make_unique_system():
        """Generate a 2x2 system with det != 0."""
        while True:
            a1 = random.randint(-5, 5)
            b1 = random.randint(-5, 5)
            a2 = random.randint(-5, 5)
            b2 = random.randint(-5, 5)
            det = a1 * b2 - a2 * b1
            if det != 0 and a1 != 0 and a2 != 0:
                c1 = random.randint(-10, 10)
                c2 = random.randint(-10, 10)
                return (a1, b1, c1, a2, b2, c2, det)

    def _make_dependent_system():
        """Generate a dependent system (infinite solutions): second eq is multiple of first."""
        a1 = random.choice([i for i in range(-4, 5) if i != 0])
        b1 = random.choice([i for i in range(-4, 5) if i != 0])
        c1 = random.randint(-5, 5)
        k = random.choice([i for i in range(-3, 4) if i not in (0, 1)])
        return (a1, b1, c1, k * a1, k * b1, k * c1, 0)

    def _make_inconsistent_system():
        """Generate an inconsistent system (no solutions): parallel lines."""
        a1 = random.choice([i for i in range(-4, 5) if i != 0])
        b1 = random.choice([i for i in range(-4, 5) if i != 0])
        c1 = random.randint(-5, 5)
        k = random.choice([i for i in range(-3, 4) if i not in (0, 1)])
        # Same coefficients, different constant
        c2 = k * c1 + random.choice([i for i in range(-5, 6) if i != 0])
        return (a1, b1, c1, k * a1, k * b1, c2, 0)

    def _fmt_system(a1, b1, c1, a2, b2, c2, _det):
        def _fmt_eq(a, b, c):
            parts = []
            if a == 1:
                parts.append("x")
            elif a == -1:
                parts.append("-x")
            elif a != 0:
                parts.append(f"{a}x")
            if b > 0:
                if parts:
                    if b == 1:
                        parts.append("+ y")
                    else:
                        parts.append(f"+ {b}y")
                else:
                    if b == 1:
                        parts.append("y")
                    else:
                        parts.append(f"{b}y")
            elif b < 0:
                if b == -1:
                    parts.append("- y")
                else:
                    parts.append(f"- {-b}y")
            return " ".join(parts) + f" = {c}"
        eq1 = _fmt_eq(a1, b1, c1)
        eq2 = _fmt_eq(a2, b2, c2)
        return "{ " + eq1 + " ; " + eq2 + " }"

    # Generate 1 consistent system
    unique_sys = _make_unique_system()

    # Generate 4 wrong systems: mix of dependent and inconsistent
    wrong_systems = []
    for _ in range(2):
        wrong_systems.append(_make_dependent_system())
    for _ in range(2):
        wrong_systems.append(_make_inconsistent_system())
    random.shuffle(wrong_systems)

    options = [_fmt_system(*unique_sys)] + [_fmt_system(*s) for s in wrong_systems]
    correct_index = 0

    question = (
        "Quale dei seguenti sistemi lineari in due incognite "
        "ammette una e una sola soluzione?"
    )

    det_val = unique_sys[6]
    explanation = (
        f"Il sistema {options[0]} ha determinante della matrice dei coefficienti "
        f"pari a {det_val} \u2260 0, quindi ammette un'unica soluzione "
        f"(sistema determinato). Gli altri sistemi hanno determinante nullo: "
        f"sono indeterminati (infinite soluzioni) o impossibili (nessuna soluzione)."
    )

    tip = (
        "Un sistema lineare 2\u00d72 ha un'unica soluzione quando il determinante "
        "della matrice dei coefficienti e' diverso da zero: "
        "det = a\u2081b\u2082 - a\u2082b\u2081 \u2260 0. "
        "Se det = 0, il sistema puo' essere indeterminato o impossibile."
    )

    return {
        "question": question,
        "options": options,
        "correct_index": correct_index,
        "explanation": explanation,
        "did_you_know": tip,
    }


def _which_parabola_passes_through() -> dict:
    """Quale parabola passa per i punti A e B?"""
    # Pick two points with small integer coordinates
    x1 = random.randint(-3, 0)
    x2 = random.randint(1, 4)
    y1 = random.randint(-5, 5)
    y2 = random.randint(-5, 5)

    # Generate the correct parabola y = ax^2 + bx + c
    # We need 3 coefficients but only 2 constraints, so fix one
    # Pick a random 'a' (nonzero) and solve for b, c
    a_coeff = random.choice([i for i in range(-3, 4) if i != 0])

    # System: a*x1^2 + b*x1 + c = y1 and a*x2^2 + b*x2 + c = y2
    # Subtract: a*(x1^2 - x2^2) + b*(x1 - x2) = y1 - y2
    # Since x1 != x2: a*(x1 + x2) + b = (y1 - y2)/(x1 - x2)
    diff_x = x1 - x2
    diff_y = y1 - y2
    # b = (y1-y2)/(x1-x2) - a*(x1+x2)
    # Use Fraction for exact arithmetic
    b_frac = Fraction(diff_y, diff_x) - Fraction(a_coeff * (x1 + x2))
    c_frac = Fraction(y1) - Fraction(a_coeff * x1 * x1) - b_frac * x1

    # Only proceed if b and c are integers (for clean display)
    if b_frac.denominator != 1 or c_frac.denominator != 1:
        # Retry with forced integer solution
        # Pick a, b directly and compute y1, y2
        a_coeff = random.choice([1, -1, 2, -2])
        b_coeff = random.randint(-3, 3)
        c_coeff = random.randint(-5, 5)
        x1 = random.randint(-2, 0)
        x2 = random.randint(1, 3)
        y1 = a_coeff * x1 * x1 + b_coeff * x1 + c_coeff
        y2 = a_coeff * x2 * x2 + b_coeff * x2 + c_coeff
        b_frac = Fraction(b_coeff)
        c_frac = Fraction(c_coeff)

    b_coeff_int = int(b_frac)
    c_coeff_int = int(c_frac)

    def _fmt_parabola(a, b, c):
        parts = []
        if a == 1:
            parts.append("y = x\u00b2")
        elif a == -1:
            parts.append("y = -x\u00b2")
        else:
            parts.append(f"y = {a}x\u00b2")
        if b > 0:
            if b == 1:
                parts[0] += " + x"
            else:
                parts[0] += f" + {b}x"
        elif b < 0:
            if b == -1:
                parts[0] += " - x"
            else:
                parts[0] += f" - {-b}x"
        if c > 0:
            parts[0] += f" + {c}"
        elif c < 0:
            parts[0] += f" - {-c}"
        return parts[0]

    correct_str = _fmt_parabola(a_coeff, b_coeff_int, c_coeff_int)

    # Generate 4 wrong parabolas by perturbing coefficients
    wrong_parabolas = []
    perturbations = [
        (a_coeff, b_coeff_int + random.choice([1, -1, 2]), c_coeff_int),
        (a_coeff, b_coeff_int, c_coeff_int + random.choice([1, -1, 2, -2])),
        (-a_coeff, b_coeff_int, c_coeff_int + random.choice([0, 1, -1])),
        (a_coeff + random.choice([1, -1]), b_coeff_int, c_coeff_int),
    ]
    for pa, pb, pc in perturbations:
        if pa == 0:
            pa = 1
        s = _fmt_parabola(pa, pb, pc)
        if s != correct_str and s not in wrong_parabolas:
            wrong_parabolas.append(s)

    # Ensure we have exactly 4 wrong options
    while len(wrong_parabolas) < 4:
        pa = random.choice([i for i in range(-3, 4) if i != 0])
        pb = random.randint(-5, 5)
        pc = random.randint(-5, 5)
        s = _fmt_parabola(pa, pb, pc)
        if s != correct_str and s not in wrong_parabolas:
            wrong_parabolas.append(s)

    options = [correct_str] + wrong_parabolas[:4]
    correct_index = 0

    question = (
        f"Quale delle seguenti parabole passa per i punti "
        f"A({x1}, {y1}) e B({x2}, {y2})?"
    )

    explanation = (
        f"La parabola corretta e' {correct_str}. "
        f"Verifica: per x = {x1}, y = {a_coeff}\u00b7{x1}\u00b2 + "
        f"{b_coeff_int}\u00b7{x1} + {c_coeff_int} = {y1}; "
        f"per x = {x2}, y = {a_coeff}\u00b7{x2}\u00b2 + "
        f"{b_coeff_int}\u00b7{x2} + {c_coeff_int} = {y2}."
    )

    tip = (
        "Per verificare se una parabola y = ax\u00b2 + bx + c passa per un punto (x\u2080, y\u2080), "
        "basta sostituire x = x\u2080 nell'equazione e controllare che si ottenga y\u2080. "
        "Se due punti sono dati, puoi impostare un sistema di 2 equazioni in 3 incognite."
    )

    return {
        "question": question,
        "options": options,
        "correct_index": correct_index,
        "explanation": explanation,
        "did_you_know": tip,
    }


def _which_always_positive() -> dict:
    """Quale espressione e' positiva per ogni x reale?"""
    # Always positive expressions (correct answers)
    # Generate quadratic ax^2 + bx + c with a > 0 and discriminant < 0
    def _make_always_positive():
        a = random.choice([1, 2, 3])
        # Ensure b^2 - 4ac < 0, i.e., c > b^2/(4a)
        b = random.randint(-4, 4)
        min_c = (b * b) // (4 * a) + 1
        c = random.randint(max(min_c, 1), max(min_c + 5, 6))
        disc = b * b - 4 * a * c
        assert disc < 0
        return a, b, c, disc

    # Not always positive (wrong answers): some have roots or can be <= 0
    def _make_has_roots():
        a = random.choice([1, 2])
        # Ensure discriminant >= 0
        b = random.randint(-6, 6)
        max_c = (b * b) // (4 * a)
        c = random.randint(min(max_c - 3, -3), max_c)
        disc = b * b - 4 * a * c
        return a, b, c, disc

    def _fmt_quadratic(a, b, c):
        parts = []
        if a == 1:
            parts.append("x\u00b2")
        elif a == -1:
            parts.append("-x\u00b2")
        else:
            parts.append(f"{a}x\u00b2")
        if b > 0:
            if b == 1:
                parts.append("+ x")
            else:
                parts.append(f"+ {b}x")
        elif b < 0:
            if b == -1:
                parts.append("- x")
            else:
                parts.append(f"- {-b}x")
        if c > 0:
            parts.append(f"+ {c}")
        elif c < 0:
            parts.append(f"- {-c}")
        return " ".join(parts)

    a_pos, b_pos, c_pos, disc_pos = _make_always_positive()
    correct_str = _fmt_quadratic(a_pos, b_pos, c_pos)

    wrong_options = []

    # 2 quadratics with real roots
    for _ in range(2):
        for _attempt in range(20):
            ar, br, cr, disc_r = _make_has_roots()
            s = _fmt_quadratic(ar, br, cr)
            if s != correct_str and s not in wrong_options:
                wrong_options.append(s)
                break

    # 1 quadratic with a < 0 (opens downward, eventually negative)
    neg_a = random.choice([-1, -2])
    neg_b = random.randint(-3, 3)
    neg_c = random.randint(-2, 5)
    wrong_options.append(_fmt_quadratic(neg_a, neg_b, neg_c))

    # 1 expression that can be zero: (x - k)^2 is >= 0 but equals 0 at x=k
    k = random.randint(1, 4)
    wrong_options.append(f"(x - {k})\u00b2")

    options = [correct_str] + wrong_options[:4]
    correct_index = 0

    question = "Quale delle seguenti espressioni e' strettamente positiva per ogni x reale?"

    explanation = (
        f"L'espressione {correct_str} e' sempre positiva perche' e' un trinomio "
        f"di secondo grado con coefficiente direttore a = {a_pos} > 0 e "
        f"discriminante \u0394 = {b_pos}\u00b2 - 4\u00b7{a_pos}\u00b7{c_pos} = "
        f"{disc_pos} < 0: non ha radici reali, quindi non interseca l'asse x "
        f"e rimane sempre positivo."
    )

    tip = (
        "Un trinomio ax\u00b2 + bx + c con a > 0 e \u0394 < 0 e' sempre positivo. "
        "Se a > 0 e \u0394 = 0, il trinomio e' \u2265 0 (si annulla in un punto). "
        "Se a > 0 e \u0394 > 0, il trinomio assume valori negativi tra le radici."
    )

    return {
        "question": question,
        "options": options,
        "correct_index": correct_index,
        "explanation": explanation,
        "did_you_know": tip,
    }


# ================================================================
#  Main class
# ================================================================

class WhichSatisfies(Exercise):
    """Quale Soddisfa?: identifica quale oggetto matematico soddisfa una proprieta'."""

    _TEMPLATE_MAP = {
        1: [_which_log_between, _which_is_even, _which_fraction_largest],
        2: [_which_equation_has_solution, _which_not_injective,
            _which_inequality_has_interval, _which_expression_equals],
        3: [_which_system_consistent, _which_parabola_passes_through,
            _which_always_positive],
    }

    def generate(self, difficulty: int) -> dict:
        difficulty = max(1, min(3, difficulty))
        templates = self._TEMPLATE_MAP[difficulty]
        template_fn = random.choice(templates)
        result = template_fn()
        # Shuffle options
        options, correct_index = self.shuffle_options(
            result["options"], result["correct_index"]
        )
        result["options"] = options
        result["correct_index"] = correct_index
        result["difficulty"] = difficulty
        return result
