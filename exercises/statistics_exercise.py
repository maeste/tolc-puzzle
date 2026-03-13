import math
import random
from collections import Counter

from exercises.base import Exercise


def _fmt(value, decimals=2):
    """Format a numeric value: show as int if whole, otherwise round."""
    if abs(value - round(value)) < 1e-9:
        return str(int(round(value)))
    return str(round(value, decimals))


def _make_distractors(correct, count=4):
    """Generate plausible wrong answers for statistics exercises.

    Uses common statistical mistakes as distractor strategies:
    - Dividing by N-1 instead of N (or vice versa)
    - Forgetting sqrt for standard deviation
    - Off-by-one median errors
    - Close numeric neighbors
    """
    distractors = set()
    correct_str = _fmt(correct)
    attempts = 0

    # Strategy 1: common mistake - divide by N-1 vs N (variance confusion)
    if correct > 0:
        ratio_up = correct * (correct + 1) / correct if correct != 0 else correct + 1
        # Approximate N/(N-1) or (N-1)/N adjustments
        for factor in [0.8, 0.9, 1.1, 1.2, 1.25, 0.75]:
            d = round(correct * factor, 2)
            if d > 0 and _fmt(d) != correct_str:
                distractors.add(_fmt(d))

    # Strategy 2: forgetting sqrt (for std dev type problems)
    if correct > 0:
        d_sq = round(correct * correct, 2)
        if d_sq > 0 and _fmt(d_sq) != correct_str:
            distractors.add(_fmt(d_sq))
        d_sqrt = round(math.sqrt(abs(correct)), 2) if correct > 1 else None
        if d_sqrt and d_sqrt > 0 and _fmt(d_sqrt) != correct_str:
            distractors.add(_fmt(d_sqrt))

    # Strategy 3: small offsets (off-by-one type errors)
    for offset in [0.5, -0.5, 1, -1, 2, -2, 0.25, -0.25]:
        d = round(correct + offset, 2)
        if _fmt(d) != correct_str:
            distractors.add(_fmt(d))

    # Strategy 4: random spread around correct value
    spread = max(1.0, abs(correct) * 0.3)
    while len(distractors) < count and attempts < 200:
        attempts += 1
        offset = random.uniform(-spread, spread)
        d = round(correct + offset, 2)
        if abs(d - correct) > 0.01:
            formatted = _fmt(d)
            if formatted != correct_str:
                distractors.add(formatted)

    # Fallback
    fallback_attempts = 0
    while len(distractors) < count and fallback_attempts < 200:
        fallback_attempts += 1
        offset = random.uniform(1, max(2, abs(correct) * 0.5)) * random.choice([-1, 1])
        d = round(correct + offset, 2)
        formatted = _fmt(d)
        if formatted != correct_str:
            distractors.add(formatted)

    return list(distractors)[:count]


# ---------------------------------------------------------------------------
# Italian context generators
# ---------------------------------------------------------------------------

def _context_grades_10():
    """Generate a list of school grades (0-10 scale)."""
    n = random.randint(5, 9)
    return [random.randint(4, 10) for _ in range(n)], "I voti di uno studente in diverse verifiche sono"


def _context_grades_30():
    """Generate a list of university exam grades (18-30 scale)."""
    n = random.randint(5, 8)
    return [random.randint(18, 30) for _ in range(n)], "I voti degli esami universitari di uno studente sono"


def _context_temperatures():
    """Generate daily temperatures."""
    n = random.randint(5, 9)
    base = random.choice([5, 10, 15, 20, 25])
    return [base + random.randint(-5, 10) for _ in range(n)], "Le temperature giornaliere registrate in una settimana sono"


def _context_sport_scores():
    """Generate sport scores."""
    n = random.randint(5, 8)
    return [random.randint(50, 100) for _ in range(n)], "I punteggi ottenuti da un atleta nelle ultime gare sono"


def _context_measurements():
    """Generate scientific measurements."""
    n = random.randint(5, 8)
    base = random.choice([10, 25, 50, 100])
    return [base + random.randint(-3, 5) for _ in range(n)], "Le misurazioni effettuate in un esperimento sono"


_CONTEXT_GENERATORS = [
    _context_grades_10,
    _context_grades_30,
    _context_temperatures,
    _context_sport_scores,
    _context_measurements,
]


def _random_context():
    """Return a random (data_list, description) pair."""
    return random.choice(_CONTEXT_GENERATORS)()


def _list_str(data):
    """Format a list of numbers for display in Italian."""
    return ", ".join(str(x) for x in data)


# ---------------------------------------------------------------------------
# LEVEL 1 templates: Basic descriptive statistics
# ---------------------------------------------------------------------------

def _t1_media_aritmetica():
    """Compute the arithmetic mean of a list of numbers."""
    data, desc = _random_context()
    mean = sum(data) / len(data)

    question = f"{desc}: {_list_str(data)}. Qual e' la media aritmetica?"
    explanation = (
        f"La media aritmetica si calcola sommando tutti i valori e dividendo per il numero di dati.\n"
        f"Somma = {' + '.join(str(x) for x in data)} = {sum(data)}\n"
        f"Media = {sum(data)} / {len(data)} = {_fmt(mean)}"
    )
    tip = "La media aritmetica e' il valore che bilancia tutti i dati: somma / numero di dati."
    return question, mean, explanation, tip


