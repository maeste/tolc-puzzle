import math
import random

from exercises.base import Exercise


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _fraction_label(num, den):
    """Return a human-friendly Italian label for a rational factor."""
    if den == 1:
        return _integer_factor_label(num)
    if num == 1 and den == 2:
        return "si dimezza"
    if num == 1 and den == 3:
        return "diventa 1/3"
    if num == 1 and den == 4:
        return "diventa 1/4"
    return f"si moltiplica per {num}/{den}"


def _integer_factor_label(k):
    """Italian label for an integer multiplier."""
    labels = {
        1: "resta uguale",
        2: "raddoppia",
        3: "triplica",
        4: "quadruplica",
        8: "si moltiplica per 8",
        9: "si moltiplica per 9",
        16: "si moltiplica per 16",
        27: "si moltiplica per 27",
    }
    if k in labels:
        return labels[k]
    return f"si moltiplica per {k}"


def _sqrt_label(k):
    """Italian label for sqrt-type multiplier."""
    if k == 2:
        return "si moltiplica per \u221a2"
    if k == 3:
        return "si moltiplica per \u221a3"
    return f"si moltiplica per \u221a{k}"


def _factor_label(num, den):
    """General purpose factor label: handles integers, fractions, sqrt references."""
    if den == 1:
        return _integer_factor_label(num)
    return _fraction_label(num, den)


# ---------------------------------------------------------------------------
# LEVEL 1 TEMPLATES  (direct / inverse proportionality)
# ---------------------------------------------------------------------------

def _t1_direct_proportion():
    """Direct proportionality: y = k * x^n, x gets multiplied."""
    multiplier = random.choice([2, 3, 4])
    mult_word = {2: "raddoppia", 3: "triplica", 4: "quadruplica"}[multiplier]

    # power 1 keeps it simple at level 1
    var_name = random.choice(["y", "P", "F"])
    ind_var = random.choice(["x", "t", "n"])

    formulas = [
        (f"{var_name} = k{ind_var}", 1),
        (f"{var_name} = k \u00b7 {ind_var}", 1),
    ]
    formula, power = random.choice(formulas)

    result_factor = multiplier ** power  # multiplier^1
    correct = _integer_factor_label(result_factor)

    question = (
        f"Se {formula} e {ind_var} {mult_word}, come cambia {var_name}?"
    )

    # Build distractors (4 wrong answers, all distinct from correct)
    pool = [
        "raddoppia", "triplica", "quadruplica",
        "resta uguale", "si dimezza",
        "diventa 1/3", "diventa 1/4",
    ]
    distractors = [d for d in pool if d != correct]
    random.shuffle(distractors)
    distractors = distractors[:4]

    explanation = (
        f"1) Formula originale: {formula}\n"
        f"2) Sostituiamo {ind_var} con {multiplier}{ind_var}: "
        f"{var_name}' = k \u00b7 ({multiplier}{ind_var}) = {multiplier} \u00b7 k{ind_var}\n"
        f"3) Il fattore moltiplicativo e {multiplier}\n"
        f"4) Quindi {var_name} {correct}."
    )
    tip = (
        "In una proporzionalita diretta y = kx, se x viene moltiplicato per m, "
        "anche y viene moltiplicato per m."
    )
    return question, correct, distractors, explanation, tip


def _t1_inverse_proportion():
    """Inverse proportionality: y = k / x^n, x gets multiplied."""
    multiplier = random.choice([2, 3, 4])
    mult_word = {2: "raddoppia", 3: "triplica", 4: "quadruplica"}[multiplier]

    var_name = random.choice(["y", "P", "I"])
    ind_var = random.choice(["x", "d", "r"])

    formulas = [
        (f"{var_name} = k/{ind_var}", 1),
        (f"{var_name} = k/{ind_var}\u00b2", 2),
    ]
    formula, power = random.choice(formulas)

    # If x is multiplied by m, y is multiplied by 1/m^power
    den = multiplier ** power
    correct = _fraction_label(1, den)

    question = (
        f"Se {formula} e {ind_var} {mult_word}, come cambia {var_name}?"
    )

    pool = [
        "raddoppia", "triplica", "quadruplica",
        "resta uguale", "si dimezza",
        "diventa 1/3", "diventa 1/4",
        "diventa 1/9", "diventa 1/16",
        "si moltiplica per 1/8",
    ]
    distractors = [d for d in pool if d != correct]
    random.shuffle(distractors)
    distractors = distractors[:4]

    sub_text = f"{multiplier}{ind_var}" if power == 1 else f"({multiplier}{ind_var})\u00b2"
    simp_text = f"{multiplier}" if power == 1 else f"{den}"

    explanation = (
        f"1) Formula originale: {formula}\n"
        f"2) Sostituiamo {ind_var} con {multiplier}{ind_var}: "
        f"{var_name}' = k / {sub_text} = k / ({simp_text} \u00b7 {ind_var}{'' if power == 1 else '\u00b2'}) "
        f"= (1/{den}) \u00b7 {var_name}\n"
        f"3) Il fattore moltiplicativo e 1/{den}\n"
        f"4) Quindi {var_name} {correct}."
    )
    tip = (
        "In una proporzionalita inversa y = k/x, se x viene moltiplicato per m, "
        "y viene diviso per m. Con y = k/x\u00b2 il fattore e 1/m\u00b2."
    )
    return question, correct, distractors, explanation, tip


