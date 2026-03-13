import math
import random

from exercises.base import Exercise


# ── Utility helpers ───────────────────────────────────────────────────────

SUPERSCRIPT = {
    "0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴",
    "5": "⁵", "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹",
    "-": "⁻",
}


def _sup(n):
    """Return superscript string for integer *n*."""
    return "".join(SUPERSCRIPT[c] for c in str(n))


def _fmt(value, decimals=2):
    """Format a numeric value: show as int if whole, otherwise round."""
    if isinstance(value, str):
        return value
    if abs(value - round(value)) < 1e-9:
        return str(int(round(value)))
    return str(round(value, decimals))


def _ensure_unique(correct, distractors, needed=4):
    """Return *needed* distractors that are distinct from *correct* and each other."""
    seen = {correct}
    result = []
    for d in distractors:
        if d not in seen:
            seen.add(d)
            result.append(d)
        if len(result) == needed:
            break
    # Fallback: add generic wrong answers if not enough
    fallback_idx = 1
    while len(result) < needed:
        candidate = f"Nessuna delle precedenti ({fallback_idx})"
        if candidate not in seen:
            seen.add(candidate)
            result.append(candidate)
        fallback_idx += 1
    return result[:needed]


# ═══════════════════════════════════════════════════════════════════════════
# LEVEL 1 — Easy templates
# ═══════════════════════════════════════════════════════════════════════════


