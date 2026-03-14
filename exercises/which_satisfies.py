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
#  PARAMETRIC EQUATION ANALYSIS - Level 1
# ================================================================

def _which_param_linear_impossible() -> dict:
    """Per quale valore di a l'equazione parametrica lineare e' impossibile?"""
    # Build (a_coeff * a + b_coeff) x = c
    # Impossible when a_coeff * a + b_coeff = 0 and c != 0
    # Keep answer as integer: pick b_coeff divisible by a_coeff
    a_coeff = random.choice([1, 2, 3, -1, -2, -3])
    # Pick b_coeff so that a_answer = -b_coeff / a_coeff is integer
    a_answer = random.choice([i for i in range(-5, 6) if i != 0])
    b_coeff = -a_coeff * a_answer
    c_val = random.choice([i for i in range(-9, 10) if i != 0])

    # Format the coefficient of x
    coeff_str_parts = []
    if a_coeff == 1:
        coeff_str_parts.append("a")
    elif a_coeff == -1:
        coeff_str_parts.append("-a")
    else:
        coeff_str_parts.append(f"{a_coeff}a")
    if b_coeff > 0:
        coeff_str_parts.append(f" + {b_coeff}")
    elif b_coeff < 0:
        coeff_str_parts.append(f" - {-b_coeff}")
    coeff_str = "".join(coeff_str_parts)

    equation_str = f"({coeff_str})x = {c_val}"

    # Generate distractors
    distractors_set = set()
    # Common errors: sign flip, off-by-one, zero, negation
    for candidate in [a_answer + 1, a_answer - 1, -a_answer, 0,
                      a_answer + 2, a_answer - 2, 2 * a_answer]:
        if candidate != a_answer:
            distractors_set.add(candidate)
    distractors = sorted(distractors_set, key=lambda x: abs(x - a_answer))[:4]

    options = [str(a_answer)] + [str(d) for d in distractors]

    question = (
        f"Per quale valore di a l'equazione {equation_str} e' impossibile?"
    )

    explanation = (
        f"L'equazione e' impossibile quando il coefficiente di x si annulla "
        f"ma il termine noto e' diverso da zero. "
        f"Il coefficiente di x e' {coeff_str}: ponendo {coeff_str} = 0 si ottiene "
        f"a = {a_answer}. Per a = {a_answer} l'equazione diventa 0\u00b7x = {c_val}, "
        f"che e' impossibile perche' 0 \u2260 {c_val}."
    )

    tip = (
        "Un'equazione lineare parametrica (f(a))x = c e' impossibile quando "
        "il coefficiente di x si annulla (f(a) = 0) ma il termine noto c e' diverso da zero. "
        "Se anche c = 0, l'equazione ha infinite soluzioni (0\u00b7x = 0)."
    )

    return {
        "question": question,
        "options": options,
        "correct_index": 0,
        "explanation": explanation,
        "did_you_know": tip,
    }