# ---------------------------------------------------------------------------
# LEVEL 2 TEMPLATES  (squared proportion / compound percentage)
# ---------------------------------------------------------------------------

def _t2_squared_proportion():
    """Quadratic dependence in real formulas: A = pi*r^2, E = 1/2*mv^2, etc."""
    multiplier = random.choice([2, 3, 4])
    mult_word = {2: "raddoppia", 3: "triplica", 4: "quadruplica"}[multiplier]

    scenarios = [
        ("A", "r", "A = \u03c0r\u00b2", "l'area del cerchio", 2),
        ("E", "v", "E = \u00bdmv\u00b2", "l'energia cinetica", 2),
        ("F", "r", "F = GMm/r\u00b2", "la forza gravitazionale (inversamente)", -2),
        ("S", "t", "S = \u00bdat\u00b2", "lo spazio nel moto uniformemente accelerato", 2),
    ]

    dep_var, ind_var, formula, context, power = random.choice(scenarios)

    if power > 0:
        result = multiplier ** power
        correct = _integer_factor_label(result)
    else:
        den = multiplier ** abs(power)
        correct = _fraction_label(1, den)

    question = (
        f"Nella formula {formula} ({context}), se {ind_var} {mult_word}, "
        f"come cambia {dep_var}?"
    )

    pool = [
        "raddoppia", "triplica", "quadruplica",
        "si moltiplica per 8", "si moltiplica per 9", "si moltiplica per 16",
        "resta uguale", "si dimezza",
        "diventa 1/3", "diventa 1/4", "diventa 1/9", "diventa 1/16",
    ]
    distractors = [d for d in pool if d != correct]
    random.shuffle(distractors)
    distractors = distractors[:4]

    if power > 0:
        sub_text = f"({multiplier}{ind_var})\u00b2 = {multiplier**2} \u00b7 {ind_var}\u00b2"
        explanation = (
            f"1) Formula originale: {formula}\n"
            f"2) Sostituiamo {ind_var} con {multiplier}{ind_var}: "
            f"{ind_var}\u00b2 diventa {sub_text}\n"
            f"3) Il fattore moltiplicativo e {multiplier**2}\n"
            f"4) Quindi {dep_var} {correct}."
        )
    else:
        den_val = multiplier ** abs(power)
        explanation = (
            f"1) Formula originale: {formula}\n"
            f"2) Sostituiamo {ind_var} con {multiplier}{ind_var}: "
            f"{ind_var}\u00b2 diventa ({multiplier}{ind_var})\u00b2 = {den_val}{ind_var}\u00b2\n"
            f"3) Poiche {ind_var}\u00b2 e al denominatore, {dep_var} si moltiplica per 1/{den_val}\n"
            f"4) Quindi {dep_var} {correct}."
        )

    tip = (
        "Quando una variabile compare al quadrato, moltiplicarla per m "
        "produce un fattore m\u00b2, non m. Attenzione alla differenza tra "
        "dipendenza lineare e quadratica!"
    )
    return question, correct, distractors, explanation, tip


