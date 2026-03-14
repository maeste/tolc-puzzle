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
    g = math.gcd(abs(num), abs(den))
    num //= g
    den //= g
    if den < 0:
        num, den = -num, -den
    if den == 1:
        return str(num)
    return f"{num}/{den}"


def _make_distractors(correct_value, count=4):
    """Generate plausible wrong numeric answers.

    Strategies:
    - Sign errors (negate)
    - Off-by-one and off-by-small-amount
    - Common arithmetic mistakes (double, half)
    - Confusing operations (+ instead of -, * instead of /)
    """
    distractors = set()
    correct_str = _fmt(correct_value)

    # Strategy 1: sign error
    if correct_value != 0:
        distractors.add(_fmt(-correct_value))

    # Strategy 2: off-by-one
    distractors.add(_fmt(correct_value + 1))
    distractors.add(_fmt(correct_value - 1))

    # Strategy 3: off-by-two
    distractors.add(_fmt(correct_value + 2))
    distractors.add(_fmt(correct_value - 2))

    # Strategy 4: double / half
    if correct_value != 0:
        distractors.add(_fmt(correct_value * 2))
        if abs(correct_value) >= 2:
            distractors.add(_fmt(correct_value / 2))

    # Strategy 5: common factor errors
    distractors.add(_fmt(correct_value + 3))
    distractors.add(_fmt(correct_value - 3))

    # Remove the correct answer from distractors
    distractors.discard(correct_str)

    # If we still need more, add random offsets
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


def _prime_factorization(n):
    """Return prime factorization as dict {prime: exponent} and formatted string.

    Example: _prime_factorization(12) -> ({2: 2, 3: 1}, "2² × 3")
    """
    if n <= 1:
        return {n: 1}, str(n)
    factors = {}
    d = 2
    temp = n
    while d * d <= temp:
        while temp % d == 0:
            factors[d] = factors.get(d, 0) + 1
            temp //= d
        d += 1
    if temp > 1:
        factors[temp] = factors.get(temp, 0) + 1

    superscript_map = {
        0: "⁰", 1: "¹", 2: "²", 3: "³", 4: "⁴",
        5: "⁵", 6: "⁶", 7: "⁷", 8: "⁸", 9: "⁹",
    }

    def _sup(exp):
        if exp == 1:
            return ""
        return "".join(superscript_map[int(c)] for c in str(exp))

    parts = [f"{p}{_sup(e)}" for p, e in sorted(factors.items())]
    formatted = " × ".join(parts)
    return factors, formatted


def _factorization_gcd(factors_a, factors_b):
    """Compute GCD factors from two factorization dicts."""
    common = {}
    for p in set(factors_a) & set(factors_b):
        common[p] = min(factors_a[p], factors_b[p])
    return common


def _factorization_lcm(factors_a, factors_b):
    """Compute LCM factors from two factorization dicts."""
    result = dict(factors_a)
    for p, e in factors_b.items():
        result[p] = max(result.get(p, 0), e)
    return result


def _format_factors(factors):
    """Format a factor dict as a string like '2² × 3'."""
    if not factors:
        return "1"
    superscript_map = {
        0: "⁰", 1: "¹", 2: "²", 3: "³", 4: "⁴",
        5: "⁵", 6: "⁶", 7: "⁷", 8: "⁸", 9: "⁹",
    }

    def _sup(exp):
        if exp == 1:
            return ""
        return "".join(superscript_map[int(c)] for c in str(exp))

    parts = [f"{p}{_sup(e)}" for p, e in sorted(factors.items())]
    return " × ".join(parts)


def _factors_product(factors):
    """Compute the numeric value from a factor dict."""
    result = 1
    for p, e in factors.items():
        result *= p ** e
    return result


def _make_fraction_distractors(correct_num, correct_den, count=4):
    """Generate plausible wrong fraction answers."""
    correct_str = _fmt_fraction(correct_num, correct_den)
    distractors = set()

    # Swap numerator and denominator
    if correct_den != 0 and correct_num != correct_den:
        distractors.add(_fmt_fraction(correct_den, correct_num))

    # Sign error
    distractors.add(_fmt_fraction(-correct_num, correct_den))

    # Wrong operation on numerators
    distractors.add(_fmt_fraction(correct_num + 1, correct_den))
    distractors.add(_fmt_fraction(correct_num - 1, correct_den))

    # Wrong denominator
    distractors.add(_fmt_fraction(correct_num, correct_den + 1))

    # Forgot to simplify (show unsimplified version if different)
    g = math.gcd(abs(correct_num), abs(correct_den))
    if g > 1:
        distractors.add(f"{correct_num}//{correct_den}".replace("//", "/"))

    distractors.discard(correct_str)

    # Fill remaining with numeric offsets
    correct_val = correct_num / correct_den
    attempts = 0
    while len(distractors) < count and attempts < 100:
        attempts += 1
        offset = random.choice([-2, -1, 1, 2, 3])
        d_num = correct_num + offset
        if correct_den != 0:
            distractors.add(_fmt_fraction(d_num, correct_den))
        distractors.discard(correct_str)

    return list(distractors)[:count]


# ---------------------------------------------------------------------------
# LEVEL 1 Templates -- Basic calculations
# ---------------------------------------------------------------------------

def _t1_linear_equation():
    """Solve ax + b = c for x."""
    a = random.choice([i for i in range(-9, 10) if i != 0])
    x_sol = random.randint(-10, 10)
    b = random.randint(-20, 20)
    c = a * x_sol + b

    sign_b = f"+ {b}" if b >= 0 else f"- {abs(b)}"

    question = (
        f"Risolvi l'equazione {a}x {sign_b} = {c}. Quanto vale x?"
    )
    explanation = (
        f"Isoliamo x: {a}x = {c} - ({b}) = {c - b}.\n"
        f"Quindi x = {c - b} / {a} = {x_sol}."
    )
    tip = "Per risolvere un'equazione lineare, isola la variabile portando i termini noti dall'altra parte."
    return question, float(x_sol), explanation, tip


def _t1_fraction_addition():
    """Simplify a/b + c/d."""
    b = random.choice([2, 3, 4, 5, 6])
    d = random.choice([i for i in [2, 3, 4, 5, 6] if i != b])
    a = random.randint(1, b - 1)
    c = random.randint(1, d - 1)

    # Result as fraction
    result_num = a * d + c * b
    result_den = b * d
    g = math.gcd(abs(result_num), abs(result_den))
    simp_num = result_num // g
    simp_den = result_den // g

    correct_str = _fmt_fraction(simp_num, simp_den)
    distractors = _make_fraction_distractors(simp_num, simp_den)

    question = f"Calcola {a}/{b} + {c}/{d}. Esprimi il risultato come frazione ridotta ai minimi termini."
    explanation = (
        f"Troviamo il denominatore comune: {b} * {d} = {b * d}.\n"
        f"{a}/{b} + {c}/{d} = {a * d}/{b * d} + {c * b}/{b * d} = {result_num}/{result_den}.\n"
        f"Semplificando (MCD = {g}): {correct_str}."
    )
    tip = "Per sommare frazioni, trova il denominatore comune e somma i numeratori."
    return question, correct_str, distractors, explanation, tip


def _t1_powers_and_roots():
    """Simplify expressions with powers and roots."""
    variant = random.randint(1, 3)

    if variant == 1:
        # sqrt(a) * sqrt(b) = sqrt(a*b)
        a = random.choice([2, 3, 5, 6, 7])
        b = random.choice([2, 3, 5, 8])
        product = a * b
        result = math.sqrt(product)
        question = f"Calcola sqrt({a}) * sqrt({b})."
        explanation = (
            f"sqrt({a}) * sqrt({b}) = sqrt({a} * {b}) = sqrt({product}) = {_fmt(result)}."
        )
    elif variant == 2:
        # a^n / a^m = a^(n-m)
        base = random.randint(2, 5)
        n = random.randint(4, 8)
        m = random.randint(1, n - 1)
        result = float(base ** (n - m))
        question = f"Semplifica {base}^{n} / {base}^{m}."
        explanation = (
            f"Usando la proprieta' delle potenze: {base}^{n} / {base}^{m} = "
            f"{base}^({n}-{m}) = {base}^{n - m} = {_fmt(result)}."
        )
    else:
        # (a^n)^m = a^(n*m)
        base = random.randint(2, 4)
        n = random.randint(2, 3)
        m = random.randint(2, 3)
        result = float(base ** (n * m))
        question = f"Calcola ({base}^{n})^{m}."
        explanation = (
            f"({base}^{n})^{m} = {base}^({n}*{m}) = {base}^{n * m} = {_fmt(result)}."
        )

    tip = "Ricorda le proprieta' delle potenze: a^n * a^m = a^(n+m), a^n / a^m = a^(n-m), (a^n)^m = a^(n*m)."
    return question, result, explanation, tip


def _t1_percentage_calculation():
    """What is p% of N? or N is p% of what?"""
    variant = random.randint(1, 2)

    if variant == 1:
        # What is p% of N?
        p = random.choice([10, 15, 20, 25, 30, 40, 50, 75])
        n = random.choice([80, 100, 120, 150, 200, 250, 300, 400, 500])
        result = float(n * p / 100)
        question = f"Quanto vale il {p}% di {n}?"
        explanation = (
            f"Il {p}% di {n} = {n} * {p}/100 = {n} * {p / 100} = {_fmt(result)}."
        )
    else:
        # N is p% of what?
        p = random.choice([10, 20, 25, 50])
        result_base = random.choice([100, 200, 300, 400, 500])
        n = int(result_base * p / 100)
        result = float(result_base)
        question = f"{n} e' il {p}% di quale numero?"
        explanation = (
            f"Se {n} = {p}% di X, allora X = {n} / ({p}/100) = {n} / {p / 100} = {_fmt(result)}."
        )

    tip = "Percentuale: p% di N = N * p / 100. Se cerchi il totale: totale = parte / (percentuale/100)."
    return question, result, explanation, tip


def _t1_absolute_value():
    """Solve |x - a| = b. Ask for the sum of solutions."""
    a = random.randint(-8, 8)
    b = random.randint(1, 10)

    x1 = a + b
    x2 = a - b
    result = float(x1 + x2)  # always 2a

    sign_a = f"- {a}" if a >= 0 else f"+ {abs(a)}"

    question = (
        f"Risolvi |x {sign_a}| = {b}. Quanto vale la somma delle soluzioni?"
    )
    explanation = (
        f"|x {sign_a}| = {b} ha due soluzioni:\n"
        f"x {sign_a} = {b} => x = {x1}\n"
        f"x {sign_a} = -{b} => x = {x2}\n"
        f"Somma delle soluzioni: {x1} + ({x2}) = {_fmt(result)}."
    )
    tip = "L'equazione |x - a| = b ha soluzioni x = a + b e x = a - b. La somma delle soluzioni e' sempre 2a."
    return question, result, explanation, tip