def _t1_mediana_dispari():
    """Find the median of an odd-length list."""
    data, desc = _random_context()
    # Ensure odd count
    if len(data) % 2 == 0:
        data.append(random.choice(data))
    sorted_data = sorted(data)
    n = len(sorted_data)
    median = sorted_data[n // 2]

    question = f"{desc}: {_list_str(data)}. Qual e' la mediana?"
    explanation = (
        f"Per trovare la mediana, ordiniamo i dati: {_list_str(sorted_data)}.\n"
        f"Con {n} valori (dispari), la mediana e' il valore centrale, "
        f"cioe' il {n // 2 + 1}-esimo: {_fmt(median)}."
    )
    tip = "La mediana e' il valore centrale quando i dati sono ordinati. Con n dispari, e' il valore in posizione (n+1)/2."
    return question, float(median), explanation, tip


def _t1_mediana_pari():
    """Find the median of an even-length list."""
    data, desc = _random_context()
    # Ensure even count
    if len(data) % 2 != 0:
        data.append(random.choice(data))
    sorted_data = sorted(data)
    n = len(sorted_data)
    mid1 = sorted_data[n // 2 - 1]
    mid2 = sorted_data[n // 2]
    median = (mid1 + mid2) / 2

    question = f"{desc}: {_list_str(data)}. Qual e' la mediana?"
    explanation = (
        f"Ordiniamo i dati: {_list_str(sorted_data)}.\n"
        f"Con {n} valori (pari), la mediana e' la media dei due valori centrali: "
        f"({mid1} + {mid2}) / 2 = {_fmt(median)}."
    )
    tip = "Con un numero pari di dati, la mediana e' la media aritmetica dei due valori centrali."
    return question, median, explanation, tip


def _t1_moda():
    """Identify the mode of a dataset with a clear mode."""
    data, desc = _random_context()
    # Force a clear mode by repeating one value
    mode_value = random.choice(data)
    extra_count = random.randint(2, 3)
    for _ in range(extra_count):
        data.append(mode_value)
    random.shuffle(data)

    counts = Counter(data)
    max_freq = max(counts.values())
    mode = [k for k, v in counts.items() if v == max_freq][0]

    question = f"{desc}: {_list_str(data)}. Qual e' la moda?"
    explanation = (
        f"La moda e' il valore che compare piu' frequentemente.\n"
        f"Conteggio: {', '.join(f'{k} (x{v})' for k, v in sorted(counts.items()))}.\n"
        f"Il valore {mode} compare {max_freq} volte, quindi la moda e' {_fmt(mode)}."
    )
    tip = "La moda e' il valore piu' frequente. Un dataset puo' essere unimodale, bimodale o multimodale."
    return question, float(mode), explanation, tip


def _t1_range():
    """Compute the range (max - min) of a dataset."""
    data, desc = _random_context()
    data_range = max(data) - min(data)

    question = f"{desc}: {_list_str(data)}. Qual e' il range (campo di variazione)?"
    explanation = (
        f"Il range e' la differenza tra il valore massimo e il minimo.\n"
        f"Massimo = {max(data)}, Minimo = {min(data)}\n"
        f"Range = {max(data)} - {min(data)} = {_fmt(data_range)}"
    )
    tip = "Il range misura l'ampiezza totale dei dati. E' semplice ma sensibile ai valori estremi (outlier)."
    return question, float(data_range), explanation, tip


def _t1_read_histogram():
    """Lettura di un istogramma presentato come tabella di frequenze."""
    categories_pool = [
        ("Matematica", "Italiano", "Inglese", "Scienze", "Storia", "Arte"),
        ("Calcio", "Pallavolo", "Tennis", "Nuoto", "Basket", "Atletica"),
        ("Pizza", "Pasta", "Insalata", "Panino", "Sushi", "Hamburger"),
        ("Bus", "Auto", "Bici", "Treno", "A piedi", "Monopattino"),
    ]
    cats = list(random.choice(categories_pool))
    n_cats = random.randint(4, min(6, len(cats)))
    cats = random.sample(cats, k=n_cats)
    freqs = [random.randint(3, 30) for _ in cats]
    total = sum(freqs)

    table_str = ", ".join(f"{c}: {f}" for c, f in zip(cats, freqs))
    question_type = random.choice(["max_freq", "total", "min_freq"])

    if question_type == "max_freq":
        max_f = max(freqs)
        correct_cat = cats[freqs.index(max_f)]
        question = (
            f"In un'indagine si e' ottenuta la seguente tabella di frequenze: "
            f"{table_str}. Quale categoria ha la frequenza maggiore?"
        )
        correct_value = float(max_f)
        explanation = (
            f"Osservando le frequenze: {table_str}.\n"
            f"La categoria con frequenza maggiore e' '{correct_cat}' con {max_f} osservazioni."
        )
        tip = "Per leggere un istogramma, confronta le altezze delle barre: la barra piu' alta corrisponde alla frequenza maggiore."
    elif question_type == "total":
        question = (
            f"In un'indagine si e' ottenuta la seguente tabella di frequenze: "
            f"{table_str}. Quante osservazioni ci sono in totale?"
        )
        correct_value = float(total)
        explanation = (
            f"Il totale si ottiene sommando tutte le frequenze:\n"
            f"{' + '.join(str(f) for f in freqs)} = {total}"
        )
        tip = "Il totale delle osservazioni e' la somma di tutte le frequenze assolute."
    else:
        min_f = min(freqs)
        correct_cat = cats[freqs.index(min_f)]
        question = (
            f"In un'indagine si e' ottenuta la seguente tabella di frequenze: "
            f"{table_str}. Quale categoria ha la frequenza minore?"
        )
        correct_value = float(min_f)
        explanation = (
            f"Osservando le frequenze: {table_str}.\n"
            f"La categoria con frequenza minore e' '{correct_cat}' con {min_f} osservazioni."
        )
        tip = "Per individuare la categoria meno frequente, cerca il valore piu' basso nella tabella."

    return question, correct_value, explanation, tip


def _t1_read_pie_chart():
    """Lettura di un grafico a torta presentato come percentuali."""
    scenarios = [
        {
            "intro": "In un sondaggio sugli hobby preferiti",
            "cats": {"Sport": None, "Musica": None, "Cinema": None, "Lettura": None, "Altro": None},
        },
        {
            "intro": "In un'indagine sulle bevande preferite",
            "cats": {"Acqua": None, "Succo": None, "Te'": None, "Caffe'": None, "Altro": None},
        },
        {
            "intro": "In un sondaggio sul mezzo di trasporto preferito",
            "cats": {"Auto": None, "Bus": None, "Bici": None, "Treno": None, "Altro": None},
        },
    ]
    scenario = random.choice(scenarios)
    cat_names = list(scenario["cats"].keys())

    # Generate percentages that sum to 100
    raw = [random.randint(5, 40) for _ in cat_names[:-1]]
    remainder = 100 - sum(raw)
    if remainder < 1:
        raw[-1] -= (1 - remainder)
        remainder = 1
    raw.append(remainder)
    random.shuffle(raw)
    percentages = dict(zip(cat_names, raw))

    pct_str = ", ".join(f"{c} {p}%" for c, p in percentages.items())
    target_cat = random.choice(cat_names)
    target_pct = percentages[target_cat]
    n_total = random.choice([100, 200, 400, 500, 1000])
    correct_value = n_total * target_pct / 100

    question = (
        f"{scenario['intro']}, i risultati sono: {pct_str}. "
        f"Se gli intervistati sono {n_total}, quanti hanno scelto {target_cat}?"
    )
    explanation = (
        f"La percentuale di {target_cat} e' {target_pct}%.\n"
        f"Numero = {n_total} * {target_pct} / 100 = {_fmt(correct_value)}"
    )
    tip = "Per convertire una percentuale in un valore assoluto, moltiplica il totale per la percentuale e dividi per 100."
    return question, correct_value, explanation, tip


def _t1_read_bar_chart():
    """Lettura di un grafico a barre presentato come tabella di confronto."""
    contexts = [
        ("vendite (in migliaia di euro)", ["Q1", "Q2", "Q3", "Q4"]),
        ("numero di visitatori", ["Gennaio", "Febbraio", "Marzo", "Aprile"]),
        ("punteggio medio", ["Squadra A", "Squadra B", "Squadra C", "Squadra D"]),
        ("produzione (unita')", ["Stabilimento Nord", "Stabilimento Sud", "Stabilimento Est", "Stabilimento Ovest"]),
    ]
    desc, groups = random.choice(contexts)
    values = [random.randint(10, 100) for _ in groups]
    table_str = ", ".join(f"{g}: {v}" for g, v in zip(groups, values))

    question_type = random.choice(["difference", "max_min_diff", "increase"])

    if question_type == "difference" and len(groups) >= 2:
        i, j = random.sample(range(len(groups)), 2)
        diff = abs(values[i] - values[j])
        question = (
            f"I dati relativi a {desc} sono: {table_str}. "
            f"Qual e' la differenza tra {groups[i]} e {groups[j]}?"
        )
        correct_value = float(diff)
        explanation = (
            f"{groups[i]} = {values[i]}, {groups[j]} = {values[j]}\n"
            f"Differenza = |{values[i]} - {values[j]}| = {diff}"
        )
        tip = "Per calcolare la differenza tra due valori in un grafico a barre, sottrai il valore minore dal maggiore."
    elif question_type == "max_min_diff":
        diff = max(values) - min(values)
        question = (
            f"I dati relativi a {desc} sono: {table_str}. "
            f"Qual e' la differenza tra il valore massimo e il valore minimo?"
        )
        correct_value = float(diff)
        max_g = groups[values.index(max(values))]
        min_g = groups[values.index(min(values))]
        explanation = (
            f"Valore massimo: {max_g} = {max(values)}\n"
            f"Valore minimo: {min_g} = {min(values)}\n"
            f"Differenza = {max(values)} - {min(values)} = {diff}"
        )
        tip = "La differenza tra massimo e minimo (range) indica l'ampiezza della variazione tra i gruppi."
    else:
        i = random.randint(0, len(groups) - 2)
        j = i + 1
        diff = values[j] - values[i]
        correct_value = float(diff)
        question = (
            f"I dati relativi a {desc} sono: {table_str}. "
            f"Di quanto e' cambiato il valore da {groups[i]} a {groups[j]}?"
        )
        explanation = (
            f"{groups[i]} = {values[i]}, {groups[j]} = {values[j]}\n"
            f"Variazione = {values[j]} - {values[i]} = {diff}"
        )
        tip = "Un valore positivo indica un aumento, un valore negativo indica una diminuzione."

    return question, correct_value, explanation, tip


# ---------------------------------------------------------------------------
# LEVEL 2 templates: Intermediate statistics (interpretazione dati)
# ---------------------------------------------------------------------------

def _t2_media_ponderata():
    """Weighted average (e.g., grades with credits)."""
    n_exams = random.randint(4, 6)
    grades = [random.randint(18, 30) for _ in range(n_exams)]
    credits = [random.choice([3, 5, 6, 8, 9, 10, 12]) for _ in range(n_exams)]

    weighted_sum = sum(g * c for g, c in zip(grades, credits))
    total_credits = sum(credits)
    weighted_mean = weighted_sum / total_credits

    grade_credit_pairs = ", ".join(f"{g} ({c} CFU)" for g, c in zip(grades, credits))

    question = (
        f"Uno studente ha ottenuto i seguenti voti con i rispettivi crediti: "
        f"{grade_credit_pairs}. Qual e' la media ponderata?"
    )
    explanation = (
        f"La media ponderata si calcola come somma(voto * peso) / somma(pesi).\n"
        f"Numeratore = {' + '.join(f'{g}*{c}' for g, c in zip(grades, credits))} = {weighted_sum}\n"
        f"Denominatore = {' + '.join(str(c) for c in credits)} = {total_credits}\n"
        f"Media ponderata = {weighted_sum} / {total_credits} = {_fmt(weighted_mean)}"
    )
    tip = "La media ponderata tiene conto dell'importanza (peso) di ciascun valore. E' usata per calcolare la media universitaria."
    return question, weighted_mean, explanation, tip


def _t2_varianza():
    """Compute variance of a small dataset."""
    data, desc = _random_context()
    # Keep dataset small for manageable computation
    data = data[:6]
    n = len(data)
    mean = sum(data) / n
    variance = sum((x - mean) ** 2 for x in data) / n

    deviations = [f"({x} - {_fmt(mean)})^2 = {_fmt((x - mean) ** 2)}" for x in data]

    question = f"{desc}: {_list_str(data)}. Qual e' la varianza (popolazione)?"
    explanation = (
        f"Passo 1 - Media: {_fmt(mean)}\n"
        f"Passo 2 - Scarti quadratici: {'; '.join(deviations)}\n"
        f"Passo 3 - Varianza = somma scarti^2 / N = "
        f"{_fmt(sum((x - mean) ** 2 for x in data))} / {n} = {_fmt(variance)}"
    )
    tip = "La varianza misura la dispersione dei dati attorno alla media. Si calcola come media degli scarti quadratici."
    return question, variance, explanation, tip


def _t2_deviazione_standard():
    """Compute standard deviation of a small dataset."""
    data, desc = _random_context()
    data = data[:6]
    n = len(data)
    mean = sum(data) / n
    variance = sum((x - mean) ** 2 for x in data) / n
    std_dev = math.sqrt(variance)

    question = f"{desc}: {_list_str(data)}. Qual e' la deviazione standard (popolazione)?"
    explanation = (
        f"Passo 1 - Media: {_fmt(mean)}\n"
        f"Passo 2 - Varianza = {_fmt(variance)}\n"
        f"Passo 3 - Deviazione standard = sqrt(varianza) = sqrt({_fmt(variance)}) = {_fmt(std_dev)}"
    )
    tip = "La deviazione standard e' la radice quadrata della varianza. Ha il vantaggio di essere nella stessa unita' di misura dei dati."
    return question, std_dev, explanation, tip


def _t2_frequenza_relativa():
    """Given a frequency table, compute relative frequency of a category."""
    categories = random.sample(["A", "B", "C", "D", "E"], k=random.randint(3, 5))
    frequencies = [random.randint(5, 30) for _ in categories]
    total = sum(frequencies)
    target_idx = random.randint(0, len(categories) - 1)
    target_cat = categories[target_idx]
    rel_freq = frequencies[target_idx] / total

    table = ", ".join(f"{c}: {f}" for c, f in zip(categories, frequencies))

    question = (
        f"In un'indagine statistica si sono ottenute le seguenti frequenze assolute: "
        f"{table}. Qual e' la frequenza relativa della categoria {target_cat}?"
    )
    explanation = (
        f"La frequenza relativa e' il rapporto tra la frequenza assoluta e il totale.\n"
        f"Totale osservazioni = {total}\n"
        f"Frequenza relativa di {target_cat} = {frequencies[target_idx]} / {total} = {_fmt(rel_freq)}"
    )
    tip = "La frequenza relativa e' sempre compresa tra 0 e 1. La somma di tutte le frequenze relative e' 1."
    return question, rel_freq, explanation, tip


def _t2_media_frequenza():
    """Compute mean from a frequency distribution table."""
    values = sorted(random.sample(range(1, 15), k=random.randint(4, 6)))
    frequencies = [random.randint(2, 10) for _ in values]
    total_freq = sum(frequencies)
    weighted_sum = sum(v * f for v, f in zip(values, frequencies))
    mean = weighted_sum / total_freq

    table = ", ".join(f"valore {v}: frequenza {f}" for v, f in zip(values, frequencies))

    question = (
        f"Data la seguente distribuzione di frequenza: {table}. "
        f"Qual e' la media aritmetica?"
    )
    explanation = (
        f"La media da tabella di frequenza si calcola come somma(valore * frequenza) / somma(frequenze).\n"
        f"Numeratore = {' + '.join(f'{v}*{f}' for v, f in zip(values, frequencies))} = {weighted_sum}\n"
        f"Denominatore = {total_freq}\n"
        f"Media = {weighted_sum} / {total_freq} = {_fmt(mean)}"
    )
    tip = "Per calcolare la media da una tabella di frequenza, moltiplica ogni valore per la sua frequenza e dividi per il totale."
    return question, mean, explanation, tip


# ---------------------------------------------------------------------------
# LEVEL 3 templates: Advanced statistics
# ---------------------------------------------------------------------------

def _t3_varianza_formula():
    """Given mean and individual deviations, compute variance."""
    n = random.randint(5, 7)
    mean = random.randint(10, 50)
    deviations = [random.randint(-8, 8) for _ in range(n - 1)]
    # Force last deviation so they sum to zero
    deviations.append(-sum(deviations))
    random.shuffle(deviations)

    data = [mean + d for d in deviations]
    variance = sum(d ** 2 for d in deviations) / n

    question = (
        f"Un dataset di {n} valori ha media {mean}. "
        f"Gli scarti dalla media sono: {_list_str(deviations)}. "
        f"Qual e' la varianza?"
    )
    explanation = (
        f"La varianza e' la media degli scarti al quadrato.\n"
        f"Scarti^2: {', '.join(f'({d})^2 = {d**2}' for d in deviations)}\n"
        f"Somma = {sum(d ** 2 for d in deviations)}\n"
        f"Varianza = {sum(d ** 2 for d in deviations)} / {n} = {_fmt(variance)}"
    )
    tip = "La varianza puo' essere calcolata direttamente dagli scarti: Var = somma(scarti^2) / N."
    return question, variance, explanation, tip


def _t3_coefficiente_variazione():
    """Compute the coefficient of variation (CV)."""
    data, desc = _random_context()
    data = data[:6]
    n = len(data)
    mean = sum(data) / n
    # Ensure mean is not zero
    while abs(mean) < 0.1:
        data = [x + 5 for x in data]
        mean = sum(data) / n
    variance = sum((x - mean) ** 2 for x in data) / n
    std_dev = math.sqrt(variance)
    cv = (std_dev / abs(mean)) * 100

    question = (
        f"{desc}: {_list_str(data)}. "
        f"Qual e' il coefficiente di variazione (in percentuale)?"
    )
    explanation = (
        f"Passo 1 - Media: {_fmt(mean)}\n"
        f"Passo 2 - Deviazione standard: {_fmt(std_dev)}\n"
        f"Passo 3 - CV = (deviazione standard / media) * 100 "
        f"= ({_fmt(std_dev)} / {_fmt(mean)}) * 100 = {_fmt(cv)}%"
    )
    tip = "Il coefficiente di variazione (CV) permette di confrontare la variabilita' di distribuzioni con medie diverse."
    return question, cv, explanation, tip


def _t3_quartili():
    """Find Q1, Q3, or IQR from a dataset."""
    n = random.randint(8, 12)
    data = sorted([random.randint(10, 50) for _ in range(n)])
    target = random.choice(["Q1", "Q3", "IQR"])

    # Compute quartiles using the simple method (median of halves)
    mid = n // 2
    lower_half = data[:mid]
    upper_half = data[mid:] if n % 2 != 0 else data[mid:]

    def _median(lst):
        m = len(lst)
        if m % 2 == 1:
            return float(lst[m // 2])
        return (lst[m // 2 - 1] + lst[m // 2]) / 2

    q1 = _median(lower_half)
    q3 = _median(upper_half)
    iqr = q3 - q1

    if target == "Q1":
        correct = q1
        target_desc = "il primo quartile (Q1)"
    elif target == "Q3":
        correct = q3
        target_desc = "il terzo quartile (Q3)"
    else:
        correct = iqr
        target_desc = "lo scarto interquartile (IQR = Q3 - Q1)"

    question = (
        f"Dato il seguente dataset ordinato: {_list_str(data)}. "
        f"Calcola {target_desc}."
    )
    explanation = (
        f"Il dataset ha {n} valori.\n"
        f"Meta' inferiore: {_list_str(lower_half)} => Q1 = {_fmt(q1)}\n"
        f"Meta' superiore: {_list_str(upper_half)} => Q3 = {_fmt(q3)}\n"
        f"IQR = Q3 - Q1 = {_fmt(q3)} - {_fmt(q1)} = {_fmt(iqr)}\n"
        f"Risposta: {target} = {_fmt(correct)}"
    )
    tip = "I quartili dividono i dati in quattro parti uguali. L'IQR misura la dispersione del 50% centrale dei dati."
    return question, correct, explanation, tip


def _t3_media_combinata():
    """Two groups with different means and sizes: find the combined mean."""
    n1 = random.randint(10, 30)
    n2 = random.randint(10, 30)
    mean1 = round(random.uniform(15, 80), 1)
    mean2 = round(random.uniform(15, 80), 1)

    combined_mean = (mean1 * n1 + mean2 * n2) / (n1 + n2)

    group_names = random.choice([
        ("classe A", "classe B"),
        ("gruppo maschile", "gruppo femminile"),
        ("sede di Milano", "sede di Roma"),
        ("turno mattutino", "turno pomeridiano"),
    ])

    question = (
        f"La {group_names[0]} ha {n1} studenti con media {_fmt(mean1)}. "
        f"La {group_names[1]} ha {n2} studenti con media {_fmt(mean2)}. "
        f"Qual e' la media combinata dei due gruppi?"
    )
    explanation = (
        f"La media combinata si calcola come media ponderata delle medie dei gruppi.\n"
        f"Media combinata = (n1 * media1 + n2 * media2) / (n1 + n2)\n"
        f"= ({n1} * {_fmt(mean1)} + {n2} * {_fmt(mean2)}) / ({n1} + {n2})\n"
        f"= ({_fmt(mean1 * n1)} + {_fmt(mean2 * n2)}) / {n1 + n2}\n"
        f"= {_fmt(mean1 * n1 + mean2 * n2)} / {n1 + n2} = {_fmt(combined_mean)}"
    )
    tip = "La media combinata non e' la media delle medie, a meno che i due gruppi abbiano la stessa numerosita'."
    return question, combined_mean, explanation, tip


def _t3_trasformazione_lineare():
    """If each value is multiplied by a and added b, what happens to mean and std dev?"""
    data, desc = _random_context()
    data = data[:5]
    n = len(data)
    mean = sum(data) / n
    variance = sum((x - mean) ** 2 for x in data) / n
    std_dev = math.sqrt(variance)

    a = random.choice([2, 3, 5, 10])
    b = random.choice([1, 3, 5, -2, -5, 10])
    ask_what = random.choice(["media", "deviazione standard"])

    new_mean = a * mean + b
    new_std = abs(a) * std_dev

    if ask_what == "media":
        correct = new_mean
        target_desc = "la nuova media"
        calc = (
            f"Se Y = a*X + b, allora media(Y) = a * media(X) + b.\n"
            f"Media originale = {_fmt(mean)}\n"
            f"Nuova media = {a} * {_fmt(mean)} + {b} = {_fmt(new_mean)}"
        )
    else:
        correct = new_std
        target_desc = "la nuova deviazione standard"
        calc = (
            f"Se Y = a*X + b, allora dev.std(Y) = |a| * dev.std(X).\n"
            f"Dev.std originale = {_fmt(std_dev)}\n"
            f"Nuova dev.std = |{a}| * {_fmt(std_dev)} = {_fmt(new_std)}"
        )

    question = (
        f"{desc}: {_list_str(data)}. "
        f"Se ogni valore viene trasformato con Y = {a}*X + {b}, "
        f"qual e' {target_desc}?"
    )
    explanation = (
        f"Trasformazione lineare Y = {a}*X + {'+' if b >= 0 else ''}{b}.\n"
        f"{calc}"
    )
    tip = (
        "Nelle trasformazioni lineari Y = aX + b: la media si trasforma come i dati (a*media + b), "
        "ma la deviazione standard dipende solo da |a| (la traslazione b non cambia la dispersione)."
    )
    return question, correct, explanation, tip


# ---------------------------------------------------------------------------
# Variable classification templates (categorical answers)
# ---------------------------------------------------------------------------

# Pool of variables with their correct classification
_VARIABLE_POOL = [
    ("colore degli occhi", "Qualitativa nominale",
     "Il colore degli occhi e' una caratteristica non numerica senza ordinamento naturale."),
    ("altezza in cm", "Quantitativa continua",
     "L'altezza puo' assumere qualsiasi valore reale in un intervallo, quindi e' continua."),
    ("citta' di nascita", "Qualitativa nominale",
     "La citta' di nascita e' un'etichetta categorica senza ordine intrinseco."),
    ("numero di fratelli", "Quantitativa discreta",
     "Il numero di fratelli puo' assumere solo valori interi (0, 1, 2, ...)."),
    ("temperatura corporea", "Quantitativa continua",
     "La temperatura puo' assumere qualsiasi valore reale, quindi e' una variabile continua."),
    ("voto scolastico (1-10)", "Quantitativa discreta",
     "I voti scolastici assumono valori numerici interi da 1 a 10."),
    ("marca di auto preferita", "Qualitativa nominale",
     "La marca e' una categoria senza ordinamento naturale."),
    ("livello di soddisfazione (basso/medio/alto)", "Qualitativa ordinale",
     "I livelli di soddisfazione hanno un ordine naturale ma non sono misurabili numericamente."),
    ("gruppo sanguigno", "Qualitativa nominale",
     "Il gruppo sanguigno (A, B, AB, 0) e' una categoria senza ordine."),
    ("peso in kg", "Quantitativa continua",
     "Il peso puo' assumere qualsiasi valore reale positivo."),
    ("numero di esami superati", "Quantitativa discreta",
     "Il conteggio degli esami e' un numero intero non negativo."),
    ("titolo di studio (licenza media, diploma, laurea)", "Qualitativa ordinale",
     "I titoli di studio hanno un ordinamento naturale dal piu' basso al piu' alto."),
    ("codice fiscale", "Qualitativa nominale",
     "Il codice fiscale e' un identificativo alfanumerico senza ordine."),
    ("numero di pagine di un libro", "Quantitativa discreta",
     "Il numero di pagine e' un conteggio intero."),
    ("tempo di percorrenza in minuti", "Quantitativa continua",
     "Il tempo puo' assumere qualsiasi valore reale positivo."),
    ("giudizio scolastico (insufficiente, sufficiente, buono, ottimo)", "Qualitativa ordinale",
     "I giudizi scolastici hanno un ordinamento naturale di merito."),
    ("nazionalita'", "Qualitativa nominale",
     "La nazionalita' e' un'etichetta categorica senza ordine intrinseco."),
    ("reddito annuo in euro", "Quantitativa continua",
     "Il reddito puo' assumere qualsiasi valore reale positivo."),
    ("numero di figli", "Quantitativa discreta",
     "Il numero di figli e' un conteggio intero non negativo."),
    ("classe energetica (A, B, C, D, E, F, G)", "Qualitativa ordinale",
     "Le classi energetiche hanno un ordinamento dalla migliore alla peggiore."),
]

_ALL_CLASSIFICATIONS = [
    "Qualitativa nominale",
    "Qualitativa ordinale",
    "Quantitativa discreta",
    "Quantitativa continua",
]

# Pool of variable-graph pairings
_VARIABLE_GRAPH_POOL = [
    ("temperatura giornaliera nel corso di un anno", "Quantitativa continua",
     "grafico a linee",
     "Per dati continui raccolti nel tempo, il grafico a linee mostra l'andamento temporale."),
    ("colore preferito dagli studenti di una classe", "Qualitativa nominale",
     "diagramma a barre",
     "Per variabili qualitative nominali, il diagramma a barre confronta le frequenze delle categorie."),
    ("distribuzione percentuale delle spese mensili", "Qualitativa nominale",
     "diagramma a torta",
     "Il diagramma a torta mostra le proporzioni delle categorie rispetto al totale."),
    ("altezza degli studenti di una scuola", "Quantitativa continua",
     "istogramma",
     "Per dati quantitativi continui, l'istogramma mostra la distribuzione in classi."),
    ("numero di libri letti al mese", "Quantitativa discreta",
     "diagramma a barre",
     "Per dati discreti con pochi valori possibili, il diagramma a barre e' appropriato."),
    ("relazione tra ore di studio e voto all'esame", "Quantitativa continua",
     "diagramma a dispersione",
     "Il diagramma a dispersione (scatter plot) mostra la relazione tra due variabili quantitative."),
    ("andamento del fatturato trimestrale", "Quantitativa continua",
     "grafico a linee",
     "Per dati quantitativi in serie temporale, il grafico a linee mostra l'evoluzione."),
    ("composizione per genere di un'azienda", "Qualitativa nominale",
     "diagramma a torta",
     "Per mostrare le proporzioni di categorie, il diagramma a torta e' adatto."),
    ("distribuzione dei pesi di un campione", "Quantitativa continua",
     "istogramma",
     "L'istogramma e' il grafico naturale per rappresentare la distribuzione di dati continui."),
    ("numero di goal segnati per partita", "Quantitativa discreta",
     "diagramma a barre",
     "Per conteggi discreti, il diagramma a barre rappresenta ogni valore possibile."),
    ("relazione tra eta' e pressione sanguigna", "Quantitativa continua",
     "diagramma a dispersione",
     "Per analizzare la relazione tra due variabili continue, si usa il diagramma a dispersione."),
    ("livello di istruzione dei dipendenti", "Qualitativa ordinale",
     "diagramma a barre",
     "Per variabili ordinali, il diagramma a barre rispetta l'ordine naturale delle categorie."),
]

_ALL_GRAPH_TYPES = [
    "istogramma",
    "diagramma a barre",
    "diagramma a torta",
    "diagramma a dispersione",
    "grafico a linee",
]


def _t_variable_classification_basic():
    """L1: Classify a variable as qualitative/quantitative."""
    variable, correct_class, reason = random.choice(_VARIABLE_POOL)

    question = f"Come si classifica la variabile '{variable}'?"

    options = [correct_class]
    wrong = [c for c in _ALL_CLASSIFICATIONS if c != correct_class]
    options.extend(wrong)

    # Add a fifth plausible distractor
    extra_distractors = [
        "Categorica binaria",
        "Qualitativa cardinale",
        "Quantitativa proporzionale",
        "Qualitativa numerica",
        "Quantitativa categorica",
    ]
    extra = random.choice(extra_distractors)
    options.append(extra)

    correct_index = 0
    options, correct_index = Exercise.shuffle_options(options, correct_index)

    explanation = (
        f"La variabile '{variable}' e' classificata come {correct_class}.\n"
        f"{reason}\n\n"
        f"Ricorda:\n"
        f"- Qualitativa nominale: categorie senza ordine (es. colore, citta')\n"
        f"- Qualitativa ordinale: categorie con ordine (es. giudizi, titoli di studio)\n"
        f"- Quantitativa discreta: valori numerici interi (es. conteggi)\n"
        f"- Quantitativa continua: valori numerici reali (es. misure fisiche)"
    )
    tip = (
        "Le variabili qualitative descrivono qualita'/categorie, "
        "le quantitative descrivono quantita' misurabili. "
        "Le ordinali hanno un ordine, le nominali no. "
        "Le discrete contano, le continue misurano."
    )

    return {
        "question": question,
        "options": options,
        "correct_index": correct_index,
        "explanation": explanation,
        "did_you_know": tip,
        "difficulty": 1,
        "approfondimento": False,
    }


def _t_variable_classification_with_graph():
    """L2: Given a variable, identify the appropriate graph type."""
    entry = random.choice(_VARIABLE_GRAPH_POOL)
    variable_desc, var_type, correct_graph, reason = entry

    question = (
        f"La variabile '{variable_desc}' e' una variabile {var_type.lower()}. "
        f"Quale tipo di grafico e' piu' appropriato per rappresentarla?"
    )

    options = [correct_graph]
    wrong_graphs = [g for g in _ALL_GRAPH_TYPES if g != correct_graph]
    options.extend(wrong_graphs)

    correct_index = 0
    options, correct_index = Exercise.shuffle_options(options, correct_index)

    explanation = (
        f"Per la variabile '{variable_desc}' ({var_type.lower()}), "
        f"il grafico piu' appropriato e' il {correct_graph}.\n"
        f"{reason}\n\n"
        f"Regole generali:\n"
        f"- Qualitativa nominale: diagramma a barre o a torta\n"
        f"- Qualitativa ordinale: diagramma a barre (rispettando l'ordine)\n"
        f"- Quantitativa continua (distribuzione): istogramma\n"
        f"- Quantitativa continua (serie temporale): grafico a linee\n"
        f"- Due variabili quantitative (relazione): diagramma a dispersione\n"
        f"- Quantitativa discreta: diagramma a barre"
    )
    tip = (
        "La scelta del grafico dipende dal tipo di variabile: "
        "i diagrammi a barre e torta per dati categorici, "
        "l'istogramma per distribuzioni continue, "
        "il grafico a linee per serie temporali, "
        "il diagramma a dispersione per relazioni tra variabili."
    )

    return {
        "question": question,
        "options": options,
        "correct_index": correct_index,
        "explanation": explanation,
        "did_you_know": tip,
        "difficulty": 2,
        "approfondimento": False,
    }


def _t_discrete_vs_continuous():
    """L2: Distinguish between discrete and continuous quantitative variables."""
    discrete_vars = [
        (name, reason) for name, cls, reason in _VARIABLE_POOL
        if cls == "Quantitativa discreta"
    ]
    continuous_vars = [
        (name, reason) for name, cls, reason in _VARIABLE_POOL
        if cls == "Quantitativa continua"
    ]

    ask_type = random.choice(["continua", "discreta"])

    if ask_type == "continua":
        correct_name, correct_reason = random.choice(continuous_vars)
        wrong_pool = discrete_vars
        question = "Quale delle seguenti e' una variabile quantitativa continua?"
    else:
        correct_name, correct_reason = random.choice(discrete_vars)
        wrong_pool = continuous_vars
        question = "Quale delle seguenti e' una variabile quantitativa discreta?"

    # Pick 4 wrong answers: 2 from the opposite quantitative type, 2 qualitative
    qualitative_vars = [
        (name, reason) for name, cls, reason in _VARIABLE_POOL
        if cls.startswith("Qualitativa")
    ]

    wrong_quant = random.sample(wrong_pool, min(2, len(wrong_pool)))
    wrong_qual = random.sample(qualitative_vars, min(2, len(qualitative_vars)))
    wrong_names = [name for name, _ in wrong_quant + wrong_qual]

    options = [correct_name] + wrong_names[:4]
    # Ensure exactly 5 options
    while len(options) < 5:
        fallback = random.choice(_VARIABLE_POOL)
        if fallback[0] not in options:
            options.append(fallback[0])

    correct_index = 0
    options, correct_index = Exercise.shuffle_options(options, correct_index)

    explanation = (
        f"La risposta corretta e' '{correct_name}'.\n"
        f"{correct_reason}\n\n"
        f"Variabili quantitative discrete: assumono valori interi (conteggi).\n"
        f"Variabili quantitative continue: assumono qualsiasi valore reale in un intervallo (misure)."
    )
    tip = (
        "Per distinguere discreta da continua, chiediti: "
        "'Posso contare i valori possibili?' Se si', e' discreta. "
        "'Posso misurare con precisione arbitraria?' Se si', e' continua."
    )

    return {
        "question": question,
        "options": options,
        "correct_index": correct_index,
        "explanation": explanation,
        "did_you_know": tip,
        "difficulty": 2,
        "approfondimento": False,
    }


def _t_variable_classification_dataset():
    """L3: Analyze a dataset description and count/identify variable types."""
    # Build a random dataset of 4-6 variables
    n_vars = random.randint(4, 6)
    selected = random.sample(_VARIABLE_POOL, n_vars)

    var_names = [name for name, _, _ in selected]
    var_classes = [cls for _, cls, _ in selected]

    dataset_desc = ", ".join(var_names)

    # Count each type
    n_qual_nom = sum(1 for c in var_classes if c == "Qualitativa nominale")
    n_qual_ord = sum(1 for c in var_classes if c == "Qualitativa ordinale")
    n_quant_disc = sum(1 for c in var_classes if c == "Quantitativa discreta")
    n_quant_cont = sum(1 for c in var_classes if c == "Quantitativa continua")
    n_qualitative = n_qual_nom + n_qual_ord
    n_quantitative = n_quant_disc + n_quant_cont

    question_types = []
    if n_quantitative > 0:
        question_types.append("count_quantitative")
    if n_qualitative > 0:
        question_types.append("count_qualitative")
    if n_quant_cont > 0 and n_quant_disc > 0:
        question_types.append("count_continuous")

    q_type = random.choice(question_types) if question_types else "count_quantitative"

    if q_type == "count_quantitative":
        correct_value = n_quantitative
        q_text = "Quante variabili quantitative ci sono?"
        detail = "quantitative (discrete o continue)"
    elif q_type == "count_qualitative":
        correct_value = n_qualitative
        q_text = "Quante variabili qualitative ci sono?"
        detail = "qualitative (nominali o ordinali)"
    else:
        correct_value = n_quant_cont
        q_text = "Quante variabili quantitative continue ci sono?"
        detail = "quantitative continue"

    question = (
        f"In un'indagine si raccolgono le seguenti variabili: {dataset_desc}. "
        f"{q_text}"
    )

    correct_str = str(correct_value)
    # Generate distractor counts
    possible_counts = list(range(0, n_vars + 1))
    wrong_counts = [str(c) for c in possible_counts if str(c) != correct_str]
    random.shuffle(wrong_counts)
    distractors = wrong_counts[:4]

    options = [correct_str] + distractors
    # Ensure exactly 5 options
    while len(options) < 5:
        extra = str(random.randint(0, n_vars + 2))
        if extra not in options:
            options.append(extra)

    correct_index = 0
    options, correct_index = Exercise.shuffle_options(options, correct_index)

    classification_detail = "\n".join(
        f"- '{name}': {cls}" for name, cls, _ in selected
    )
    explanation = (
        f"Classificazione delle variabili nel dataset:\n"
        f"{classification_detail}\n\n"
        f"Le variabili {detail} sono {correct_value}."
    )
    tip = (
        "Per classificare correttamente le variabili di un dataset, "
        "analizza ogni variabile singolarmente: chiediti se descrive "
        "una qualita' (qualitativa) o una quantita' (quantitativa), "
        "e se ha un ordine naturale (ordinale) o meno (nominale)."
    )

    return {
        "question": question,
        "options": options,
        "correct_index": correct_index,
        "explanation": explanation,
        "did_you_know": tip,
        "difficulty": 3,
        "approfondimento": True,
    }


# ---------------------------------------------------------------------------
# Frequency exercise templates (TOLC-63)
# ---------------------------------------------------------------------------

def _t_frequency_absolute_from_data():
    """L1: Count the absolute frequency of a value in raw data."""
    # Choose a domain with limited distinct values
    domain_pool = [
        ("colore", ["rosso", "blu", "verde", "giallo", "bianco"]),
        ("voto", ["A", "B", "C", "D", "E"]),
        ("risultato del dado", ["1", "2", "3", "4", "5", "6"]),
        ("animale preferito", ["cane", "gatto", "pesce", "uccello", "coniglio"]),
        ("frutto", ["mela", "pera", "banana", "arancia", "kiwi"]),
    ]
    domain_name, domain_values = random.choice(domain_pool)
    n = random.randint(8, 15)
    data = [random.choice(domain_values) for _ in range(n)]

    # Pick a value that appears at least once
    target = random.choice(data)
    count = data.count(target)

    data_str = ", ".join(data)
    question = (
        f"Qual e' la frequenza assoluta di '{target}' nel seguente insieme di dati?\n"
        f"Dati: {data_str}"
    )

    # Build distractors
    counts_all = Counter(data)
    distractor_set = set()
    # count +/- 1
    for offset in [1, -1, 2, -2]:
        val = count + offset
        if val >= 0 and val != count:
            distractor_set.add(str(val))
    # count of adjacent values
    for v in domain_values:
        c = data.count(v)
        if c != count:
            distractor_set.add(str(c))
    # total N
    if n != count:
        distractor_set.add(str(n))
    # most/least common
    most_common_count = max(counts_all.values())
    least_common_count = min(counts_all.values())
    if most_common_count != count:
        distractor_set.add(str(most_common_count))
    if least_common_count != count:
        distractor_set.add(str(least_common_count))

    distractors = [d for d in distractor_set if d != str(count)]
    random.shuffle(distractors)
    distractors = distractors[:4]
    # Pad if needed
    fill_val = count + 3
    while len(distractors) < 4:
        s = str(fill_val)
        if s != str(count) and s not in distractors:
            distractors.append(s)
        fill_val += 1

    options = [str(count)] + distractors
    correct_index = 0
    options, correct_index = Exercise.shuffle_options(options, correct_index)

    count_detail = ", ".join(
        f"'{v}' compare {c} volta/e" for v, c in sorted(counts_all.items(), key=lambda x: -x[1])
    )
    explanation = (
        f"La frequenza assoluta e' il numero di volte che un valore compare nei dati.\n"
        f"Conteggio: {count_detail}.\n"
        f"La frequenza assoluta di '{target}' e' {count}."
    )
    tip = (
        "La frequenza assoluta di un valore e' semplicemente il numero di volte "
        "che quel valore compare nel dataset."
    )

    return {
        "question": question,
        "options": options,
        "correct_index": correct_index,
        "explanation": explanation,
        "did_you_know": tip,
        "difficulty": 1,
        "approfondimento": False,
    }


def _t_frequency_from_histogram():
    """L1: Read frequency information from a text-based histogram."""
    day_pool = [
        ("Lunedi'", "Martedi'", "Mercoledi'", "Giovedi'", "Venerdi'"),
        ("Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio"),
    ]
    category_pool = [
        ("materia", ["Matematica", "Italiano", "Scienze", "Storia", "Inglese"]),
        ("prodotto", ["Prodotto A", "Prodotto B", "Prodotto C", "Prodotto D", "Prodotto E"]),
    ]

    use_days = random.choice([True, False])
    if use_days:
        labels = list(random.choice(day_pool))
        context = "Un istogramma mostra il numero di visitatori giornalieri"
    else:
        cat_name, labels = random.choice(category_pool)
        context = f"Un istogramma mostra le vendite per {cat_name}"

    n_labels = random.randint(4, len(labels))
    labels = labels[:n_labels]
    freqs = [random.randint(2, 25) for _ in labels]

    histogram_str = ", ".join(f"{l}: {f}" for l, f in zip(labels, freqs))

    question_type = random.choice(["specific", "highest", "lowest"])

    if question_type == "specific":
        idx = random.randint(0, len(labels) - 1)
        correct_value = freqs[idx]
        question = (
            f"{context}: {histogram_str}. "
            f"Qual e' la frequenza di '{labels[idx]}'?"
        )
        explanation = (
            f"Dall'istogramma, la barra di '{labels[idx]}' ha altezza {correct_value}.\n"
            f"Quindi la frequenza assoluta e' {correct_value}."
        )
    elif question_type == "highest":
        max_freq = max(freqs)
        correct_label = labels[freqs.index(max_freq)]
        correct_value = max_freq
        question = (
            f"{context}: {histogram_str}. "
            f"Quale categoria ha la frequenza piu' alta?"
        )
        explanation = (
            f"Confrontando le frequenze: {histogram_str}.\n"
            f"La frequenza piu' alta e' {max_freq}, corrispondente a '{correct_label}'."
        )
    else:
        min_freq = min(freqs)
        correct_label = labels[freqs.index(min_freq)]
        correct_value = min_freq
        question = (
            f"{context}: {histogram_str}. "
            f"Quale categoria ha la frequenza piu' bassa?"
        )
        explanation = (
            f"Confrontando le frequenze: {histogram_str}.\n"
            f"La frequenza piu' bassa e' {min_freq}, corrispondente a '{correct_label}'."
        )

    tip = (
        "In un istogramma, l'altezza di ogni barra rappresenta la frequenza assoluta "
        "della categoria corrispondente."
    )

    # For "highest"/"lowest" the answer is a label, for "specific" it is a number
    if question_type == "specific":
        correct_str = str(correct_value)
        distractor_set = set()
        for f in freqs:
            if f != correct_value:
                distractor_set.add(str(f))
        for offset in [1, -1, 2]:
            val = correct_value + offset
            if val >= 0 and val != correct_value:
                distractor_set.add(str(val))
        distractors = list(distractor_set)[:4]
        fill_val = correct_value + 3
        while len(distractors) < 4:
            s = str(fill_val)
            if s != correct_str and s not in distractors:
                distractors.append(s)
            fill_val += 1
        options = [correct_str] + distractors
    else:
        correct_label_str = correct_label
        wrong_labels = [l for l in labels if l != correct_label_str]
        random.shuffle(wrong_labels)
        # Pad with made-up labels if needed
        extra = ["Sabato", "Domenica", "Prodotto X", "Altro"]
        for e in extra:
            if e not in labels and len(wrong_labels) < 4:
                wrong_labels.append(e)
        options = [correct_label_str] + wrong_labels[:4]

    correct_index = 0
    options, correct_index = Exercise.shuffle_options(options, correct_index)

    return {
        "question": question,
        "options": options,
        "correct_index": correct_index,
        "explanation": explanation,
        "did_you_know": tip,
        "difficulty": 1,
        "approfondimento": False,
    }


def _t_frequency_relative_percentage():
    """L2: Compute relative frequency as fraction or percentage."""
    scenarios = [
        ("In {n} lanci di un dado, il {val} e' uscito {k} volte", "dado", ["1", "2", "3", "4", "5", "6"]),
        ("In {n} estrazioni, la pallina {val} e' stata estratta {k} volte", "pallina", ["rossa", "blu", "verde", "bianca"]),
        ("Su {n} studenti intervistati, {k} hanno scelto {val}", "preferenza", ["calcio", "nuoto", "tennis", "basket"]),
    ]
    scenario_template, domain, values = random.choice(scenarios)
    n = random.choice([20, 25, 30, 40, 50, 60, 80, 100])
    val = random.choice(values)
    k = random.randint(max(1, n // 10), n // 3)
    rel_freq = k / n
    percentage = rel_freq * 100

    # Format the scenario
    scenario_text = scenario_template.format(n=n, val=val, k=k)

    ask_format = random.choice(["fraction", "percentage"])
    if ask_format == "fraction":
        question = f"{scenario_text}. Qual e' la frequenza relativa di '{val}'?"
        correct_value = rel_freq
        correct_str = _fmt(rel_freq)
        explanation = (
            f"La frequenza relativa = frequenza assoluta / totale osservazioni.\n"
            f"Frequenza relativa = {k} / {n} = {_fmt(rel_freq)}"
        )
    else:
        question = f"{scenario_text}. Qual e' la frequenza relativa percentuale di '{val}'?"
        correct_value = percentage
        correct_str = _fmt(percentage) + "%"
        explanation = (
            f"La frequenza relativa percentuale = (frequenza assoluta / totale) * 100.\n"
            f"Frequenza relativa = {k} / {n} = {_fmt(rel_freq)}\n"
            f"Percentuale = {_fmt(rel_freq)} * 100 = {_fmt(percentage)}%"
        )

    tip = (
        "La frequenza relativa e' il rapporto tra la frequenza assoluta e il totale. "
        "Per ottenere la percentuale, moltiplica la frequenza relativa per 100."
    )

    # Build distractors
    distractor_set = set()
    # Common mistakes
    if ask_format == "fraction":
        # Confusing absolute with relative
        distractor_set.add(str(k))
        # Wrong denominator
        if n - 1 > 0:
            distractor_set.add(_fmt(k / (n - 1)))
        distractor_set.add(_fmt(k / (n + 1)))
        # Percentage instead of fraction
        distractor_set.add(_fmt(percentage))
    else:
        # Confusing absolute with relative
        distractor_set.add(str(k) + "%")
        # Fraction instead of percentage
        distractor_set.add(_fmt(rel_freq) + "%")
        # x10 instead of x100
        distractor_set.add(_fmt(rel_freq * 10) + "%")
        # Wrong denominator
        if n - 1 > 0:
            distractor_set.add(_fmt(k / (n - 1) * 100) + "%")

    # Remove correct
    distractor_set.discard(correct_str)
    distractors = list(distractor_set)[:4]

    # Pad with numeric neighbors
    if ask_format == "fraction":
        base = correct_value
        for offset in [0.02, -0.02, 0.05, -0.05, 0.1, -0.1]:
            val_d = base + offset
            if 0 < val_d < 1:
                s = _fmt(val_d)
                if s != correct_str and s not in distractors:
                    distractors.append(s)
            if len(distractors) >= 4:
                break
    else:
        base = correct_value
        for offset in [2, -2, 5, -5, 10, -10]:
            val_d = base + offset
            if val_d > 0:
                s = _fmt(val_d) + "%"
                if s != correct_str and s not in distractors:
                    distractors.append(s)
            if len(distractors) >= 4:
                break

    distractors = distractors[:4]

    options = [correct_str] + distractors
    correct_index = 0
    options, correct_index = Exercise.shuffle_options(options, correct_index)

    return {
        "question": question,
        "options": options,
        "correct_index": correct_index,
        "explanation": explanation,
        "did_you_know": tip,
        "difficulty": 2,
        "approfondimento": False,
    }


def _t_frequency_compare():
    """L2: Compare frequencies across categories in a frequency table."""
    categories = random.sample(["A", "B", "C", "D", "E", "F"], k=random.randint(4, 5))
    frequencies = [random.randint(3, 30) for _ in categories]
    # Ensure no ties for max/min
    while frequencies.count(max(frequencies)) > 1:
        frequencies[frequencies.index(max(frequencies))] += 1
    while frequencies.count(min(frequencies)) > 1:
        frequencies[frequencies.index(min(frequencies))] -= 1
        if min(frequencies) < 1:
            frequencies[frequencies.index(min(frequencies))] = 1

    total = sum(frequencies)
    table_str = ", ".join(f"{c}: {f}" for c, f in zip(categories, frequencies))

    question_type = random.choice(["highest_relative", "lowest_relative", "compare_two"])

    if question_type == "highest_relative":
        rel_freqs = [(c, f / total) for c, f in zip(categories, frequencies)]
        best = max(rel_freqs, key=lambda x: x[1])
        correct_label = best[0]
        question = (
            f"Data la tabella di frequenze assolute: {table_str} (totale = {total}). "
            f"Quale categoria ha la frequenza relativa piu' alta?"
        )
        explanation = (
            f"Frequenze relative: {', '.join(f'{c}: {f}/{total} = {_fmt(f/total)}' for c, f in zip(categories, frequencies))}.\n"
            f"La categoria con frequenza relativa piu' alta e' '{correct_label}' ({_fmt(best[1])})."
        )
    elif question_type == "lowest_relative":
        rel_freqs = [(c, f / total) for c, f in zip(categories, frequencies)]
        worst = min(rel_freqs, key=lambda x: x[1])
        correct_label = worst[0]
        question = (
            f"Data la tabella di frequenze assolute: {table_str} (totale = {total}). "
            f"Quale categoria ha la frequenza relativa piu' bassa?"
        )
        explanation = (
            f"Frequenze relative: {', '.join(f'{c}: {f}/{total} = {_fmt(f/total)}' for c, f in zip(categories, frequencies))}.\n"
            f"La categoria con frequenza relativa piu' bassa e' '{correct_label}' ({_fmt(worst[1])})."
        )
    else:
        idx_a, idx_b = random.sample(range(len(categories)), 2)
        cat_a, freq_a = categories[idx_a], frequencies[idx_a]
        cat_b, freq_b = categories[idx_b], frequencies[idx_b]
        rel_a = freq_a / total
        rel_b = freq_b / total
        if rel_a > rel_b:
            correct_label = cat_a
        else:
            correct_label = cat_b
        question = (
            f"Data la tabella di frequenze assolute: {table_str} (totale = {total}). "
            f"Tra '{cat_a}' e '{cat_b}', quale ha frequenza relativa maggiore?"
        )
        explanation = (
            f"Frequenza relativa di '{cat_a}' = {freq_a}/{total} = {_fmt(rel_a)}\n"
            f"Frequenza relativa di '{cat_b}' = {freq_b}/{total} = {_fmt(rel_b)}\n"
            f"La categoria con frequenza relativa maggiore e' '{correct_label}'."
        )

    tip = (
        "La frequenza relativa permette di confrontare categorie indipendentemente "
        "dal totale delle osservazioni. Si calcola come frequenza assoluta / totale."
    )

    wrong_labels = [c for c in categories if c != correct_label]
    random.shuffle(wrong_labels)
    # Add a couple of plausible extra labels
    extras = ["Nessuna", "Tutte uguali"]
    wrong_labels.extend(extras)
    options = [correct_label] + wrong_labels[:4]

    correct_index = 0
    options, correct_index = Exercise.shuffle_options(options, correct_index)

    return {
        "question": question,
        "options": options,
        "correct_index": correct_index,
        "explanation": explanation,
        "did_you_know": tip,
        "difficulty": 2,
        "approfondimento": False,
    }


def _t_frequency_reconstruct_stats():
    """L3: Compute mean, median, or total from a frequency table."""
    values = sorted(random.sample(range(1, 12), k=random.randint(4, 6)))
    frequencies = [random.randint(1, 8) for _ in values]
    total_freq = sum(frequencies)
    weighted_sum = sum(v * f for v, f in zip(values, frequencies))

    table_str = ", ".join(f"valore {v}: frequenza {f}" for v, f in zip(values, frequencies))

    stat_type = random.choice(["mean", "median", "total"])

    if stat_type == "mean":
        correct_value = weighted_sum / total_freq
        question = (
            f"Data la seguente tabella di frequenza: {table_str}. "
            f"Qual e' la media aritmetica?"
        )
        explanation = (
            f"La media da tabella di frequenza = somma(valore * frequenza) / somma(frequenze).\n"
            f"Numeratore = {' + '.join(f'{v}*{f}' for v, f in zip(values, frequencies))} = {weighted_sum}\n"
            f"Denominatore = {total_freq}\n"
            f"Media = {weighted_sum} / {total_freq} = {_fmt(correct_value)}\n"
            f"Attenzione: non basta sommare i valori e dividere per il numero di valori distinti!"
        )
    elif stat_type == "median":
        # Expand data from frequency table
        expanded = []
        for v, f in zip(values, frequencies):
            expanded.extend([v] * f)
        expanded.sort()
        n = len(expanded)
        if n % 2 == 1:
            correct_value = float(expanded[n // 2])
            median_detail = f"Con {n} dati (dispari), la mediana e' il valore in posizione {n // 2 + 1}: {_fmt(correct_value)}"
        else:
            mid1 = expanded[n // 2 - 1]
            mid2 = expanded[n // 2]
            correct_value = (mid1 + mid2) / 2
            median_detail = (
                f"Con {n} dati (pari), la mediana e' la media dei valori in posizione "
                f"{n // 2} e {n // 2 + 1}: ({mid1} + {mid2}) / 2 = {_fmt(correct_value)}"
            )
        question = (
            f"Data la seguente tabella di frequenza: {table_str}. "
            f"Qual e' la mediana?"
        )
        explanation = (
            f"Per trovare la mediana, espandiamo i dati: totale {n} osservazioni.\n"
            f"{median_detail}\n"
            f"Ricorda: bisogna considerare le frequenze per posizionare correttamente i valori!"
        )
    else:
        correct_value = float(total_freq)
        question = (
            f"Data la seguente tabella di frequenza: {table_str}. "
            f"Quante osservazioni sono state raccolte in totale?"
        )
        explanation = (
            f"Il totale delle osservazioni e' la somma di tutte le frequenze.\n"
            f"Totale = {' + '.join(str(f) for f in frequencies)} = {total_freq}\n"
            f"Attenzione: il totale non e' il numero di valori distinti ({len(values)})!"
        )

    tip = (
        "Quando si lavora con tabelle di frequenza, ricorda che ogni valore "
        "va 'pesato' per la sua frequenza. La media si calcola come "
        "somma(valore * frequenza) / somma(frequenze)."
    )

    correct_str = _fmt(correct_value)
    distractors = _make_distractors(correct_value)
    # Add common mistakes
    if stat_type == "mean":
        # Mistake: simple average of distinct values
        simple_avg = sum(values) / len(values)
        simple_str = _fmt(simple_avg)
        if simple_str != correct_str and simple_str not in distractors:
            distractors[0] = simple_str
    elif stat_type == "total":
        # Mistake: number of distinct values
        n_distinct_str = str(len(values))
        if n_distinct_str != correct_str and n_distinct_str not in distractors:
            distractors[0] = n_distinct_str

    options = [correct_str] + distractors[:4]
    correct_index = 0
    options, correct_index = Exercise.shuffle_options(options, correct_index)

    return {
        "question": question,
        "options": options,
        "correct_index": correct_index,
        "explanation": explanation,
        "did_you_know": tip,
        "difficulty": 3,
        "approfondimento": True,
    }


# Sentinel marker for templates that return full dicts
_DICT_TEMPLATES = {
    _t_variable_classification_basic,
    _t_variable_classification_with_graph,
    _t_discrete_vs_continuous,
    _t_variable_classification_dataset,
    _t_frequency_absolute_from_data,
    _t_frequency_from_histogram,
    _t_frequency_relative_percentage,
    _t_frequency_compare,
    _t_frequency_reconstruct_stats,
}


# ---------------------------------------------------------------------------
# Main Exercise class
# ---------------------------------------------------------------------------

class StatisticsExercise(Exercise):
    """Statistica -- exercises covering descriptive statistics for TOLC-B."""

    TEMPLATES_L1 = [
        _t1_media_aritmetica,
        _t1_mediana_dispari,
        _t1_mediana_pari,
        _t1_moda,
        _t1_range,
        _t1_read_histogram,
        _t1_read_pie_chart,
        _t1_read_bar_chart,
        _t_variable_classification_basic,
        _t_frequency_absolute_from_data,
        _t_frequency_from_histogram,
    ]

    TEMPLATES_L2 = [
        _t2_media_ponderata,
        _t2_frequenza_relativa,
        _t2_media_frequenza,
        _t_variable_classification_with_graph,
        _t_discrete_vs_continuous,
        _t_frequency_relative_percentage,
        _t_frequency_compare,
    ]

    TEMPLATES_L3 = [
        _t2_varianza,
        _t2_deviazione_standard,
        _t3_varianza_formula,
        _t3_coefficiente_variazione,
        _t3_quartili,
        _t3_media_combinata,
        _t3_trasformazione_lineare,
        _t_variable_classification_dataset,
        _t_frequency_reconstruct_stats,
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

        # Templates that return full dicts (categorical answers) bypass
        # the numeric distractor generation pipeline.
        if template_fn in _DICT_TEMPLATES:
            return template_fn()

        question, correct_value, explanation, tip = template_fn()

        correct_str = _fmt(correct_value)
        distractors = _make_distractors(correct_value)

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
            "approfondimento": difficulty == 3,
        }
