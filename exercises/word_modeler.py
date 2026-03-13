import math
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

    @staticmethod
    def _supermarket_shopping():
        name = _pick_name()
        n_packs = random.randint(2, 8)
        price_pasta = random.choice([1, 2, 3])
        price_oil = random.choice([5, 6, 7, 8, 9])
        total = n_packs * price_pasta + price_oil
        question = (
            f"{name} compra {n_packs} confezioni di pasta a x euro ciascuna "
            f"e una bottiglia d'olio a {price_oil} euro. "
            f"Spende in tutto {total} euro. "
            f"Quale equazione modella il costo della pasta x?"
        )
        correct = f"{n_packs} * x + {price_oil} = {total}"
        d1 = f"x + {price_oil} = {total}"
        d2 = f"{n_packs} * x * {price_oil} = {total}"
        d3 = f"{n_packs} + x + {price_oil} = {total}"
        d4 = f"x * {price_oil} + {n_packs} = {total}"
        explanation = (
            f"Il problema dice che {name} compra {n_packs} confezioni a x euro "
            f"piu' una bottiglia d'olio a {price_oil} euro per un totale di {total} euro. "
            f"Che si traduce in {n_packs} * x + {price_oil} = {total} "
            f"perche' il costo totale e' la somma di {n_packs} confezioni per il prezzo unitario piu' l'olio."
        )
        tip = "Costo totale = (quantita' * prezzo unitario) + costi fissi. Identifica cosa e' l'incognita."
        return question, correct, [d1, d2, d3, d4], explanation, tip

    @staticmethod
    def _phone_plan():
        name = _pick_name()
        fixed = random.choice([5, 7, 8, 10, 12])
        cents_per_min = random.choice([5, 10, 15, 20])
        rate = round(cents_per_min / 100, 2)
        minutes = random.randint(50, 300)
        total = round(fixed + rate * minutes, 2)
        question = (
            f"Un piano telefonico costa {fixed} euro al mese di fisso "
            f"piu' {cents_per_min} centesimi al minuto. "
            f"{name} ha speso {total} euro questo mese. "
            f"Quanti minuti m ha parlato?"
        )
        correct = f"{fixed} + {rate} * m = {total}"
        d1 = f"{fixed} * m + {rate} = {total}"
        d2 = f"{fixed} + {cents_per_min} * m = {total}"
        d3 = f"m * {fixed} = {total} - {rate}"
        d4 = f"{rate} * m - {fixed} = {total}"
        explanation = (
            f"Il problema dice che il costo e' {fixed} euro fissi piu' {cents_per_min} centesimi "
            f"({rate} euro) per ogni minuto m. "
            f"Che si traduce in {fixed} + {rate} * m = {total} "
            f"perche' il costo totale e' la parte fissa piu' la parte variabile."
        )
        tip = "Attenzione alle unita': converti sempre i centesimi in euro (dividi per 100) prima di scrivere l'equazione."
        return question, correct, [d1, d2, d3, d4], explanation, tip

    @staticmethod
    def _cooking_recipe():
        name = _pick_name()
        people_orig = random.choice([4, 6, 8])
        people_target = random.choice([2, 3, 5, 10, 12])
        while people_target == people_orig:
            people_target = random.choice([2, 3, 5, 10, 12])
        grams = random.choice([200, 250, 300, 400, 500])
        question = (
            f"Una ricetta per {people_orig} persone richiede {grams} grammi di farina. "
            f"{name} deve cucinare per {people_target} persone. "
            f"Quanta farina x (in grammi) gli serve?"
        )
        correct = f"{people_orig} : {grams} = {people_target} : x"
        d1 = f"{grams} : {people_orig} = x : {people_target}"
        d2 = f"x / {people_target} = {grams} * {people_orig}"
        d3 = f"{people_orig} * x = {grams} + {people_target}"
        d4 = f"x = {grams} - {people_orig} + {people_target}"
        explanation = (
            f"Il problema e' una proporzione diretta: se {people_orig} persone richiedono {grams} g, "
            f"allora {people_target} persone richiedono x g. "
            f"Che si traduce in {people_orig} : {grams} = {people_target} : x "
            f"perche' il rapporto persone/farina deve restare costante."
        )
        tip = "Nelle proporzioni dirette A : B = C : D, il prodotto dei medi e' uguale al prodotto degli estremi: A*D = B*C."
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

    @staticmethod
    def _train_tickets():
        name = _pick_name()
        n_adult = random.randint(2, 5)
        n_child = random.randint(1, 4)
        adult_price = random.choice([12, 15, 18, 20, 25])
        child_price = adult_price // 2
        total = n_adult * adult_price + n_child * child_price
        question = (
            f"{name} compra {n_adult} biglietti del treno adulto (x euro ciascuno) "
            f"e {n_child} biglietti bambino (y euro ciascuno). "
            f"Spende in tutto {total} euro. "
            f"Il biglietto bambino costa meta' del biglietto adulto. "
            f"Quale sistema modella il problema?"
        )
        correct = f"{n_adult} * x + {n_child} * y = {total}, y = x / 2"
        d1 = f"{n_adult} * x + {n_child} * y = {total}, x = y / 2"
        d2 = f"{n_adult} * x + {n_child} * y = {total}, y = x - 2"
        d3 = f"x + y = {total}, {n_adult} * x = {n_child} * y"
        d4 = f"{n_adult} + {n_child} = {total}, y = x / 2"
        explanation = (
            f"Il problema dice che {name} spende {total} euro per {n_adult} biglietti adulto e "
            f"{n_child} biglietti bambino, con il bambino a meta' prezzo. "
            f"Che si traduce in {n_adult}x + {n_child}y = {total} e y = x/2 "
            f"perche' 'meta' del prezzo adulto' significa y = x/2."
        )
        tip = "'Costa la meta'' si traduce con y = x/2, non con x = y/2. Attenzione a chi e' la meta' di chi!"
        return question, correct, [d1, d2, d3, d4], explanation, tip

    @staticmethod
    def _sports_training():
        name = _pick_name()
        total_hours = random.randint(6, 20)
        # running = 2 * swimming, so swimming = total / 3 (we just need total divisible nicely)
        question = (
            f"{name} si allena x ore di corsa e y ore di nuoto a settimana. "
            f"In totale si allena {total_hours} ore. "
            f"Corre il doppio delle ore in cui nuota. "
            f"Quale sistema modella il problema?"
        )
        correct = f"x + y = {total_hours}, x = 2 * y"
        d1 = f"x + y = {total_hours}, y = 2 * x"
        d2 = f"x * y = {total_hours}, x = 2 * y"
        d3 = f"x + y = {total_hours}, x = y + 2"
        d4 = f"x - y = {total_hours}, x = 2 * y"
        explanation = (
            f"Il problema dice che il totale e' {total_hours} ore e che {name} corre il doppio "
            f"delle ore di nuoto. "
            f"Che si traduce in x + y = {total_hours} e x = 2y "
            f"perche' 'il doppio' indica moltiplicazione per 2, non addizione di 2."
        )
        tip = "'Il doppio di' si traduce con moltiplicazione (x = 2y), non con addizione (x = y + 2)."
        return question, correct, [d1, d2, d3, d4], explanation, tip

    @staticmethod
    def _electricity_bill():
        fixed = random.randint(8, 25)
        cost_kwh = random.choice([0.15, 0.20, 0.25, 0.30])
        consumption_a = random.randint(100, 300)
        consumption_b = random.randint(150, 400)
        while consumption_b == consumption_a:
            consumption_b = random.randint(150, 400)
        total_a = round(fixed + cost_kwh * consumption_a, 2)
        total_b = round(fixed + cost_kwh * consumption_b, 2)
        question = (
            f"La bolletta elettrica ha un costo fisso di x euro piu' un costo variabile "
            f"di y euro per kWh. "
            f"A gennaio il consumo e' stato {consumption_a} kWh con bolletta di {total_a} euro. "
            f"A febbraio il consumo e' stato {consumption_b} kWh con bolletta di {total_b} euro. "
            f"Quale sistema modella il problema?"
        )
        correct = f"x + {consumption_a} * y = {total_a}, x + {consumption_b} * y = {total_b}"
        d1 = f"{consumption_a} * x + y = {total_a}, {consumption_b} * x + y = {total_b}"
        d2 = f"x + y = {total_a}, x + y = {total_b}"
        d3 = f"x * {consumption_a} * y = {total_a}, x * {consumption_b} * y = {total_b}"
        d4 = f"x + {consumption_a} + y = {total_a}, x + {consumption_b} + y = {total_b}"
        explanation = (
            f"Il problema dice che la bolletta e' composta da un costo fisso x piu' un costo variabile "
            f"y per ogni kWh consumato. "
            f"Che si traduce in x + {consumption_a}y = {total_a} e x + {consumption_b}y = {total_b} "
            f"perche' bolletta = fisso + (consumo * costo_unitario)."
        )
        tip = "Nei costi con parte fissa e variabile: totale = fisso + (quantita' * prezzo_unitario). Con due mesi diversi si ottiene un sistema."
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

    @staticmethod
    def _travel_planning():
        name = _pick_name()
        speed_1 = random.choice([60, 80, 90, 100])
        speed_2 = random.choice([30, 40, 50, 60])
        while speed_2 == speed_1:
            speed_2 = random.choice([30, 40, 50, 60])
        total_time = random.randint(3, 8)
        question = (
            f"{name} va da citta' A a citta' B. "
            f"Percorre la prima meta' del tragitto a {speed_1} km/h "
            f"e la seconda meta' a {speed_2} km/h. "
            f"Il viaggio dura in tutto {total_time} ore. "
            f"Quanto e' lungo il percorso totale d?"
        )
        correct = f"d / (2 * {speed_1}) + d / (2 * {speed_2}) = {total_time}"
        d1 = f"d / {speed_1} + d / {speed_2} = {total_time}"
        d2 = f"d / ({speed_1} + {speed_2}) = {total_time}"
        d3 = f"(d * {speed_1} + d * {speed_2}) / 2 = {total_time}"
        d4 = f"d / (2 * {speed_1}) * d / (2 * {speed_2}) = {total_time}"
        explanation = (
            f"Il problema dice che {name} percorre meta' della distanza (d/2) a {speed_1} km/h "
            f"e l'altra meta' (d/2) a {speed_2} km/h. "
            f"Che si traduce in d/(2*{speed_1}) + d/(2*{speed_2}) = {total_time} "
            f"perche' tempo = distanza/velocita' per ciascun tratto, e i tempi si sommano."
        )
        tip = "Quando la distanza e' divisa in parti, calcola il tempo di ogni tratto separatamente e poi sommali."
        return question, correct, [d1, d2, d3, d4], explanation, tip

    @staticmethod
    def _shared_apartment():
        n1, n2 = _pick_two_names()
        n3 = _pick_name(exclude=n1)
        while n3 == n2:
            n3 = _pick_name(exclude=n1)
        diff = random.choice([50, 80, 100, 120, 150])
        total_rent = random.randint(800, 1800)
        question = (
            f"Tre coinquilini dividono l'affitto di {total_rent} euro al mese. "
            f"{n1} paga x euro, il doppio di {n2} (y euro) perche' ha la stanza piu' grande. "
            f"{n3} paga z euro, cioe' {diff} euro in meno di {n1}. "
            f"Quale sistema modella il problema?"
        )
        correct = f"x + y + z = {total_rent}, x = 2 * y, z = x - {diff}"
        d1 = f"x + y + z = {total_rent}, y = 2 * x, z = x - {diff}"
        d2 = f"x + y + z = {total_rent}, x = 2 * y, z = x + {diff}"
        d3 = f"x * y * z = {total_rent}, x = 2 * y, z = x - {diff}"
        d4 = f"x + y + z = {total_rent}, x = y + 2, z = x - {diff}"
        explanation = (
            f"Il problema dice che l'affitto totale e' {total_rent}, {n1} paga il doppio di {n2}, "
            f"e {n3} paga {diff} euro in meno di {n1}. "
            f"Che si traduce in x + y + z = {total_rent}, x = 2y e z = x - {diff} "
            f"perche' 'il doppio' e' moltiplicazione e '{diff} in meno' e' sottrazione."
        )
        tip = "Nei problemi con piu' incognite, scrivi una equazione per ogni relazione data e una per il totale."
        return question, correct, [d1, d2, d3, d4], explanation, tip

    # ================================================================
    #  NUMERIC-ANSWER TEMPLATES
    #  Each returns (question, correct_answer_str, distractors, explanation, tip)
    #  where correct_answer_str and distractors are numeric strings.
    # ================================================================

    # --- helpers for numeric distractors ---
    @staticmethod
    def _numeric_distractors(correct, offsets=None):
        """Generate 4 distinct numeric distractors around *correct* (int).

        *offsets*, if given, must be a list of 4 non-zero integers.
        Otherwise reasonable defaults are computed.
        All returned values are stringified integers, guaranteed distinct
        from *correct* and from each other.
        """
        if offsets is None:
            offsets = [-2, -1, 1, 2]
        candidates = []
        for o in offsets:
            v = correct + o
            if v != correct and v not in candidates:
                candidates.append(v)
        # fill up to 4 if collisions removed some
        extra = 3
        while len(candidates) < 4:
            extra += 1
            v = correct + extra
            if v != correct and v not in candidates:
                candidates.append(v)
        return [str(c) for c in candidates[:4]]

    # ---- Level 1 numeric templates ----

    @staticmethod
    def _numeric_age_sum():
        """Age problem: A is N years older than B, sum of ages is S. How old is A?"""
        name_a, name_b = _pick_two_names()
        diff = random.randint(3, 15)
        # ensure sum is even-friendly: b = (total - diff) / 2 must be positive integer
        b_age = random.randint(8, 35)
        a_age = b_age + diff
        total = a_age + b_age
        question = (
            f"{name_a} ha {diff} anni piu di {name_b}. "
            f"La somma delle loro eta e {total}. "
            f"Quanti anni ha {name_a}?"
        )
        correct = a_age
        distractors = WordModeler._numeric_distractors(
            correct, [-(diff), -1, diff, b_age - a_age if b_age != a_age else 3]
        )
        explanation = (
            f"Se {name_b} ha x anni, allora {name_a} ha x + {diff}. "
            f"Dalla somma: x + (x + {diff}) = {total}, quindi 2x = {total - diff}, "
            f"x = {b_age}, e {name_a} ha {b_age} + {diff} = {a_age} anni."
        )
        tip = "Nei problemi di eta con somma e differenza: il maggiore = (somma + differenza) / 2."
        return question, str(correct), distractors, explanation, tip

    @staticmethod
    def _numeric_discount():
        """Price with percentage discount: what is the discounted price?"""
        name = _pick_name()
        original = random.choice([40, 50, 60, 80, 100, 120, 150, 200])
        perc = random.choice([10, 15, 20, 25, 30, 40, 50])
        discounted = int(original * (100 - perc) / 100)
        # ensure clean integer result
        while discounted != original * (100 - perc) / 100:
            original = random.choice([40, 50, 60, 80, 100, 120, 150, 200])
            perc = random.choice([10, 20, 25, 30, 40, 50])
            discounted = int(original * (100 - perc) / 100)
        question = (
            f"{name} vuole comprare un articolo che costa {original} euro. "
            f"Il negozio applica uno sconto del {perc}%. "
            f"Qual e il prezzo scontato?"
        )
        correct = discounted
        wrong_add = original + int(original * perc / 100)
        wrong_sub_flat = original - perc
        wrong_half = original // 2
        distractors = WordModeler._numeric_distractors(
            correct, [wrong_add - correct, wrong_sub_flat - correct, wrong_half - correct, 5]
        )
        explanation = (
            f"Il prezzo scontato = {original} - {original} * {perc}/100 = "
            f"{original} - {int(original * perc / 100)} = {discounted} euro."
        )
        tip = "Sconto del p%: prezzo_finale = prezzo * (1 - p/100). Non sottrarre la percentuale direttamente!"
        return question, str(correct), distractors, explanation, tip

    @staticmethod
    def _numeric_percentage_of():
        """Percentage of a group: how many satisfy a condition?"""
        name = _pick_name()
        total_students = random.choice([20, 25, 30, 40, 50, 60])
        perc = random.choice([10, 20, 25, 30, 40, 50, 60, 75, 80])
        count = int(total_students * perc / 100)
        while count != total_students * perc / 100:
            total_students = random.choice([20, 25, 30, 40, 50, 60])
            perc = random.choice([10, 20, 25, 30, 40, 50, 60, 75, 80])
            count = int(total_students * perc / 100)
        activity = random.choice(["pratica sport", "studia musica", "parla inglese", "usa i mezzi pubblici"])
        question = (
            f"In una classe di {total_students} studenti, il {perc}% {activity}. "
            f"Quanti studenti {activity}?"
        )
        correct = count
        distractors = WordModeler._numeric_distractors(
            correct, [-count if count > 2 else -2, perc - count, total_students - count, 3]
        )
        explanation = (
            f"Il {perc}% di {total_students} = {total_students} * {perc}/100 = {count} studenti."
        )
        tip = "Per calcolare il p% di N: moltiplica N * p / 100."
        return question, str(correct), distractors, explanation, tip

    # ---- Level 2 numeric templates ----

    @staticmethod
    def _numeric_average_add():
        """Average changes when a new number is added."""
        n = random.randint(4, 8)
        mean_old = random.randint(8, 20)
        total_old = n * mean_old
        new_value = random.randint(mean_old + 2, mean_old + 20)
        total_new = total_old + new_value
        new_mean = total_new // (n + 1)
        # ensure integer mean
        while total_new % (n + 1) != 0:
            new_value += 1
            total_new = total_old + new_value
        new_mean = total_new // (n + 1)
        question = (
            f"La media di {n} numeri e {mean_old}. "
            f"Se aggiungiamo il numero {new_value}, qual e la nuova media?"
        )
        correct = new_mean
        distractors = WordModeler._numeric_distractors(
            correct, [mean_old - correct, -1, 1, new_value - correct]
        )
        explanation = (
            f"La somma dei {n} numeri e {n} * {mean_old} = {total_old}. "
            f"Aggiungendo {new_value}, la nuova somma e {total_new}. "
            f"La nuova media e {total_new} / {n + 1} = {new_mean}."
        )
        tip = "Media = somma / conteggio. Quando aggiungi un valore, aggiorna sia la somma che il conteggio."
        return question, str(correct), distractors, explanation, tip

    @staticmethod
    def _numeric_work_rate():
        """Two pipes/workers together: how long to complete?"""
        name_a, name_b = _pick_two_names()
        # pick hours so that combined time is integer
        # 1/a + 1/b = 1/t  =>  t = ab/(a+b)
        a = random.randint(2, 10)
        b = random.randint(2, 10)
        while (a * b) % (a + b) != 0 or a == b:
            a = random.randint(2, 10)
            b = random.randint(2, 10)
        t = (a * b) // (a + b)
        question = (
            f"Un rubinetto riempie una vasca in {a} ore, un altro in {b} ore. "
            f"Se entrambi sono aperti, in quante ore riempiono la vasca insieme?"
        )
        correct = t
        distractors = WordModeler._numeric_distractors(
            correct, [a - correct, b - correct, (a + b) - correct, -1 if correct > 1 else 1]
        )
        explanation = (
            f"Il primo rubinetto fa 1/{a} della vasca all'ora, il secondo 1/{b}. "
            f"Insieme: 1/{a} + 1/{b} = ({a} + {b})/({a} * {b}) = {a + b}/{a * b}. "
            f"Tempo = {a * b}/{a + b} = {t} ore."
        )
        tip = "Lavoro congiunto: 1/t = 1/a + 1/b, quindi t = (a*b)/(a+b)."
        return question, str(correct), distractors, explanation, tip

    @staticmethod
    def _numeric_profit():
        """Buy at cost, sell at markup: what is the profit?"""
        name = _pick_name()
        cost = random.choice([50, 80, 100, 120, 150, 200])
        markup_perc = random.choice([10, 20, 25, 30, 40, 50])
        markup = int(cost * markup_perc / 100)
        while markup != cost * markup_perc / 100:
            cost = random.choice([50, 80, 100, 120, 150, 200])
            markup_perc = random.choice([10, 20, 25, 30, 40, 50])
            markup = int(cost * markup_perc / 100)
        sell = cost + markup
        question = (
            f"{name} compra un prodotto a {cost} euro e lo rivende "
            f"con un ricarico del {markup_perc}%. "
            f"Qual e il guadagno in euro?"
        )
        correct = markup
        distractors = WordModeler._numeric_distractors(
            correct, [sell - correct, cost - correct, markup_perc - correct, -5]
        )
        explanation = (
            f"Il ricarico e {cost} * {markup_perc}/100 = {markup} euro. "
            f"Il prezzo di vendita e {cost} + {markup} = {sell} euro, "
            f"ma il guadagno e solo {markup} euro."
        )
        tip = "Guadagno = prezzo_vendita - costo_acquisto = costo * ricarico/100."
        return question, str(correct), distractors, explanation, tip

    # ---- Level 3 numeric templates ----

    @staticmethod
    def _numeric_system_ages():
        """System of ages: A + B = total, A is N more than twice B. Find A."""
        name_a, name_b = _pick_two_names()
        # a = 2*b + diff, a + b = total  =>  3*b + diff = total  =>  b = (total - diff)/3
        diff = random.choice([1, 2, 3, 4, 5])
        b_age = random.randint(5, 20)
        a_age = 2 * b_age + diff
        total = a_age + b_age
        question = (
            f"La somma delle eta di {name_a} e {name_b} e {total} anni. "
            f"{name_a} ha {diff} anni piu del doppio dell'eta di {name_b}. "
            f"Quanti anni ha {name_a}?"
        )
        correct = a_age
        distractors = WordModeler._numeric_distractors(
            correct, [b_age - correct, -diff, diff, total - correct]
        )
        explanation = (
            f"Sia x l'eta di {name_b}. Allora {name_a} ha 2x + {diff} anni. "
            f"Dalla somma: x + 2x + {diff} = {total}, 3x = {total - diff}, x = {b_age}. "
            f"Quindi {name_a} ha 2 * {b_age} + {diff} = {a_age} anni."
        )
        tip = "Con 'il doppio piu N': A = 2B + N. Sostituisci nel vincolo della somma per trovare B."
        return question, str(correct), distractors, explanation, tip

    @staticmethod
    def _numeric_combined_distance():
        """Two travelers meet: how many km did each travel?"""
        name_a, name_b = _pick_two_names()
        v_a = random.choice([40, 50, 60, 80])
        v_b = random.choice([50, 60, 70, 90, 100])
        while v_b == v_a:
            v_b = random.choice([50, 60, 70, 90, 100])
        # t must be integer: dist = (v_a + v_b) * t
        t = random.randint(1, 5)
        dist = (v_a + v_b) * t
        d_a = v_a * t
        question = (
            f"{name_a} parte dalla citta A a {v_a} km/h e {name_b} parte dalla citta B a {v_b} km/h. "
            f"Le due citta distano {dist} km e si muovono uno verso l'altro. "
            f"Quanti chilometri percorre {name_a} prima di incontrarsi?"
        )
        correct = d_a
        d_b = v_b * t
        distractors = WordModeler._numeric_distractors(
            correct, [d_b - correct, dist - correct, t - correct, -v_a if v_a != correct else 10]
        )
        explanation = (
            f"Si incontrano dopo t ore: ({v_a} + {v_b}) * t = {dist}, "
            f"t = {dist} / {v_a + v_b} = {t} ore. "
            f"{name_a} percorre {v_a} * {t} = {d_a} km."
        )
        tip = "Quando due si avvicinano: tempo = distanza / (v1 + v2). Poi distanza_singolo = velocita * tempo."
        return question, str(correct), distractors, explanation, tip

    # ---- New numeric templates (exam-style) ----

    @staticmethod
    def _numeric_bus_cost():
        """Bus/vehicle rental cost split among group, requires rounding up."""
        n_people = random.choice([23, 27, 31, 37, 43, 47, 53])
        bus_capacity = random.choice([20, 25, 30, 40, 50])
        bus_cost = random.choice([200, 250, 300, 350, 400, 450, 500])

        n_buses = math.ceil(n_people / bus_capacity)
        total_cost = n_buses * bus_cost

        question = (
            f"Un gruppo di {n_people} persone deve noleggiare dei pullman da {bus_capacity} posti "
            f"al costo di {bus_cost}\u20ac ciascuno. "
            f"Quanti pullman servono e quanto spende in totale il gruppo?"
        )
        correct = total_cost
        distractors_raw = [
            (n_buses - 1) * bus_cost if n_buses > 1 else bus_cost + 50,
            n_people * bus_cost // max(bus_capacity, 1),
            (n_buses + 1) * bus_cost,
            n_people * bus_cost,
        ]
        offsets = [d - correct for d in distractors_raw if d != correct and d > 0][:4]
        distractors = WordModeler._numeric_distractors(correct, offsets if len(offsets) >= 4 else None)

        explanation = (
            f"Servono {n_people}/{bus_capacity} = {n_people / bus_capacity:.1f} pullman, "
            f"quindi bisogna arrotondare per eccesso: {n_buses} pullman. "
            f"Costo totale: {n_buses} \u00d7 {bus_cost} = {total_cost}\u20ac."
        )
        tip = "Quando dividi persone in gruppi, arrotonda sempre per eccesso: non puoi lasciare nessuno a piedi!"
        return question, str(correct), distractors, explanation, tip

    @staticmethod
    def _numeric_fraction_redistribution():
        """Fraction of items given away, then fraction of remainder."""
        name_a, name_b = _pick_two_names()
        max_attempts = 200
        for _ in range(max_attempts):
            total = random.choice([24, 30, 36, 40, 48, 60])
            frac_num1, frac_den1 = random.choice([(1, 3), (1, 4), (2, 5), (1, 6), (3, 4)])
            if (total * frac_num1) % frac_den1 != 0:
                continue
            given_away = total * frac_num1 // frac_den1
            remainder = total - given_away
            frac_num2, frac_den2 = random.choice([(1, 2), (1, 3), (2, 3), (1, 4), (3, 4)])
            if (remainder * frac_num2) % frac_den2 != 0:
                continue
            kept_by_a = remainder * frac_num2 // frac_den2
            final_remainder = remainder - kept_by_a
            if final_remainder > 0:
                break
        else:
            # Fallback to guaranteed clean values
            total, frac_num1, frac_den1 = 24, 1, 3
            given_away = 8
            remainder = 16
            frac_num2, frac_den2 = 1, 2
            kept_by_a = 8
            final_remainder = 8

        question = (
            f"{name_a} ha {total} cioccolatini. Ne regala {frac_num1}/{frac_den1} a {name_b}. "
            f"Di quelli rimasti, {name_a} ne mangia {frac_num2}/{frac_den2}. "
            f"Quanti cioccolatini restano?"
        )
        correct = final_remainder
        offsets = [
            given_away - correct,
            kept_by_a - correct,
            remainder - correct,
            total - correct - 1,
        ]
        distractors = WordModeler._numeric_distractors(correct, offsets)
        explanation = (
            f"{name_a} regala {frac_num1}/{frac_den1} di {total} = {given_away} cioccolatini. "
            f"Ne restano {total} - {given_away} = {remainder}. "
            f"Poi mangia {frac_num2}/{frac_den2} di {remainder} = {kept_by_a}. "
            f"Restano {remainder} - {kept_by_a} = {final_remainder} cioccolatini."
        )
        tip = "Nei problemi con frazioni successive, calcola ogni passaggio separatamente sul resto aggiornato."
        return question, str(correct), distractors, explanation, tip

    @staticmethod
    def _numeric_percentage_multistep():
        """X% of candidates passed. Y passed. How many total candidates?"""
        perc_pass = random.choice([60, 65, 70, 75, 80, 85])
        max_attempts = 200
        for _ in range(max_attempts):
            n_passed = random.randint(12, 50)
            total_candidate = n_passed * 100 / perc_pass
            if total_candidate == int(total_candidate) and total_candidate > n_passed:
                total = int(total_candidate)
                break
        else:
            # Fallback
            perc_pass, n_passed, total = 80, 40, 50

        n_failed = total - n_passed
        question = (
            f"All'esame di guida, il {perc_pass}% dei candidati ha superato la prova. "
            f"Sapendo che {n_passed} persone hanno superato l'esame, "
            f"quante persone in totale hanno sostenuto la prova?"
        )
        correct = total
        offsets = [n_failed - correct, -n_passed, n_passed, -(total // 2)]
        distractors = WordModeler._numeric_distractors(correct, offsets)
        explanation = (
            f"Se il {perc_pass}% corrisponde a {n_passed} persone, "
            f"il totale \u00e8 {n_passed} \u00d7 100 / {perc_pass} = {total} persone."
        )
        tip = "Per trovare il totale da una percentuale: totale = parte \u00d7 100 / percentuale."
        return question, str(correct), distractors, explanation, tip

    @staticmethod
    def _numeric_exam_scores():
        """Student average problem: find number of exams from old and new average."""
        name = _pick_name()
        max_attempts = 300
        for _ in range(max_attempts):
            old_avg = random.choice([22, 23, 24, 25, 26])
            new_score = random.choice([28, 29, 30])
            n_exams = random.randint(4, 10)
            total_old = old_avg * n_exams
            new_avg_num = total_old + new_score
            new_avg_den = n_exams + 1
            if new_avg_num % new_avg_den == 0:
                new_avg = new_avg_num // new_avg_den
                if new_avg > old_avg:
                    break
        else:
            # Fallback: old_avg=24, new_score=30, n=5 => total_old=120, new=150/6=25
            old_avg, new_score, n_exams, new_avg = 24, 30, 5, 25

        question = (
            f"{name} ha una media di {old_avg} punti su un certo numero di esami. "
            f"Dopo aver preso {new_score} all'ultimo esame, la media sale a {new_avg}. "
            f"Quanti esami aveva sostenuto prima dell'ultimo?"
        )
        correct = n_exams
        distractors = WordModeler._numeric_distractors(correct, [-2, -1, 1, 2])
        explanation = (
            f"Se la media era {old_avg} su n esami, il totale era {old_avg}n. "
            f"Dopo l'esame: ({old_avg}n + {new_score}) / (n + 1) = {new_avg}. "
            f"Risolvendo: {old_avg}n + {new_score} = {new_avg}n + {new_avg}, "
            f"quindi n({new_avg} - {old_avg}) = {new_score} - {new_avg}, "
            f"n = {new_score - new_avg} / {new_avg - old_avg} = {n_exams}."
        )
        tip = "Media = somma / numero. Se conosci la nuova media e il nuovo voto, imposta l'equazione e risolvi per n."
        return question, str(correct), distractors, explanation, tip

    @staticmethod
    def _numeric_successive_operations():
        """Multi-step: price increase then coupon then tax."""
        original = random.choice([80, 100, 120, 150, 200])
        increase_pct = random.choice([10, 15, 20, 25])
        coupon = random.choice([5, 10, 15, 20])
        tax_pct = random.choice([4, 10, 22])

        after_increase = original * (100 + increase_pct) / 100
        after_coupon = after_increase - coupon
        final = after_coupon * (100 + tax_pct) / 100
        final_rounded = round(final)

        question = (
            f"Un prodotto costa {original}\u20ac. Il prezzo aumenta del {increase_pct}%, "
            f"poi viene applicato un buono sconto di {coupon}\u20ac, "
            f"e infine si aggiunge l'IVA al {tax_pct}%. "
            f"Qual \u00e8 il prezzo finale (arrotondato all'euro)?"
        )
        correct = final_rounded

        wrong1 = round(original * (100 + increase_pct - tax_pct) / 100 - coupon)
        wrong2 = round((original - coupon) * (100 + increase_pct + tax_pct) / 100)
        wrong3 = round(original * (100 + increase_pct) / 100 * (100 + tax_pct) / 100)
        wrong4 = final_rounded + random.choice([-3, -2, 2, 3])

        offsets = [d - correct for d in [wrong1, wrong2, wrong3, wrong4] if d != correct][:4]
        distractors = WordModeler._numeric_distractors(correct, offsets if len(offsets) >= 4 else None)

        explanation = (
            f"Aumento {increase_pct}%: {original} \u00d7 {1 + increase_pct / 100} = {after_increase:.2f}\u20ac. "
            f"Buono: {after_increase:.2f} - {coupon} = {after_coupon:.2f}\u20ac. "
            f"IVA {tax_pct}%: {after_coupon:.2f} \u00d7 {1 + tax_pct / 100} = {final:.2f}\u20ac \u2248 {final_rounded}\u20ac."
        )
        tip = "Nelle operazioni successive, applica ogni passaggio al risultato precedente, non al prezzo originale!"
        return question, str(correct), distractors, explanation, tip

    # ================================================================
    #  Template registry by difficulty
    # ================================================================

    def _get_equation_templates(self, difficulty):
        level_1 = [
            self._tank_fill,
            self._discount_price,
            self._age_problem_simple,
            self._speed_distance_simple,
            self._percentage_increase,
            self._rectangle_perimeter,
            self._consecutive_numbers,
            self._supermarket_shopping,
            self._phone_plan,
            self._cooking_recipe,
        ]
        level_2 = [
            self._two_workers,
            self._mixture,
            self._two_prices,
            self._age_problem_double,
            self._speed_encounter,
            self._train_tickets,
            self._sports_training,
            self._electricity_bill,
        ]
        level_3 = [
            self._system_ages,
            self._tank_two_pipes,
            self._investment_system,
            self._geometry_triangle_system,
            self._work_rate_system,
            self._travel_planning,
            self._shared_apartment,
        ]
        if difficulty == 1:
            return level_1
        elif difficulty == 2:
            return level_2
        else:
            return level_3

    def _get_numeric_templates(self, difficulty):
        level_1 = [
            self._numeric_age_sum,
            self._numeric_discount,
            self._numeric_percentage_of,
            self._numeric_bus_cost,
            self._numeric_fraction_redistribution,
        ]
        level_2 = [
            self._numeric_average_add,
            self._numeric_work_rate,
            self._numeric_profit,
            self._numeric_percentage_multistep,
            self._numeric_exam_scores,
        ]
        level_3 = [
            self._numeric_system_ages,
            self._numeric_combined_distance,
            self._numeric_successive_operations,
        ]
        if difficulty == 1:
            return level_1
        elif difficulty == 2:
            return level_2
        else:
            return level_3

    def _get_templates(self, difficulty):
        return self._get_equation_templates(difficulty) + self._get_numeric_templates(difficulty)

    def generate(self, difficulty: int, exam_mode: bool = False) -> dict:
        difficulty = max(1, min(3, difficulty))
        if exam_mode and random.random() < 0.6:
            templates = self._get_numeric_templates(difficulty)
        else:
            templates = self._get_templates(difficulty)
        template_fn = random.choice(templates)
        question, correct_eq, distractors, explanation, tip = template_fn()
        return self._build_result(question, correct_eq, distractors, explanation, tip, difficulty)