def _t1_simple_expression():
    """Evaluate a numeric expression with order of operations."""
    a = random.randint(2, 8)
    b = random.randint(2, 6)
    c = random.randint(1, 5)
    d = random.randint(2, 4)

    result = float(a + b * c - d)

    question = f"Calcola {a} + {b} * {c} - {d}."
    explanation = (
        f"Rispettiamo l'ordine delle operazioni:\n"
        f"Prima la moltiplicazione: {b} * {c} = {b * c}.\n"
        f"Poi: {a} + {b * c} - {d} = {_fmt(result)}."
    )
    tip = "Ricorda l'ordine delle operazioni: prima potenze e radici, poi moltiplicazioni e divisioni, infine addizioni e sottrazioni."
    return question, result, explanation, tip


def _t1_gcd_two_simple():
    """GCD of two small numbers with step-by-step prime factorization."""
    # Build from a common factor to guarantee non-trivial GCD
    common = random.choice([2, 3, 4, 5, 6])
    mult_a = random.randint(2, 6)
    mult_b = random.randint(2, 6)
    while mult_a == mult_b:
        mult_b = random.randint(2, 6)
    a = common * mult_a
    b = common * mult_b

    result = float(math.gcd(a, b))
    factors_a, fmt_a = _prime_factorization(a)
    factors_b, fmt_b = _prime_factorization(b)
    gcd_factors = _factorization_gcd(factors_a, factors_b)
    gcd_fmt = _format_factors(gcd_factors)

    question = (
        f"Calcola il MCD (Massimo Comun Divisore) di {a} e {b} "
        f"usando la scomposizione in fattori primi."
    )
    explanation = (
        f"Scomposizione in fattori primi:\n"
        f"{a} = {fmt_a}\n"
        f"{b} = {fmt_b}\n"
        f"MCD = prodotto dei fattori comuni con esponente minimo = {gcd_fmt} = {_fmt(result)}."
    )
    tip = (
        "Per trovare il MCD, scomponi i numeri in fattori primi e "
        "prendi i fattori comuni con l'esponente piu' piccolo."
    )
    return question, result, explanation, tip


def _t1_lcm_two_simple():
    """LCM of two small numbers with prime factorization explanation."""
    a = random.randint(4, 28)
    b = random.randint(4, 28)
    while a == b:
        b = random.randint(4, 28)

    result = float(math.lcm(a, b))
    factors_a, fmt_a = _prime_factorization(a)
    factors_b, fmt_b = _prime_factorization(b)
    lcm_factors = _factorization_lcm(factors_a, factors_b)
    lcm_fmt = _format_factors(lcm_factors)

    question = (
        f"Calcola il mcm (minimo comune multiplo) di {a} e {b} "
        f"usando la scomposizione in fattori primi."
    )
    explanation = (
        f"Scomposizione in fattori primi:\n"
        f"{a} = {fmt_a}\n"
        f"{b} = {fmt_b}\n"
        f"mcm = prodotto di tutti i fattori con esponente massimo = {lcm_fmt} = {_fmt(result)}."
    )
    tip = (
        "Per trovare il mcm, scomponi i numeri in fattori primi e "
        "prendi tutti i fattori con l'esponente piu' grande."
    )
    return question, result, explanation, tip


# ---------------------------------------------------------------------------
# LEVEL 2 Templates -- Intermediate
# ---------------------------------------------------------------------------

def _t2_quadratic_equation():
    """Solve ax^2 + bx + c = 0. Ask for sum or product of roots."""
    # Generate from roots to ensure integer solutions
    r1 = random.randint(-8, 8)
    r2 = random.randint(-8, 8)
    a_coeff = random.choice([1, 1, 1, 2])  # mostly a=1

    # ax^2 - a(r1+r2)x + a*r1*r2 = 0
    b_coeff = -a_coeff * (r1 + r2)
    c_coeff = a_coeff * r1 * r2

    ask_what = random.choice(["sum", "product"])

    sign_b = f"+ {b_coeff}" if b_coeff >= 0 else f"- {abs(b_coeff)}"
    sign_c = f"+ {c_coeff}" if c_coeff >= 0 else f"- {abs(c_coeff)}"

    eq_str = f"{a_coeff}x^2 {sign_b}x {sign_c} = 0" if a_coeff != 1 else f"x^2 {sign_b}x {sign_c} = 0"

    if ask_what == "sum":
        result = float(r1 + r2)
        question = f"Risolvi l'equazione {eq_str}. Quanto vale la somma delle soluzioni?"
        explanation = (
            f"Le soluzioni sono x1 = {r1} e x2 = {r2}.\n"
            f"La somma e': {r1} + ({r2}) = {_fmt(result)}.\n"
            f"(Per Viete: somma delle radici = -b/a = {-b_coeff}/{a_coeff} = {_fmt(result)})."
        )
    else:
        result = float(r1 * r2)
        question = f"Risolvi l'equazione {eq_str}. Quanto vale il prodotto delle soluzioni?"
        explanation = (
            f"Le soluzioni sono x1 = {r1} e x2 = {r2}.\n"
            f"Il prodotto e': {r1} * ({r2}) = {_fmt(result)}.\n"
            f"(Per Viete: prodotto delle radici = c/a = {c_coeff}/{a_coeff} = {_fmt(result)})."
        )

    tip = "Per le formule di Viete: somma delle radici = -b/a, prodotto = c/a. Utile per risparmiare calcoli."
    return question, result, explanation, tip


def _t2_system_linear():
    """Solve a 2x2 system of linear equations."""
    # Generate from known solution
    x_sol = random.randint(-5, 5)
    y_sol = random.randint(-5, 5)

    a1 = random.choice([i for i in range(-4, 5) if i != 0])
    b1 = random.choice([i for i in range(-4, 5) if i != 0])
    a2 = random.choice([i for i in range(-4, 5) if i != 0])
    b2 = random.choice([i for i in range(-4, 5) if i != 0])

    # Ensure non-zero determinant
    det = a1 * b2 - a2 * b1
    while det == 0:
        b2 = random.choice([i for i in range(-4, 5) if i != 0])
        det = a1 * b2 - a2 * b1

    e1 = a1 * x_sol + b1 * y_sol
    e2 = a2 * x_sol + b2 * y_sol

    ask_what = random.choice(["x+y", "x*y", "x"])

    def _fmt_eq(a, var1, b, var2, e):
        sign_b = f"+ {b}" if b >= 0 else f"- {abs(b)}"
        return f"{a}x {sign_b}y = {e}"

    eq1_str = _fmt_eq(a1, "x", b1, "y", e1)
    eq2_str = _fmt_eq(a2, "x", b2, "y", e2)

    if ask_what == "x+y":
        result = float(x_sol + y_sol)
        ask_str = "x + y"
    elif ask_what == "x*y":
        result = float(x_sol * y_sol)
        ask_str = "x * y"
    else:
        result = float(x_sol)
        ask_str = "x"

    question = (
        f"Risolvi il sistema:\n"
        f"  {eq1_str}\n"
        f"  {eq2_str}\n"
        f"Quanto vale {ask_str}?"
    )
    explanation = (
        f"Risolvendo il sistema si ottiene x = {x_sol}, y = {y_sol}.\n"
        f"Verifica: {a1}*({x_sol}) + {b1}*({y_sol}) = {e1} (corretto).\n"
        f"Quindi {ask_str} = {_fmt(result)}."
    )
    tip = "Per risolvere un sistema 2x2 puoi usare sostituzione, riduzione o la regola di Cramer."
    return question, result, explanation, tip


def _t2_expression_simplification():
    """Simplify (a+b)^2 - (a-b)^2 type expressions."""
    a = random.randint(2, 10)
    b = random.randint(1, 8)

    variant = random.randint(1, 2)

    if variant == 1:
        # (a+b)^2 - (a-b)^2 = 4ab
        result = float(4 * a * b)
        question = f"Semplifica ({a} + {b})^2 - ({a} - {b})^2."
        explanation = (
            f"({a} + {b})^2 = {(a + b) ** 2}\n"
            f"({a} - {b})^2 = {(a - b) ** 2}\n"
            f"Differenza: {(a + b) ** 2} - {(a - b) ** 2} = {_fmt(result)}.\n"
            f"Usando la formula: (a+b)^2 - (a-b)^2 = 4ab = 4 * {a} * {b} = {_fmt(result)}."
        )
    else:
        # (a+b)^2 + (a-b)^2 = 2(a^2 + b^2)
        result = float(2 * (a * a + b * b))
        question = f"Semplifica ({a} + {b})^2 + ({a} - {b})^2."
        explanation = (
            f"({a} + {b})^2 = {(a + b) ** 2}\n"
            f"({a} - {b})^2 = {(a - b) ** 2}\n"
            f"Somma: {(a + b) ** 2} + {(a - b) ** 2} = {_fmt(result)}.\n"
            f"Usando la formula: (a+b)^2 + (a-b)^2 = 2(a^2 + b^2) = 2*({a * a} + {b * b}) = {_fmt(result)}."
        )

    tip = "Prodotti notevoli utili: (a+b)^2 - (a-b)^2 = 4ab e (a+b)^2 + (a-b)^2 = 2(a^2 + b^2)."
    return question, result, explanation, tip


def _t2_logarithmic_expression():
    """Simplify log expressions like log_2(8) + log_2(4)."""
    base = random.choice([2, 3, 5, 10])

    # Generate two values that are powers of the base
    exp1 = random.randint(1, 4)
    exp2 = random.randint(1, 4)
    val1 = base ** exp1
    val2 = base ** exp2

    variant = random.randint(1, 2)

    if variant == 1:
        # log_b(val1) + log_b(val2) = log_b(val1 * val2) = exp1 + exp2
        result = float(exp1 + exp2)
        question = f"Calcola log_{base}({val1}) + log_{base}({val2})."
        explanation = (
            f"log_{base}({val1}) = {exp1} (perche' {base}^{exp1} = {val1})\n"
            f"log_{base}({val2}) = {exp2} (perche' {base}^{exp2} = {val2})\n"
            f"Somma: {exp1} + {exp2} = {_fmt(result)}."
        )
    else:
        # log_b(val1) - log_b(val2) = exp1 - exp2
        result = float(exp1 - exp2)
        question = f"Calcola log_{base}({val1}) - log_{base}({val2})."
        explanation = (
            f"log_{base}({val1}) = {exp1} (perche' {base}^{exp1} = {val1})\n"
            f"log_{base}({val2}) = {exp2} (perche' {base}^{exp2} = {val2})\n"
            f"Differenza: {exp1} - {exp2} = {_fmt(result)}."
        )

    tip = "Proprieta' dei logaritmi: log(a*b) = log(a) + log(b), log(a/b) = log(a) - log(b), log(a^n) = n*log(a)."
    return question, result, explanation, tip