def _which_param_linear_infinite() -> dict:
    """Per quale valore di a l'equazione parametrica lineare ha infinite soluzioni?"""
    # Build (a_coeff * a + b_coeff) x = d_coeff * a + e_coeff
    # Infinite solutions when both sides are 0: coeff of x = 0 AND rhs = 0
    # a_coeff * a + b_coeff = 0 => a = -b_coeff / a_coeff (integer)
    # d_coeff * a + e_coeff = 0 => must also be 0 at same a value
    a_coeff = random.choice([1, 2, 3, -1, -2, -3])
    a_answer = random.choice([i for i in range(-5, 6) if i != 0])
    b_coeff = -a_coeff * a_answer

    # RHS must also be zero at a = a_answer
    d_coeff = random.choice([i for i in range(-4, 5) if i != 0])
    e_coeff = -d_coeff * a_answer

    # Format LHS coefficient
    lhs_parts = []
    if a_coeff == 1:
        lhs_parts.append("a")
    elif a_coeff == -1:
        lhs_parts.append("-a")
    else:
        lhs_parts.append(f"{a_coeff}a")
    if b_coeff > 0:
        lhs_parts.append(f" + {b_coeff}")
    elif b_coeff < 0:
        lhs_parts.append(f" - {-b_coeff}")
    lhs_str = "".join(lhs_parts)

    # Format RHS
    rhs_parts = []
    if d_coeff == 1:
        rhs_parts.append("a")
    elif d_coeff == -1:
        rhs_parts.append("-a")
    else:
        rhs_parts.append(f"{d_coeff}a")
    if e_coeff > 0:
        rhs_parts.append(f" + {e_coeff}")
    elif e_coeff < 0:
        rhs_parts.append(f" - {-e_coeff}")
    rhs_str = "".join(rhs_parts)

    equation_str = f"({lhs_str})x = {rhs_str}"

    # Distractors
    distractors_set = set()
    for candidate in [a_answer + 1, a_answer - 1, -a_answer, 0,
                      a_answer + 2, a_answer - 2]:
        if candidate != a_answer:
            distractors_set.add(candidate)
    distractors = sorted(distractors_set, key=lambda x: abs(x - a_answer))[:4]

    options = [str(a_answer)] + [str(d) for d in distractors]

    question = (
        f"Per quale valore di a l'equazione {equation_str} ha infinite soluzioni?"
    )

    explanation = (
        f"L'equazione ha infinite soluzioni quando si riduce a 0\u00b7x = 0. "
        f"Il coefficiente di x e' {lhs_str}: ponendo {lhs_str} = 0 si ottiene a = {a_answer}. "
        f"Il termine destro e' {rhs_str}: per a = {a_answer} vale "
        f"{d_coeff}\u00b7{a_answer} + {e_coeff} = 0. "
        f"Quindi per a = {a_answer} l'equazione diventa 0\u00b7x = 0, "
        f"che e' soddisfatta da ogni x reale."
    )

    tip = (
        "Un'equazione parametrica ha infinite soluzioni quando si riduce a 0\u00b7x = 0. "
        "Bisogna trovare il valore del parametro che annulla simultaneamente "
        "il coefficiente di x e il termine noto."
    )

    return {
        "question": question,
        "options": options,
        "correct_index": 0,
        "explanation": explanation,
        "did_you_know": tip,
    }


# ================================================================
#  PARAMETRIC EQUATION ANALYSIS - Level 2
# ================================================================

def _which_param_quadratic_no_real() -> dict:
    """Per quale valore di k l'equazione quadratica non ha soluzioni reali?"""
    # Structure: x^2 + 2kx + (k + c) = 0
    # Discriminant: 4k^2 - 4(k + c) = 4(k^2 - k - c)
    # No real solutions when k^2 - k - c < 0
    # Pick c so the inequality k^2 - k - c < 0 has a nice interval
    # k^2 - k - c < 0 => roots of k^2 - k - c = 0 are (1 +/- sqrt(1+4c))/2
    # For c = 2: k^2 - k - 2 < 0 => (k-2)(k+1) < 0 => -1 < k < 2
    # Correct answer: pick an integer inside the interval
    c_choices = [
        # (c, interval_description, correct_k_values, boundary_values)
        (2, "(-1, 2)", [0, 1], [-1, 2]),
        (6, "(-2, 3)", [-1, 0, 1, 2], [-2, 3]),
        (12, "(-3, 4)", [-2, -1, 0, 1, 2, 3], [-3, 4]),
        (20, "(-4, 5)", [-3, -2, -1, 0, 1, 2, 3, 4], [-4, 5]),
    ]

    c_val, interval_desc, valid_ks, boundary_ks = random.choice(c_choices)
    k_answer = random.choice(valid_ks)

    # Distractors: values outside the interval or on boundary
    distractors_set = set()
    for bk in boundary_ks:
        distractors_set.add(bk)
    # Add values outside interval
    for candidate in [boundary_ks[0] - 1, boundary_ks[0] - 2,
                      boundary_ks[1] + 1, boundary_ks[1] + 2]:
        distractors_set.add(candidate)
    distractors_set.discard(k_answer)
    distractors = sorted(distractors_set)[:4]

    options = [str(k_answer)] + [str(d) for d in distractors]

    equation_str = f"x\u00b2 + 2kx + (k + {c_val}) = 0"

    question = (
        f"Per quale valore di k l'equazione {equation_str} "
        f"non ha soluzioni reali?"
    )

    disc_at_k = k_answer * k_answer - k_answer - c_val
    explanation = (
        f"Il discriminante dell'equazione e' \u0394 = (2k)\u00b2 - 4(k + {c_val}) = "
        f"4k\u00b2 - 4k - {4 * c_val} = 4(k\u00b2 - k - {c_val}). "
        f"L'equazione non ha soluzioni reali quando \u0394 < 0, cioe' "
        f"k\u00b2 - k - {c_val} < 0. Risolvendo: k \u2208 {interval_desc}. "
        f"Per k = {k_answer}: k\u00b2 - k - {c_val} = {disc_at_k} < 0. \u2714"
    )

    tip = (
        "Per un'equazione ax\u00b2 + bx + c = 0 parametrica, "
        "studia il segno del discriminante \u0394 = b\u00b2 - 4ac come disequazione "
        "nel parametro. Se \u0394 < 0, l'equazione non ha soluzioni reali."
    )

    return {
        "question": question,
        "options": options,
        "correct_index": 0,
        "explanation": explanation,
        "did_you_know": tip,
    }


