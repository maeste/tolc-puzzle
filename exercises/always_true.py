import math
import random

from exercises.base import Exercise


# --- Variable name pools for parametric variety ---
_VAR_PAIRS = [
    ("a", "b"), ("x", "y"), ("m", "n"), ("p", "q"), ("s", "t"),
]
_VAR_TRIPLES = [
    ("a", "b", "c"), ("x", "y", "z"), ("m", "n", "p"), ("p", "q", "r"),
]


def _pick_vars(n=2):
    """Pick a random variable name tuple of size n."""
    if n == 2:
        return random.choice(_VAR_PAIRS)
    return random.choice(_VAR_TRIPLES)


# ================================================================
#  LEVEL 1 — Easy (common algebraic misconceptions)
# ================================================================

def _t1_square_sum():
    """(a+b)^2 = a^2 + b^2 — FALSE (never true when ab != 0)."""
    v1, v2 = _pick_vars(2)
    coeff = random.choice([1, 2, 3])
    if coeff == 1:
        lhs = f"({v1} + {v2})²"
        rhs = f"{v1}² + {v2}²"
        expand_lhs = f"{v1}² + 2{v1}{v2} + {v2}²"
        counter_a, counter_b = 1, 1
        lhs_val = (counter_a + counter_b) ** 2  # 4
        rhs_val = counter_a ** 2 + counter_b ** 2  # 2
    elif coeff == 2:
        lhs = f"({v1} - {v2})²"
        rhs = f"{v1}² - {v2}²"
        expand_lhs = f"{v1}² - 2{v1}{v2} + {v2}²"
        counter_a, counter_b = 2, 1
        lhs_val = (counter_a - counter_b) ** 2  # 1
        rhs_val = counter_a ** 2 - counter_b ** 2  # 3
    else:
        lhs = f"(2{v1} + {v2})²"
        rhs = f"4{v1}² + {v2}²"
        expand_lhs = f"4{v1}² + 4{v1}{v2} + {v2}²"
        counter_a, counter_b = 1, 1
        lhs_val = (2 * counter_a + counter_b) ** 2  # 9
        rhs_val = 4 * counter_a ** 2 + counter_b ** 2  # 5

    statement = f"{lhs} = {rhs}"
    question = (
        f"Considera la seguente affermazione: {statement}. "
        f"Quale delle seguenti e' corretta?"
    )
    correct = f"Non e' mai vera (per {v1}{v2} ≠ 0)"
    distractors = [
        "E' sempre vera, per ogni valore reale",
        f"E' vera solo se {v1} = 0",
        f"E' vera solo se {v1} = {v2}",
        f"E' vera solo se {v1} e {v2} sono positivi",
    ]
    explanation = (
        f"Sviluppando il quadrato: {lhs} = {expand_lhs}, che e' diverso da {rhs}. "
        f"Controesempio: {v1} = {counter_a}, {v2} = {counter_b} → "
        f"{lhs} = {lhs_val}, {rhs} = {rhs_val}. "
        f"L'uguaglianza vale solo nel caso banale in cui il termine misto si annulla, "
        f"cioe' quando {v1} = 0 oppure {v2} = 0."
    )
    tip = (
        "Ricorda: (a+b)² = a² + 2ab + b². Il termine 2ab non si puo' mai ignorare!"
    )
    return question, correct, distractors, explanation, tip


def _t1_fraction_distribution():
    """a/(b+c) = a/b + a/c — FALSE (never true for b,c != 0 and b+c != 0)."""
    v1, v2, v3 = _pick_vars(3)
    variant = random.choice(["sum", "diff"])
    if variant == "sum":
        statement = f"{v1}/({v2} + {v3}) = {v1}/{v2} + {v1}/{v3}"
        counter_vals = (1, 1, 1)
        lhs_val = "1/2"
        rhs_val = "2"
    else:
        statement = f"{v1}/({v2} - {v3}) = {v1}/{v2} - {v1}/{v3}"
        counter_vals = (1, 2, 1)
        lhs_val = "1/1 = 1"
        rhs_val = "1/2 - 1/1 = -1/2"

    question = (
        f"Considera la seguente affermazione: {statement}. "
        f"Quale delle seguenti e' corretta?"
    )
    correct = f"Non e' mai vera (per {v2}, {v3} ≠ 0)"
    distractors = [
        "E' sempre vera, per ogni valore reale",
        f"E' vera solo se {v1} = 1",
        f"E' vera solo se {v2} = {v3}",
        "E' vera solo per numeri interi",
    ]
    cv = counter_vals
    explanation = (
        f"La divisione NON si distribuisce sulla somma/differenza al denominatore. "
        f"Controesempio: {v1} = {cv[0]}, {v2} = {cv[1]}, {v3} = {cv[2]} → "
        f"lato sinistro = {lhs_val}, lato destro = {rhs_val}. "
        f"Attenzione: si distribuisce al NUMERATORE, cioe' ({v1}+{v2})/{v3} = {v1}/{v3} + {v2}/{v3}, "
        f"ma NON al denominatore."
    )
    tip = (
        "La frazione si 'spezza' al numeratore ma MAI al denominatore: "
        "(a+b)/c = a/c + b/c, ma a/(b+c) ≠ a/b + a/c."
    )
    return question, correct, distractors, explanation, tip