def _t2_compound_percentage():
    """Compound percentage: two successive % changes don't simply add up."""
    p1 = random.choice([10, 15, 20, 25, 30])
    p2 = random.choice([5, 10, 15, 20, 25])

    # Randomly decide if second change is increase or decrease
    second_increase = random.choice([True, False])
    if second_increase:
        factor = (1 + p1 / 100) * (1 + p2 / 100)
        total_pct = round((factor - 1) * 100, 1)
        # Clean up .0
        if total_pct == int(total_pct):
            total_pct = int(total_pct)
        correct = f"{total_pct}%"
        verb2 = f"aumenta del {p2}%"
    else:
        factor = (1 + p1 / 100) * (1 - p2 / 100)
        total_pct = round((factor - 1) * 100, 1)
        if total_pct == int(total_pct):
            total_pct = int(total_pct)
        correct = f"{total_pct}%"
        verb2 = f"diminuisce del {p2}%"

    question = (
        f"Un prezzo aumenta del {p1}% e poi {verb2}. "
        f"Di quanto e variato in totale rispetto al valore iniziale?"
    )

    # Common mistakes
    if second_increase:
        naive_sum = p1 + p2
    else:
        naive_sum = p1 - p2
    naive_product = round(p1 * p2 / 100, 1)
    if naive_product == int(naive_product):
        naive_product = int(naive_product)

    d_candidates = [
        f"{naive_sum}%",
        f"{naive_product}%",
        f"{p1}%",
        f"{p2}%",
        f"{abs(total_pct) + 5}%",
        f"{abs(total_pct) - 3}%" if abs(total_pct) > 3 else f"{abs(total_pct) + 3}%",
    ]
    distractors = list(dict.fromkeys(d for d in d_candidates if d != correct))
    random.shuffle(distractors)
    distractors = distractors[:4]
    # Ensure we have exactly 4
    while len(distractors) < 4:
        extra = f"{random.randint(1, 50)}%"
        if extra != correct and extra not in distractors:
            distractors.append(extra)

    f1 = round(1 + p1 / 100, 4)
    if second_increase:
        f2 = round(1 + p2 / 100, 4)
        explanation = (
            f"1) Aumento del {p1}%: il fattore e {f1}\n"
            f"2) Aumento del {p2}%: il fattore e {f2}\n"
            f"3) Fattore composto: {f1} \u00d7 {f2} = {round(factor, 4)}\n"
            f"4) Variazione totale: ({round(factor, 4)} - 1) \u00d7 100 = {total_pct}%\n"
            f"Attenzione: NON si sommano semplicemente {p1}% + {p2}% = {p1 + p2}%!"
        )
    else:
        f2 = round(1 - p2 / 100, 4)
        explanation = (
            f"1) Aumento del {p1}%: il fattore e {f1}\n"
            f"2) Diminuzione del {p2}%: il fattore e {f2}\n"
            f"3) Fattore composto: {f1} \u00d7 {f2} = {round(factor, 4)}\n"
            f"4) Variazione totale: ({round(factor, 4)} - 1) \u00d7 100 = {total_pct}%\n"
            f"Attenzione: NON si sottraggono semplicemente {p1}% - {p2}% = {p1 - p2}%!"
        )

    tip = (
        "Le percentuali successive si compongono moltiplicando i fattori, "
        "non sommando le percentuali. Fattore = (1 + p1/100) \u00d7 (1 + p2/100)."
    )
    return question, correct, distractors, explanation, tip


# ---------------------------------------------------------------------------
# LEVEL 3 TEMPLATES  (parameter variation / combined variation)
# ---------------------------------------------------------------------------

