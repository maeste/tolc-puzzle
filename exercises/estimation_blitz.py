import random
import math

from exercises.base import Exercise


class EstimationBlitz(Exercise):
    """Stima Flash: estimate orders of magnitude under time pressure."""

    # Default per-question time limit in seconds
    DEFAULT_TIME_LIMIT = 8

    def generate(self, difficulty: int, exam_mode: bool = False) -> dict:
        difficulty = max(1, min(3, difficulty))

        if difficulty == 1:
            templates = [
                self._mult_two_integers,
                self._div_two_numbers,
                self._add_sub_three,
                self._fraction_sum,
                self._mult_three_small,
            ]
            time_limit = 10
        elif difficulty == 2:
            templates = [
                self._square_number,
                self._sqrt_number,
                self._power_of_two,
                self._power_times_factor,
                self._sqrt_times_factor,
            ]
            time_limit = 8
        else:
            templates = [
                self._log2_estimate,
                self._ln_times_sqrt,
                self._power_div_log,
                self._sqrt_times_log2,
                self._mixed_log_power_root,
            ]
            time_limit = 6

        template_fn = random.choice(templates)
        result = template_fn()

        if exam_mode:
            # In exam mode: no time_limit, exam-appropriate question text
            question = result["question"]
            # Replace the speed-oriented prompt with an exam-appropriate one
            if question.startswith("Stima velocemente il risultato di:\n"):
                expr = question.replace("Stima velocemente il risultato di:\n", "")
                result["question"] = f"Senza calcolatrice, stimare il valore di:\n{expr}"
        else:
            result["time_limit"] = time_limit

        result["difficulty"] = difficulty
        return result

    # ------------------------------------------------------------------ helpers

    @staticmethod
    def _approx_label(value: float) -> str:
        """Return a human-friendly 'circa X' label for a numeric value."""
        if abs(value) < 0.01:
            return "circa 0"
        abs_val = abs(value)
        sign = "-" if value < 0 else ""
        if abs_val < 1:
            # Show one significant digit
            return f"circa {sign}{round(abs_val, 2)}"
        if abs_val < 10:
            return f"circa {sign}{round(abs_val)}"
        # Round to nearest order-of-magnitude-friendly number
        magnitude = 10 ** int(math.log10(abs_val))
        rounded = round(abs_val / magnitude) * magnitude
        if rounded == 0:
            rounded = magnitude
        return f"circa {sign}{int(rounded)}"

    @staticmethod
    def _generate_distractors(correct_value: float, count: int = 4) -> list[float]:
        """Generate distractor values at different orders of magnitude."""
        abs_val = abs(correct_value) if correct_value != 0 else 1
        distractors = set()

        # Try orders of magnitude away
        candidates = [
            abs_val * 10,
            abs_val / 10,
            abs_val * 100,
            abs_val / 100,
            abs_val * 0.5,
            abs_val * 2,
            abs_val * 5,
            abs_val * 0.2,
            abs_val * 3,
            abs_val * 0.3,
        ]

        # Filter out values too close to correct
        for c in candidates:
            ratio = c / abs_val if abs_val > 0 else float("inf")
            if 0.7 < ratio < 1.4:
                continue
            if correct_value < 0:
                distractors.add(-c)
            else:
                distractors.add(c)
            if len(distractors) >= count * 2:
                break

        result = random.sample(list(distractors), min(count, len(distractors)))

        # Fill if needed
        while len(result) < count:
            factor = random.choice([0.1, 0.01, 10, 100, 0.05, 20])
            val = abs_val * factor
            if correct_value < 0:
                val = -val
            result.append(val)

        return result[:count]

    def _build_estimation_result(
        self,
        question_expr: str,
        correct_value: float,
        explanation: str,
        did_you_know: str,
    ) -> dict:
        """Build a complete result dict with 4 options at different magnitudes."""
        correct_label = self._approx_label(correct_value)
        distractors = self._generate_distractors(correct_value)
        distractor_labels = [self._approx_label(d) for d in distractors]

        # Ensure no duplicate labels
        seen = {correct_label}
        unique_distractors = []
        for label in distractor_labels:
            if label not in seen:
                seen.add(label)
                unique_distractors.append(label)

        # Fill if duplicates removed too many
        fallback_factors = [0.05, 0.15, 7, 15, 50, 200]
        idx = 0
        abs_val = abs(correct_value) if correct_value != 0 else 1
        while len(unique_distractors) < 4:
            val = abs_val * fallback_factors[idx % len(fallback_factors)]
            if correct_value < 0:
                val = -val
            label = self._approx_label(val)
            if label not in seen:
                seen.add(label)
                unique_distractors.append(label)
            idx += 1

        options = [correct_label] + unique_distractors[:4]
        correct_index = 0
        options, correct_index = Exercise.shuffle_options(options, correct_index)

        question = f"Stima velocemente il risultato di:\n{question_expr}"

        return {
            "question": question,
            "options": options,
            "correct_index": correct_index,
            "explanation": explanation,
            "did_you_know": did_you_know,
        }

    # ================================================================
    #  LEVEL 1 TEMPLATES: integers and fractions
    # ================================================================

    def _mult_two_integers(self) -> dict:
        a = random.randint(10, 99)
        b = random.randint(10, 99)
        result = a * b
        expr = f"{a} x {b}"

        a_round = round(a, -1)
        b_round = round(b, -1)
        approx = a_round * b_round

        explanation = (
            f"{a} ≈ {a_round} e {b} ≈ {b_round}, "
            f"quindi {a_round} x {b_round} = {approx}. "
            f"Il risultato esatto e' {result}."
        )
        tip = (
            "Per moltiplicare mentalmente, arrotonda i fattori alla decina "
            "piu' vicina e moltiplica i numeri semplificati."
        )
        return self._build_estimation_result(expr, result, explanation, tip)

    def _div_two_numbers(self) -> dict:
        b = random.choice([3, 4, 6, 7, 8, 9, 11, 12, 13])
        result = random.randint(5, 50)
        a = b * result + random.randint(-2, 2)
        actual = a / b
        expr = f"{a} / {b}"

        a_approx = round(a / b) * b
        explanation = (
            f"{a} ≈ {a_approx} che e' divisibile per {b}: "
            f"{a_approx} / {b} = {a_approx // b}. "
            f"Il risultato esatto e' {actual:.2f}."
        )
        tip = (
            "Per dividere mentalmente, cerca il multiplo del divisore "
            "piu' vicino al dividendo."
        )
        return self._build_estimation_result(expr, actual, explanation, tip)

    def _add_sub_three(self) -> dict:
        a = random.randint(100, 999)
        b = random.randint(100, 999)
        c = random.randint(50, 500)
        result = a + b - c
        expr = f"{a} + {b} - {c}"

        a_r = round(a, -2)
        b_r = round(b, -2)
        c_r = round(c, -2)
        approx = a_r + b_r - c_r

        explanation = (
            f"{a} ≈ {a_r}, {b} ≈ {b_r}, {c} ≈ {c_r}. "
            f"Quindi {a_r} + {b_r} - {c_r} = {approx}. "
            f"Il risultato esatto e' {result}."
        )
        tip = (
            "Per addizioni e sottrazioni con numeri grandi, arrotonda "
            "alle centinaia e calcola il risultato approssimato."
        )
        return self._build_estimation_result(expr, result, explanation, tip)

    def _fraction_sum(self) -> dict:
        num1 = random.randint(1, 7)
        den1 = random.randint(2, 9)
        num2 = random.randint(1, 7)
        den2 = random.randint(2, 9)
        while den1 == den2:
            den2 = random.randint(2, 9)

        result = num1 / den1 + num2 / den2
        expr = f"{num1}/{den1} + {num2}/{den2}"

        v1 = round(num1 / den1, 2)
        v2 = round(num2 / den2, 2)

        explanation = (
            f"{num1}/{den1} ≈ {v1} e {num2}/{den2} ≈ {v2}, "
            f"quindi la somma e' circa {v1} + {v2} = {round(v1 + v2, 2)}. "
            f"Il risultato esatto e' {result:.4f}."
        )
        tip = (
            "Per stimare frazioni, converti ciascuna nel decimale piu' vicino: "
            "1/3 ≈ 0.33, 1/4 = 0.25, 1/5 = 0.2, ecc."
        )
        return self._build_estimation_result(expr, result, explanation, tip)

    def _mult_three_small(self) -> dict:
        a = random.randint(2, 9)
        b = random.randint(2, 9)
        c = random.randint(2, 9)
        result = a * b * c
        expr = f"{a} x {b} x {c}"

        partial = a * b
        explanation = (
            f"Prima {a} x {b} = {partial}, poi {partial} x {c} = {result}. "
            f"Il risultato esatto e' {result}."
        )
        tip = (
            "Per prodotti di piu' fattori, procedi a coppie: "
            "moltiplica i primi due, poi il risultato per il terzo."
        )
        return self._build_estimation_result(expr, result, explanation, tip)

    # ================================================================
    #  LEVEL 2 TEMPLATES: powers, roots, scientific notation
    # ================================================================

    def _square_number(self) -> dict:
        a = random.randint(11, 35)
        result = a * a
        expr = f"{a}^2"

        # Use nearest known square
        nearest_10 = round(a, -1)
        nearest_sq = nearest_10 * nearest_10

        explanation = (
            f"{a} ≈ {nearest_10}, e {nearest_10}^2 = {nearest_sq}. "
            f"Il risultato esatto e' {a}^2 = {result}."
        )
        tip = (
            "Per quadrati, usa l'identita' (a+b)^2 = a^2 + 2ab + b^2. "
            "Ad esempio 23^2 = (20+3)^2 = 400 + 120 + 9 = 529."
        )
        return self._build_estimation_result(expr, result, explanation, tip)

    def _sqrt_number(self) -> dict:
        perfect_squares = [49, 64, 81, 100, 121, 144, 169, 196, 225, 256,
                           289, 324, 400, 625, 900, 1600, 2500, 4900, 8100]
        target_sq = random.choice(perfect_squares)
        # Add small noise
        noise = random.randint(-5, 5)
        n = target_sq + noise
        if n <= 0:
            n = target_sq
        result = math.sqrt(n)
        expr = f"sqrt({n})"

        perfect_root = int(math.sqrt(target_sq))
        explanation = (
            f"{n} ≈ {target_sq} = {perfect_root}^2, "
            f"quindi sqrt({n}) ≈ {perfect_root}. "
            f"Il risultato esatto e' {result:.2f}."
        )
        tip = (
            "Per stimare radici quadrate, trova il quadrato perfetto piu' vicino: "
            "sqrt(50) ≈ sqrt(49) = 7, sqrt(80) ≈ sqrt(81) = 9."
        )
        return self._build_estimation_result(expr, result, explanation, tip)

    def _power_of_two(self) -> dict:
        exp = random.randint(6, 14)
        result = 2 ** exp
        expr = f"2^{exp}"

        # Show doubling approach
        ref_exp = 10
        ref_val = 1024

        if exp <= 10:
            explanation = (
                f"2^10 = 1024 ≈ 1000. Partendo da li': "
                f"2^{exp} = 2^10 / 2^{10 - exp} = 1024 / {2 ** (10 - exp)} = {result}."
            )
        else:
            explanation = (
                f"2^10 = 1024 ≈ 1000. Quindi "
                f"2^{exp} = 2^10 x 2^{exp - 10} = 1024 x {2 ** (exp - 10)} = {result}."
            )

        tip = (
            "Memorizza 2^10 = 1024 ≈ 1000. Da questo puoi derivare "
            "qualsiasi potenza di 2 moltiplicando o dividendo per 2."
        )
        return self._build_estimation_result(expr, result, explanation, tip)

    def _power_times_factor(self) -> dict:
        base = random.choice([3, 4, 5])
        exp = random.randint(2, 5)
        factor = random.randint(2, 5)
        power_val = base ** exp
        result = power_val * factor
        expr = f"{base}^{exp} x {factor}"

        explanation = (
            f"{base}^{exp} = {power_val}, "
            f"quindi {power_val} x {factor} = {result}."
        )
        tip = (
            "Memorizza le potenze piu' comuni: 3^3=27, 3^4=81, 4^3=64, "
            "5^3=125, 5^4=625. Sono fondamentali per la stima rapida."
        )
        return self._build_estimation_result(expr, result, explanation, tip)

    def _sqrt_times_factor(self) -> dict:
        base_values = [50, 75, 120, 200, 250, 300, 500, 800]
        n = random.choice(base_values)
        factor = random.randint(2, 5)
        sqrt_val = math.sqrt(n)
        result = sqrt_val * factor
        expr = f"sqrt({n}) x {factor}"

        # Find nearest perfect square
        nearest_root = round(sqrt_val)
        nearest_sq = nearest_root * nearest_root

        explanation = (
            f"sqrt({n}) ≈ sqrt({nearest_sq}) = {nearest_root}. "
            f"Quindi {nearest_root} x {factor} = {nearest_root * factor}. "
            f"Il risultato esatto e' {result:.2f}."
        )
        tip = (
            "Per radici di numeri non perfetti, inquadra il numero tra "
            "due quadrati perfetti: sqrt(50) sta tra sqrt(49)=7 e sqrt(64)=8."
        )
        return self._build_estimation_result(expr, result, explanation, tip)

    # ================================================================
    #  LEVEL 3 TEMPLATES: logarithms and mixed expressions
    # ================================================================

    def _log2_estimate(self) -> dict:
        n = random.choice([100, 200, 500, 1000, 2000, 5000, 10000])
        result = math.log2(n)
        expr = f"log_2({n})"

        # Use 2^10 = 1024 ≈ 1000 as reference
        if n <= 1024:
            explanation = (
                f"2^10 = 1024 ≈ 1000, quindi log_2(1000) ≈ 10. "
                f"Dato che {n} e' circa {n}, log_2({n}) ≈ {result:.1f}."
            )
        else:
            power_approx = round(math.log2(n))
            explanation = (
                f"2^10 = 1024 ≈ 1000 e 2^{power_approx} = {2**power_approx}. "
                f"Quindi log_2({n}) ≈ {result:.1f}."
            )

        tip = (
            "Per log_2, conta quante volte devi raddoppiare per raggiungere il numero. "
            "log_2(1000) ≈ 10 perche' 2^10 = 1024 ≈ 1000."
        )
        return self._build_estimation_result(expr, result, explanation, tip)

    def _ln_times_sqrt(self) -> dict:
        # ln(e^k) * sqrt(perfect_square)
        k = random.randint(2, 5)
        sq = random.choice([4, 9, 16, 25, 36, 49])
        sqrt_val = int(math.sqrt(sq))
        result = k * sqrt_val
        expr = f"ln(e^{k}) x sqrt({sq})"

        explanation = (
            f"ln(e^{k}) = {k} (per definizione di logaritmo naturale). "
            f"sqrt({sq}) = {sqrt_val}. "
            f"Quindi {k} x {sqrt_val} = {result}."
        )
        tip = (
            "Ricorda: ln(e^x) = x sempre. Il logaritmo naturale e l'esponenziale "
            "sono funzioni inverse: si annullano a vicenda."
        )
        return self._build_estimation_result(expr, result, explanation, tip)

    def _power_div_log(self) -> dict:
        # 2^exp / log10(power_of_10)
        exp = random.randint(8, 12)
        log_arg_exp = random.randint(2, 5)
        log_arg = 10 ** log_arg_exp

        power_val = 2 ** exp
        log_val = log_arg_exp  # log10(10^k) = k
        result = power_val / log_val
        expr = f"2^{exp} / log_10({log_arg})"

        explanation = (
            f"2^{exp} = {power_val}. "
            f"log_10({log_arg}) = {log_val} (perche' {log_arg} = 10^{log_val}). "
            f"Quindi {power_val} / {log_val} = {result:.1f}."
        )
        tip = (
            "log_10(10^n) = n sempre. Questo rende semplice calcolare "
            "il logaritmo in base 10 di qualsiasi potenza di 10."
        )
        return self._build_estimation_result(expr, result, explanation, tip)

    def _sqrt_times_log2(self) -> dict:
        # sqrt(approx_square) * log2(power_of_2)
        sq_choices = [81, 100, 121, 144, 169, 196]
        sq = random.choice(sq_choices)
        noise = random.choice([-2, -1, 0, 1, 2])
        n = sq + noise
        if n <= 0:
            n = sq

        log_exp = random.randint(3, 7)
        log_arg = 2 ** log_exp

        sqrt_val = math.sqrt(n)
        result = sqrt_val * log_exp
        expr = f"sqrt({n}) x log_2({log_arg})"

        nearest_root = int(math.sqrt(sq))
        explanation = (
            f"sqrt({n}) ≈ sqrt({sq}) = {nearest_root}. "
            f"log_2({log_arg}) = {log_exp} (perche' 2^{log_exp} = {log_arg}). "
            f"Quindi {nearest_root} x {log_exp} = {nearest_root * log_exp}. "
            f"Il risultato esatto e' {result:.2f}."
        )
        tip = (
            "Combina le stime: prima semplifica ogni pezzo separatamente, "
            "poi moltiplica i risultati approssimati."
        )
        return self._build_estimation_result(expr, result, explanation, tip)

    def _mixed_log_power_root(self) -> dict:
        # sqrt(a) * log2(b) + c^d
        a_choices = [99, 101, 48, 50, 80, 82, 120, 122]
        a = random.choice(a_choices)
        b_exp = random.randint(3, 6)
        b = 2 ** b_exp
        c = random.choice([2, 3, 4, 5])
        d = random.randint(2, 3)

        sqrt_a = math.sqrt(a)
        log_b = b_exp
        c_d = c ** d
        result = sqrt_a * log_b + c_d
        expr = f"sqrt({a}) x log_2({b}) + {c}^{d}"

        # Find estimation
        nearest_sq_root = round(sqrt_a)
        nearest_sq = nearest_sq_root ** 2

        approx_product = nearest_sq_root * log_b
        approx_total = approx_product + c_d

        explanation = (
            f"sqrt({a}) ≈ sqrt({nearest_sq}) = {nearest_sq_root}. "
            f"log_2({b}) = {log_b}. "
            f"{c}^{d} = {c_d}. "
            f"Quindi {nearest_sq_root} x {log_b} + {c_d} = "
            f"{approx_product} + {c_d} = {approx_total}. "
            f"Il risultato esatto e' {result:.2f}."
        )
        tip = (
            "Per espressioni miste, stima ogni componente separatamente: "
            "radici, logaritmi e potenze. Poi combina i risultati. "
            "La precisione non conta, conta l'ordine di grandezza!"
        )
        return self._build_estimation_result(expr, result, explanation, tip)