def _t2_radical_simplification():
    """Simplify sqrt(n) to a*sqrt(b) form."""
    # Pick a perfect square factor
    a = random.randint(2, 7)
    b = random.choice([2, 3, 5, 6, 7])
    n = a * a * b

    result = math.sqrt(n)

    question = f"Semplifica sqrt({n}). Quanto vale il risultato numerico (approssimato)?"
    explanation = (
        f"sqrt({n}) = sqrt({a * a} * {b}) = {a} * sqrt({b}).\n"
        f"Numericamente: {a} * sqrt({b}) = {a} * {_fmt(math.sqrt(b))} = {_fmt(result)}."
    )
    tip = "Per semplificare sqrt(n), cerca il quadrato perfetto piu' grande che divide n."
    return question, result, explanation, tip


def _t2_gcd_lcm():
    """Compute GCD or LCM of two numbers."""
    a = random.randint(6, 60)
    b = random.randint(6, 60)
    while a == b:
        b = random.randint(6, 60)

    variant = random.randint(1, 2)

    if variant == 1:
        result = float(math.gcd(a, b))
        question = f"Calcola il MCD (Massimo Comun Divisore) di {a} e {b}."
        explanation = (
            f"Scomponiamo: {a} e {b}.\n"
            f"MCD({a}, {b}) = {_fmt(result)}."
        )
    else:
        result = float(math.lcm(a, b))
        question = f"Calcola il mcm (minimo comune multiplo) di {a} e {b}."
        explanation = (
            f"mcm({a}, {b}) = ({a} * {b}) / MCD({a}, {b}) = "
            f"{a * b} / {math.gcd(a, b)} = {_fmt(result)}."
        )

    tip = "MCD e mcm sono legati dalla relazione: MCD(a,b) * mcm(a,b) = a * b."
    return question, result, explanation, tip


def _t2_lcm_periodicity():
    """Applied LCM problem: two periodic events coinciding."""
    contexts = [
        (
            "Un autobus passa ogni {a} minuti e un altro ogni {b} minuti. "
            "Se partono insieme adesso, tra quanti minuti passeranno di nuovo insieme?",
            "minuti",
        ),
        (
            "Una campana suona ogni {a} minuti e un'altra ogni {b} minuti. "
            "Se suonano insieme adesso, tra quanti minuti suoneranno di nuovo insieme?",
            "minuti",
        ),
        (
            "Anna innaffia le piante ogni {a} giorni e Marco ogni {b} giorni. "
            "Se oggi innaffiano entrambi, tra quanti giorni innaffieranno di nuovo lo stesso giorno?",
            "giorni",
        ),
        (
            "Un semaforo diventa verde ogni {a} secondi e un altro ogni {b} secondi. "
            "Se diventano verdi insieme adesso, tra quanti secondi lo saranno di nuovo?",
            "secondi",
        ),
    ]
    a = random.choice([2, 3, 4, 5, 6, 8, 10, 12, 15])
    b = random.choice([3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 15])
    while a == b or (math.gcd(a, b) == 1 and a * b > 100):
        b = random.choice([3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 15])

    result = float(math.lcm(a, b))
    context_template, unit = random.choice(contexts)
    question = context_template.format(a=a, b=b)

    explanation = (
        f"Dobbiamo trovare il minimo comune multiplo di {a} e {b}.\n"
        f"mcm({a}, {b}) = {_fmt(result)} {unit}.\n"
        f"Verifica: {_fmt(result)} / {a} = {_fmt(result / a)}, "
        f"{_fmt(result)} / {b} = {_fmt(result / b)} (entrambi interi)."
    )
    tip = (
        "Quando due eventi periodici devono coincidere, "
        "il tempo di attesa e' il mcm dei loro periodi."
    )
    return question, result, explanation, tip


def _t2_gcd_equal_groups():
    """Applied GCD problem: dividing items into equal groups."""
    # Pick a GCD first, then derive a and b
    gcd_val = random.choice([2, 3, 4, 5, 6, 7, 8])
    mult_a = random.randint(2, 8)
    mult_b = random.randint(2, 8)
    while mult_a == mult_b or math.gcd(mult_a, mult_b) != 1:
        mult_b = random.randint(2, 8)
    a = gcd_val * mult_a
    b = gcd_val * mult_b

    result = float(gcd_val)

    contexts = [
        (
            f"Hai {a} palline rosse e {b} palline blu. "
            f"Qual e' il numero massimo di gruppi identici che puoi formare usando tutte le palline?",
            f"Ogni gruppo conterra' {mult_a} palline rosse e {mult_b} palline blu.",
        ),
        (
            f"Un pasticcere ha {a} biscotti al cioccolato e {b} biscotti alla vaniglia. "
            f"Qual e' il numero massimo di sacchetti identici che puo' preparare usando tutti i biscotti?",
            f"Ogni sacchetto conterra' {mult_a} biscotti al cioccolato e {mult_b} alla vaniglia.",
        ),
        (
            f"In una scuola ci sono {a} quaderni di matematica e {b} quaderni di italiano. "
            f"Qual e' il numero massimo di kit identici che si possono preparare usando tutti i quaderni?",
            f"Ogni kit conterra' {mult_a} quaderni di matematica e {mult_b} di italiano.",
        ),
    ]
    question_text, extra_info = random.choice(contexts)

    explanation = (
        f"Dobbiamo trovare il MCD di {a} e {b}.\n"
        f"MCD({a}, {b}) = {_fmt(result)}.\n"
        f"{extra_info}"
    )
    tip = (
        "Per dividere oggetti in gruppi uguali il piu' possibile, "
        "il numero di gruppi e' dato dal MCD delle quantita'."
    )
    return question_text, result, explanation, tip


def _t2_fraction_simplification():
    """Simplify a fraction to lowest terms using GCD."""
    # Generate a fraction that needs simplification
    gcd_val = random.choice([2, 3, 4, 5, 6, 7, 8, 9, 10])
    simp_num = random.randint(1, 12)
    simp_den = random.randint(2, 12)
    while simp_num == simp_den or math.gcd(simp_num, simp_den) != 1:
        simp_den = random.randint(2, 12)

    orig_num = simp_num * gcd_val
    orig_den = simp_den * gcd_val

    correct_str = _fmt_fraction(simp_num, simp_den)
    distractors = _make_fraction_distractors(simp_num, simp_den)

    question = (
        f"Riduci ai minimi termini la frazione {orig_num}/{orig_den}."
    )
    explanation = (
        f"Troviamo il MCD di {orig_num} e {orig_den}:\n"
        f"MCD({orig_num}, {orig_den}) = {gcd_val}.\n"
        f"Dividiamo numeratore e denominatore per {gcd_val}:\n"
        f"{orig_num}/{orig_den} = {simp_num}/{simp_den} = {correct_str}."
    )
    tip = (
        "Per ridurre una frazione ai minimi termini, dividi numeratore e "
        "denominatore per il loro MCD."
    )
    return question, correct_str, distractors, explanation, tip


# ---------------------------------------------------------------------------
# LEVEL 3 Templates -- Advanced
# ---------------------------------------------------------------------------

def _t3_parametric_equation():
    """For which value of k does kx + b = c have solution x = n?"""
    x_sol = random.choice([i for i in range(-6, 7) if i != 0])
    b = random.randint(-10, 10)
    c = random.randint(-10, 10)

    # kx + b = c => k = (c - b) / x_sol
    k_val = (c - b) / x_sol
    # Ensure k is an integer
    while abs(k_val - round(k_val)) > 1e-9:
        c = random.randint(-10, 10)
        k_val = (c - b) / x_sol

    result = float(k_val)

    sign_b = f"+ {b}" if b >= 0 else f"- {abs(b)}"

    question = (
        f"Per quale valore di k l'equazione kx {sign_b} = {c} ha soluzione x = {x_sol}?"
    )
    explanation = (
        f"Sostituiamo x = {x_sol}:\n"
        f"k * ({x_sol}) {sign_b} = {c}\n"
        f"k * ({x_sol}) = {c} - ({b}) = {c - b}\n"
        f"k = {c - b} / {x_sol} = {_fmt(result)}."
    )
    tip = "Per trovare un parametro, sostituisci il valore noto della soluzione e risolvi per il parametro."
    return question, result, explanation, tip


def _t3_inequality():
    """Solve a linear inequality and find the smallest integer solution or an interval boundary."""
    a = random.choice([i for i in range(-6, 7) if i != 0])
    b = random.randint(-20, 20)
    c = random.randint(-20, 20)

    # ax + b > c => x > (c-b)/a or x < (c-b)/a depending on sign of a
    boundary = (c - b) / a

    sign_b = f"+ {b}" if b >= 0 else f"- {abs(b)}"

    if a > 0:
        # x > boundary, ask for smallest integer
        smallest_int = math.floor(boundary) + 1
        if abs(boundary - round(boundary)) < 1e-9:
            smallest_int = int(round(boundary)) + 1
        result = float(smallest_int)
        question = (
            f"Risolvi la disequazione {a}x {sign_b} > {c}. "
            f"Qual e' il piu' piccolo intero che soddisfa la disequazione?"
        )
        explanation = (
            f"{a}x > {c} - ({b}) = {c - b}\n"
            f"x > {c - b}/{a} = {_fmt(boundary)}\n"
            f"Il piu' piccolo intero maggiore di {_fmt(boundary)} e' {_fmt(result)}."
        )
    else:
        # a < 0, inequality flips: x < boundary
        largest_int = math.ceil(boundary) - 1
        if abs(boundary - round(boundary)) < 1e-9:
            largest_int = int(round(boundary)) - 1
        result = float(largest_int)
        question = (
            f"Risolvi la disequazione {a}x {sign_b} > {c}. "
            f"Qual e' il piu' grande intero che soddisfa la disequazione?"
        )
        explanation = (
            f"{a}x > {c} - ({b}) = {c - b}\n"
            f"Dividendo per {a} (negativo, il verso cambia): x < {c - b}/{a} = {_fmt(boundary)}\n"
            f"Il piu' grande intero minore di {_fmt(boundary)} e' {_fmt(result)}."
        )

    tip = "Quando dividi una disequazione per un numero negativo, il verso della disuguaglianza si inverte."
    return question, result, explanation, tip