def _t1_root_sum():
    """sqrt(a^2 + b^2) = a + b — FALSE (never true for a, b > 0)."""
    v1, v2 = _pick_vars(2)
    variant = random.choice(["sum", "diff"])
    if variant == "sum":
        statement = f"√({v1}² + {v2}²) = {v1} + {v2}"
        counter_a, counter_b = 3, 4
        lhs_val = 5  # sqrt(9+16) = 5
        rhs_val = 7  # 3+4
    else:
        statement = f"√({v1}² + {v2}²) = |{v1}| + |{v2}|"
        counter_a, counter_b = 3, 4
        lhs_val = 5
        rhs_val = 7

    question = (
        f"Considera la seguente affermazione (per {v1}, {v2} > 0): {statement}. "
        f"Quale delle seguenti e' corretta?"
    )
    correct = f"Non e' mai vera (per {v1}, {v2} > 0)"
    distractors = [
        "E' sempre vera, per ogni valore reale positivo",
        f"E' vera solo se {v1} = {v2}",
        f"E' vera solo se {v1} = 0",
        "E' vera per la terna pitagorica 3, 4, 5",
    ]
    explanation = (
        f"La radice NON si distribuisce sulla somma. "
        f"Controesempio: {v1} = {counter_a}, {v2} = {counter_b} → "
        f"√({counter_a}² + {counter_b}²) = √({counter_a**2} + {counter_b**2}) = √{counter_a**2 + counter_b**2} = {lhs_val}, "
        f"ma {v1} + {v2} = {rhs_val}. "
        f"Per la disuguaglianza triangolare, √(a² + b²) ≤ |a| + |b|, "
        f"con uguaglianza solo se uno dei due e' zero."
    )
    tip = (
        "√(a² + b²) ≠ a + b. La radice quadrata non si distribuisce sulla somma. "
        "Pensa al teorema di Pitagora: l'ipotenusa e' sempre minore della somma dei cateti."
    )
    return question, correct, distractors, explanation, tip


# ================================================================
#  LEVEL 2 — Medium (conditional truths)
# ================================================================

def _t2_am_gm():
    """a/b + b/a >= 2 — TRUE only if a, b same sign (concordi)."""
    v1, v2 = _pick_vars(2)
    threshold = random.choice([2, 2, 2])  # keep it at 2 for AM-GM
    statement = f"{v1}/{v2} + {v2}/{v1} ≥ {threshold}"

    question = (
        f"Considera la seguente affermazione (per {v1}, {v2} ≠ 0): {statement}. "
        f"Quale delle seguenti e' corretta?"
    )
    correct = f"E' vera solo se {v1} e {v2} sono concordi ({v1}{v2} > 0)"
    distractors = [
        f"E' sempre vera, per ogni {v1}, {v2} ≠ 0",
        "Non e' mai vera",
        f"E' vera solo se {v1} = {v2}",
        f"E' vera solo se {v1} > 0 e {v2} > 0",
    ]
    explanation = (
        f"Quando {v1}{v2} > 0 (stessi segni), poniamo t = {v1}/{v2} > 0. "
        f"Allora t + 1/t ≥ 2 per la disuguaglianza AM-GM (con uguaglianza per t = 1, cioe' {v1} = {v2}). "
        f"Ma se {v1}{v2} < 0 (segni opposti), t < 0 e t + 1/t ≤ -2. "
        f"Controesempio: {v1} = 1, {v2} = -1 → 1/(-1) + (-1)/1 = -2 < 2."
    )
    tip = (
        "La disuguaglianza t + 1/t ≥ 2 vale solo per t > 0 (variabili concordi). "
        "Per t < 0 si ha t + 1/t ≤ -2. E' un caso classico di AM-GM."
    )
    return question, correct, distractors, explanation, tip