def _which_param_quadratic_one_solution() -> dict:
    """Per quale valore di k l'equazione quadratica ha esattamente una soluzione reale?"""
    # Structure: x^2 - 2kx + c = 0 where c is a perfect square
    # Discriminant: 4k^2 - 4c = 0 => k^2 = c => k = +/- sqrt(c)
    c_choices = [1, 4, 9, 16, 25]
    c_val = random.choice(c_choices)
    k_positive = int(math.isqrt(c_val))
    # Pick one of the two correct values
    k_answer = random.choice([k_positive, -k_positive])

    # Distractors: the other root is tempting but we pick only one as correct
    distractors_set = set()
    # Add wrong values
    for candidate in [k_answer + 1, k_answer - 1, -k_answer + 1, -k_answer - 1,
                      0, k_answer + 2, k_answer - 2, c_val]:
        if candidate != k_answer:
            distractors_set.add(candidate)
    distractors = sorted(distractors_set, key=lambda x: abs(x))[:4]

    options = [str(k_answer)] + [str(d) for d in distractors]

    equation_str = f"x\u00b2 - 2kx + {c_val} = 0"

    question = (
        f"Per quale valore di k l'equazione {equation_str} "
        f"ha esattamente una soluzione reale?"
    )

    explanation = (
        f"Il discriminante e' \u0394 = (-2k)\u00b2 - 4\u00b7{c_val} = 4k\u00b2 - {4 * c_val}. "
        f"L'equazione ha esattamente una soluzione quando \u0394 = 0, cioe' "
        f"4k\u00b2 = {4 * c_val}, k\u00b2 = {c_val}, k = \u00b1{k_positive}. "
        f"Il valore k = {k_answer} e' corretto."
    )

    tip = (
        "Un'equazione di secondo grado ha esattamente una soluzione reale (radice doppia) "
        "quando il discriminante e' nullo: \u0394 = b\u00b2 - 4ac = 0. "
        "Risolvere \u0394 = 0 rispetto al parametro da' i valori cercati."
    )

    return {
        "question": question,
        "options": options,
        "correct_index": 0,
        "explanation": explanation,
        "did_you_know": tip,
    }


# ================================================================
#  PARAMETRIC EQUATION ANALYSIS - Level 3
# ================================================================