def _t3_exponential_equation():
    """Solve exponential equations like 2^x = 32 or 3^(2x) = 81."""
    base = random.choice([2, 3, 5])
    variant = random.randint(1, 2)

    if variant == 1:
        # b^x = b^n => x = n
        n = random.randint(2, 6)
        target = base ** n
        result = float(n)
        question = f"Risolvi l'equazione {base}^x = {target}. Quanto vale x?"
        explanation = (
            f"{target} = {base}^{n}, quindi {base}^x = {base}^{n}.\n"
            f"Percio' x = {n}."
        )
    else:
        # b^(2x) = b^n => 2x = n => x = n/2
        n = random.choice([2, 4, 6])
        target = base ** n
        result = float(n / 2)
        question = f"Risolvi l'equazione {base}^(2x) = {target}. Quanto vale x?"
        explanation = (
            f"{target} = {base}^{n}, quindi {base}^(2x) = {base}^{n}.\n"
            f"2x = {n}, percio' x = {n}/{2} = {_fmt(result)}."
        )

    tip = "Per le equazioni esponenziali, esprimi entrambi i membri con la stessa base e uguaglia gli esponenti."
    return question, result, explanation, tip


def _t3_system_with_quadratic():
    """System with one linear and one simple quadratic equation."""
    # y = mx + q and y = x^2 + k
    # Intersection: x^2 + k = mx + q => x^2 - mx + (k - q) = 0
    # Choose roots first
    x1 = random.randint(-4, 4)
    x2 = random.randint(-4, 4)
    while x1 == x2:
        x2 = random.randint(-4, 4)

    m = random.choice([1, 2, -1, -2])
    q = random.randint(-5, 5)

    y1 = m * x1 + q

    # From y = x^2 + k: k = y1 - x1^2
    k = y1 - x1 * x1

    # Verify x2 also satisfies
    y2_linear = m * x2 + q
    y2_quad = x2 * x2 + k

    # If they don't match, generate differently
    # Actually, let's use a simpler approach: y = x^2 and y = mx + q
    # x^2 = mx + q => x^2 - mx - q = 0
    # roots: x1, x2 such that x1 + x2 = m and x1 * x2 = -q
    x1 = random.randint(-3, 3)
    x2 = random.randint(-3, 3)
    while x1 == x2:
        x2 = random.randint(-3, 3)

    m = x1 + x2
    q_neg = x1 * x2  # -q = x1*x2 => q = -x1*x2
    q = -q_neg

    # Ask for x1 + x2
    result = float(x1 + x2)

    sign_q = f"+ {q}" if q >= 0 else f"- {abs(q)}"
    sign_m_display = f"{m}x" if m != 1 else "x"
    if m == -1:
        sign_m_display = "-x"

    question = (
        f"Risolvi il sistema:\n"
        f"  y = x^2\n"
        f"  y = {sign_m_display} {sign_q}\n"
        f"Quanto vale la somma delle ascisse dei punti di intersezione?"
    )
    explanation = (
        f"Uguagliamo: x^2 = {sign_m_display} {sign_q}\n"
        f"x^2 - {sign_m_display} {'-' if q >= 0 else '+'} {abs(q)} = 0\n"
        f"Le soluzioni sono x1 = {x1} e x2 = {x2}.\n"
        f"Somma: {x1} + ({x2}) = {_fmt(result)}."
    )
    tip = "Per risolvere un sistema con una parabola e una retta, sostituisci e risolvi l'equazione di secondo grado."
    return question, result, explanation, tip


def _t3_function_evaluation():
    """Given f(x) = expression, compute f(a) - f(b)."""
    variant = random.randint(1, 3)

    if variant == 1:
        # f(x) = x^2 + px + q
        p = random.randint(-5, 5)
        q = random.randint(-5, 5)
        a = random.randint(-4, 4)
        b = random.randint(-4, 4)
        while a == b:
            b = random.randint(-4, 4)

        fa = a * a + p * a + q
        fb = b * b + p * b + q
        result = float(fa - fb)

        sign_p = f"+ {p}" if p >= 0 else f"- {abs(p)}"
        sign_q = f"+ {q}" if q >= 0 else f"- {abs(q)}"

        question = f"Data f(x) = x^2 {sign_p}x {sign_q}, calcola f({a}) - f({b})."
        explanation = (
            f"f({a}) = ({a})^2 {sign_p}*({a}) {sign_q} = {a * a} {'+' if p * a >= 0 else '-'} {abs(p * a)} {sign_q} = {fa}\n"
            f"f({b}) = ({b})^2 {sign_p}*({b}) {sign_q} = {b * b} {'+' if p * b >= 0 else '-'} {abs(p * b)} {sign_q} = {fb}\n"
            f"f({a}) - f({b}) = {fa} - ({fb}) = {_fmt(result)}."
        )
    elif variant == 2:
        # f(x) = 2x + c
        c = random.randint(-10, 10)
        a = random.randint(-5, 5)
        b = random.randint(-5, 5)
        while a == b:
            b = random.randint(-5, 5)

        fa = 2 * a + c
        fb = 2 * b + c
        result = float(fa - fb)

        sign_c = f"+ {c}" if c >= 0 else f"- {abs(c)}"

        question = f"Data f(x) = 2x {sign_c}, calcola f({a}) - f({b})."
        explanation = (
            f"f({a}) = 2*({a}) {sign_c} = {fa}\n"
            f"f({b}) = 2*({b}) {sign_c} = {fb}\n"
            f"f({a}) - f({b}) = {fa} - ({fb}) = {_fmt(result)}."
        )
    else:
        # f(x) = x^3 - x
        a = random.randint(-3, 3)
        b = random.randint(-3, 3)
        while a == b:
            b = random.randint(-3, 3)

        fa = a ** 3 - a
        fb = b ** 3 - b
        result = float(fa - fb)

        question = f"Data f(x) = x^3 - x, calcola f({a}) - f({b})."
        explanation = (
            f"f({a}) = ({a})^3 - ({a}) = {a ** 3} - {a} = {fa}\n"
            f"f({b}) = ({b})^3 - ({b}) = {b ** 3} - {b} = {fb}\n"
            f"f({a}) - f({b}) = {fa} - ({fb}) = {_fmt(result)}."
        )

    tip = "Per valutare f(a), sostituisci x con a nell'espressione e calcola con attenzione i segni."
    return question, result, explanation, tip


def _t3_compound_fraction():
    """Simplify a compound fraction expression."""
    a = random.randint(1, 6)
    b = random.randint(1, 6)
    c = random.randint(1, 6)
    while a == b:
        b = random.randint(1, 6)

    # Expression: (a/b) / (c/a) = a^2 / (b*c)
    result_num = a * a
    result_den = b * c
    g = math.gcd(result_num, result_den)
    simp_num = result_num // g
    simp_den = result_den // g
    result = float(simp_num / simp_den)

    question = f"Semplifica ({a}/{b}) / ({c}/{a}). Esprimi il risultato come numero decimale."
    explanation = (
        f"({a}/{b}) / ({c}/{a}) = ({a}/{b}) * ({a}/{c}) = {a * a}/({b}*{c}) = {result_num}/{result_den}.\n"
        f"Semplificando: {simp_num}/{simp_den} = {_fmt(result)}."
    )
    tip = "Dividere per una frazione equivale a moltiplicare per il suo reciproco: (a/b) / (c/d) = (a/b) * (d/c)."
    return question, result, explanation, tip


def _t3_gcd_three_numbers():
    """GCD of three numbers with prime factorization."""
    # Pick a common GCD factor, then build three numbers with coprime multipliers
    gcd_val = random.choice([2, 3, 4, 5, 6])
    # Pre-select three distinct multipliers whose GCD is 1
    coprime_triples = [
        (2, 3, 5), (2, 3, 7), (2, 5, 7), (2, 5, 9), (3, 4, 5),
        (3, 5, 7), (3, 7, 8), (4, 5, 7), (4, 5, 9), (4, 7, 9),
        (3, 4, 7), (5, 6, 7), (5, 7, 9), (2, 7, 9), (3, 5, 8),
    ]
    mult_a, mult_b, mult_c = random.choice(coprime_triples)

    a = gcd_val * mult_a
    b = gcd_val * mult_b
    c = gcd_val * mult_c

    result = float(math.gcd(a, math.gcd(b, c)))

    factors_a, fmt_a = _prime_factorization(a)
    factors_b, fmt_b = _prime_factorization(b)
    factors_c, fmt_c = _prime_factorization(c)

    question = (
        f"Calcola il MCD (Massimo Comun Divisore) di {a}, {b} e {c}."
    )
    explanation = (
        f"Scomposizione in fattori primi:\n"
        f"{a} = {fmt_a}\n"
        f"{b} = {fmt_b}\n"
        f"{c} = {fmt_c}\n"
        f"MCD = prodotto dei fattori comuni a tutti e tre con esponente minimo = {_fmt(result)}."
    )
    tip = (
        "Il MCD di tre numeri si calcola prendendo i fattori primi comuni a tutti "
        "con l'esponente piu' piccolo, oppure: MCD(a, b, c) = MCD(MCD(a, b), c)."
    )
    return question, result, explanation, tip


def _t3_lcm_three_numbers():
    """LCM of three numbers — applied traffic light problem."""
    values = [2, 3, 4, 5, 6, 8, 10, 12, 15, 20]
    a = random.choice(values)
    b = random.choice(values)
    c = random.choice(values)
    while a == b or a == c or b == c or math.lcm(a, b, c) > 300:
        a = random.choice(values)
        b = random.choice(values)
        c = random.choice(values)

    result = float(math.lcm(a, b, c))

    factors_a, fmt_a = _prime_factorization(a)
    factors_b, fmt_b = _prime_factorization(b)
    factors_c, fmt_c = _prime_factorization(c)

    contexts = [
        (
            f"Tre semafori cambiano colore ogni {a}, {b} e {c} secondi rispettivamente. "
            f"Se diventano tutti verdi nello stesso momento, dopo quanti secondi saranno di nuovo tutti verdi insieme?",
            "secondi",
        ),
        (
            f"Tre campanelle suonano ogni {a}, {b} e {c} minuti rispettivamente. "
            f"Se suonano insieme adesso, dopo quanti minuti suoneranno di nuovo tutte insieme?",
            "minuti",
        ),
        (
            f"Tre autobus partono dalla stessa fermata ogni {a}, {b} e {c} minuti. "
            f"Se partono insieme adesso, dopo quanti minuti partiranno di nuovo insieme?",
            "minuti",
        ),
    ]
    question_text, unit = random.choice(contexts)

    explanation = (
        f"Scomposizione in fattori primi:\n"
        f"{a} = {fmt_a}\n"
        f"{b} = {fmt_b}\n"
        f"{c} = {fmt_c}\n"
        f"mcm = prodotto di tutti i fattori con esponente massimo = {_fmt(result)} {unit}."
    )
    tip = (
        "Il mcm di tre numeri si calcola prendendo tutti i fattori primi presenti "
        "con l'esponente piu' grande, oppure: mcm(a, b, c) = mcm(mcm(a, b), c)."
    )
    return question_text, result, explanation, tip


# ---------------------------------------------------------------------------
# TRIGONOMETRY Templates
# ---------------------------------------------------------------------------