def _t2_absolute_value():
    """|a+b| = |a| + |b| — TRUE only if ab >= 0."""
    v1, v2 = _pick_vars(2)
    variant = random.choice(["sum", "diff", "scaled"])
    if variant == "sum":
        statement = f"|{v1} + {v2}| = |{v1}| + |{v2}|"
        condition = f"{v1} e {v2} concordi ({v1}{v2} ≥ 0)"
        counter_a, counter_b = 1, -1
        lhs_val = 0
        rhs_val = 2
    elif variant == "diff":
        statement = f"|{v1} - {v2}| = |{v1}| - |{v2}|"
        condition = f"|{v1}| ≥ |{v2}| e {v1}{v2} ≥ 0"
        counter_a, counter_b = 1, -2
        lhs_val = 3
        rhs_val = -1
    else:
        statement = f"|2{v1} + {v2}| = 2|{v1}| + |{v2}|"
        condition = f"{v1} e {v2} concordi ({v1}{v2} ≥ 0)"
        counter_a, counter_b = 1, -1
        lhs_val = 1
        rhs_val = 3

    question = (
        f"Considera la seguente affermazione: {statement}. "
        f"Quale delle seguenti e' corretta?"
    )
    correct = f"E' vera solo se {condition}"
    distractors = [
        "E' sempre vera, per ogni valore reale",
        "Non e' mai vera",
        f"E' vera solo se {v1} > 0",
        f"E' vera solo se {v1} = {v2}",
    ]
    explanation = (
        f"La proprieta' |a + b| = |a| + |b| vale se e solo se a e b hanno lo stesso segno "
        f"(o almeno uno e' zero). In generale vale |a + b| ≤ |a| + |b| (disuguaglianza triangolare). "
        f"Controesempio: {v1} = {counter_a}, {v2} = {counter_b} → "
        f"lato sinistro = {lhs_val}, lato destro = {rhs_val}."
    )
    tip = (
        "La disuguaglianza triangolare |a + b| ≤ |a| + |b| diventa uguaglianza "
        "quando a e b hanno lo stesso segno. Pensa ai segmenti su una retta."
    )
    return question, correct, distractors, explanation, tip


def _t2_power_inequality():
    """a^n > b^n implies a > b — TRUE only for n odd."""
    v1, v2 = _pick_vars(2)
    n = random.choice([2, 3, 4, 5])
    statement = f"Se {v1}^{n} > {v2}^{n}, allora {v1} > {v2}"

    if n % 2 == 0:
        correct = f"Non e' sempre vera (falsa per n = {n} pari)"
        condition_text = "n dispari"
        counter_a, counter_b = -3, 2
        explanation = (
            f"Per n = {n} (pari), la funzione x^{n} non e' monotona su tutto R. "
            f"Controesempio: {v1} = {counter_a}, {v2} = {counter_b} → "
            f"{v1}^{n} = {counter_a**n}, {v2}^{n} = {counter_b**n}. "
            f"Si ha {counter_a**n} > {counter_b**n}, ma {counter_a} < {counter_b}. "
            f"Per n pari, a^n > b^n implica solo |a| > |b|."
        )
    else:
        correct = f"E' sempre vera (per n = {n} dispari)"
        condition_text = "n dispari"
        explanation = (
            f"Per n = {n} (dispari), la funzione x^{n} e' strettamente crescente su tutto R. "
            f"Quindi {v1}^{n} > {v2}^{n} implica {v1} > {v2}. "
            f"Attenzione: questo NON vale per n pari! "
            f"Esempio con n pari: (-3)² = 9 > 4 = 2², ma -3 < 2."
        )

    question = (
        f"Considera la seguente affermazione: {statement}. "
        f"Quale delle seguenti e' corretta?"
    )
    distractors = [
        "E' sempre vera, per ogni n naturale",
        "Non e' mai vera",
        f"E' vera solo se {v1}, {v2} > 0",
        f"E' vera solo se {v1} = -{v2}",
    ]
    tip = (
        "Le potenze pari 'perdono il segno': (-a)^n = a^n per n pari. "
        "Le potenze dispari preservano l'ordine: a > b ⟺ a^n > b^n."
    )
    return question, correct, distractors, explanation, tip


# ================================================================
#  LEVEL 3 — Hard (number theory and logarithms)
# ================================================================