def _which_param_quadratic_positive_roots() -> dict:
    """Per quale valore di k l'equazione ha due radici reali positive?"""
    # Structure: x^2 - sx + p = 0 where s = sum of roots, p = product
    # Conditions for two positive roots: delta >= 0, sum > 0, product > 0
    # Use: x^2 - (k + a)x + b*k = 0 so sum = k + a, product = b*k
    # Need: k + a > 0, b*k > 0, delta = (k+a)^2 - 4bk >= 0
    # Pick b > 0 so product > 0 requires k > 0
    b_val = random.choice([1, 2, 3])
    a_val = random.choice([1, 2, 3])

    # sum = k + a_val > 0 => k > -a_val (auto-satisfied if k > 0)
    # product = b_val * k > 0 => k > 0
    # delta = (k + a_val)^2 - 4*b_val*k >= 0
    # = k^2 + 2*a_val*k + a_val^2 - 4*b_val*k
    # = k^2 + (2*a_val - 4*b_val)*k + a_val^2
    # This is a quadratic in k that's >= 0 outside its roots (if they exist)

    # For simplicity, pick k values that clearly satisfy all conditions
    # and verify computationally
    valid_ks = []
    for k_candidate in range(1, 15):
        s = k_candidate + a_val
        p = b_val * k_candidate
        delta = s * s - 4 * p
        if delta >= 0 and s > 0 and p > 0:
            valid_ks.append(k_candidate)

    if len(valid_ks) < 1:
        # Fallback to safe values
        a_val, b_val = 2, 1
        valid_ks = [k for k in range(1, 15)
                    if (k + 2) ** 2 - 4 * k >= 0 and k > 0]

    k_answer = random.choice(valid_ks[:5])  # pick from smaller values

    # Distractors: negative values (violate product > 0), zero, or values with delta < 0
    distractors_set = set()
    # Negative k violates product > 0
    for candidate in [-1, -2, -k_answer, 0]:
        distractors_set.add(candidate)
    # Find k with delta < 0 if possible
    for k_try in range(1, 20):
        s = k_try + a_val
        p = b_val * k_try
        delta = s * s - 4 * p
        if delta < 0:
            distractors_set.add(k_try)
            break
    distractors_set.discard(k_answer)
    distractors = sorted(distractors_set)[:4]
    # Pad if needed
    extra = -3
    while len(distractors) < 4:
        if extra != k_answer and extra not in distractors:
            distractors.append(extra)
        extra -= 1

    options = [str(k_answer)] + [str(d) for d in distractors[:4]]

    # Format equation
    sum_str_parts = []
    if a_val == 0:
        sum_str_parts.append("k")
    else:
        sum_str_parts.append(f"(k + {a_val})")
    prod_str = f"{b_val}k" if b_val != 1 else "k"

    equation_str = f"x\u00b2 - {sum_str_parts[0]}x + {prod_str} = 0"

    s_val = k_answer + a_val
    p_val = b_val * k_answer
    delta_val = s_val * s_val - 4 * p_val

    question = (
        f"Per quale valore di k l'equazione {equation_str} "
        f"ha due radici reali positive?"
    )

    explanation = (
        f"Per avere due radici reali positive servono tre condizioni (Vieta): "
        f"\u0394 \u2265 0, somma > 0, prodotto > 0. "
        f"Somma = k + {a_val}, prodotto = {prod_str}. "
        f"Per k = {k_answer}: somma = {s_val} > 0, prodotto = {p_val} > 0, "
        f"\u0394 = {s_val}\u00b2 - 4\u00b7{p_val} = {delta_val} \u2265 0. \u2714"
    )

    tip = (
        "Per verificare che un'equazione x\u00b2 - sx + p = 0 abbia due radici reali positive, "
        "usa le relazioni di Vieta: somma delle radici = s > 0, prodotto = p > 0, "
        "e discriminante \u0394 = s\u00b2 - 4p \u2265 0."
    )

    return {
        "question": question,
        "options": options,
        "correct_index": 0,
        "explanation": explanation,
        "did_you_know": tip,
    }