# Notable trigonometric values table
_TRIG_NOTABLE = {
    0: {"sin": 0, "cos": 1, "tan": 0},
    30: {"sin": 0.5, "cos": math.sqrt(3) / 2, "tan": math.sqrt(3) / 3},
    45: {"sin": math.sqrt(2) / 2, "cos": math.sqrt(2) / 2, "tan": 1},
    60: {"sin": math.sqrt(3) / 2, "cos": 0.5, "tan": math.sqrt(3)},
    90: {"sin": 1, "cos": 0, "tan": None},
}

_TRIG_NOTABLE_STR = {
    (0, "sin"): "0", (0, "cos"): "1", (0, "tan"): "0",
    (30, "sin"): "1/2", (30, "cos"): "√3/2", (30, "tan"): "√3/3",
    (45, "sin"): "√2/2", (45, "cos"): "√2/2", (45, "tan"): "1",
    (60, "sin"): "√3/2", (60, "cos"): "1/2", (60, "tan"): "√3",
    (90, "sin"): "1", (90, "cos"): "0",
}


def _trig_str_distractors(correct_str, angle, func):
    """Generate plausible wrong trig value answers."""
    all_values = set()
    for a in _TRIG_NOTABLE_STR:
        all_values.add(_TRIG_NOTABLE_STR[a])
    # Add some common wrong answers
    all_values.update(["1/2", "√2/2", "√3/2", "√3/3", "0", "1", "√3", "2", "-1"])
    all_values.discard(correct_str)
    distractors = list(all_values)
    random.shuffle(distractors)
    return distractors[:4]


def _t1_trig_notable_values():
    """Ask for a notable trigonometric value: sin/cos/tan of 0°, 30°, 45°, 60°."""
    func = random.choice(["sin", "cos", "tan"])
    if func == "tan":
        angle = random.choice([0, 30, 45, 60])
    else:
        angle = random.choice([0, 30, 45, 60, 90])

    correct_str = _TRIG_NOTABLE_STR[(angle, func)]
    distractors = _trig_str_distractors(correct_str, angle, func)

    question = f"Quanto vale {func}({angle}°)?"
    explanation = (
        f"Dai valori notevoli della trigonometria: {func}({angle}°) = {correct_str}."
    )
    tip = (
        "Valori notevoli: sin(30°)=1/2, sin(45°)=√2/2, sin(60°)=√3/2, "
        "cos(30°)=√3/2, cos(45°)=√2/2, cos(60°)=1/2, tan(45°)=1."
    )
    return question, correct_str, distractors, explanation, tip


def _t1_trig_basic_identity():
    """If sin(α) = a/c, find cos(α) using sin²+cos²=1."""
    # Use Pythagorean triples for clean answers
    triples = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25)]
    a, b, c = random.choice(triples)
    # sin = a/c, cos = b/c or vice versa
    if random.choice([True, False]):
        sin_val, cos_val = a, b
        given_func, asked_func = "sin", "cos"
    else:
        sin_val, cos_val = b, a
        given_func, asked_func = "cos", "sin"

    given_str = _fmt_fraction(sin_val, c)
    correct_str = _fmt_fraction(cos_val, c)
    distractors = _make_fraction_distractors(cos_val, c)

    question = (
        f"Se {given_func}(α) = {given_str} e α e' un angolo del primo quadrante, "
        f"quanto vale {asked_func}(α)?"
    )
    explanation = (
        f"Usiamo l'identita' fondamentale: sin²(α) + cos²(α) = 1.\n"
        f"{given_func}²(α) = ({given_str})² = {sin_val**2}/{c**2}\n"
        f"{asked_func}²(α) = 1 - {sin_val**2}/{c**2} = {cos_val**2}/{c**2}\n"
        f"{asked_func}(α) = {cos_val}/{c} = {correct_str} (positivo nel primo quadrante)."
    )
    tip = "L'identita' fondamentale sin²(α) + cos²(α) = 1 permette di trovare una funzione dall'altra."
    return question, correct_str, distractors, explanation, tip


def _t2_trig_equation_simple():
    """How many solutions does sin(x)=k or cos(x)=k have in [0°, 360°)?"""
    scenarios = [
        ("sin", "1/2", 2, "sin(x)=1/2 ha soluzioni x=30° e x=150°"),
        ("sin", "√2/2", 2, "sin(x)=√2/2 ha soluzioni x=45° e x=135°"),
        ("sin", "√3/2", 2, "sin(x)=√3/2 ha soluzioni x=60° e x=120°"),
        ("sin", "1", 1, "sin(x)=1 ha unica soluzione x=90°"),
        ("sin", "0", 2, "sin(x)=0 ha soluzioni x=0° e x=180°"),
        ("cos", "1/2", 2, "cos(x)=1/2 ha soluzioni x=60° e x=300°"),
        ("cos", "√2/2", 2, "cos(x)=√2/2 ha soluzioni x=45° e x=315°"),
        ("cos", "√3/2", 2, "cos(x)=√3/2 ha soluzioni x=30° e x=330°"),
        ("cos", "0", 2, "cos(x)=0 ha soluzioni x=90° e x=270°"),
        ("cos", "1", 1, "cos(x)=1 ha unica soluzione x=0°"),
    ]
    func, val_str, n_solutions, detail = random.choice(scenarios)
    result = float(n_solutions)

    question = (
        f"Quante soluzioni ha l'equazione {func}(x) = {val_str} "
        f"nell'intervallo [0°, 360°)?"
    )
    explanation = (
        f"{detail}.\n"
        f"Quindi ci sono {n_solutions} soluzioni nell'intervallo [0°, 360°)."
    )
    tip = (
        "Nell'intervallo [0°, 360°), sin(x)=k e cos(x)=k hanno generalmente "
        "2 soluzioni (tranne per k=±1 che ne hanno 1, e k=0 che ne ha 2)."
    )
    return question, result, explanation, tip


def _t2_trig_expression():
    """Evaluate trigonometric expressions using notable values."""
    variant = random.randint(1, 3)

    if variant == 1:
        # sin²(a) + cos²(a) = 1
        angle = random.choice([30, 45, 60])
        result = 1.0
        question = f"Calcola sin²({angle}°) + cos²({angle}°)."
        explanation = (
            f"Per l'identita' fondamentale, sin²(α) + cos²(α) = 1 per ogni α.\n"
            f"Quindi sin²({angle}°) + cos²({angle}°) = 1."
        )
    elif variant == 2:
        # sin(a)·cos(b) + cos(a)·sin(b) = sin(a+b)
        a, b = random.choice([(30, 60), (30, 45)])
        sin_a = _TRIG_NOTABLE[a]["sin"]
        cos_a = _TRIG_NOTABLE[a]["cos"]
        sin_b = _TRIG_NOTABLE[b]["sin"]
        cos_b = _TRIG_NOTABLE[b]["cos"]
        result = round(sin_a * cos_b + cos_a * sin_b, 10)
        sum_angle = a + b
        question = (
            f"Calcola sin({a}°)·cos({b}°) + cos({a}°)·sin({b}°)."
        )
        explanation = (
            f"Questa e' la formula di addizione: sin(α+β) = sin(α)cos(β) + cos(α)sin(β).\n"
            f"Quindi sin({a}°)·cos({b}°) + cos({a}°)·sin({b}°) = sin({sum_angle}°) = {_fmt(result)}."
        )
    else:
        # 2·sin(a)·cos(a) = sin(2a)
        a = random.choice([30, 45])
        sin_a = _TRIG_NOTABLE[a]["sin"]
        cos_a = _TRIG_NOTABLE[a]["cos"]
        result = round(2 * sin_a * cos_a, 10)
        question = f"Calcola 2·sin({a}°)·cos({a}°)."
        explanation = (
            f"Questa e' la formula del seno doppio: 2·sin(α)·cos(α) = sin(2α).\n"
            f"2·sin({a}°)·cos({a}°) = sin({2 * a}°) = {_fmt(result)}."
        )

    tip = (
        "Formule utili: sin(α+β) = sin(α)cos(β)+cos(α)sin(β), "
        "sin(2α) = 2·sin(α)·cos(α), cos(2α) = cos²(α)-sin²(α)."
    )
    return question, result, explanation, tip


def _t2_trig_convert_deg_rad():
    """Convert degrees to radians or vice versa."""
    variant = random.randint(1, 2)

    deg_rad_map = {
        30: ("π/6", 1, 6), 45: ("π/4", 1, 4), 60: ("π/3", 1, 3),
        90: ("π/2", 1, 2), 120: ("2π/3", 2, 3), 135: ("3π/4", 3, 4),
        150: ("5π/6", 5, 6), 180: ("π", 1, 1), 210: ("7π/6", 7, 6),
        270: ("3π/2", 3, 2), 300: ("5π/3", 5, 3), 360: ("2π", 2, 1),
    }

    if variant == 1:
        # Degrees to radians (string answer)
        angle = random.choice(list(deg_rad_map.keys()))
        correct_str, num, den = deg_rad_map[angle]
        # Generate distractors: other radian values
        other_rads = [v[0] for k, v in deg_rad_map.items() if k != angle]
        random.shuffle(other_rads)
        distractors = other_rads[:4]

        question = f"Converti {angle}° in radianti."
        explanation = (
            f"Per convertire gradi in radianti: radianti = gradi × π/180.\n"
            f"{angle}° = {angle} × π/180 = {correct_str}."
        )
        tip = "Conversione: radianti = gradi × π/180. Gradi = radianti × 180/π."
        return question, correct_str, distractors, explanation, tip
    else:
        # Radians to degrees (numeric answer)
        angle = random.choice(list(deg_rad_map.keys()))
        rad_str, num, den = deg_rad_map[angle]
        result = float(angle)

        question = f"Converti {rad_str} radianti in gradi."
        explanation = (
            f"Per convertire radianti in gradi: gradi = radianti × 180/π.\n"
            f"{rad_str} = {rad_str} × 180/π = {_fmt(result)}°."
        )
        tip = "Conversione: gradi = radianti × 180/π. Angoli importanti: π/6=30°, π/4=45°, π/3=60°, π/2=90°."
        return question, result, explanation, tip


