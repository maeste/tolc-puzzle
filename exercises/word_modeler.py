import random

from exercises.base import Exercise


# --- Name pools for parametric variation ---
_NOMI_MASCHILI = ["Marco", "Luca", "Andrea", "Giovanni", "Paolo", "Matteo", "Alessandro", "Davide", "Simone", "Roberto"]
_NOMI_FEMMINILI = ["Sara", "Laura", "Giulia", "Anna", "Maria", "Elena", "Chiara", "Francesca", "Valentina", "Silvia"]
_NOMI = _NOMI_MASCHILI + _NOMI_FEMMINILI


def _pick_name(exclude=None):
    pool = [n for n in _NOMI if n != exclude] if exclude else _NOMI
    return random.choice(pool)


def _pick_two_names():
    a = _pick_name()
    b = _pick_name(exclude=a)
    return a, b


class WordModeler(Exercise):
    """Traduci la Storia -- translate word problems into equations."""

    # Each template function returns (question, correct_eq, distractors, explanation, tip)
    # distractors is a list of 4 wrong equations.

    # ------------------------------------------------------------------ helpers
    @staticmethod
    def _build_result(question, correct_eq, distractors, explanation, tip, difficulty):
        options = [correct_eq] + distractors
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

    # ================================================================
    #  LEVEL 1 TEMPLATES  (1 unknown)
    # ================================================================

    @staticmethod
    def _tank_fill():
        name = _pick_name()
        rate = random.randint(3, 12)
        capacity = random.randint(50, 200)
        question = (
            f"{name} riempie una vasca con un rubinetto che eroga {rate} litri al minuto. "
            f"La vasca ha una capacita di {capacity} litri. "
            f"Quanti minuti servono per riempirla completamente?"
        )
        correct = f"{rate} * x = {capacity}"
        d1 = f"x / {rate} = {capacity}"
        d2 = f"{rate} + x = {capacity}"
        d3 = f"{rate} * {capacity} = x"
        d4 = f"x = {capacity} - {rate}"
        explanation = (
            f"Il problema dice che il rubinetto eroga {rate} litri al minuto per x minuti, "
            f"che si traduce in {rate} * x = {capacity} perche il prodotto portata per tempo da il volume totale."
        )
        tip = "Nei problemi di riempimento, volume = portata * tempo. Identifica quale grandezza e l'incognita."
        return question, correct, [d1, d2, d3, d4], explanation, tip

    @staticmethod
    def _discount_price():
        name = _pick_name()
        perc = random.choice([10, 15, 20, 25, 30])
        final = random.randint(30, 150)
        question = (
            f"{name} compra una giacca scontata del {perc}%. "
            f"Paga {final} euro. "
            f"Qual era il prezzo originale x della giacca?"
        )
        factor = round(1 - perc / 100, 2)
        correct = f"x * {factor} = {final}"
        d1 = f"x - {perc} = {final}"
        d2 = f"x * {perc}/100 = {final}"
        d3 = f"x + x * {factor} = {final}"
        d4 = f"x * (1 + {perc}/100) = {final}"
        explanation = (
            f"Il problema dice che il prezzo originale x, scontato del {perc}%, diventa {final} euro. "
            f"Che si traduce in x * (1 - {perc}/100) = x * {factor} = {final} "
            f"perche paghi il {100 - perc}% del prezzo originale."
        )
        tip = "Sconto del p% significa pagare (100 - p)% del prezzo, cioe moltiplicare per (1 - p/100)."
        return question, correct, [d1, d2, d3, d4], explanation, tip

    @staticmethod
    def _age_problem_simple():
        name = _pick_name()
        years = random.randint(3, 15)
        future_age = random.randint(20, 50)
        question = (
            f"Tra {years} anni {name} avra {future_age} anni. "
            f"Quanti anni ha adesso?"
        )
        correct = f"x + {years} = {future_age}"
        d1 = f"x - {years} = {future_age}"
        d2 = f"{years} * x = {future_age}"
        d3 = f"x = {future_age} + {years}"
        d4 = f"{future_age} - x = {years}"
        explanation = (
            f"Il problema dice che l'eta attuale x, aumentata di {years} anni, "
            f"sara {future_age}. Che si traduce in x + {years} = {future_age} "
            f"perche 'tra {years} anni' significa aggiungere {years} all'eta attuale."
        )
        tip = "'Tra N anni' si traduce sempre con + N; 'N anni fa' con - N."
        return question, correct, [d1, d2, d3, d4], explanation, tip

    @staticmethod
    def _speed_distance_simple():
        name = _pick_name()
        speed = random.randint(40, 120)
        distance = random.randint(100, 500)
        question = (
            f"{name} guida a una velocita media di {speed} km/h. "
            f"Deve percorrere {distance} km. "
            f"Quanto tempo x (in ore) impieghera?"
        )
        correct = f"{speed} * x = {distance}"
        d1 = f"x / {speed} = {distance}"
        d2 = f"x * {distance} = {speed}"
        d3 = f"{speed} + x = {distance}"
        d4 = f"x = {speed} / {distance}"
        explanation = (
            f"Il problema dice che {name} viaggia a {speed} km/h per x ore percorrendo {distance} km. "
            f"Che si traduce in {speed} * x = {distance} perche distanza = velocita * tempo."
        )
        tip = "La formula fondamentale e: distanza = velocita * tempo. Risolvi per l'incognita."
        return question, correct, [d1, d2, d3, d4], explanation, tip

    @staticmethod
    def _percentage_increase():
        name = _pick_name()
        perc = random.choice([5, 8, 10, 12, 15, 20])
        original = random.randint(200, 1000)
        question = (
            f"Il prezzo di un prodotto acquistato da {name} "
            f"e aumentato del {perc}% rispetto all'anno scorso. "
            f"Se l'anno scorso costava {original} euro, quanto costa ora (x)?"
        )
        factor = round(1 + perc / 100, 2)
        correct = f"x = {original} * {factor}"
        d1 = f"x = {original} + {perc}"
        d2 = f"x = {original} * {perc}"
        d3 = f"x = {original} / {factor}"
        d4 = f"x = {original} + {original} * {perc}"
        explanation = (
            f"Il problema dice che il prezzo e aumentato del {perc}%. "
            f"Che si traduce in x = {original} * (1 + {perc}/100) = {original} * {factor} "
            f"perche un aumento del {perc}% moltiplica il valore originale per {factor}."
        )
        tip = "Aumento del p% significa moltiplicare per (1 + p/100), non sommare p al valore."
        return question, correct, [d1, d2, d3, d4], explanation, tip

    @staticmethod
    def _rectangle_perimeter():
        base = random.randint(5, 20)
        perimeter = random.randint(base * 4, base * 8)
        # make sure perimeter is even for nice numbers
        perimeter = perimeter if perimeter % 2 == 0 else perimeter + 1
        question = (
            f"Un rettangolo ha la base di {base} cm e il perimetro di {perimeter} cm. "
            f"Quanto misura l'altezza x?"
        )
        correct = f"2 * ({base} + x) = {perimeter}"
        d1 = f"2 * {base} + x = {perimeter}"
        d2 = f"{base} * x = {perimeter}"
        d3 = f"2 * {base} * x = {perimeter}"
        d4 = f"{base} + x = {perimeter}"
        explanation = (
            f"Il problema dice che il perimetro e {perimeter} cm con base {base} cm. "
            f"Che si traduce in 2 * ({base} + x) = {perimeter} "
            f"perche il perimetro del rettangolo e 2 * (base + altezza)."
        )
        tip = "Perimetro del rettangolo = 2 * (base + altezza). Non confondere con l'area = base * altezza."
        return question, correct, [d1, d2, d3, d4], explanation, tip

    @staticmethod
    def _consecutive_numbers():
        total = random.randint(20, 100)
        question = (
            f"La somma di tre numeri interi consecutivi e {total}. "
            f"Trova il primo numero x."
        )
        correct = f"x + (x + 1) + (x + 2) = {total}"
        d1 = f"3x = {total}"
        d2 = f"x + x + x = {total}"
        d3 = f"x * (x + 1) * (x + 2) = {total}"
        d4 = f"x + (x + 2) + (x + 4) = {total}"
        explanation = (
            f"Il problema dice che tre numeri consecutivi sommano a {total}. "
            f"Che si traduce in x + (x + 1) + (x + 2) = {total} "
            f"perche 'consecutivi' significa che ogni successivo e 1 in piu del precedente."
        )
        tip = "Numeri consecutivi: x, x+1, x+2, ... Non confondere con multipli consecutivi: x, 2x, 3x."
        return question, correct, [d1, d2, d3, d4], explanation, tip

    # ================================================================
    #  LEVEL 2 TEMPLATES  (2 unknowns)
    # ================================================================

    @staticmethod
    def _two_workers():
        name_a, name_b = _pick_two_names()
        total_hours = random.randint(10, 40)
        ratio = random.randint(2, 5)
        question = (
            f"{name_a} e {name_b} lavorano insieme per un totale di {total_hours} ore. "
            f"{name_a} lavora {ratio} volte le ore di {name_b}. "
            f"Quante ore lavora ciascuno (x = ore di {name_b}, y = ore di {name_a})?"
        )
        correct = f"x + y = {total_hours}, y = {ratio} * x"
        d1 = f"x + y = {total_hours}, x = {ratio} * y"
        d2 = f"x * y = {total_hours}, y = {ratio} * x"
        d3 = f"x + y = {total_hours}, y = x + {ratio}"
        d4 = f"x + y = {total_hours}, y - x = {ratio}"
        explanation = (
            f"Il problema dice che il totale delle ore e {total_hours} e che {name_a} lavora "
            f"{ratio} volte le ore di {name_b}. Che si traduce in x + y = {total_hours} e y = {ratio} * x "
            f"perche '{ratio} volte' indica una moltiplicazione, non un'addizione."
        )
        tip = "'A e il doppio/triplo di B' si traduce con A = 2B o A = 3B, mai con A = B + 2."
        return question, correct, [d1, d2, d3, d4], explanation, tip

    @staticmethod
    def _mixture():
        name = _pick_name()
        conc_a = random.choice([10, 15, 20, 25])
        conc_b = random.choice([40, 50, 60, 70])
        target = random.randint(conc_a + 5, conc_b - 5)
        total = random.randint(10, 50)
        question = (
            f"{name} vuole preparare {total} litri di una soluzione al {target}%. "
            f"Ha una soluzione al {conc_a}% (x litri) e una al {conc_b}% (y litri). "
            f"Come si modella il problema?"
        )
        correct = f"x + y = {total}, {conc_a}/100 * x + {conc_b}/100 * y = {target}/100 * {total}"
        d1 = f"x + y = {total}, {conc_a} * x + {conc_b} * y = {target}"
        d2 = f"x + y = {total}, x/{conc_a} + y/{conc_b} = {total}/{target}"
        d3 = f"x * y = {total}, {conc_a} * x + {conc_b} * y = {target} * {total}"
        d4 = f"x + y = {total}, ({conc_a} + {conc_b})/2 * (x + y) = {target}/100 * {total}"
        explanation = (
            f"Il problema dice che x + y = {total} litri totali e la concentrazione risultante e {target}%. "
            f"Che si traduce in {conc_a}/100 * x + {conc_b}/100 * y = {target}/100 * {total} "
            f"perche la quantita di soluto nella miscela e la somma dei soluti delle due soluzioni."
        )
        tip = "Nei problemi di miscele: quantita_soluto = concentrazione * volume. Somma i soluti, non le concentrazioni."
        return question, correct, [d1, d2, d3, d4], explanation, tip

    @staticmethod
    def _two_prices():
        name = _pick_name()
        n_pens = random.randint(2, 6)
        n_notebooks = random.randint(1, 4)
        total = random.randint(10, 30)
        question = (
            f"{name} compra {n_pens} penne (al prezzo x ciascuna) e "
            f"{n_notebooks} quaderni (al prezzo y ciascuno) spendendo {total} euro. "
            f"Ogni quaderno costa 2 euro in piu di ogni penna. "
            f"Quale sistema modella il problema?"
        )
        correct = f"{n_pens} * x + {n_notebooks} * y = {total}, y = x + 2"
        d1 = f"{n_pens} * x + {n_notebooks} * y = {total}, x = y + 2"
        d2 = f"x + y = {total}, {n_pens} * x = {n_notebooks} * y"
        d3 = f"{n_pens} + {n_notebooks} = {total}, y - x = 2"
        d4 = f"{n_pens} * x + {n_notebooks} * y = {total}, y * x = 2"
        explanation = (
            f"Il problema dice che la spesa totale e {total} euro con {n_pens} penne e {n_notebooks} quaderni, "
            f"e che ogni quaderno costa 2 euro in piu. Che si traduce in {n_pens}x + {n_notebooks}y = {total} "
            f"e y = x + 2 perche 'costa 2 euro in piu' significa y = x + 2."
        )
        tip = "'Costa N euro in piu' si traduce con y = x + N, non con x = y + N. Attenzione al verso!"
        return question, correct, [d1, d2, d3, d4], explanation, tip

    @staticmethod
    def _age_problem_double():
        name_a, name_b = _pick_two_names()
        diff = random.randint(3, 15)
        total = random.randint(30, 80)
        question = (
            f"{name_a} ha {diff} anni piu di {name_b}. "
            f"La somma delle loro eta e {total} anni. "
            f"Quanti anni ha ciascuno (x = eta di {name_b}, y = eta di {name_a})?"
        )
        correct = f"y = x + {diff}, x + y = {total}"
        d1 = f"x = y + {diff}, x + y = {total}"
        d2 = f"y - x = {diff}, y - x = {total}"
        d3 = f"y = x + {diff}, x * y = {total}"
        d4 = f"y = {diff} * x, x + y = {total}"
        explanation = (
            f"Il problema dice che {name_a} ha {diff} anni piu di {name_b} e la somma e {total}. "
            f"Che si traduce in y = x + {diff} e x + y = {total} "
            f"perche 'N anni piu' significa sommare N all'eta del piu giovane."
        )
        tip = "Nelle relazioni 'A ha N anni piu di B': A = B + N. La somma delle eta e un'equazione separata."
        return question, correct, [d1, d2, d3, d4], explanation, tip

    @staticmethod
    def _speed_encounter():
        name_a, name_b = _pick_two_names()
        v_a = random.randint(40, 80)
        v_b = random.randint(50, 90)
        dist = random.randint(200, 600)
        question = (
            f"{name_a} parte dalla citta A a {v_a} km/h e {name_b} parte dalla citta B a {v_b} km/h. "
            f"Le due citta distano {dist} km. Si muovono uno verso l'altro. "
            f"Dopo quanto tempo t si incontrano?"
        )
        correct = f"{v_a} * t + {v_b} * t = {dist}"
        d1 = f"{v_a} * t - {v_b} * t = {dist}"
        d2 = f"{v_a} * {v_b} * t = {dist}"
        d3 = f"({v_a} + {v_b}) / t = {dist}"
        d4 = f"{v_a} * t = {v_b} * t + {dist}"
        explanation = (
            f"Il problema dice che i due si avvicinano contemporaneamente. "
            f"Che si traduce in {v_a}t + {v_b}t = {dist} "
            f"perche le distanze percorse si sommano fino a coprire la distanza totale."
        )
        tip = "Quando due oggetti si avvicinano, le distanze si sommano. Quando si allontanano, si sottraggono."
        return question, correct, [d1, d2, d3, d4], explanation, tip

    # ================================================================
    #  LEVEL 3 TEMPLATES  (systems of equations / harder)
    # ================================================================

    @staticmethod
    def _system_ages():
        name_a, name_b = _pick_two_names()
        years = random.randint(3, 10)
        mult = random.randint(2, 4)
        total_now = random.randint(30, 70)
        question = (
            f"La somma delle eta di {name_a} (x) e {name_b} (y) e {total_now} anni. "
            f"Tra {years} anni, {name_a} avra {mult} volte l'eta di {name_b}. "
            f"Quale sistema di equazioni modella il problema?"
        )
        correct = f"x + y = {total_now}, x + {years} = {mult} * (y + {years})"
        d1 = f"x + y = {total_now}, x + {years} = {mult} * y"
        d2 = f"x + y = {total_now}, x = {mult} * (y + {years})"
        d3 = f"x + y + {years} = {total_now}, x = {mult} * y + {years}"
        d4 = f"x + y = {total_now}, x * {mult} = y + {years}"
        explanation = (
            f"Il problema dice che la somma e {total_now} e che tra {years} anni x sara {mult} volte y. "
            f"Che si traduce in x + y = {total_now} e x + {years} = {mult} * (y + {years}) "
            f"perche 'tra {years} anni' si applica a ENTRAMBE le eta, non solo a una."
        )
        tip = "Errore comune: dimenticare di aggiungere gli anni a ENTRAMBE le persone in 'tra N anni'."
        return question, correct, [d1, d2, d3, d4], explanation, tip

    @staticmethod
    def _tank_two_pipes():
        rate_fill = random.randint(5, 15)
        rate_drain = random.randint(2, rate_fill - 1)
        capacity = random.randint(100, 400)
        question = (
            f"Una vasca da {capacity} litri ha un rubinetto che riempie a {rate_fill} litri/min "
            f"e uno scarico che svuota a {rate_drain} litri/min. "
            f"Se entrambi sono aperti, dopo quanto tempo t la vasca e piena? "
            f"Quanta acqua x esce dallo scarico nel frattempo?"
        )
        correct = f"{rate_fill} * t - {rate_drain} * t = {capacity}, x = {rate_drain} * t"
        d1 = f"{rate_fill} * t + {rate_drain} * t = {capacity}, x = {rate_drain} * t"
        d2 = f"{rate_fill} * t = {capacity}, x = {rate_drain} * t"
        d3 = f"({rate_fill} - {rate_drain}) * x = {capacity}, t = x / {rate_drain}"
        d4 = f"{rate_fill} / t - {rate_drain} / t = {capacity}, x = {rate_drain} * t"
        explanation = (
            f"Il problema dice che il rubinetto riempie e lo scarico svuota simultaneamente. "
            f"Che si traduce in {rate_fill}t - {rate_drain}t = {capacity} e x = {rate_drain}t "
            f"perche il volume netto e la differenza tra quanto entra e quanto esce."
        )
        tip = "Con flussi opposti, il risultato netto e la differenza delle portate, non la somma."
        return question, correct, [d1, d2, d3, d4], explanation, tip

    @staticmethod
    def _investment_system():
        name = _pick_name()
        total_invest = random.randint(5000, 20000)
        rate_a = random.randint(2, 5)
        rate_b = random.randint(6, 10)
        total_interest = random.randint(200, 1000)
        question = (
            f"{name} investe {total_invest} euro in due fondi: "
            f"il fondo A rende il {rate_a}% e il fondo B rende il {rate_b}%. "
            f"L'interesse totale annuo e {total_interest} euro. "
            f"Quanto ha investito in ciascun fondo (x nel fondo A, y nel fondo B)?"
        )
        correct = f"x + y = {total_invest}, {rate_a}/100 * x + {rate_b}/100 * y = {total_interest}"
        d1 = f"x + y = {total_invest}, {rate_a} * x + {rate_b} * y = {total_interest}"
        d2 = f"x + y = {total_interest}, {rate_a}/100 * x + {rate_b}/100 * y = {total_invest}"
        d3 = f"x * y = {total_invest}, x/{rate_a} + y/{rate_b} = {total_interest}"
        d4 = f"x * y = {total_invest}, {rate_a}/100 * x + {rate_b}/100 * y = {total_interest}"
        explanation = (
            f"Il problema dice che il totale investito e {total_invest} e l'interesse totale e {total_interest}. "
            f"Che si traduce in x + y = {total_invest} e {rate_a}/100 * x + {rate_b}/100 * y = {total_interest} "
            f"perche l'interesse e capitale * tasso percentuale."
        )
        tip = "Nei problemi di investimento, l'interesse = capitale * (tasso/100). Non dimenticare di dividere per 100!"
        return question, correct, [d1, d2, d3, d4], explanation, tip

    @staticmethod
    def _geometry_triangle_system():
        perimeter = random.randint(30, 80)
        diff_ab = random.randint(2, 8)
        mult_c = random.randint(2, 3)
        question = (
            f"Un triangolo ha perimetro {perimeter} cm. "
            f"Il lato b e {diff_ab} cm piu lungo del lato a. "
            f"Il lato c e {mult_c} volte il lato a. "
            f"Modella il problema con x = lato a."
        )
        correct = f"x + (x + {diff_ab}) + {mult_c} * x = {perimeter}"
        d1 = f"x + x + {diff_ab} + {mult_c} = {perimeter}"
        d2 = f"3x + {diff_ab} * {mult_c} = {perimeter}"
        d3 = f"x * (x + {diff_ab}) * {mult_c} = {perimeter}"
        d4 = f"x + x + {diff_ab} + {mult_c} * x = {perimeter}"
        explanation = (
            f"Il problema dice che a = x, b = x + {diff_ab}, c = {mult_c}x e il perimetro e {perimeter}. "
            f"Che si traduce in x + (x + {diff_ab}) + {mult_c}x = {perimeter} "
            f"perche il perimetro e la somma dei tre lati, ognuno espresso in funzione di x."
        )
        tip = "Esprimi tutti i lati in funzione di una sola variabile prima di scrivere l'equazione del perimetro."
        return question, correct, [d1, d2, d3, d4], explanation, tip

    @staticmethod
    def _work_rate_system():
        name_a, name_b = _pick_two_names()
        hours_a = random.randint(3, 8)
        hours_b = random.randint(4, 10)
        question = (
            f"{name_a} completa un lavoro in {hours_a} ore, {name_b} in {hours_b} ore. "
            f"Se lavorano insieme, quanto tempo t impiegano a completare il lavoro?"
        )
        correct = f"t/{hours_a} + t/{hours_b} = 1"
        d1 = f"t * ({hours_a} + {hours_b}) = 1"
        d2 = f"{hours_a} + {hours_b} = t"
        d3 = f"1/{hours_a} + 1/{hours_b} = t"
        d4 = f"{hours_a} * t + {hours_b} * t = 1"
        explanation = (
            f"Il problema dice che {name_a} fa 1/{hours_a} del lavoro all'ora e {name_b} fa 1/{hours_b}. "
            f"Che si traduce in t/{hours_a} + t/{hours_b} = 1 "
            f"perche in t ore ciascuno completa una frazione del lavoro, e insieme fanno il lavoro intero (= 1)."
        )
        tip = "Nei problemi di lavoro congiunto, somma le frazioni di lavoro: (t/tempo_A) + (t/tempo_B) = 1."
        return question, correct, [d1, d2, d3, d4], explanation, tip

    # ================================================================
    #  Template registry by difficulty
    # ================================================================

    def _get_templates(self, difficulty):
        level_1 = [
            self._tank_fill,
            self._discount_price,
            self._age_problem_simple,
            self._speed_distance_simple,
            self._percentage_increase,
            self._rectangle_perimeter,
            self._consecutive_numbers,
        ]
        level_2 = [
            self._two_workers,
            self._mixture,
            self._two_prices,
            self._age_problem_double,
            self._speed_encounter,
        ]
        level_3 = [
            self._system_ages,
            self._tank_two_pipes,
            self._investment_system,
            self._geometry_triangle_system,
            self._work_rate_system,
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
        question, correct_eq, distractors, explanation, tip = template_fn()
        return self._build_result(question, correct_eq, distractors, explanation, tip, difficulty)