def _t3_parameter_variation():
    """Keep a dependent variable constant while one independent var changes."""
    multiplier = random.choice([2, 3, 4])
    mult_word = {2: "raddoppia", 3: "triplica", 4: "quadruplica"}[multiplier]

    scenarios = [
        # (formula_display, dep_var, changing_var, changing_power,
        #  target_var, target_power, context)
        ("a = 2b/c\u00b2", "a", "b", 1, "c", 2, "una relazione fisica"),
        ("V = \u03c0r\u00b2h", "V", "r", 2, "h", 1, "il volume del cilindro"),
        ("P = F/A", "P", "F", 1, "A", 1, "la pressione"),
        ("E = \u00bdmv\u00b2", "E", "v", 2, "m", 1, "l'energia cinetica"),
    ]

    formula_display, dep_var, ch_var, ch_pow, tgt_var, tgt_pow, context = random.choice(scenarios)

    # If changing_var is multiplied by `multiplier`, the changing_var contributes
    # a factor of multiplier^ch_pow. To keep dep_var constant, target_var must
    # compensate: target_var^tgt_pow must also produce multiplier^ch_pow,
    # so target_var must be multiplied by multiplier^(ch_pow/tgt_pow).

    # Compute rational exponent for target
    # factor_needed^tgt_pow = multiplier^ch_pow
    # factor_needed = multiplier^(ch_pow/tgt_pow)
    exp_num = ch_pow
    exp_den = tgt_pow

    # Simplify
    g = math.gcd(exp_num, exp_den)
    exp_num //= g
    exp_den //= g

    # Build correct answer label
    base = multiplier ** exp_num
    if exp_den == 1:
        correct = f"{tgt_var} {_integer_factor_label(base)}"
    elif exp_den == 2:
        # sqrt case
        if exp_num == 1:
            correct = f"{tgt_var} si moltiplica per \u221a{multiplier}"
        else:
            correct = f"{tgt_var} si moltiplica per \u221a{base}"
    else:
        correct = f"{tgt_var} si moltiplica per {base}^(1/{exp_den})"

    question = (
        f"Nella formula {formula_display} ({context}), se {ch_var} {mult_word}, "
        f"di quanto devi moltiplicare {tgt_var} per mantenere {dep_var} costante?"
    )

    pool = [
        f"{tgt_var} raddoppia",
        f"{tgt_var} triplica",
        f"{tgt_var} quadruplica",
        f"{tgt_var} si dimezza",
        f"{tgt_var} si moltiplica per \u221a2",
        f"{tgt_var} si moltiplica per \u221a3",
        f"{tgt_var} resta uguale",
        f"{tgt_var} si moltiplica per 4",
        f"{tgt_var} si moltiplica per 1/4",
    ]
    distractors = [d for d in pool if d != correct]
    random.shuffle(distractors)
    distractors = distractors[:4]

    factor_display = multiplier ** ch_pow
    if exp_den == 1:
        factor_tgt_display = f"{base}"
    elif exp_den == 2:
        factor_tgt_display = f"\u221a{base}" if exp_num > 1 else f"\u221a{multiplier}"
    else:
        factor_tgt_display = f"{base}^(1/{exp_den})"

    explanation = (
        f"1) Formula: {formula_display}\n"
        f"2) {ch_var} {mult_word}: il contributo di {ch_var} si moltiplica per "
        f"{multiplier}^{ch_pow} = {factor_display}\n"
        f"3) Per mantenere {dep_var} costante, {tgt_var}^{tgt_pow} deve compensare "
        f"con lo stesso fattore {factor_display}\n"
        f"4) Quindi {tgt_var} deve moltiplicarsi per {factor_tgt_display}\n"
        f"5) Conclusione: {correct}."
    )
    tip = (
        "Per mantenere costante una grandezza quando un parametro cambia, "
        "bisogna compensare con gli altri parametri tenendo conto degli esponenti."
    )
    return question, correct, distractors, explanation, tip