def _t3_trig_equation_parametric():
    """For which values of k does sin(x)=k have solutions?"""
    variant = random.randint(1, 2)

    if variant == 1:
        # sin(x) = k has solutions iff -1 <= k <= 1
        k = random.choice([0.5, 1.5, -0.5, 2, -1, 1, 0, -2, 3])
        has_solution = -1 <= k <= 1
        result = 1.0 if has_solution else 0.0
        question = (
            f"L'equazione sin(x) = {_fmt(k)} ha soluzioni reali? "
            f"Rispondi 1 per si', 0 per no."
        )
        explanation = (
            f"La funzione sin(x) ha codominio [-1, 1].\n"
            f"Poiche' {_fmt(k)} {'appartiene' if has_solution else 'non appartiene'} "
            f"all'intervallo [-1, 1], l'equazione "
            f"{'ha' if has_solution else 'non ha'} soluzioni."
        )
    else:
        # Find the range of sin or cos
        func = random.choice(["sin", "cos"])
        # "Qual e' il valore massimo di sin(x) + 3?"
        offset = random.randint(1, 5)
        result = float(1 + offset)  # max of sin/cos is 1
        question = (
            f"Qual e' il valore massimo di {func}(x) + {offset}?"
        )
        explanation = (
            f"Il valore massimo di {func}(x) e' 1.\n"
            f"Quindi il valore massimo di {func}(x) + {offset} = 1 + {offset} = {_fmt(result)}."
        )

    tip = "sin(x) e cos(x) hanno codominio [-1, 1]. Il massimo e' 1, il minimo e' -1."
    return question, result, explanation, tip


def _t3_trig_simplification():
    """Simplify trigonometric expressions like (1-cos²x)/sinx = sinx."""
    variant = random.randint(1, 3)

    if variant == 1:
        # (1 - cos²(α)) / sin(α) = sin²(α)/sin(α) = sin(α)
        angle = random.choice([30, 45, 60])
        sin_val = _TRIG_NOTABLE[angle]["sin"]
        result = round(sin_val, 10)
        question = (
            f"Semplifica e calcola (1 - cos²({angle}°)) / sin({angle}°)."
        )
        explanation = (
            f"Per l'identita' fondamentale: 1 - cos²(α) = sin²(α).\n"
            f"Quindi (1 - cos²({angle}°)) / sin({angle}°) = sin²({angle}°) / sin({angle}°) = sin({angle}°) = {_fmt(result)}."
        )
    elif variant == 2:
        # tan(α) · cos(α) = sin(α)
        angle = random.choice([30, 45, 60])
        sin_val = _TRIG_NOTABLE[angle]["sin"]
        result = round(sin_val, 10)
        question = (
            f"Semplifica e calcola tan({angle}°) · cos({angle}°)."
        )
        explanation = (
            f"tan(α) = sin(α)/cos(α), quindi tan(α)·cos(α) = sin(α).\n"
            f"tan({angle}°)·cos({angle}°) = sin({angle}°) = {_fmt(result)}."
        )
    else:
        # sin²(α) + cos²(α) + tan²(α) = 1 + tan²(α) = 1/cos²(α)
        angle = random.choice([30, 45, 60])
        cos_val = _TRIG_NOTABLE[angle]["cos"]
        result = round(1.0 / (cos_val ** 2), 10)
        question = (
            f"Calcola sin²({angle}°) + cos²({angle}°) + tan²({angle}°)."
        )
        explanation = (
            f"sin²(α) + cos²(α) = 1, quindi l'espressione vale 1 + tan²({angle}°).\n"
            f"Per l'identita': 1 + tan²(α) = 1/cos²(α).\n"
            f"1/cos²({angle}°) = 1/({_fmt(cos_val)})² = {_fmt(result)}."
        )

    tip = (
        "Identita' utili: sin²+cos²=1, 1+tan²=1/cos², "
        "tan=sin/cos, (1-cos²)/sin = sin."
    )
    return question, result, explanation, tip


# ---------------------------------------------------------------------------
# EXPONENTIAL & LOGARITHMIC Templates
# ---------------------------------------------------------------------------

def _t1_exp_basic():
    """Solve b^x = b^n for x (same base)."""
    base = random.choice([2, 3, 5, 10])
    n = random.randint(1, 6)
    target = base ** n
    result = float(n)

    question = f"Risolvi l'equazione {base}^x = {target}. Quanto vale x?"
    explanation = (
        f"{target} = {base}^{n}, quindi {base}^x = {base}^{n}.\n"
        f"Uguagliando gli esponenti: x = {n}."
    )
    tip = "Se a^x = a^n con a > 0 e a ≠ 1, allora x = n."
    return question, result, explanation, tip


def _t1_log_basic():
    """Compute log_b(v) where v is a perfect power of b."""
    base = random.choice([2, 3, 5, 10])
    exp = random.randint(1, 5)
    value = base ** exp
    result = float(exp)

    question = f"Calcola log_{base}({value})."
    explanation = (
        f"log_{base}({value}) = x significa {base}^x = {value}.\n"
        f"Poiche' {base}^{exp} = {value}, il risultato e' {exp}."
    )
    tip = "log_b(x) = n significa b^n = x. In pratica, il logaritmo chiede: 'a quale potenza devo elevare la base?'"
    return question, result, explanation, tip


def _t2_exp_equation_different_bases():
    """Solve a^x = b where a and b have a common base: e.g. 4^x = 2^6."""
    common_base = random.choice([2, 3])
    exp_a = random.choice([2, 3])  # a = common_base^exp_a
    a = common_base ** exp_a
    exp_target = random.choice([2, 3, 4, 6])
    target = common_base ** exp_target

    # a^x = target => (common_base^exp_a)^x = common_base^exp_target
    # => exp_a * x = exp_target => x = exp_target / exp_a
    x_val = exp_target / exp_a
    result = float(x_val)

    question = f"Risolvi l'equazione {a}^x = {target}. Quanto vale x?"
    explanation = (
        f"Scriviamo tutto in base {common_base}: {a} = {common_base}^{exp_a} e {target} = {common_base}^{exp_target}.\n"
        f"({common_base}^{exp_a})^x = {common_base}^{exp_target}\n"
        f"{common_base}^({exp_a}x) = {common_base}^{exp_target}\n"
        f"{exp_a}x = {exp_target}, quindi x = {exp_target}/{exp_a} = {_fmt(result)}."
    )
    tip = "Per risolvere equazioni esponenziali con basi diverse, cerca di ricondurle alla stessa base."
    return question, result, explanation, tip


def _t2_log_properties():
    """Use log properties: log(a·b) = log(a)+log(b), log(a^n) = n·log(a)."""
    base = random.choice([2, 3, 5, 10])
    variant = random.randint(1, 3)

    if variant == 1:
        # log_b(a·c) where a and c are powers of b
        exp1 = random.randint(1, 3)
        exp2 = random.randint(1, 3)
        val1 = base ** exp1
        val2 = base ** exp2
        product = val1 * val2
        result = float(exp1 + exp2)
        question = f"Calcola log_{base}({product}) sapendo che {product} = {val1} × {val2}."
        explanation = (
            f"log_{base}({product}) = log_{base}({val1} × {val2}) = log_{base}({val1}) + log_{base}({val2})\n"
            f"= {exp1} + {exp2} = {_fmt(result)}."
        )
    elif variant == 2:
        # n · log_b(v) = log_b(v^n)
        exp = random.randint(1, 4)
        n = random.randint(2, 3)
        val = base ** exp
        result = float(n * exp)
        question = f"Calcola {n} · log_{base}({val})."
        explanation = (
            f"{n} · log_{base}({val}) = {n} × {exp} = {_fmt(result)}.\n"
            f"(Proprieta': n·log(a) = log(a^n), quindi = log_{base}({val}^{n}) = log_{base}({val ** n}))."
        )
    else:
        # log_b(a/c)
        exp1 = random.randint(2, 5)
        exp2 = random.randint(1, exp1 - 1)
        val1 = base ** exp1
        val2 = base ** exp2
        result = float(exp1 - exp2)
        question = f"Calcola log_{base}({val1}/{val2})."
        explanation = (
            f"log_{base}({val1}/{val2}) = log_{base}({val1}) - log_{base}({val2})\n"
            f"= {exp1} - {exp2} = {_fmt(result)}."
        )

    tip = (
        "Proprieta' dei logaritmi: log(a·b) = log(a)+log(b), "
        "log(a/b) = log(a)-log(b), log(a^n) = n·log(a)."
    )
    return question, result, explanation, tip


def _t3_log_domain():
    """Find the minimum value of x for log function domain."""
    base = random.choice([2, 3, 10])
    # f(x) = log_base(x - a) requires x - a > 0 => x > a
    a = random.randint(-5, 10)

    variant = random.randint(1, 2)
    if variant == 1:
        # log_b(x - a), domain: x > a
        result = float(a)
        question = (
            f"Qual e' il valore minimo (escluso) che puo' assumere x affinche' "
            f"f(x) = log_{base}(x - {a}) sia definita?"
        )
        sign_a = f"- {a}" if a >= 0 else f"+ {abs(a)}"
        explanation = (
            f"La funzione logaritmo e' definita solo per argomento positivo.\n"
            f"x {sign_a} > 0 => x > {a}.\n"
            f"Il valore minimo (escluso) e' x = {a}."
        )
    else:
        # log_b(2x - a), domain: x > a/2
        a = random.choice([2, 4, 6, 8, 10])
        result = float(a / 2)
        question = (
            f"Qual e' il valore minimo (escluso) che puo' assumere x affinche' "
            f"f(x) = log_{base}(2x - {a}) sia definita?"
        )
        explanation = (
            f"La funzione logaritmo e' definita solo per argomento positivo.\n"
            f"2x - {a} > 0 => 2x > {a} => x > {a}/2 = {_fmt(result)}.\n"
            f"Il valore minimo (escluso) e' x = {_fmt(result)}."
        )

    tip = "Il dominio di log_b(f(x)) richiede f(x) > 0. Risolvi la disequazione nell'argomento."
    return question, result, explanation, tip


def _t3_exp_inequality():
    """Solve exponential inequalities: b^x > b^n."""
    base = random.choice([2, 3, 5])
    n = random.randint(1, 5)
    target = base ** n

    variant = random.randint(1, 2)
    if variant == 1:
        # b^x > target => x > n (base > 1)
        result = float(n + 1)  # smallest integer > n
        question = (
            f"Risolvi la disequazione {base}^x > {target}. "
            f"Qual e' il piu' piccolo intero che soddisfa la disequazione?"
        )
        explanation = (
            f"{target} = {base}^{n}, quindi {base}^x > {base}^{n}.\n"
            f"Poiche' la base {base} > 1, la funzione esponenziale e' crescente:\n"
            f"x > {n}. Il piu' piccolo intero e' {_fmt(result)}."
        )
    else:
        # b^x <= target => x <= n
        result = float(n)  # largest integer <= n
        question = (
            f"Risolvi la disequazione {base}^x ≤ {target}. "
            f"Qual e' il piu' grande intero che soddisfa la disequazione?"
        )
        explanation = (
            f"{target} = {base}^{n}, quindi {base}^x ≤ {base}^{n}.\n"
            f"Poiche' la base {base} > 1, la funzione esponenziale e' crescente:\n"
            f"x ≤ {n}. Il piu' grande intero e' {_fmt(result)}."
        )

    tip = (
        "Per disequazioni esponenziali con base > 1: b^x > b^n => x > n "
        "(la funzione e' crescente, il verso si conserva)."
    )
    return question, result, explanation, tip


