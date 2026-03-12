import random
import math

from exercises.base import Exercise


class TrapCalculator(Exercise):
    """Trova la Trappola: find the wrong step in a calculation."""

    def generate(self, difficulty: int) -> dict:
        difficulty = max(1, min(3, difficulty))

        templates = [
            self._trap_sqrt_square,
            self._trap_operator_precedence,
            self._trap_negative_exponent,
            self._trap_compound_percentage,
            self._trap_notable_product_sum_sq,
            self._trap_notable_product_diff_sq,
            self._trap_notable_product_diff_of_sq,
            self._trap_fraction_sign,
            self._trap_log_sum,
            self._trap_log_power,
            self._trap_division_by_negative,
            self._trap_exponent_of_product,
            self._trap_sqrt_of_sum,
            self._trap_fraction_addition,
            self._trap_percentage_increase_decrease,
            self._trap_negative_square,
            self._trap_log_subtraction,
            self._trap_power_of_power,
            self._trap_distribute_exponent_over_sum,
        ]

        template_fn = random.choice(templates)
        return template_fn(difficulty)

    # ------------------------------------------------------------------ helpers
    @staticmethod
    def _fmt(val: float) -> str:
        """Format a number nicely: integers without decimals, floats with up to 4 decimals."""
        if val == int(val):
            return str(int(val))
        return f"{val:.4g}"

    @staticmethod
    def _build_result(
        steps: list[str],
        correct_index: int,
        explanation: str,
        did_you_know: str,
    ) -> dict:
        return {
            "question": "Trova il passaggio sbagliato nel calcolo seguente:",
            "steps": steps,
            "correct_index": correct_index,
            "explanation": explanation,
            "did_you_know": did_you_know,
        }

    # ======================================================================
    #  TEMPLATE 1 : sqrt(a^2) = |a|, not a
    # ======================================================================
    def _trap_sqrt_square(self, difficulty: int) -> dict:
        a = random.choice([-7, -5, -4, -3, -2])
        a_sq = a * a

        if difficulty == 1:
            steps = [
                f"Calcola: sqrt(({a})^2)",
                f"({a})^2 = {a_sq}",
                f"sqrt({a_sq}) = {a}",
            ]
            wrong_idx = 2
        elif difficulty == 2:
            b = random.randint(1, 5)
            steps = [
                f"Semplifica: sqrt(({a})^2) + {b}",
                f"({a})^2 = {a_sq}",
                f"sqrt({a_sq}) = {a}",
                f"Risultato: {a} + {b} = {a + b}",
            ]
            wrong_idx = 2
        else:
            b = random.randint(2, 6)
            c = random.randint(1, 4)
            steps = [
                f"Semplifica: sqrt(({a})^2) * {b} + {c}",
                f"({a})^2 = {a_sq}",
                f"sqrt({a_sq}) = {a}",
                f"{a} * {b} = {a * b}",
                f"Risultato: {a * b} + {c} = {a * b + c}",
            ]
            wrong_idx = 2

        return self._build_result(
            steps=steps,
            correct_index=wrong_idx,
            explanation=(
                f"Errore: sqrt(({a})^2) = |{a}| = {abs(a)}, non {a}. "
                f"La radice quadrata restituisce sempre un valore non negativo."
            ),
            did_you_know=(
                "Ricorda: sqrt(x^2) = |x| per ogni x reale. "
                "La radice quadrata principale e' sempre >= 0."
            ),
        )

    # ======================================================================
    #  TEMPLATE 2 : operator precedence (moltiplicazione prima dell'addizione)
    # ======================================================================
    def _trap_operator_precedence(self, difficulty: int) -> dict:
        a = random.randint(2, 9)
        b = random.randint(2, 9)
        c = random.randint(2, 9)

        if difficulty == 1:
            wrong_val = (a + b) * c
            right_val = a + b * c
            steps = [
                f"Calcola: {a} + {b} * {c}",
                f"= ({a} + {b}) * {c}",
                f"= {a + b} * {c} = {wrong_val}",
            ]
            wrong_idx = 1
        elif difficulty == 2:
            d = random.randint(1, 5)
            wrong_val = (a + b) * c - d
            steps = [
                f"Calcola: {a} + {b} * {c} - {d}",
                f"= ({a} + {b}) * {c} - {d}",
                f"= {a + b} * {c} - {d}",
                f"= {wrong_val}",
            ]
            wrong_idx = 1
        else:
            d = random.randint(2, 5)
            e = random.randint(1, 4)
            steps = [
                f"Calcola: {a} + {b} * {c} - {d} + {e}",
                f"Prima le moltiplicazioni: {b} * {c} = {b * c}",
                f"Poi: ({a} + {b * c}) * 1 - {d} + {e}",
                f"= ({a + b * c}) - {d} + {e}",
                f"= {(a + b * c) - d + e}",
            ]
            # Step 2 sneaks in a wrong grouping multiplication by 1 but conceptually
            # rewrite for clarity:
            wrong_intermediate = (a + b) * c
            steps = [
                f"Calcola: {a} + {b} * {c}^2 - {d}",
                f"{c}^2 = {c * c}",
                f"({a} + {b}) * {c * c} = {(a + b) * c * c}",
                f"Risultato: {(a + b) * c * c} - {d} = {(a + b) * c * c - d}",
            ]
            wrong_idx = 2

        return self._build_result(
            steps=steps,
            correct_index=wrong_idx,
            explanation=(
                "Errore: la moltiplicazione ha precedenza sull'addizione. "
                f"Si deve prima calcolare {b} * {c} e poi sommare {a}, "
                "non sommare prima {a} + {b}."
            ),
            did_you_know=(
                "Le operazioni seguono l'ordine PEMDAS: Parentesi, Esponenti, "
                "Moltiplicazione/Divisione (da sinistra a destra), "
                "Addizione/Sottrazione (da sinistra a destra)."
            ),
        )

    # ======================================================================
    #  TEMPLATE 3 : segno negativo con esponenti: (-a)^2 vs -(a^2)
    # ======================================================================
    def _trap_negative_exponent(self, difficulty: int) -> dict:
        a = random.randint(2, 7)
        a_sq = a * a

        if difficulty == 1:
            steps = [
                f"Calcola: -{a}^2",
                f"= (-{a}) * (-{a})",
                f"= {a_sq}",
            ]
            wrong_idx = 1
        elif difficulty == 2:
            b = random.randint(1, 5)
            steps = [
                f"Calcola: -{a}^2 + {b}",
                f"-(({a})^2) = -({a_sq})",
                f"Ma scriviamo: -{a}^2 = (-{a})^2 = {a_sq}",
                f"Risultato: {a_sq} + {b} = {a_sq + b}",
            ]
            wrong_idx = 2
        else:
            b = random.randint(2, 5)
            c = random.randint(1, 4)
            steps = [
                f"Semplifica: -{a}^2 + {b} * {c}",
                f"-{a}^2 = (-{a})^2 = {a_sq}",
                f"{b} * {c} = {b * c}",
                f"Risultato: {a_sq} + {b * c} = {a_sq + b * c}",
            ]
            wrong_idx = 1

        return self._build_result(
            steps=steps,
            correct_index=wrong_idx,
            explanation=(
                f"Errore: -{a}^2 significa -(({a})^2) = -{a_sq}, NON (-{a})^2 = {a_sq}. "
                "Il segno meno non e' dentro la base dell'esponente se non ci sono parentesi."
            ),
            did_you_know=(
                "Attenzione alla differenza: (-a)^2 = a^2 (positivo), "
                "ma -a^2 = -(a^2) (negativo). Le parentesi cambiano tutto!"
            ),
        )

    # ======================================================================
    #  TEMPLATE 4 : percentuali composte (aumento e diminuzione non si annullano)
    # ======================================================================
    def _trap_compound_percentage(self, difficulty: int) -> dict:
        p = random.choice([10, 15, 20, 25, 30])
        val = random.choice([100, 200, 500, 1000])

        after_increase = val * (1 + p / 100)
        after_decrease = after_increase * (1 - p / 100)
        actual_loss = val - after_decrease

        if difficulty == 1:
            steps = [
                f"Un prezzo di {val} euro aumenta del {p}% e poi diminuisce del {p}%.",
                f"Aumento: {val} + {p}% = {self._fmt(after_increase)}",
                f"Diminuzione: il prezzo torna a {val} euro",
            ]
            wrong_idx = 2
        elif difficulty == 2:
            steps = [
                f"Un prezzo di {val} euro aumenta del {p}% e poi diminuisce del {p}%.",
                f"Aumento del {p}%: {val} * {self._fmt(1 + p / 100)} = {self._fmt(after_increase)}",
                f"Diminuzione del {p}%: si toglie lo stesso importo aggiunto",
                f"Prezzo finale: {val} euro (invariato)",
            ]
            wrong_idx = 2
        else:
            p2 = random.choice([5, 10, 15])
            after_inc2 = after_decrease * (1 + p2 / 100)
            steps = [
                f"Un prezzo di {val} euro aumenta del {p}%, poi cala del {p}%, poi cresce del {p2}%.",
                f"Dopo +{p}%: {val} * {self._fmt(1 + p / 100)} = {self._fmt(after_increase)}",
                f"Dopo -{p}%: torna a {val} (perche' +{p}% e -{p}% si annullano)",
                f"Dopo +{p2}%: {val} * {self._fmt(1 + p2 / 100)} = {self._fmt(val * (1 + p2 / 100))}",
            ]
            wrong_idx = 2

        return self._build_result(
            steps=steps,
            correct_index=wrong_idx,
            explanation=(
                f"Errore: +{p}% e poi -{p}% NON si annullano! "
                f"Dopo +{p}%: {self._fmt(after_increase)}. "
                f"Dopo -{p}% di {self._fmt(after_increase)}: {self._fmt(after_decrease)}. "
                f"Si perde {self._fmt(actual_loss)} euro."
            ),
            did_you_know=(
                "Le percentuali sono moltiplicative, non additive. "
                f"+{p}% e poi -{p}% danno un fattore di "
                f"{self._fmt((1 + p / 100) * (1 - p / 100))}, cioe' una piccola perdita netta."
            ),
        )

    # ======================================================================
    #  TEMPLATE 5 : prodotto notevole (a+b)^2 = a^2+2ab+b^2 (non a^2+b^2)
    # ======================================================================
    def _trap_notable_product_sum_sq(self, difficulty: int) -> dict:
        a = random.randint(2, 6)
        b = random.randint(1, 5)

        if difficulty == 1:
            steps = [
                f"Espandi: ({a} + {b})^2",
                f"= {a}^2 + {b}^2",
                f"= {a * a} + {b * b} = {a * a + b * b}",
            ]
            wrong_idx = 1
        elif difficulty == 2:
            steps = [
                f"Espandi: (x + {b})^2",
                f"= x^2 + {b}^2",
                f"= x^2 + {b * b}",
            ]
            wrong_idx = 1
        else:
            c = random.randint(1, 3)
            steps = [
                f"Espandi: ({a}x + {b})^2 - {c}",
                f"({a}x + {b})^2 = ({a}x)^2 + {b}^2",
                f"= {a * a}x^2 + {b * b}",
                f"Risultato: {a * a}x^2 + {b * b} - {c} = {a * a}x^2 + {b * b - c}",
            ]
            wrong_idx = 1

        return self._build_result(
            steps=steps,
            correct_index=wrong_idx,
            explanation=(
                f"Errore: (a + b)^2 = a^2 + 2ab + b^2, NON a^2 + b^2. "
                f"Manca il doppio prodotto 2 * {a} * {b} = {2 * a * b}."
            ),
            did_you_know=(
                "Il quadrato di un binomio (a+b)^2 ha SEMPRE tre termini: "
                "a^2 + 2ab + b^2. Non dimenticare mai il doppio prodotto 2ab!"
            ),
        )

    # ======================================================================
    #  TEMPLATE 6 : prodotto notevole (a-b)^2 = a^2-2ab+b^2 (non a^2-b^2)
    # ======================================================================
    def _trap_notable_product_diff_sq(self, difficulty: int) -> dict:
        a = random.randint(3, 8)
        b = random.randint(1, a - 1)

        if difficulty == 1:
            steps = [
                f"Espandi: ({a} - {b})^2",
                f"= {a}^2 - {b}^2",
                f"= {a * a} - {b * b} = {a * a - b * b}",
            ]
            wrong_idx = 1
        elif difficulty == 2:
            steps = [
                f"Espandi: (x - {b})^2",
                f"= x^2 - 2 * x * {b} + {b}^2",
                f"= x^2 - {2 * b}x - {b * b}",
            ]
            wrong_idx = 2
        else:
            c = random.randint(2, 5)
            steps = [
                f"Espandi: ({a}x - {b})^2 + {c}x",
                f"({a}x)^2 = {a * a}x^2",
                f"({a}x - {b})^2 = {a * a}x^2 - {b * b}",
                f"Risultato: {a * a}x^2 - {b * b} + {c}x",
            ]
            wrong_idx = 2

        return self._build_result(
            steps=steps,
            correct_index=wrong_idx,
            explanation=(
                f"Errore: (a - b)^2 = a^2 - 2ab + b^2, NON a^2 - b^2. "
                f"Manca il termine -2ab e il segno di b^2 deve essere positivo."
            ),
            did_you_know=(
                "Attenzione: (a-b)^2 NON e' uguale a a^2 - b^2. "
                "a^2 - b^2 e' la differenza di quadrati: (a+b)(a-b)."
            ),
        )

    # ======================================================================
    #  TEMPLATE 7 : differenza di quadrati a^2-b^2 = (a+b)(a-b)
    # ======================================================================
    def _trap_notable_product_diff_of_sq(self, difficulty: int) -> dict:
        a = random.randint(3, 9)
        b = random.randint(1, a - 1)

        if difficulty == 1:
            steps = [
                f"Fattorizza: {a * a} - {b * b}",
                f"= ({a} - {b})^2",
                f"= {(a - b) ** 2}",
            ]
            wrong_idx = 1
        elif difficulty == 2:
            steps = [
                f"Fattorizza: x^2 - {b * b}",
                f"= (x - {b})^2",
                f"= x^2 - {2 * b}x + {b * b}",
            ]
            wrong_idx = 1
        else:
            c = random.randint(2, 4)
            steps = [
                f"Fattorizza: {c}x^2 - {c * b * b}",
                f"= {c}(x^2 - {b * b})",
                f"= {c}(x - {b})^2",
                f"= {c}(x^2 - {2 * b}x + {b * b})",
            ]
            wrong_idx = 2

        return self._build_result(
            steps=steps,
            correct_index=wrong_idx,
            explanation=(
                f"Errore: a^2 - b^2 = (a + b)(a - b), NON (a - b)^2. "
                "La differenza di quadrati si fattorizza come prodotto di somma per differenza."
            ),
            did_you_know=(
                "Prodotti notevoli da ricordare: "
                "a^2 - b^2 = (a+b)(a-b), "
                "(a+b)^2 = a^2 + 2ab + b^2, "
                "(a-b)^2 = a^2 - 2ab + b^2."
            ),
        )

    # ======================================================================
    #  TEMPLATE 8 : errore di segno nelle frazioni
    # ======================================================================
    def _trap_fraction_sign(self, difficulty: int) -> dict:
        a = random.randint(2, 8)
        b = random.randint(2, 8)
        c = random.randint(2, 6)

        if difficulty == 1:
            steps = [
                f"Semplifica: -({a}/{b})",
                f"= {a}/(-{b})",
                f"= {a}/{b}",
            ]
            wrong_idx = 2
        elif difficulty == 2:
            steps = [
                f"Calcola: (-{a})/(-{b}) + {c}",
                f"(-{a})/(-{b}) = -({a}/{b})",
                f"= -{self._fmt(a / b)} + {c}",
                f"= {self._fmt(-a / b + c)}",
            ]
            wrong_idx = 1
        else:
            d = random.randint(1, 5)
            steps = [
                f"Semplifica: (-{a})/(-{b}) - (-{c})/({d})",
                f"(-{a})/(-{b}) = -({a}/{b})",
                f"-(-{c})/({d}) = -{c}/{d}",
                f"= -{self._fmt(a / b)} - {self._fmt(c / d)}",
                f"= {self._fmt(-a / b - c / d)}",
            ]
            wrong_idx = 1

        return self._build_result(
            steps=steps,
            correct_index=wrong_idx,
            explanation=(
                "Errore di segno nella frazione: (-a)/(-b) = a/b (positivo), "
                "non -(a/b). Meno diviso meno fa piu'!"
            ),
            did_you_know=(
                "Regola dei segni per le frazioni: "
                "(-a)/(-b) = a/b, (-a)/b = -(a/b) = a/(-b). "
                "Il segno puo' stare al numeratore, al denominatore o davanti."
            ),
        )

    # ======================================================================
    #  TEMPLATE 9 : log(a) + log(b) = log(a*b), NON log(a+b)
    # ======================================================================
    def _trap_log_sum(self, difficulty: int) -> dict:
        a = random.randint(2, 9)
        b = random.randint(2, 9)

        if difficulty == 1:
            steps = [
                f"Semplifica: log({a}) + log({b})",
                f"= log({a} + {b})",
                f"= log({a + b})",
            ]
            wrong_idx = 1
        elif difficulty == 2:
            c = random.randint(2, 5)
            steps = [
                f"Semplifica: log({a}) + log({b}) - log({c})",
                f"log({a}) + log({b}) = log({a} + {b}) = log({a + b})",
                f"log({a + b}) - log({c}) = log({a + b}/{c})",
                f"= log({self._fmt((a + b) / c)})",
            ]
            wrong_idx = 1
        else:
            c = random.randint(2, 4)
            steps = [
                f"Semplifica: log({a}) + log({b}) + {c} * log({a})",
                f"log({a}) + log({b}) = log({a} + {b})",
                f"{c} * log({a}) = log({a}^{c}) = log({a ** c})",
                f"log({a + b}) + log({a ** c}) = log({(a + b) * a ** c})",
            ]
            wrong_idx = 1

        return self._build_result(
            steps=steps,
            correct_index=wrong_idx,
            explanation=(
                f"Errore: log(a) + log(b) = log(a * b), NON log(a + b). "
                f"Quindi log({a}) + log({b}) = log({a * b}), non log({a + b})."
            ),
            did_you_know=(
                "Proprieta' fondamentali dei logaritmi: "
                "log(a) + log(b) = log(a*b), "
                "log(a) - log(b) = log(a/b), "
                "n * log(a) = log(a^n)."
            ),
        )

    # ======================================================================
    #  TEMPLATE 10 : n*log(a) = log(a^n), NON log(n*a)
    # ======================================================================
    def _trap_log_power(self, difficulty: int) -> dict:
        a = random.randint(2, 5)
        n = random.randint(2, 4)

        if difficulty == 1:
            steps = [
                f"Semplifica: {n} * log({a})",
                f"= log({n} * {a})",
                f"= log({n * a})",
            ]
            wrong_idx = 1
        elif difficulty == 2:
            b = random.randint(2, 5)
            steps = [
                f"Semplifica: {n} * log({a}) + log({b})",
                f"{n} * log({a}) = log({n} * {a}) = log({n * a})",
                f"log({n * a}) + log({b}) = log({n * a} * {b})",
                f"= log({n * a * b})",
            ]
            wrong_idx = 1
        else:
            b = random.randint(2, 4)
            m = random.randint(2, 3)
            steps = [
                f"Semplifica: {n} * log({a}) - {m} * log({b})",
                f"{n} * log({a}) = log({n * a})",
                f"{m} * log({b}) = log({b}^{m}) = log({b ** m})",
                f"log({n * a}) - log({b ** m}) = log({n * a}/{b ** m})",
                f"= log({self._fmt(n * a / b ** m)})",
            ]
            wrong_idx = 1

        return self._build_result(
            steps=steps,
            correct_index=wrong_idx,
            explanation=(
                f"Errore: n * log(a) = log(a^n), NON log(n*a). "
                f"Quindi {n} * log({a}) = log({a}^{n}) = log({a ** n}), "
                f"non log({n * a})."
            ),
            did_you_know=(
                "Il coefficiente davanti al logaritmo diventa esponente dell'argomento: "
                "n * log(a) = log(a^n). Non confonderlo con log(n * a)!"
            ),
        )

    # ======================================================================
    #  TEMPLATE 11 : divisione per un numero negativo e cambio segno
    # ======================================================================
    def _trap_division_by_negative(self, difficulty: int) -> dict:
        a = random.randint(2, 10)
        b = random.randint(2, 6)
        c = random.randint(1, 8)

        if difficulty == 1:
            steps = [
                f"Risolvi: -{b}x > {c}",
                f"x > {c}/(-{b})",
                f"x > {self._fmt(-c / b)}",
            ]
            wrong_idx = 1
        elif difficulty == 2:
            steps = [
                f"Risolvi: {a} - {b}x > {c}",
                f"-{b}x > {c} - {a}",
                f"x > ({c} - {a})/(-{b})",
                f"x > {self._fmt((c - a) / (-b))}",
            ]
            wrong_idx = 2
        else:
            d = random.randint(1, 4)
            steps = [
                f"Risolvi: {a} - {b}x > {c} + {d}x",
                f"-{b}x - {d}x > {c} - {a}",
                f"-{b + d}x > {c - a}",
                f"x > {self._fmt((c - a) / (-(b + d)))}",
            ]
            wrong_idx = 3

        return self._build_result(
            steps=steps,
            correct_index=wrong_idx,
            explanation=(
                "Errore: quando si divide una disequazione per un numero negativo, "
                "il verso della disuguaglianza si INVERTE. "
                "Dividendo per un negativo, > diventa <."
            ),
            did_you_know=(
                "Regola fondamentale delle disequazioni: moltiplicando o dividendo "
                "entrambi i membri per un numero NEGATIVO, il verso si inverte: "
                "se a > b e c < 0, allora ac < bc."
            ),
        )

    # ======================================================================
    #  TEMPLATE 12 : (ab)^n = a^n * b^n, NON a * b^n
    # ======================================================================
    def _trap_exponent_of_product(self, difficulty: int) -> dict:
        a = random.randint(2, 5)
        b = random.randint(2, 5)
        n = random.randint(2, 3)

        if difficulty == 1:
            steps = [
                f"Calcola: ({a} * {b})^{n}",
                f"= {a} * {b}^{n}",
                f"= {a} * {b ** n} = {a * b ** n}",
            ]
            wrong_idx = 1
        elif difficulty == 2:
            c = random.randint(1, 5)
            steps = [
                f"Calcola: ({a} * {b})^{n} + {c}",
                f"({a} * {b})^{n} = {a} * {b}^{n}",
                f"= {a} * {b ** n} = {a * b ** n}",
                f"Risultato: {a * b ** n} + {c} = {a * b ** n + c}",
            ]
            wrong_idx = 1
        else:
            c = random.randint(2, 4)
            steps = [
                f"Semplifica: ({a} * {b})^{n} / {c}",
                f"({a} * {b})^{n} = {a}^{n} * {b}^{n}",
                f"Attenzione: {a}^{n} * {b}^{n} = {a} * {b}^{n} = {a * b ** n}",
                f"Risultato: {a * b ** n}/{c} = {self._fmt(a * b ** n / c)}",
            ]
            wrong_idx = 2

        return self._build_result(
            steps=steps,
            correct_index=wrong_idx,
            explanation=(
                f"Errore: (a*b)^n = a^n * b^n. L'esponente si applica a ENTRAMBI i fattori. "
                f"({a}*{b})^{n} = {a}^{n} * {b}^{n} = {a ** n} * {b ** n} = {(a * b) ** n}."
            ),
            did_you_know=(
                "La potenza di un prodotto e' il prodotto delle potenze: "
                "(a*b)^n = a^n * b^n. L'esponente si distribuisce su OGNI fattore."
            ),
        )

    # ======================================================================
    #  TEMPLATE 13 : sqrt(a+b) != sqrt(a) + sqrt(b)
    # ======================================================================
    def _trap_sqrt_of_sum(self, difficulty: int) -> dict:
        a = random.choice([4, 9, 16, 25, 36])
        b = random.choice([4, 9, 16, 25, 36])
        sqrt_a = int(math.isqrt(a))
        sqrt_b = int(math.isqrt(b))

        if difficulty == 1:
            steps = [
                f"Calcola: sqrt({a} + {b})",
                f"= sqrt({a}) + sqrt({b})",
                f"= {sqrt_a} + {sqrt_b} = {sqrt_a + sqrt_b}",
            ]
            wrong_idx = 1
        elif difficulty == 2:
            c = random.randint(1, 5)
            steps = [
                f"Semplifica: sqrt({a} + {b}) + {c}",
                f"sqrt({a} + {b}) = sqrt({a}) + sqrt({b})",
                f"= {sqrt_a} + {sqrt_b} = {sqrt_a + sqrt_b}",
                f"Risultato: {sqrt_a + sqrt_b} + {c} = {sqrt_a + sqrt_b + c}",
            ]
            wrong_idx = 1
        else:
            c = random.choice([4, 9, 16])
            sqrt_c = int(math.isqrt(c))
            steps = [
                f"Semplifica: sqrt({a} + {b}) - sqrt({c})",
                f"sqrt({a} + {b}) = sqrt({a}) + sqrt({b}) = {sqrt_a} + {sqrt_b}",
                f"sqrt({c}) = {sqrt_c}",
                f"Risultato: {sqrt_a} + {sqrt_b} - {sqrt_c} = {sqrt_a + sqrt_b - sqrt_c}",
            ]
            wrong_idx = 1

        return self._build_result(
            steps=steps,
            correct_index=wrong_idx,
            explanation=(
                f"Errore: sqrt(a + b) NON e' uguale a sqrt(a) + sqrt(b). "
                f"sqrt({a} + {b}) = sqrt({a + b}) = {self._fmt(math.sqrt(a + b))}, "
                f"mentre sqrt({a}) + sqrt({b}) = {sqrt_a} + {sqrt_b} = {sqrt_a + sqrt_b}."
            ),
            did_you_know=(
                "La radice quadrata NON si distribuisce sulla somma: "
                "sqrt(a + b) != sqrt(a) + sqrt(b). "
                "Funziona solo col prodotto: sqrt(a * b) = sqrt(a) * sqrt(b)."
            ),
        )

    # ======================================================================
    #  TEMPLATE 14 : somma di frazioni con denominatori diversi
    # ======================================================================
    def _trap_fraction_addition(self, difficulty: int) -> dict:
        a = random.randint(1, 5)
        b = random.randint(2, 6)
        c = random.randint(1, 5)
        d = random.randint(2, 6)
        # Ensure different denominators
        while d == b:
            d = random.randint(2, 6)

        if difficulty == 1:
            steps = [
                f"Calcola: {a}/{b} + {c}/{d}",
                f"= ({a} + {c}) / ({b} + {d})",
                f"= {a + c}/{b + d}",
            ]
            wrong_idx = 1
        elif difficulty == 2:
            steps = [
                f"Calcola: {a}/{b} + {c}/{d}",
                f"Sommiamo numeratori e denominatori: ({a}+{c})/({b}+{d})",
                f"= {a + c}/{b + d}",
                f"= {self._fmt((a + c) / (b + d))}",
            ]
            wrong_idx = 1
        else:
            e = random.randint(1, 4)
            f_val = random.randint(2, 5)
            steps = [
                f"Calcola: {a}/{b} + {c}/{d} - {e}/{f_val}",
                f"{a}/{b} + {c}/{d} = ({a}+{c})/({b}+{d}) = {a + c}/{b + d}",
                f"{a + c}/{b + d} - {e}/{f_val}",
                f"= ({(a + c) * f_val} - {e * (b + d)}) / {(b + d) * f_val}",
            ]
            wrong_idx = 1

        lcm_bd = (b * d) // math.gcd(b, d)
        correct_num = a * (lcm_bd // b) + c * (lcm_bd // d)
        return self._build_result(
            steps=steps,
            correct_index=wrong_idx,
            explanation=(
                f"Errore: per sommare frazioni con denominatori diversi, "
                f"si deve trovare il denominatore comune. "
                f"{a}/{b} + {c}/{d} = ({a * (lcm_bd // b)}+{c * (lcm_bd // d)})/{lcm_bd} "
                f"= {correct_num}/{lcm_bd}. "
                "NON si sommano i denominatori!"
            ),
            did_you_know=(
                "Per sommare frazioni: trovare il mcm dei denominatori, "
                "adattare i numeratori, poi sommare. "
                "Mai sommare direttamente i denominatori!"
            ),
        )

    # ======================================================================
    #  TEMPLATE 15 : aumento e diminuzione percentuali non sono simmetrici
    # ======================================================================
    def _trap_percentage_increase_decrease(self, difficulty: int) -> dict:
        p = random.choice([20, 25, 30, 40, 50])
        val = random.choice([100, 200, 400, 500, 800])
        decreased = val * (1 - p / 100)
        # To recover val from decreased, need to increase by p/(100-p)*100 %
        needed_pct = (p / (100 - p)) * 100

        if difficulty == 1:
            steps = [
                f"Un prezzo cala del {p}%: da {val} a {self._fmt(decreased)} euro.",
                f"Per tornare a {val}, basta aumentare del {p}%.",
                f"{self._fmt(decreased)} + {p}% = {val} euro.",
            ]
            wrong_idx = 1
        elif difficulty == 2:
            wrong_recovery = decreased * (1 + p / 100)
            steps = [
                f"Un valore scende del {p}%: da {val} a {self._fmt(decreased)}.",
                f"Aumento del {p}%: {self._fmt(decreased)} * {self._fmt(1 + p / 100)}",
                f"= {self._fmt(wrong_recovery)}",
                f"Conclusione: si torna al valore originale {val}.",
            ]
            wrong_idx = 3
        else:
            wrong_recovery = decreased * (1 + p / 100)
            steps = [
                f"Un investimento perde il {p}%. Da {val} scende a {self._fmt(decreased)}.",
                f"Per recuperare, calcoliamo +{p}% di {self._fmt(decreased)}.",
                f"{self._fmt(decreased)} * {self._fmt(p / 100)} = {self._fmt(decreased * p / 100)}",
                f"Nuovo valore: {self._fmt(decreased)} + {self._fmt(decreased * p / 100)} = {self._fmt(wrong_recovery)}",
                f"Recupero completo: si torna a {val}.",
            ]
            wrong_idx = 4

        return self._build_result(
            steps=steps,
            correct_index=wrong_idx,
            explanation=(
                f"Errore: dopo un calo del {p}%, per tornare al valore iniziale "
                f"serve un aumento del {self._fmt(needed_pct)}%, non del {p}%. "
                f"Infatti {self._fmt(decreased)} + {p}% = {self._fmt(decreased * (1 + p / 100))}, "
                f"che e' diverso da {val}."
            ),
            did_you_know=(
                f"Dopo un calo del {p}%, la base e' piu' piccola. "
                f"Serve un aumento percentuale maggiore per tornare al valore iniziale. "
                f"Formula: percentuale di recupero = {p}/(100-{p}) * 100 = {self._fmt(needed_pct)}%."
            ),
        )

    # ======================================================================
    #  TEMPLATE 16 : (-a)^2 vs -(a^2) con variabili
    # ======================================================================
    def _trap_negative_square(self, difficulty: int) -> dict:
        a = random.randint(2, 6)
        n = random.choice([2, 4])

        if difficulty == 1:
            steps = [
                f"Calcola: (-{a})^{n} e -{a}^{n}",
                f"(-{a})^{n} = -{a ** n}",
                f"I due risultati sono uguali.",
            ]
            wrong_idx = 1
        elif difficulty == 2:
            b = random.randint(1, 5)
            steps = [
                f"Calcola: (-{a})^{n} + {b}",
                f"(-{a})^{n} = -{a ** n}",
                f"Risultato: -{a ** n} + {b} = {-a ** n + b}",
            ]
            wrong_idx = 1
        else:
            b = random.randint(2, 5)
            odd_n = random.choice([3, 5])
            steps = [
                f"Confronta: (-{a})^{odd_n} e (-{a})^{n}",
                f"(-{a})^{odd_n} = {a ** odd_n}",
                f"(-{a})^{n} = {a ** n}",
                f"Somma: {a ** odd_n} + {a ** n} = {a ** odd_n + a ** n}",
            ]
            wrong_idx = 1

        return self._build_result(
            steps=steps,
            correct_index=wrong_idx,
            explanation=(
                f"Errore: (-{a})^{n} = {a ** n} (positivo, perche' l'esponente e' pari). "
                f"Un numero negativo elevato a potenza pari da' risultato positivo."
                if difficulty <= 2
                else (
                    f"Errore: (-{a})^{odd_n} = {(-a) ** odd_n} (negativo, esponente dispari), "
                    f"non {a ** odd_n}."
                )
            ),
            did_you_know=(
                "Regola dei segni con le potenze: "
                "(-a)^n e' positivo se n e' pari, negativo se n e' dispari. "
                "Questo perche' (-)*(-)=+ e si ripete."
            ),
        )

    # ======================================================================
    #  TEMPLATE 17 : log(a) - log(b) = log(a/b), NON log(a-b)
    # ======================================================================
    def _trap_log_subtraction(self, difficulty: int) -> dict:
        a = random.randint(10, 50)
        b = random.randint(2, 9)
        while a <= b:
            a = random.randint(10, 50)

        if difficulty == 1:
            steps = [
                f"Semplifica: log({a}) - log({b})",
                f"= log({a} - {b})",
                f"= log({a - b})",
            ]
            wrong_idx = 1
        elif difficulty == 2:
            c = random.randint(2, 5)
            steps = [
                f"Semplifica: log({a}) - log({b}) + log({c})",
                f"log({a}) - log({b}) = log({a} - {b}) = log({a - b})",
                f"log({a - b}) + log({c}) = log({(a - b) * c})",
            ]
            wrong_idx = 1
        else:
            c = random.randint(2, 4)
            d = random.randint(2, 5)
            steps = [
                f"Semplifica: {c} * log({a}) - log({b}^{d})",
                f"{c} * log({a}) = log({a}^{c}) = log({a ** c})",
                f"log({b}^{d}) = log({b ** d})",
                f"log({a ** c}) - log({b ** d}) = log({a ** c} - {b ** d})",
                f"= log({a ** c - b ** d})",
            ]
            wrong_idx = 3

        return self._build_result(
            steps=steps,
            correct_index=wrong_idx,
            explanation=(
                f"Errore: log(a) - log(b) = log(a/b), NON log(a - b). "
                f"log({a}) - log({b}) = log({a}/{b}) = log({self._fmt(a / b)})."
            ),
            did_you_know=(
                "La differenza di logaritmi diventa il logaritmo del quoziente: "
                "log(a) - log(b) = log(a/b). "
                "Non sottrarre mai gli argomenti direttamente!"
            ),
        )

    # ======================================================================
    #  TEMPLATE 18 : (a^m)^n = a^(m*n), NON a^(m+n)
    # ======================================================================
    def _trap_power_of_power(self, difficulty: int) -> dict:
        a = random.randint(2, 5)
        m = random.randint(2, 4)
        n = random.randint(2, 3)

        if difficulty == 1:
            steps = [
                f"Semplifica: ({a}^{m})^{n}",
                f"= {a}^({m} + {n})",
                f"= {a}^{m + n} = {a ** (m + n)}",
            ]
            wrong_idx = 1
        elif difficulty == 2:
            b = random.randint(2, 4)
            steps = [
                f"Semplifica: ({a}^{m})^{n} * {a}^{b}",
                f"({a}^{m})^{n} = {a}^({m}+{n}) = {a}^{m + n}",
                f"{a}^{m + n} * {a}^{b} = {a}^{m + n + b}",
                f"= {a ** (m + n + b)}",
            ]
            wrong_idx = 1
        else:
            b = random.randint(2, 3)
            c = random.randint(2, 3)
            steps = [
                f"Semplifica: ({a}^{m})^{n} / ({a}^{b})^{c}",
                f"({a}^{m})^{n} = {a}^({m}+{n}) = {a}^{m + n}",
                f"({a}^{b})^{c} = {a}^({b}*{c}) = {a}^{b * c}",
                f"Risultato: {a}^({m + n} - {b * c}) = {a}^{m + n - b * c}",
            ]
            wrong_idx = 1

        return self._build_result(
            steps=steps,
            correct_index=wrong_idx,
            explanation=(
                f"Errore: (a^m)^n = a^(m*n), NON a^(m+n). "
                f"({a}^{m})^{n} = {a}^({m}*{n}) = {a}^{m * n} = {a ** (m * n)}. "
                f"Gli esponenti si MOLTIPLICANO, non si sommano."
            ),
            did_you_know=(
                "Regole delle potenze: "
                "(a^m)^n = a^(m*n) (potenza di potenza: si moltiplicano), "
                "a^m * a^n = a^(m+n) (stesso base: si sommano). "
                "Non confondere le due regole!"
            ),
        )

    # ======================================================================
    #  TEMPLATE 19 : (a+b)^n != a^n + b^n
    # ======================================================================
    def _trap_distribute_exponent_over_sum(self, difficulty: int) -> dict:
        a = random.randint(2, 5)
        b = random.randint(1, 4)
        n = random.choice([2, 3])

        if difficulty == 1:
            steps = [
                f"Calcola: ({a} + {b})^{n}",
                f"= {a}^{n} + {b}^{n}",
                f"= {a ** n} + {b ** n} = {a ** n + b ** n}",
            ]
            wrong_idx = 1
        elif difficulty == 2:
            c = random.randint(1, 5)
            steps = [
                f"Semplifica: ({a} + {b})^{n} - {c}",
                f"({a} + {b})^{n} = {a}^{n} + {b}^{n}",
                f"= {a ** n} + {b ** n} = {a ** n + b ** n}",
                f"Risultato: {a ** n + b ** n} - {c} = {a ** n + b ** n - c}",
            ]
            wrong_idx = 1
        else:
            c = random.randint(2, 4)
            steps = [
                f"Semplifica: ({a}x + {b})^{n} per x = {c}",
                f"Sostituisco: ({a}*{c} + {b})^{n} = ({a * c} + {b})^{n}",
                f"= ({a * c})^{n} + {b}^{n}",
                f"= {(a * c) ** n} + {b ** n} = {(a * c) ** n + b ** n}",
            ]
            wrong_idx = 2

        correct_val = (a + b) ** n
        return self._build_result(
            steps=steps,
            correct_index=wrong_idx,
            explanation=(
                f"Errore: (a + b)^{n} NON e' uguale a a^{n} + b^{n}. "
                f"({a} + {b})^{n} = {a + b}^{n} = {correct_val}, "
                f"mentre {a}^{n} + {b}^{n} = {a ** n + b ** n}."
            ),
            did_you_know=(
                f"L'esponente NON si distribuisce sulla somma: "
                f"(a+b)^n != a^n + b^n. "
                f"Questo e' uno degli errori piu' comuni in algebra! "
                f"Per n=2, usare il prodotto notevole (a+b)^2 = a^2 + 2ab + b^2."
            ),
        )