def _which_param_system_inconsistent() -> dict:
    """Per quale valore di a il sistema lineare 2x2 non ha soluzioni?"""
    # System: { a1*x + b1*y = c1 ; a2*x + b2*y = c2 }
    # Inconsistent when det = 0 AND not proportional constants
    # Structure: { a*x + b1*y = c1 ; d*x + e*y = f }
    # where det = a*e - d*b1 = 0 at a = a_answer, but c1*e != f*b1

    # Pick b1, e such that b1*d/e gives integer a_answer
    # Simpler: { a*x + b_val*y = c1 ; k*a_answer*x + k*b_val*y = c2 }
    # det = a*k*b_val - k*a_answer*b_val = k*b_val*(a - a_answer)
    # det = 0 when a = a_answer
    # Inconsistent when c2 != k*c1

    a_answer = random.choice([i for i in range(-5, 6) if i != 0])
    b_val = random.choice([i for i in range(-4, 5) if i != 0])
    c1 = random.choice([i for i in range(-6, 7) if i != 0])
    k = random.choice([2, 3, -2, -3])
    # c2 must differ from k*c1
    c2_wrong = k * c1
    c2 = c2_wrong + random.choice([i for i in range(-3, 4) if i != 0])

    # Second row coefficients
    a2_coeff = k * a_answer
    b2_coeff = k * b_val

    # Format system
    def _fmt_eq_param(a_str, b, c):
        parts = []
        parts.append(f"{a_str}x")
        if b == 1:
            parts.append("+ y")
        elif b == -1:
            parts.append("- y")
        elif b > 0:
            parts.append(f"+ {b}y")
        elif b < 0:
            parts.append(f"- {-b}y")
        return " ".join(parts) + f" = {c}"

    eq1 = _fmt_eq_param("a", b_val, c1)
    eq2_a2 = str(a2_coeff) if a2_coeff != 1 else ""
    if a2_coeff == -1:
        eq2_a2 = "-"
    eq2 = _fmt_eq_param(str(a2_coeff), b2_coeff, c2)
    system_str = "{ " + eq1 + " ; " + eq2 + " }"

    # Distractors
    distractors_set = set()
    for candidate in [a_answer + 1, a_answer - 1, -a_answer, 0,
                      a_answer + 2, a_answer * 2, a_answer - 2,
                      a_answer + 3, a_answer - 3]:
        if candidate != a_answer:
            distractors_set.add(candidate)
    distractors = sorted(distractors_set, key=lambda x: abs(x - a_answer))[:4]
    # Pad if somehow still short
    pad = a_answer + 10
    while len(distractors) < 4:
        if pad != a_answer and pad not in distractors:
            distractors.append(pad)
        pad += 1

    options = [str(a_answer)] + [str(d) for d in distractors[:4]]

    question = (
        f"Per quale valore di a il sistema {system_str} non ha soluzioni?"
    )

    det_general = f"a\u00b7{b2_coeff} - {a2_coeff}\u00b7{b_val}"
    explanation = (
        f"Il sistema non ha soluzioni quando il determinante dei coefficienti e' zero "
        f"ma il sistema non e' proporzionale. "
        f"det = {det_general} = {b2_coeff}a - {a2_coeff * b_val}. "
        f"Ponendo det = 0: {b2_coeff}a = {a2_coeff * b_val}, a = {a_answer}. "
        f"Per a = {a_answer} le equazioni hanno coefficienti proporzionali "
        f"ma termini noti diversi ({c1}\u00b7{k} = {k * c1} \u2260 {c2}), "
        f"quindi il sistema e' impossibile."
    )

    tip = (
        "Un sistema lineare 2\u00d72 non ha soluzioni (e' impossibile) quando "
        "il determinante della matrice dei coefficienti e' zero e le equazioni "
        "non sono proporzionali. Geometricamente, le due rette sono parallele."
    )

    return {
        "question": question,
        "options": options,
        "correct_index": 0,
        "explanation": explanation,
        "did_you_know": tip,
    }


# ================================================================
#  Main class
# ================================================================

class WhichSatisfies(Exercise):
    """Quale Soddisfa?: identifica quale oggetto matematico soddisfa una proprieta'."""

    _TEMPLATE_MAP = {
        1: [_which_log_between, _which_is_even, _which_fraction_largest,
            _which_param_linear_impossible, _which_param_linear_infinite],
        2: [_which_equation_has_solution, _which_not_injective,
            _which_inequality_has_interval, _which_expression_equals,
            _which_param_quadratic_no_real, _which_param_quadratic_one_solution],
        3: [_which_system_consistent, _which_parabola_passes_through,
            _which_always_positive,
            _which_param_quadratic_positive_roots, _which_param_system_inconsistent],
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