# ---------------------------------------------------------------------------
# Rational Exponent Templates
# ---------------------------------------------------------------------------


def _t1_rational_exponent_basic():
    """Simplify (sqrt(a))^n where n is even, result is a^(n/2) integer.

    Example: (sqrt(2))^6 = 2^3 = 8
    """
    a = random.choice([2, 3, 5])
    half_exp = random.randint(2, 5)
    n = half_exp * 2  # ensure n is even so a^(n/2) is integer
    result = float(a ** half_exp)

    question = f"Semplifica (√{a})^{n}. Quanto vale?"
    explanation = (
        f"(√{a})^{n} = ({a}^(1/2))^{n} = {a}^({n}/2) = {a}^{half_exp} = {_fmt(result)}."
    )
    tip = (
        "Ricorda che √a = a^(1/2), quindi (√a)^n = a^(n/2). "
        "Se n e' pari, il risultato e' una potenza intera della base."
    )
    return question, result, explanation, tip


def _t2_rational_exponent_cube():
    """Simplify (cbrt(a))^n where n is multiple of 3, result is a^(n/3) integer.

    Example: (cbrt(3))^9 = 3^3 = 27
    """
    a = random.choice([2, 3, 5])
    third_exp = random.randint(2, 4)
    n = third_exp * 3  # ensure n is multiple of 3
    result = float(a ** third_exp)

    question = f"Semplifica (∛{a})^{n}. Quanto vale?"
    explanation = (
        f"(∛{a})^{n} = ({a}^(1/3))^{n} = {a}^({n}/3) = {a}^{third_exp} = {_fmt(result)}."
    )
    tip = (
        "Ricorda che ∛a = a^(1/3), quindi (∛a)^n = a^(n/3). "
        "Se n e' multiplo di 3, il risultato e' una potenza intera della base."
    )
    return question, result, explanation, tip


def _t2_rational_exponent_general():
    """Simplify a^(m/n) where a is a perfect n-th power and result is integer.

    Example: 8^(2/3) = (8^(1/3))^2 = 2^2 = 4
    """
    # Pick a small base and root index, then build a = base^n so a^(1/n) = base
    base = random.choice([2, 3, 5])
    n = random.choice([2, 3])  # root index
    m = random.randint(2, 4)   # numerator exponent
    # Ensure m/n is not an integer already (that would be trivial)
    while m % n == 0:
        m = random.randint(2, 4)
    a = base ** n  # a is a perfect n-th power
    result = float(base ** m)

    # Build readable step-by-step
    root_name = "quadrata" if n == 2 else "cubica"
    question = f"Calcola {a}^({m}/{n}). Quanto vale?"
    explanation = (
        f"{a}^({m}/{n}) = ({a}^(1/{n}))^{m}.\n"
        f"La radice {root_name} di {a} e' {base} (perche' {base}^{n} = {a}).\n"
        f"Quindi {a}^({m}/{n}) = {base}^{m} = {_fmt(result)}."
    )
    tip = (
        "a^(m/n) si puo' calcolare come (a^(1/n))^m, cioe' prima si estrae "
        "la radice n-esima e poi si eleva alla potenza m."
    )
    return question, result, explanation, tip


# ---------------------------------------------------------------------------
# Radical equations with domain validation (L2 and L3)
# ---------------------------------------------------------------------------


def _t2_solve_radical_simple():
    """Solve sqrt(ax + b) = c with domain validation."""
    a = random.randint(1, 3)
    c = random.randint(2, 5)
    c_sq = c * c
    # Pick x_sol so that (c^2 - b) / a is integer and b stays small
    x_sol = random.randint(1, 10)
    b = c_sq - a * x_sol  # ensures ax+b = c^2 exactly

    # Format the radicand
    if a == 1:
        radicand = f"x + {b}" if b >= 0 else f"x - {abs(b)}"
    else:
        radicand = f"{a}x + {b}" if b >= 0 else f"{a}x - {abs(b)}"

    question = f"Risolvi l'equazione √({radicand}) = {c}"
    correct_str = f"x = {x_sol}"

    distractors = [
        f"x = {-x_sol}",
        f"x = {c_sq}",
        f"x = {c}",
        "Nessuna soluzione",
    ]

    explanation = (
        f"Eleviamo al quadrato entrambi i membri: {radicand} = {c}² = {c_sq}.\n"
        f"Risolvendo: {a}x = {c_sq} - {f'({b})' if b < 0 else b} = {c_sq - b}, "
        f"quindi x = {x_sol}.\n"
        f"Verifica dominio: {a}·{x_sol} + {f'({b})' if b < 0 else b} = {c_sq} ≥ 0 ✓\n"
        f"Verifica: √({c_sq}) = {c} ✓"
    )
    tip = (
        "Per risolvere equazioni con radicali: eleva al quadrato entrambi i "
        "membri e poi verifica che la soluzione appartenga al dominio "
        "(l'argomento del radicale deve essere ≥ 0)."
    )
    return question, correct_str, distractors, explanation, tip


def _t2_solve_radical_linear():
    """Solve sqrt(x + b) = x + d, with extraneous solution check."""
    # Pick a valid solution x_sol (positive, small)
    x_sol = random.randint(1, 6)
    # Pick d so that x_sol + d >= 0 and sqrt value is nice
    # sqrt(x_sol + b) = x_sol + d  =>  x_sol + b = (x_sol + d)^2
    # We need x_sol + d > 0 (right side of original equation must be >= 0)
    d = random.choice([-1, 0, 1, 2])
    rhs_val = x_sol + d
    if rhs_val < 0:
        d = 0
        rhs_val = x_sol + d

    b = rhs_val ** 2 - x_sol  # so x_sol + b = (x_sol + d)^2

    # After squaring: x + b = (x + d)^2 = x^2 + 2dx + d^2
    # => x^2 + (2d - 1)x + (d^2 - b) = 0
    A_coeff = 1
    B_coeff = 2 * d - 1
    C_coeff = d * d - b
    discriminant = B_coeff ** 2 - 4 * A_coeff * C_coeff

    solutions = []
    if discriminant >= 0:
        sqrt_disc = math.isqrt(max(0, discriminant)) if discriminant == int(discriminant) else -1
        if sqrt_disc >= 0 and sqrt_disc * sqrt_disc == discriminant:
            s1 = (-B_coeff + sqrt_disc) // (2 * A_coeff) if (-B_coeff + sqrt_disc) % (2 * A_coeff) == 0 else None
            s2 = (-B_coeff - sqrt_disc) // (2 * A_coeff) if (-B_coeff - sqrt_disc) % (2 * A_coeff) == 0 else None
            for s in [s1, s2]:
                if s is not None:
                    solutions.append(s)

    # Validate each solution: x + b >= 0 AND x + d >= 0 AND sqrt(x+b) == x+d
    valid = []
    extraneous = []
    for s in set(solutions):
        if s + b >= 0 and s + d >= 0 and abs(math.isqrt(s + b) - (s + d)) < 1e-9:
            val_check = s + b
            sqrt_val = math.isqrt(val_check)
            if sqrt_val * sqrt_val == val_check and sqrt_val == s + d:
                valid.append(s)
            else:
                extraneous.append(s)
        else:
            extraneous.append(s)

    # Ensure we always have at least x_sol as valid
    if x_sol not in valid:
        valid = [x_sol]
        extraneous = [s for s in solutions if s != x_sol]

    # Format radicand
    radicand = f"x + {b}" if b >= 0 else f"x - {abs(b)}"
    rhs = f"x + {d}" if d >= 0 else f"x - {abs(d)}"
    if d == 0:
        rhs = "x"

    question = f"Risolvi √({radicand}) = {rhs}. Indica la/le soluzione/i valida/e."

    if len(valid) == 1:
        correct_str = f"x = {valid[0]}"
    else:
        valid_sorted = sorted(valid)
        correct_str = f"x = {valid_sorted[0]} e x = {valid_sorted[1]}"

    # Build distractors
    distractors = []
    if extraneous:
        distractors.append(f"x = {extraneous[0]}")
    if len(solutions) >= 2:
        all_sorted = sorted(set(solutions))
        distractors.append(f"x = {all_sorted[0]} e x = {all_sorted[1]}")
    distractors.append("Nessuna soluzione")
    # Add arithmetic-error distractor
    distractors.append(f"x = {x_sol + 2}")
    # Ensure exactly 4
    extra_vals = [x_sol - 1, x_sol + 3, -x_sol, x_sol * 2]
    for ev in extra_vals:
        if len(distractors) >= 4:
            break
        candidate = f"x = {ev}"
        if candidate != correct_str and candidate not in distractors:
            distractors.append(candidate)
    distractors = [d for d in distractors if d != correct_str][:4]
    while len(distractors) < 4:
        distractors.append(f"x = {x_sol + len(distractors) + 5}")

    explanation = (
        f"Eleviamo al quadrato: {radicand} = ({rhs})² = x² + {2*d}x + {d*d}.\n"
        f"Riordinando: x² + {2*d - 1}x + {d*d - b} = 0.\n"
    )
    if len(valid) == 1:
        explanation += (
            f"Risolvendo e verificando il dominio ({radicand} ≥ 0 e {rhs} ≥ 0), "
            f"l'unica soluzione valida e' x = {valid[0]}."
        )
    else:
        explanation += (
            f"Risolvendo e verificando il dominio, le soluzioni valide sono: "
            + ", ".join(f"x = {v}" for v in sorted(valid)) + "."
        )
    if extraneous:
        explanation += (
            f"\nx = {extraneous[0]} e' una soluzione estranea "
            f"(non soddisfa il dominio)."
        )

    tip = (
        "Quando risolvi equazioni irrazionali, dopo aver elevato al quadrato "
        "devi SEMPRE verificare le soluzioni nell'equazione originale. "
        "L'elevamento al quadrato puo' introdurre soluzioni estranee."
    )
    return question, correct_str, distractors, explanation, tip