def _t1_negative_exponents():
    """Simplify expressions with negative exponents.

    Pattern: (a⁻¹ + a⁻²) / (a⁻³ − a⁻⁴)  with base a chosen randomly.
    """
    a = random.choice([2, 3, 5])
    # (a⁻¹ + a⁻²) = (a + 1)/a²
    # (a⁻³ - a⁻⁴) = (a - 1)/a⁴
    # ratio = (a+1)/a² * a⁴/(a-1) = a²(a+1)/(a-1)
    numerator_val = a * a * (a + 1)
    denominator_val = a - 1
    g = math.gcd(abs(numerator_val), abs(denominator_val))
    num_s = numerator_val // g
    den_s = denominator_val // g

    expr = f"({a}{_sup(-1)} + {a}{_sup(-2)}) / ({a}{_sup(-3)} − {a}{_sup(-4)})"
    question = f"L'espressione {expr} è uguale a:"

    if den_s == 1:
        correct = str(num_s)
    else:
        correct = f"{num_s}/{den_s}"

    # Distractors based on common errors
    distractors = [
        _fmt(a * a),                         # forgot (a+1)/(a-1) factor
        _fmt(a * (a + 1)),                    # exponent error: a instead of a²
        _fmt(numerator_val),                  # forgot to divide by (a-1)
        _fmt(-num_s // den_s if den_s != 0 else 0),  # sign error
        _fmt(a ** 3),                         # wild guess
    ]

    explanation = (
        f"Riscriviamo: {a}{_sup(-1)} = 1/{a}, {a}{_sup(-2)} = 1/{a}², "
        f"{a}{_sup(-3)} = 1/{a}³, {a}{_sup(-4)} = 1/{a}⁴.\n"
        f"Numeratore: 1/{a} + 1/{a}² = ({a}+1)/{a}² = {a + 1}/{a}².\n"
        f"Denominatore: 1/{a}³ − 1/{a}⁴ = ({a}−1)/{a}⁴ = {a - 1}/{a}⁴.\n"
        f"Rapporto = ({a + 1}/{a}²) · ({a}⁴/{a - 1}) = {a}²·({a + 1})/({a - 1}) = {correct}."
    )
    tip = "Quando hai esponenti negativi, riscrivi come frazioni e poi semplifica."

    return question, correct, _ensure_unique(correct, distractors), explanation, tip


def _t1_common_factor():
    """Factor out common factor.

    Pattern: k·10ⁿ + m·10ⁿ⁻¹  =>  (k·10 + m) · 10ⁿ⁻¹
    """
    k = random.randint(1, 9)
    m = random.randint(1, 9)
    n = random.randint(3, 8)

    expr = f"{k}·10{_sup(n)} + {m}·10{_sup(n - 1)}"
    question = f"L'espressione {expr} è uguale a:"

    coeff = k * 10 + m
    correct = f"{coeff}·10{_sup(n - 1)}"

    distractors = [
        f"{k + m}·10{_sup(n)}",              # added coefficients, wrong exponent
        f"{coeff}·10{_sup(n)}",              # right coeff, wrong exponent
        f"{k * m}·10{_sup(n - 1)}",          # multiplied instead of combined
        f"{k + m}·10{_sup(n - 1)}",          # just added k+m
        f"{coeff}·10{_sup(n + 1)}",          # wrong exponent direction
    ]

    explanation = (
        f"Raccogliamo 10{_sup(n - 1)} come fattore comune:\n"
        f"{k}·10{_sup(n)} + {m}·10{_sup(n - 1)} = "
        f"10{_sup(n - 1)}·({k}·10 + {m}) = "
        f"10{_sup(n - 1)}·{coeff} = {correct}."
    )
    tip = "Raccogli la potenza di 10 con l'esponente più piccolo come fattore comune."

    return question, correct, _ensure_unique(correct, distractors), explanation, tip


def _t1_power_of_power():
    """Simplify (aⁿ)ᵐ expressions.

    Pattern: (aⁿ)ᵐ · aᵖ  where we compute the total exponent.
    """
    a = random.choice([2, 3, 5, 7])
    n = random.randint(2, 4)
    m = random.randint(2, 3)
    p = random.randint(1, 3)

    total_exp = n * m + p
    expr = f"({a}{_sup(n)}){_sup(m)} · {a}{_sup(p)}"
    question = f"L'espressione {expr} è uguale a:"

    correct = f"{a}{_sup(total_exp)}"

    distractors = [
        f"{a}{_sup(n + m + p)}",             # added n+m instead of n*m
        f"{a}{_sup(n * m * p)}",             # multiplied all three
        f"{a}{_sup(n * m)}",                 # forgot ·aᵖ
        f"{a * a}{_sup(n * m)}",             # wrong base
        f"{a}{_sup(n + m)}",                 # added instead of multiplied
    ]

    explanation = (
        f"Per la regola (aⁿ)ᵐ = a^(n·m):\n"
        f"({a}{_sup(n)}){_sup(m)} = {a}{_sup(n * m)}.\n"
        f"Poi: {a}{_sup(n * m)} · {a}{_sup(p)} = {a}{_sup(n * m)}⁺{_sup(p)} = {a}{_sup(total_exp)}."
    )
    tip = "Ricorda: (aⁿ)ᵐ = a^(n·m), e aⁿ·aᵐ = a^(n+m)."

    return question, correct, _ensure_unique(correct, distractors), explanation, tip


def _t1_fraction_sum():
    """Sum of simple fractions: 1/a + 1/b.

    Choose a, b coprime so the answer is clean.
    """
    pairs = [(2, 3), (3, 4), (2, 5), (3, 5), (4, 5), (3, 7), (2, 7),
             (5, 6), (4, 7), (5, 7)]
    a, b = random.choice(pairs)
    if random.random() < 0.5:
        a, b = b, a

    num = a + b
    den = a * b
    g = math.gcd(num, den)
    num_s, den_s = num // g, den // g

    expr = f"1/{a} + 1/{b}"
    question = f"L'espressione {expr} è uguale a:"

    correct = f"{num_s}/{den_s}"

    distractors = [
        f"1/{a + b}",                        # added denominators
        f"1/{a * b}",                         # multiplied denominators only
        f"2/{a + b}",                         # numerator 2 with sum of den
        f"{a + b}/{a * b + 1}",              # off by one in denominator
        f"2/{a * b}",                         # numerator 2 with product den
    ]

    explanation = (
        f"1/{a} + 1/{b} = {b}/({a}·{b}) + {a}/({a}·{b}) = "
        f"({b}+{a})/({a}·{b}) = {a + b}/{a * b}"
        + (f" = {num_s}/{den_s}." if g > 1 else ".")
    )
    tip = "Per sommare frazioni, trova il denominatore comune e somma i numeratori."

    return question, correct, _ensure_unique(correct, distractors), explanation, tip


# ═══════════════════════════════════════════════════════════════════════════
# LEVEL 2 — Medium templates
# ═══════════════════════════════════════════════════════════════════════════


def _t2_log_simplification():
    """Simplify log expressions.

    Pattern: log_b(b^k · c) where c is nice, or
             log(a^n) / log(a^m) = n/m
    """
    a = random.choice([2, 3, 5, 10])
    n = random.randint(2, 6)
    m = random.randint(2, 4)
    while math.gcd(n, m) == n or math.gcd(n, m) == m:
        n = random.randint(2, 6)
        m = random.randint(2, 4)

    g = math.gcd(n, m)
    num_s = n // g
    den_s = m // g

    expr = f"log({a}{_sup(n)}) / log({a}{_sup(m)})"
    question = f"L'espressione {expr} è uguale a:"

    if den_s == 1:
        correct = str(num_s)
    else:
        correct = f"{num_s}/{den_s}"

    distractors = [
        f"{n}/{m}" if f"{n}/{m}" != correct else f"{n + 1}/{m}",
        _fmt(n - m),                         # subtracted exponents
        _fmt(n * m),                          # multiplied
        f"{m}/{n}" if f"{m}/{n}" != correct else f"{m + 1}/{n}",  # inverted
        _fmt(n + m),                          # added exponents
    ]

    explanation = (
        f"Usiamo la proprietà log(aⁿ) = n·log(a):\n"
        f"log({a}{_sup(n)}) / log({a}{_sup(m)}) = "
        f"{n}·log({a}) / ({m}·log({a})) = {n}/{m}"
        + (f" = {correct}." if g > 1 else ".")
    )
    tip = "Ricorda: log(aⁿ) = n·log(a). Questa proprietà semplifica molte espressioni."

    return question, correct, _ensure_unique(correct, distractors), explanation, tip


def _t2_notable_products():
    """Factorization with notable products.

    Pattern: a² − b² = (a+b)(a−b)  with algebraic expressions.
    """
    variants = ["diff_squares", "perfect_square", "sum_cubes"]
    variant = random.choice(variants)

    if variant == "diff_squares":
        # (ka)² - (mb)² where k,m are small integers
        k = random.randint(1, 4)
        m = random.randint(1, 4)
        expr = f"({k}a)² − ({m}b)²" if k > 1 and m > 1 else (
            f"a² − ({m}b)²" if k == 1 else f"({k}a)² − b²"
        )
        if k == 1 and m == 1:
            expr = "a² − b²"

        ka_str = f"{k}a" if k > 1 else "a"
        mb_str = f"{m}b" if m > 1 else "b"
        correct = f"({ka_str} + {mb_str})({ka_str} − {mb_str})"

        distractors = [
            f"({ka_str} − {mb_str})²",                    # confused with perfect square
            f"({ka_str} + {mb_str})²",                     # confused with perfect square
            f"({ka_str} − {mb_str})({ka_str} − {mb_str})",  # forgot sign change
            f"({k}a² − {m}b²)",                            # didn't factor
            f"({ka_str} + {mb_str})({mb_str} − {ka_str})",  # sign error
        ]
        question = f"L'espressione {expr} è uguale a:"
        explanation = (
            f"Riconosciamo la differenza di quadrati: A² − B² = (A+B)(A−B).\n"
            f"Con A = {ka_str} e B = {mb_str}:\n"
            f"{expr} = {correct}."
        )

    elif variant == "perfect_square":
        # a² + 2ab + b² = (a+b)²  or  a² - 2ab + b² = (a-b)²
        k = random.randint(1, 3)
        m = random.randint(1, 3)
        sign = random.choice(["+", "−"])

        ka_str = f"{k}a" if k > 1 else "a"
        mb_str = f"{m}b" if m > 1 else "b"
        coeff_mid = 2 * k * m
        k_sq = k * k
        m_sq = m * m

        k_sq_str = f"{k_sq}a²" if k_sq > 1 else "a²"
        m_sq_str = f"{m_sq}b²" if m_sq > 1 else "b²"
        mid_str = f"{coeff_mid}ab" if coeff_mid > 1 else "ab"

        expr = f"{k_sq_str} {sign} {mid_str} + {m_sq_str}"
        op = "+" if sign == "+" else "−"
        correct = f"({ka_str} {op} {mb_str})²"

        wrong_op = "−" if op == "+" else "+"
        distractors = [
            f"({ka_str} {wrong_op} {mb_str})²",           # wrong sign
            f"({ka_str} {op} {mb_str})({ka_str} {wrong_op} {mb_str})",  # diff of squares
            f"({k_sq_str} {op} {m_sq_str})",               # dropped middle term
            f"({ka_str} {op} {mb_str})",                   # forgot square
            f"{k_sq_str} {op} {m_sq_str}",                 # ignored middle term
        ]
        question = f"L'espressione {expr} è uguale a:"
        explanation = (
            f"Riconosciamo il quadrato di binomio: "
            f"A² ± 2AB + B² = (A ± B)².\n"
            f"Con A = {ka_str} e B = {mb_str}:\n"
            f"{expr} = {correct}."
        )
    else:
        # a³ + b³ = (a+b)(a²-ab+b²)  or  a³ - b³ = (a-b)(a²+ab+b²)
        sign_plus = random.choice([True, False])
        expr = "a³ + b³" if sign_plus else "a³ − b³"
        if sign_plus:
            correct = "(a + b)(a² − ab + b²)"
            distractors = [
                "(a + b)(a² + ab + b²)",           # wrong sign in trinomial
                "(a − b)(a² − ab + b²)",           # wrong sign in binomial
                "(a + b)³",                        # confused with cube of sum
                "(a + b)(a − b)",                  # confused with diff of squares
                "(a² + b²)(a + b)",                # wrong factorization
            ]
        else:
            correct = "(a − b)(a² + ab + b²)"
            distractors = [
                "(a − b)(a² − ab + b²)",           # wrong sign in trinomial
                "(a + b)(a² + ab + b²)",           # wrong sign in binomial
                "(a − b)³",                        # confused with cube of diff
                "(a − b)(a + b)",                  # confused with diff of squares
                "(a² − b²)(a − b)",                # wrong factorization
            ]
        question = f"L'espressione {expr} è uguale a:"
        explanation = (
            f"Usiamo la formula {'della somma' if sign_plus else 'della differenza'} di cubi:\n"
            f"{'a³ + b³ = (a+b)(a²−ab+b²)' if sign_plus else 'a³ − b³ = (a−b)(a²+ab+b²)'}.\n"
            f"Quindi {expr} = {correct}."
        )

    tip = "I prodotti notevoli sono strumenti fondamentali: studiali bene e riconoscili a colpo d'occhio."
    return question, correct, _ensure_unique(correct, distractors), explanation, tip


def _t2_algebraic_fractions():
    """Simplify compound algebraic fractions.

    Pattern: (a²−b²)/(a+b) = a−b  or similar.
    """
    k = random.randint(2, 5)
    m = random.randint(1, 4)
    while k == m:
        m = random.randint(1, 4)

    # (x² - k²) / (x + k) = x - k
    # We use numeric-looking version for variety
    variants = ["basic", "with_coeff"]
    variant = random.choice(variants)

    if variant == "basic":
        expr = f"(x² − {k}²) / (x + {k})"
        correct = f"x − {k}"
        distractors = [
            f"x + {k}",                           # sign error
            f"x² − {k}",                          # incomplete simplification
            f"(x − {k})²",                        # wrong: squared
            f"x − {k}²",                          # didn't simplify k²
            f"{k} − x",                            # reversed
        ]
        explanation = (
            f"Riconosciamo al numeratore la differenza di quadrati:\n"
            f"x² − {k}² = (x + {k})(x − {k}).\n"
            f"Quindi (x² − {k}²)/(x + {k}) = (x + {k})(x − {k})/(x + {k}) = x − {k}."
        )
    else:
        # (kx² - km²) / (x + m) = k(x - m)
        expr = f"({k}x² − {k * m * m}) / (x + {m})"
        correct = f"{k}(x − {m})" if k > 1 else f"x − {m}"
        k_str = f"{k}" if k > 1 else ""
        distractors = [
            f"{k}(x + {m})",                      # sign error
            f"x − {k * m}",                        # wrong simplification
            f"{k}x − {m}",                         # partial factoring
            f"({k}x − {m})(x + {m})",             # didn't cancel
            f"{k}(x − {m * m})",                   # forgot to simplify m²
        ]
        explanation = (
            f"Raccogliamo {k} al numeratore:\n"
            f"{k}x² − {k * m * m} = {k}(x² − {m}²) = {k}(x + {m})(x − {m}).\n"
            f"Quindi ({k}x² − {k * m * m})/(x + {m}) = {k}(x − {m})."
        )

    question = f"L'espressione {expr} è uguale a:"
    tip = "Cerca sempre di fattorizzare numeratore e denominatore prima di semplificare."
    return question, correct, _ensure_unique(correct, distractors), explanation, tip


# ═══════════════════════════════════════════════════════════════════════════
# LEVEL 3 — Hard templates
# ═══════════════════════════════════════════════════════════════════════════


def _t3_nested_radicals():
    """Nested radicals using difference of squares.

    Pattern: √((√(a²+k²) − k)(√(a²+k²) + k))
    = √(a²+k² − k²) = √(a²) = |a|
    """
    a = random.randint(2, 7)
    k = random.randint(1, 5)

    s = a * a + k * k
    expr = f"√((√{s} − {k})(√{s} + {k}))"
    question = f"L'espressione {expr} è uguale a:"

    correct = f"|{a}|" if random.random() < 0.5 else str(a)
    # Accept both |a| and a since a > 0
    correct = str(a)

    distractors = [
        f"√{s}",                               # didn't simplify
        f"√{s} − {k}",                         # only partial
        f"{a}²",                                # forgot square root
        str(s - k * k + 1),                     # off by one
        f"√{a}",                                # wrong: sqrt of a instead of a
    ]

    explanation = (
        f"Usiamo la differenza di quadrati (A−B)(A+B) = A²−B²:\n"
        f"(√{s} − {k})(√{s} + {k}) = (√{s})² − {k}² = {s} − {k * k} = {a * a}.\n"
        f"Quindi √({a * a}) = {a}."
    )
    tip = "Il prodotto (A−B)(A+B) = A²−B² si applica anche con radicali al posto di A o B."
    return question, correct, _ensure_unique(correct, distractors), explanation, tip


def _t3_compound_algebraic():
    """Complex algebraic fraction simplification.

    Pattern: (1/a − 1/b) / (1/a + 1/b) = (b−a)/(b+a)
    """
    a = random.randint(2, 6)
    b = random.randint(2, 6)
    while a == b:
        b = random.randint(2, 6)

    expr = f"(1/{a} − 1/{b}) / (1/{a} + 1/{b})"
    question = f"L'espressione {expr} è uguale a:"

    num = b - a
    den = b + a
    g = math.gcd(abs(num), abs(den))
    num_s = num // g
    den_s = den // g
    if den_s < 0:
        num_s, den_s = -num_s, -den_s

    if den_s == 1:
        correct = str(num_s)
    else:
        correct = f"{num_s}/{den_s}"

    distractors = [
        f"{a - b}/{a + b}" if f"{a - b}/{a + b}" != correct else f"{a}/{b}",  # swapped order
        f"{a + b}/{b - a}" if b != a else "1",   # inverted
        f"{a}/{b}",                              # wrong simplification
        f"{b}/{a}",                              # wrong simplification
        f"1/{a * b}",                            # common mistake
    ]

    explanation = (
        f"Numeratore: 1/{a} − 1/{b} = ({b}−{a})/({a}·{b}) = {b - a}/{a * b}.\n"
        f"Denominatore: 1/{a} + 1/{b} = ({b}+{a})/({a}·{b}) = {b + a}/{a * b}.\n"
        f"Rapporto = ({b - a}/{a * b}) / ({b + a}/{a * b}) = "
        f"({b - a})/({b + a}) = {correct}."
    )
    tip = "Nelle frazioni composte, calcola separatamente numeratore e denominatore, poi dividi."
    return question, correct, _ensure_unique(correct, distractors), explanation, tip


def _t3_mixed_log_exp():
    """Mixed logarithm and exponent simplification.

    Pattern: a^(log_a(b)) = b   or   log_a(a^n) = n   with more complexity.
    Specifically: a^(2·log_a(b)) + a^(log_a(b²)) = 2b²
    """
    a = random.choice([2, 3, 5, 10])
    b = random.randint(2, 5)

    # a^(2·log_a(b)) = (a^(log_a(b)))² = b²
    # a^(log_a(b²)) = b²
    # Sum = b² + b² = 2b²
    result = 2 * b * b

    if a == 10:
        log_str = "log"
    else:
        log_str = f"log_{a}"

    expr = f"{a}^(2·{log_str}({b})) + {a}^({log_str}({b}²))"
    question = f"L'espressione {expr} è uguale a:"

    correct = f"2·{b}² = {result}" if b <= 3 else str(result)
    correct = str(result)

    distractors = [
        str(b * b),                            # forgot the factor 2
        str(2 * b),                            # confused b² with b
        str(b ** 3),                           # wrong exponent
        str(result + b),                       # added b extra
        str(b * b + b),                        # one term wrong
    ]

    explanation = (
        f"Usiamo la proprietà a^(log_a(x)) = x:\n"
        f"• {a}^(2·{log_str}({b})) = {a}^({log_str}({b}²)) = {b}² = {b * b}\n"
        f"  (perché 2·{log_str}({b}) = {log_str}({b}²)).\n"
        f"• {a}^({log_str}({b}²)) = {b}² = {b * b}.\n"
        f"Somma = {b * b} + {b * b} = {result}."
    )
    tip = "Le proprietà fondamentali: a^(log_a(x)) = x e n·log(x) = log(xⁿ)."
    return question, correct, _ensure_unique(correct, distractors), explanation, tip


# ═══════════════════════════════════════════════════════════════════════════
# Exercise class
# ═══════════════════════════════════════════════════════════════════════════


class SimplificationExercise(Exercise):
    """Expression simplification: identify the equivalent form."""

    TEMPLATES_L1 = [
        _t1_negative_exponents,
        _t1_common_factor,
        _t1_power_of_power,
        _t1_fraction_sum,
    ]

    TEMPLATES_L2 = [
        _t2_log_simplification,
        _t2_notable_products,
        _t2_algebraic_fractions,
    ]

    TEMPLATES_L3 = [
        _t3_nested_radicals,
        _t3_compound_algebraic,
        _t3_mixed_log_exp,
    ]

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
