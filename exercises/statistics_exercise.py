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
        if d > 0 and _fmt(d) != correct_str:
            distractors.add(_fmt(d))

    # Strategy 4: random spread around correct value
    spread = max(1.0, abs(correct) * 0.3)
    while len(distractors) < count and attempts < 200:
        attempts += 1
        offset = random.uniform(-spread, spread)
        d = round(correct + offset, 2)
        if d > 0 and abs(d - correct) > 0.01:
            formatted = _fmt(d)
            if formatted != correct_str:
                distractors.add(formatted)

    # Fallback
    while len(distractors) < count:
        d = round(correct * random.uniform(0.5, 1.8), 2)
        if d > 0:
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
    ]

    TEMPLATES_L2 = [
        _t2_media_ponderata,
        _t2_frequenza_relativa,
        _t2_media_frequenza,
    ]

    TEMPLATES_L3 = [
        _t2_varianza,
        _t2_deviazione_standard,
        _t3_varianza_formula,
        _t3_coefficiente_variazione,
        _t3_quartili,
        _t3_media_combinata,
        _t3_trasformazione_lineare,
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