def _t3_divisibility():
    """If a | bc, then a | b or a | c — FALSE in general, true only if a is prime."""
    v1, v2, v3 = _pick_vars(3)
    # Pick concrete composite counterexample
    examples = [
        (6, 4, 3, 12),   # 6|12 but 6∤4, 6∤3
        (12, 6, 4, 24),   # 12|24 but 12∤6, 12∤4
        (10, 4, 5, 20),   # 10|20 but 10∤4, 10∤5... wait 10|5? No. But 5|5. Hmm, let's verify
        (6, 4, 9, 36),    # 6|36 but 6∤4, 6∤9
    ]
    ce_a, ce_b, ce_c, ce_prod = random.choice([(6, 4, 3, 12), (6, 4, 9, 36), (12, 6, 4, 24)])

    statement = (
        f"Se {v1} divide {v2}·{v3}, allora {v1} divide {v2} oppure {v1} divide {v3}"
    )
    question = (
        f"Considera la seguente affermazione: {statement}. "
        f"Quale delle seguenti e' corretta?"
    )
    correct = f"E' vera solo se {v1} e' un numero primo"
    distractors = [
        "E' sempre vera, per ogni intero",
        "Non e' mai vera",
        f"E' vera solo se {v2} e {v3} sono coprimi",
        f"E' vera solo se {v1} divide sia {v2} che {v3}",
    ]
    explanation = (
        f"Questa proprieta' vale per i numeri primi (e' anzi una caratterizzazione dei primi: "
        f"p e' primo se e solo se p | ab implica p | a oppure p | b). "
        f"Controesempio con {v1} composto: {v1} = {ce_a}, {v2} = {ce_b}, {v3} = {ce_c} → "
        f"{v2}·{v3} = {ce_prod}, e {ce_a} divide {ce_prod}, "
        f"ma {ce_a} non divide {ce_b} e {ce_a} non divide {ce_c}."
    )
    tip = (
        "La proprieta' 'p | ab ⟹ p | a o p | b' e' il Lemma di Euclide "
        "e vale SOLO per p primo. E' in realta' la definizione stessa di numero primo "
        "nella teoria degli anelli."
    )
    return question, correct, distractors, explanation, tip


def _t3_log_inequality():
    """If log_a(x) > log_a(y) then x > y — TRUE only if a > 1."""
    v1, v2 = _pick_vars(2)
    base_var = random.choice(["a", "b", "c"])
    # Avoid collision with v1, v2
    while base_var in (v1, v2):
        base_var = random.choice(["a", "b", "c", "t"])

    statement = (
        f"Se log_{base_var}({v1}) > log_{base_var}({v2}), allora {v1} > {v2}"
    )
    question = (
        f"Considera la seguente affermazione (per {v1}, {v2} > 0 e "
        f"{base_var} > 0, {base_var} ≠ 1): {statement}. "
        f"Quale delle seguenti e' corretta?"
    )
    correct = f"E' vera solo se {base_var} > 1"
    distractors = [
        "E' sempre vera, per ogni base ammissibile",
        "Non e' mai vera",
        f"E' vera solo se {base_var} < 1",
        f"E' vera solo se {v1} e {v2} sono interi",
    ]
    explanation = (
        f"Il logaritmo in base {base_var} > 1 e' una funzione strettamente CRESCENTE, "
        f"quindi preserva l'ordine: log_{base_var}({v1}) > log_{base_var}({v2}) ⟹ {v1} > {v2}. "
        f"Ma per 0 < {base_var} < 1 il logaritmo e' DECRESCENTE, e l'ordine si inverte. "
        f"Controesempio: base = 1/2, {v1} = 1/4, {v2} = 1/2 → "
        f"log_{{1/2}}(1/4) = 2 > 1 = log_{{1/2}}(1/2), ma 1/4 < 1/2."
    )
    tip = (
        "Il logaritmo in base > 1 e' crescente (preserva l'ordine). "
        "Il logaritmo in base compresa tra 0 e 1 e' decrescente (inverte l'ordine). "
        "Regola: cambiando base da >1 a <1, il verso della disuguaglianza si ribalta."
    )
    return question, correct, distractors, explanation, tip


class AlwaysTrueExercise(Exercise):
    """Sempre o Mai Vero? — reasoning about mathematical properties."""

    @staticmethod
    def _build_result(question, correct, distractors, explanation, tip, difficulty):
        options = [correct] + distractors
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
        level_1 = [
            _t1_square_sum,
            _t1_fraction_distribution,
            _t1_root_sum,
        ]
        level_2 = [
            _t2_am_gm,
            _t2_absolute_value,
            _t2_power_inequality,
        ]
        level_3 = [
            _t3_divisibility,
            _t3_log_inequality,
        ]
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
        question, correct, distractors, explanation, tip = template_fn()
        return self._build_result(question, correct, distractors, explanation, tip, difficulty)