def _t3_combined_variation():
    """Two variables change simultaneously in a multi-variable formula."""
    scenarios = [
        # (formula, dep_var, vars_with_powers, context)
        ("V = \u03c0r\u00b2h", "V", [("r", 2), ("h", 1)], "il volume del cilindro"),
        ("A = 2\u03c0rh", "A", [("r", 1), ("h", 1)], "la superficie laterale del cilindro"),
        ("F = GMm/d\u00b2", "F", [("M", 1), ("d", -2)], "la forza gravitazionale"),
        ("E = \u00bdmv\u00b2", "E", [("m", 1), ("v", 2)], "l'energia cinetica"),
        ("V = \u2153\u03c0r\u00b2h", "V", [("r", 2), ("h", 1)], "il volume del cono"),
    ]

    formula, dep_var, vars_powers, context = random.choice(scenarios)

    # Assign multipliers to each variable
    mult_choices = [2, 3, 4]
    # Also allow "si dimezza" = 1/2
    frac_choices = [(1, 2), (1, 3)]

    changes = []
    total_factor_num = 1
    total_factor_den = 1

    for var_name, power in vars_powers:
        if random.random() < 0.3:
            # Use fraction
            fn, fd = random.choice(frac_choices)
        else:
            fn = random.choice(mult_choices)
            fd = 1

        # Effect of multiplying var by fn/fd when power is p:
        # factor = (fn/fd)^p
        if power >= 0:
            total_factor_num *= fn ** power
            total_factor_den *= fd ** power
        else:
            # negative power: (fn/fd)^(-|p|) = (fd/fn)^|p|
            ap = abs(power)
            total_factor_num *= fd ** ap
            total_factor_den *= fn ** ap

        if fn == 1 and fd == 2:
            change_word = "si dimezza"
        elif fn == 1 and fd == 3:
            change_word = "diventa 1/3"
        else:
            change_word = {2: "raddoppia", 3: "triplica", 4: "quadruplica"}.get(fn, f"si moltiplica per {fn}")

        changes.append((var_name, change_word, fn, fd))

    # Simplify the total factor
    g = math.gcd(total_factor_num, total_factor_den)
    total_factor_num //= g
    total_factor_den //= g

    correct = _factor_label(total_factor_num, total_factor_den)
    correct = f"{dep_var} {correct}"

    # Build question text
    change_parts = [f"{var_name} {cw}" for var_name, cw, _, _ in changes]
    change_text = " e ".join(change_parts)

    question = (
        f"Nella formula {formula} ({context}), se {change_text}, "
        f"come cambia {dep_var}?"
    )

    pool = [
        f"{dep_var} raddoppia",
        f"{dep_var} triplica",
        f"{dep_var} quadruplica",
        f"{dep_var} si dimezza",
        f"{dep_var} resta uguale",
        f"{dep_var} si moltiplica per 9/2",
        f"{dep_var} si moltiplica per 3/2",
        f"{dep_var} si moltiplica per 6",
        f"{dep_var} si moltiplica per 8",
        f"{dep_var} si moltiplica per 4/3",
        f"{dep_var} si moltiplica per 2/3",
        f"{dep_var} si moltiplica per 1/4",
        f"{dep_var} si moltiplica per 16",
        f"{dep_var} si moltiplica per 9",
        f"{dep_var} diventa 1/3",
        f"{dep_var} diventa 1/4",
    ]
    distractors = [d for d in pool if d != correct]
    random.shuffle(distractors)
    distractors = distractors[:4]

    # Build explanation steps
    step_lines = [f"1) Formula: {formula}"]
    step_num = 2
    for var_name, cw, fn, fd in changes:
        power = next(p for v, p in vars_powers if v == var_name)
        if fd == 1:
            factor_str = f"{fn}"
        else:
            factor_str = f"{fn}/{fd}"
        step_lines.append(
            f"{step_num}) {var_name} {cw}: contributo al fattore = "
            f"({factor_str})^{abs(power)} = {fn**abs(power)}/{fd**abs(power)}"
            + (f" (al denominatore)" if power < 0 else "")
        )
        step_num += 1

    step_lines.append(
        f"{step_num}) Fattore totale: {total_factor_num}/{total_factor_den}"
        if total_factor_den > 1
        else f"{step_num}) Fattore totale: {total_factor_num}"
    )
    step_num += 1
    step_lines.append(f"{step_num}) Conclusione: {correct}.")

    explanation = "\n".join(step_lines)

    tip = (
        "Quando piu variabili cambiano contemporaneamente, il fattore totale "
        "e il prodotto dei singoli fattori, ciascuno elevato alla propria potenza nella formula."
    )
    return question, correct, distractors, explanation, tip


# ---------------------------------------------------------------------------
# Exercise class
# ---------------------------------------------------------------------------

class ProportionalReasoning(Exercise):
    """Ragionamento Proporzionale -- reason about how variables change."""

    @staticmethod
    def _build_result(question, correct_str, distractors, explanation, tip, difficulty):
        options = [correct_str] + distractors
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

    def _get_templates(self, difficulty):
        level_1 = [_t1_direct_proportion, _t1_inverse_proportion]
        level_2 = [_t2_squared_proportion, _t2_compound_percentage]
        level_3 = [_t3_parameter_variation, _t3_combined_variation]
        if difficulty == 1:
            return level_1
        elif difficulty == 2:
            return level_2
        else:
            return level_3

    def generate(self, difficulty: int) -> dict:
        difficulty = max(1, min(3, difficulty))
        templates = self._get_templates(difficulty)
        template_fn = random.choice(templates)
        question, correct_str, distractors, explanation, tip = template_fn()
        return self._build_result(question, correct_str, distractors, explanation, tip, difficulty)