def _t3_solve_radical_two_radicals():
    """Solve sqrt(x+b) + sqrt(x+d) = e with two radicals."""
    # Pick x_sol and b, d so that sqrt values are integers
    # sqrt(x_sol + b) = p, sqrt(x_sol + d) = q, e = p + q
    p = random.randint(1, 5)
    q = random.randint(1, 5)
    while p == q:
        q = random.randint(1, 5)
    e = p + q
    x_sol = random.randint(0, 8)
    b = p * p - x_sol
    d = q * q - x_sol

    # Verify
    assert x_sol + b == p * p
    assert x_sol + d == q * q

    # Format radicands
    rad1 = f"x + {b}" if b >= 0 else f"x - {abs(b)}"
    rad2 = f"x + {d}" if d >= 0 else f"x - {abs(d)}"

    question = f"Risolvi √({rad1}) + √({rad2}) = {e}"
    correct_str = f"x = {x_sol}"

    # Distractors: common mistakes
    wrong1 = e * e  # squaring the sum directly
    wrong2 = x_sol + p  # confusing p with answer shift
    wrong3 = -x_sol if x_sol != 0 else x_sol + 3  # sign error
    wrong4_candidates = [x_sol + 1, x_sol - 1, x_sol + 2, x_sol * 2, e]
    wrong4 = wrong4_candidates[0]
    for wc in wrong4_candidates:
        if wc not in (x_sol, wrong1, wrong2, wrong3):
            wrong4 = wc
            break

    distractors_set = set()
    for val in [wrong1, wrong2, wrong3, wrong4]:
        candidate = f"x = {val}"
        if candidate != correct_str:
            distractors_set.add(candidate)
    distractors_set.add("Nessuna soluzione")
    distractors = list(distractors_set)[:4]
    while len(distractors) < 4:
        filler = f"x = {x_sol + len(distractors) + 10}"
        if filler not in distractors and filler != correct_str:
            distractors.append(filler)

    explanation = (
        f"Isoliamo un radicale: √({rad1}) = {e} - √({rad2}).\n"
        f"Eleviamo al quadrato: {rad1} = {e}² - 2·{e}·√({rad2}) + ({rad2}).\n"
        f"Semplificando e isolando il radicale residuo, eleviamo ancora al quadrato.\n"
        f"La soluzione e' x = {x_sol}.\n"
        f"Verifica: √({x_sol + b}) + √({x_sol + d}) = {p} + {q} = {e} ✓"
    )
    tip = (
        "Con due radicali, isola un radicale da un lato, eleva al quadrato, "
        "poi isola il radicale restante ed eleva di nuovo al quadrato. "
        "Verifica sempre la soluzione nell'equazione originale."
    )
    return question, correct_str, distractors, explanation, tip


def _t3_solve_radical_extraneous():
    """Equation where squaring introduces an extraneous solution."""
    # Equation: sqrt(a - x) = x - c
    # Domain: a - x >= 0  =>  x <= a
    # AND: x - c >= 0  =>  x >= c
    # After squaring: a - x = x^2 - 2cx + c^2
    # => x^2 + (1 - 2c)x + (c^2 - a) = 0

    # Pick parameters to get one valid and one extraneous solution
    # Pick c small, a so discriminant gives integer roots
    c = random.randint(1, 3)
    # We want two integer solutions from x^2 + (1-2c)x + (c^2-a) = 0
    # Pick two roots r1, r2: r1 + r2 = 2c - 1, r1 * r2 = c^2 - a
    # Pick r1 (valid) and r2 (extraneous)
    # Valid: c <= r1 <= a, and sqrt(a-r1) = r1 - c
    r1 = c + random.randint(0, 3)  # valid: r1 >= c
    # r1 + r2 = 2c - 1 => r2 = 2c - 1 - r1
    r2 = 2 * c - 1 - r1
    # a = c^2 - r1 * r2
    a = c * c - r1 * r2

    # Verify r1 is valid
    valid_r1 = (a - r1 >= 0) and (r1 - c >= 0) and (a - r1 == (r1 - c) ** 2)
    # Verify r2 is extraneous
    if r2 == r1:
        # Degenerate, retry with fixed values
        c, r1, r2, a = 2, 3, -2, 5
        # sqrt(5 - x) = x - 2: at x=3, sqrt(2)=1 ✓ (wait, 3-2=1, 5-3=2, sqrt(2)!=1)
        # Let's use a known working example
        # sqrt(a - x) = x - c with c=1, r1=3: sqrt(a-3)=2, a-3=4, a=7
        # r2 = 2*1-1-3 = -2, c^2 - r1*r2 = 1-3*(-2)=7 ✓
        # Check r2=-2: a-r2=9, sqrt(9)=3, r2-c=-3, 3 != -3 => extraneous ✓
        c, r1, a = 1, 3, 7
        r2 = 2 * c - 1 - r1  # = -2

    if not valid_r1:
        # Fallback to known good example
        c, r1, a = 1, 3, 7
        r2 = -2

    # Double-check
    assert a - r1 >= 0 and r1 - c >= 0
    assert (r1 - c) ** 2 == a - r1

    # Check r2 is extraneous
    r2_extraneous = True
    if a - r2 >= 0 and r2 - c >= 0:
        if (r2 - c) ** 2 == a - r2:
            r2_extraneous = False

    if not r2_extraneous:
        # Both valid — pick different params where one is extraneous
        c, r1, a = 1, 3, 7
        r2 = -2

    # Format equation
    radicand = f"{a} - x" if a > 0 else f"-x - {abs(a)}"
    rhs = f"x - {c}" if c > 0 else f"x + {abs(c)}"

    if r2_extraneous:
        num_solutions = 1
        correct_str = f"1 soluzione: x = {r1}"
        distractors = [
            f"2 soluzioni: x = {r1} e x = {r2}",
            f"1 soluzione: x = {r2}",
            "Nessuna soluzione",
            f"2 soluzioni: x = {r1} e x = {r1 + 1}",
        ]
    else:
        num_solutions = 2
        sorted_sols = sorted([r1, r2])
        correct_str = f"2 soluzioni: x = {sorted_sols[0]} e x = {sorted_sols[1]}"
        distractors = [
            f"1 soluzione: x = {r1}",
            f"1 soluzione: x = {r2}",
            "Nessuna soluzione",
            f"2 soluzioni: x = {r1} e x = {r1 + 2}",
        ]

    question = (
        f"Risolvi √({radicand}) = {rhs}. Quante soluzioni valide ha?"
    )

    explanation = (
        f"Eleviamo al quadrato: {radicand} = ({rhs})².\n"
        f"Otteniamo x² + {1 - 2*c}x + {c*c - a} = 0.\n"
        f"Le soluzioni dell'equazione quadratica sono x = {r1} e x = {r2}.\n"
    )
    if r2_extraneous:
        explanation += (
            f"Verifica x = {r1}: √({a} - {r1}) = √({a - r1}) = {r1 - c}, "
            f"e {r1} - {c} = {r1 - c} ✓\n"
            f"Verifica x = {r2}: dominio richiede x - {c} ≥ 0, "
            f"ma {r2} - {c} = {r2 - c} < 0 ✗ (soluzione estranea).\n"
            f"Quindi c'e' una sola soluzione: x = {r1}."
        )
    else:
        explanation += "Entrambe le soluzioni soddisfano il dominio."

    tip = (
        "Attenzione alle soluzioni estranee! Quando elevi al quadrato "
        "un'equazione irrazionale, puoi introdurre soluzioni che non "
        "soddisfano l'equazione originale. Verifica SEMPRE ogni soluzione."
    )
    return question, correct_str, distractors, explanation, tip


# ---------------------------------------------------------------------------
# Template registries
# ---------------------------------------------------------------------------

# Templates that return (question, correct_value, explanation, tip)
# i.e., 4-tuple templates (numeric answer)
_NUMERIC_TEMPLATES_L1 = [
    _t1_linear_equation,
    _t1_powers_and_roots,
    _t1_percentage_calculation,
    _t1_absolute_value,
    _t1_simple_expression,
    _t1_gcd_two_simple,
    _t1_lcm_two_simple,
    _t1_exp_basic,
    _t1_log_basic,
    _t1_rational_exponent_basic,
]

_NUMERIC_TEMPLATES_L2 = [
    _t2_quadratic_equation,
    _t2_system_linear,
    _t2_expression_simplification,
    _t2_logarithmic_expression,
    _t2_radical_simplification,
    _t2_gcd_lcm,
    _t2_lcm_periodicity,
    _t2_gcd_equal_groups,
    _t2_trig_equation_simple,
    _t2_trig_expression,
    _t2_exp_equation_different_bases,
    _t2_log_properties,
    _t2_rational_exponent_cube,
    _t2_rational_exponent_general,
]

_NUMERIC_TEMPLATES_L3 = [
    _t3_parametric_equation,
    _t3_inequality,
    _t3_exponential_equation,
    _t3_system_with_quadratic,
    _t3_function_evaluation,
    _t3_compound_fraction,
    _t3_gcd_three_numbers,
    _t3_lcm_three_numbers,
    _t3_trig_equation_parametric,
    _t3_trig_simplification,
    _t3_log_domain,
    _t3_exp_inequality,
]

# Templates that return (question, correct_str, distractors_list, explanation, tip)
# i.e., 5-tuple templates (string answer with custom distractors)
_STRING_TEMPLATES_L1 = [
    _t1_fraction_addition,
    _t2_fraction_simplification,
    _t1_trig_notable_values,
    _t1_trig_basic_identity,
]

# Some L2 templates return 5-tuple (string) depending on variant
_STRING_TEMPLATES_L2 = [
    _t2_trig_convert_deg_rad,
    _t2_solve_radical_simple,
    _t2_solve_radical_linear,
]

_STRING_TEMPLATES_L3 = [
    _t3_solve_radical_two_radicals,
    _t3_solve_radical_extraneous,
]


class SolveExercise(Exercise):
    """Calcola e Risolvi -- solve equations and expressions, choose the correct answer."""

    TEMPLATES_L1_NUMERIC = _NUMERIC_TEMPLATES_L1
    TEMPLATES_L1_STRING = _STRING_TEMPLATES_L1
    TEMPLATES_L2_NUMERIC = _NUMERIC_TEMPLATES_L2
    TEMPLATES_L2_STRING = _STRING_TEMPLATES_L2
    TEMPLATES_L3 = _NUMERIC_TEMPLATES_L3
    TEMPLATES_L3_STRING = _STRING_TEMPLATES_L3

    @staticmethod
    def _build_from_result(result_tuple, difficulty):
        """Build exercise dict from a template result (4-tuple numeric or 5-tuple string)."""
        if len(result_tuple) == 5:
            question, correct_str, distractors, explanation, tip = result_tuple
            options = [str(correct_str)] + [str(d) for d in distractors[:4]]
        else:
            question, correct_value, explanation, tip = result_tuple
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

    def generate(self, difficulty: int) -> dict:
        difficulty = max(1, min(3, difficulty))

        if difficulty == 1:
            all_templates = (
                list(self.TEMPLATES_L1_NUMERIC)
                + list(self.TEMPLATES_L1_STRING)
            )
        elif difficulty == 2:
            all_templates = (
                list(self.TEMPLATES_L2_NUMERIC)
                + list(self.TEMPLATES_L2_STRING)
            )
        else:
            all_templates = (
                list(self.TEMPLATES_L3)
                + list(self.TEMPLATES_L3_STRING)
            )

        template_fn = random.choice(all_templates)
        result_tuple = template_fn()
        return self._build_from_result(result_tuple, difficulty)
