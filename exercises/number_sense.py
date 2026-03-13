import random
import math
from fractions import Fraction

from exercises.base import Exercise


class NumberSense(Exercise):
    """Senso Numerico: percentuali, frazioni, potenze e notazione scientifica."""

    def generate(self, difficulty: int) -> dict:
        difficulty = max(1, min(3, difficulty))

        if difficulty == 1:
            templates = [
                self._percentage_of_quantity,
                self._decimal_to_fraction,
                self._power_small_decimal,
                self._fraction_of_quantity,
            ]
        elif difficulty == 2:
            templates = [
                self._order_of_magnitude_sum,
                self._percentage_time_conversion,
                self._power_rules_numeric,
                self._scientific_notation_order,
            ]
        else:
            templates = [
                self._successive_percentage,
                self._nested_fraction_compute,
                self._estimation_product,
                self._percentage_reverse,
            ]

        template_fn = random.choice(templates)
        result = template_fn()
        result["difficulty"] = difficulty
        return result

    # ------------------------------------------------------------------ helpers

    @staticmethod
    def _make_numeric_distractors(
        correct: str, error_variants: list[str]
    ) -> tuple[list[str], int]:
        """Build 5 distinct options (1 correct + 4 distractors) and shuffle.

        Args:
            correct: the correct answer as a string
            error_variants: list of plausible wrong answers as strings

        Returns:
            (options, correct_index) after shuffling
        """
        distractors: list[str] = []
        seen = {correct}
        for v in error_variants:
            if v not in seen:
                seen.add(v)
                distractors.append(v)
            if len(distractors) == 4:
                break

        # If not enough distinct distractors, add small perturbations
        if len(distractors) < 4:
            # Try to parse correct as a number for perturbation
            try:
                base_val = float(correct.replace(",", "."))
                perturbation_factors = [1.05, 0.95, 1.12, 0.88, 1.21, 0.79, 1.33, 0.67]
                for factor in perturbation_factors:
                    candidate = base_val * factor
                    # Format like the correct answer
                    if "." in correct or "," in correct:
                        cand_str = f"{candidate:.2f}".rstrip("0").rstrip(".")
                    else:
                        cand_str = str(int(round(candidate)))
                    if cand_str not in seen:
                        seen.add(cand_str)
                        distractors.append(cand_str)
                    if len(distractors) == 4:
                        break
            except (ValueError, ZeroDivisionError):
                pass

        # Last resort: append numbered placeholders
        fallback_idx = 1
        while len(distractors) < 4:
            fb = f"N/D ({fallback_idx})"
            if fb not in seen:
                seen.add(fb)
                distractors.append(fb)
            fallback_idx += 1

        options = [correct] + distractors[:4]
        correct_index = 0
        options, correct_index = Exercise.shuffle_options(options, correct_index)
        return options, correct_index

    @staticmethod
    def _format_time(total_minutes: float) -> str:
        """Format a duration in minutes as 'X ore Y minuti Z secondi'."""
        total_seconds = round(total_minutes * 60)
        total_mins = total_seconds // 60
        secs = total_seconds % 60
        hours = total_mins // 60
        mins = total_mins % 60
        parts = []
        if hours > 0:
            parts.append(f"{hours} {'ora' if hours == 1 else 'ore'}")
        if mins > 0:
            parts.append(f"{mins} {'minuto' if mins == 1 else 'minuti'}")
        if secs > 0:
            parts.append(f"{secs} {'secondo' if secs == 1 else 'secondi'}")
        if not parts:
            return "0 minuti"
        return " e ".join(parts) if len(parts) <= 2 else ", ".join(parts[:-1]) + " e " + parts[-1]

    # ================================================================
    #  LEVEL 1 — Basic Arithmetic (4 templates)
    # ================================================================

    def _percentage_of_quantity(self) -> dict:
        """Parametric percentage-of-time problems."""
        p = random.choice([15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 79, 80, 85])
        h = random.choice([1, 2, 3, 4, 5])
        total_minutes = h * 60
        elapsed_minutes = total_minutes * p / 100
        remaining_minutes = total_minutes * (100 - p) / 100

        correct = self._format_time(remaining_minutes)

        # Distractors
        d1 = self._format_time(elapsed_minutes)  # swap: use p% instead of (100-p)%
        d2 = self._format_time(remaining_minutes + 1)  # +1 minute
        d3 = self._format_time(max(0, remaining_minutes - 1))  # -1 minute
        # Swap minutes and seconds logic: compute with wrong conversion
        wrong_secs = total_minutes * (100 - p) / 100
        d4 = self._format_time(wrong_secs * 0.8)  # 80% of correct

        options, correct_index = self._make_numeric_distractors(
            correct, [d1, d2, d3, d4]
        )

        question = f"È passato il {p}% di {h} {'ora' if h == 1 else 'ore'}. Quanto tempo manca?"
        explanation = (
            f"Il tempo totale è {total_minutes} minuti. "
            f"Il {p}% corrisponde a {elapsed_minutes:.0f} minuti. "
            f"Il tempo rimanente è {100 - p}% = {remaining_minutes:.0f} minuti, "
            f"ovvero {correct}."
        )
        did_you_know = (
            "Per calcolare le percentuali a mente, spezza il numero: "
            "il 15% = 10% + 5%, il 25% = un quarto, il 75% = tre quarti."
        )

        return {
            "question": question,
            "options": options,
            "correct_index": correct_index,
            "explanation": explanation,
            "did_you_know": did_you_know,
        }

    def _decimal_to_fraction(self) -> dict:
        """Convert decimal to irreducible fraction."""
        decimal_fraction_map = {
            "0.125": Fraction(1, 8),
            "0.2": Fraction(1, 5),
            "0.25": Fraction(1, 4),
            "0.375": Fraction(3, 8),
            "0.4": Fraction(2, 5),
            "0.5": Fraction(1, 2),
            "0.6": Fraction(3, 5),
            "0.625": Fraction(5, 8),
            "0.75": Fraction(3, 4),
            "0.8": Fraction(4, 5),
            "0.875": Fraction(7, 8),
        }
        d_str = random.choice(list(decimal_fraction_map.keys()))
        frac = decimal_fraction_map[d_str]
        correct = f"{frac.numerator}/{frac.denominator}"

        # Distractors: unreduced, inverted, off-by-one
        distractors = []
        # Unreduced form
        unreduced_n = frac.numerator * 2
        unreduced_d = frac.denominator * 2
        distractors.append(f"{unreduced_n}/{unreduced_d}")
        # Inverted
        distractors.append(f"{frac.denominator}/{frac.numerator}")
        # Off-by-one numerator
        distractors.append(f"{frac.numerator + 1}/{frac.denominator}")
        # Off-by-one denominator
        distractors.append(f"{frac.numerator}/{frac.denominator + 1}")
        # Wrong fraction from nearby decimal
        distractors.append(f"{frac.numerator + 2}/{frac.denominator}")
        distractors.append(f"{frac.numerator}/{frac.denominator - 1}" if frac.denominator > 1 else "1/1")

        options, correct_index = self._make_numeric_distractors(correct, distractors)

        question = f"Quale frazione in forma ridotta genera il numero decimale {d_str}?"
        explanation = (
            f"Il decimale {d_str} corrisponde alla frazione {correct}. "
            f"Si può verificare dividendo {frac.numerator} per {frac.denominator}: "
            f"{frac.numerator} ÷ {frac.denominator} = {d_str}."
        )
        did_you_know = (
            "Le frazioni con denominatore che è potenza di 2 o 5 (o loro prodotto) "
            "producono sempre decimali finiti. Ad esempio 1/8 = 0.125 perché 8 = 2³."
        )

        return {
            "question": question,
            "options": options,
            "correct_index": correct_index,
            "explanation": explanation,
            "did_you_know": did_you_know,
        }

    def _power_small_decimal(self) -> dict:
        """Compute powers of small decimals."""
        base = random.choice([0.001, 0.002, 0.003, 0.005, 0.007, 0.01, 0.02, 0.03, 0.05])
        exp = random.choice([2, 3])
        result = base ** exp

        # Format in scientific notation
        if result == 0:
            correct = "0"
        else:
            exponent_10 = math.floor(math.log10(abs(result)))
            mantissa = result / (10 ** exponent_10)
            # Round mantissa to avoid floating point noise
            mantissa = round(mantissa, 6)
            if mantissa == int(mantissa):
                correct = f"{int(mantissa)} × 10^{exponent_10}"
            else:
                correct = f"{mantissa} × 10^{exponent_10}"

        # Distractors: wrong exponent, wrong mantissa
        distractors = []
        if result != 0:
            exponent_10 = math.floor(math.log10(abs(result)))
            mantissa = round(result / (10 ** exponent_10), 6)
            # Wrong exponent +1
            distractors.append(f"{int(mantissa) if mantissa == int(mantissa) else mantissa} × 10^{exponent_10 + 1}")
            # Wrong exponent -1
            distractors.append(f"{int(mantissa) if mantissa == int(mantissa) else mantissa} × 10^{exponent_10 - 1}")
            # Wrong mantissa
            wrong_m = mantissa * 2 if mantissa * 2 != mantissa else mantissa + 1
            distractors.append(f"{int(wrong_m) if wrong_m == int(wrong_m) else wrong_m} × 10^{exponent_10}")
            # Wrong both
            distractors.append(f"{int(wrong_m) if wrong_m == int(wrong_m) else wrong_m} × 10^{exponent_10 - 1}")
            # Another wrong exponent
            distractors.append(f"{int(mantissa) if mantissa == int(mantissa) else mantissa} × 10^{exponent_10 + 2}")

        options, correct_index = self._make_numeric_distractors(correct, distractors)

        base_str = str(base)
        question = f"Quanto vale ({base_str})^{exp}?"
        explanation = (
            f"({base_str})^{exp} = {result}. "
            f"In notazione scientifica: {correct}. "
            f"Ricorda: quando elevi una potenza di 10 a un esponente, "
            f"moltiplichi gli esponenti."
        )
        did_you_know = (
            "Per elevare a potenza un numero in notazione scientifica (a × 10^n)^k, "
            "si ottiene a^k × 10^(n×k). Ad esempio (2 × 10^{-3})² = 4 × 10^{-6}."
        )

        return {
            "question": question,
            "options": options,
            "correct_index": correct_index,
            "explanation": explanation,
            "did_you_know": did_you_know,
        }

    def _fraction_of_quantity(self) -> dict:
        """Multi-step fraction reasoning."""
        total = random.choice([20, 24, 30, 36, 40, 48, 50, 60])
        fractions_list = [
            (2, 3), (3, 4), (3, 5), (4, 5), (2, 5), (5, 6),
        ]
        a, b = random.choice(fractions_list)

        # Ensure the fraction gives a whole number
        first_result = total * a // b
        if total * a % b != 0:
            # Adjust total to be divisible
            total = b * random.choice([4, 5, 6, 8, 10])
            first_result = total * a // b

        # Second operation: give away c items
        c = random.randint(2, min(5, first_result - 1))
        final = first_result - c

        item = random.choice(["mele", "biscotti", "caramelle", "figurine", "libri"])
        name = random.choice(["Marco", "Giulia", "Luca", "Sara", "Anna"])

        correct = str(final)
        # Distractors
        d1 = str(first_result)  # forgot to subtract
        d2 = str(total - first_result - c)  # used complement fraction
        d3 = str(final + c)  # added instead of subtracted
        d4 = str(first_result + c)  # added c to first result
        d5 = str(total - c)  # subtracted c from total
        d6 = str(abs(final - 2))  # off by 2

        options, correct_index = self._make_numeric_distractors(
            correct, [d1, d2, d3, d4, d5, d6]
        )

        question = (
            f"{name} ha {total} {item}. Ne prende {a}/{b} e poi ne regala {c}. "
            f"Quante {item} gli restano?"
        )
        explanation = (
            f"{a}/{b} di {total} = {first_result}. "
            f"Dopo averne regalate {c}: {first_result} - {c} = {final} {item}."
        )
        did_you_know = (
            "Per calcolare una frazione di un numero, dividi per il denominatore "
            "e moltiplica per il numeratore. Ad esempio, 3/4 di 40 = 40 ÷ 4 × 3 = 30."
        )

        return {
            "question": question,
            "options": options,
            "correct_index": correct_index,
            "explanation": explanation,
            "did_you_know": did_you_know,
        }

    # ================================================================
    #  LEVEL 2 — Orders of Magnitude (4 templates)
    # ================================================================

    def _order_of_magnitude_sum(self) -> dict:
        """Sums of powers of 10."""
        a = random.randint(6, 12)
        b = a - 1  # one order of magnitude below

        # Expression like: 10^a + 10^b + 10^a = 2*10^a + 10^b
        coeff_a = random.choice([1, 2, 3])
        coeff_b = random.choice([1, 2])

        val = coeff_a * (10 ** a) + coeff_b * (10 ** b)

        # Express result in scientific notation
        exp_result = math.floor(math.log10(val))
        mantissa = val / (10 ** exp_result)
        mantissa = round(mantissa, 2)

        if mantissa == int(mantissa):
            correct = f"{int(mantissa)} × 10^{exp_result}"
        else:
            # Use comma for Italian decimal separator in display
            correct = f"{mantissa} × 10^{exp_result}"

        # Build expression string
        terms = []
        for _ in range(coeff_a):
            terms.append(f"10^{a}")
        for _ in range(coeff_b):
            terms.append(f"10^{b}")
        random.shuffle(terms)
        expr = " + ".join(terms)

        # Distractors
        distractors = []
        # Wrong coefficient
        distractors.append(f"{int(mantissa) + 1 if mantissa == int(mantissa) else round(mantissa + 1, 2)} × 10^{exp_result}")
        # Wrong exponent
        distractors.append(f"{int(mantissa) if mantissa == int(mantissa) else mantissa} × 10^{exp_result + 1}")
        distractors.append(f"{int(mantissa) if mantissa == int(mantissa) else mantissa} × 10^{exp_result - 1}")
        # Sum of exponents (common error)
        distractors.append(f"{coeff_a + coeff_b} × 10^{a + b}")
        # Wrong coefficient and exponent
        distractors.append(f"{coeff_a + coeff_b} × 10^{a}")

        options, correct_index = self._make_numeric_distractors(correct, distractors)

        question = f"Quanto vale {expr}?"
        explanation = (
            f"Raccogliamo 10^{b}: "
            f"{coeff_a} × 10^{a} + {coeff_b} × 10^{b} = "
            f"{coeff_a} × 10 × 10^{b} + {coeff_b} × 10^{b} = "
            f"({coeff_a * 10} + {coeff_b}) × 10^{b} = {coeff_a * 10 + coeff_b} × 10^{b}. "
            f"In notazione scientifica: {correct}."
        )
        did_you_know = (
            "Quando sommi potenze di 10 con esponenti diversi, raccogli la potenza "
            "con l'esponente più piccolo. Non si possono sommare gli esponenti!"
        )

        return {
            "question": question,
            "options": options,
            "correct_index": correct_index,
            "explanation": explanation,
            "did_you_know": did_you_know,
        }

    def _percentage_time_conversion(self) -> dict:
        """Percentage of time with hours AND minutes as base."""
        hours = random.choice([1, 2, 3, 4])
        minutes = random.choice([10, 15, 20, 30, 40, 45])
        p = random.choice([10, 15, 20, 25, 30, 37, 40, 50, 60, 75])

        total_minutes = hours * 60 + minutes
        result_minutes = total_minutes * p / 100

        # Round to avoid floating point issues
        result_minutes = round(result_minutes, 2)

        if result_minutes == int(result_minutes):
            correct = f"{int(result_minutes)} minuti"
        else:
            whole_mins = int(result_minutes)
            secs = round((result_minutes - whole_mins) * 60)
            if secs == 0:
                correct = f"{whole_mins} minuti"
            else:
                correct = f"{whole_mins} minuti e {secs} secondi"

        # Distractors
        d1_val = hours * 60 * p / 100  # forgot the extra minutes
        d2_val = total_minutes * (100 - p) / 100  # used complement
        d3_val = result_minutes + minutes * p / 100  # double-counted minutes
        d4_val = abs(result_minutes - 5)  # off by 5

        def _fmt_mins(m: float) -> str:
            m = round(m, 2)
            if m == int(m):
                return f"{int(m)} minuti"
            whole = int(m)
            s = round((m - whole) * 60)
            if s == 0:
                return f"{whole} minuti"
            return f"{whole} minuti e {s} secondi"

        distractors = [_fmt_mins(d1_val), _fmt_mins(d2_val), _fmt_mins(d3_val), _fmt_mins(d4_val)]

        options, correct_index = self._make_numeric_distractors(correct, distractors)

        question = (
            f"Il {p}% di {hours} {'ora' if hours == 1 else 'ore'} e {minutes} minuti "
            f"equivale a quanti minuti?"
        )
        explanation = (
            f"Il tempo totale è {hours} × 60 + {minutes} = {total_minutes} minuti. "
            f"Il {p}% di {total_minutes} = {result_minutes} minuti. "
            f"Risposta: {correct}."
        )
        did_you_know = (
            "Per calcolare percentuali di tempi misti, converti sempre tutto in minuti "
            "(o secondi) prima di applicare la percentuale."
        )

        return {
            "question": question,
            "options": options,
            "correct_index": correct_index,
            "explanation": explanation,
            "did_you_know": did_you_know,
        }

    def _power_rules_numeric(self) -> dict:
        """Apply power rules to compute a numeric result: 2^a × 4^b / 8^c."""
        a = random.randint(2, 8)
        b = random.randint(1, 4)
        c = random.randint(1, 3)

        # Everything in base 2: 4^b = 2^(2b), 8^c = 2^(3c)
        total_exp = a + 2 * b - 3 * c
        result = 2 ** total_exp if total_exp >= 0 else Fraction(1, 2 ** (-total_exp))

        if total_exp >= 0:
            correct = str(2 ** total_exp)
        else:
            correct = f"1/{2 ** (-total_exp)}"

        # Distractors: wrong exponent calculations
        distractors = []
        # Added all exponents instead of applying rules
        wrong1 = 2 ** (a + b + c) if a + b + c < 30 else 2 ** 15
        distractors.append(str(wrong1))
        # Forgot to convert bases
        wrong2_exp = a + b - c
        if wrong2_exp >= 0:
            distractors.append(str(2 ** wrong2_exp))
        else:
            distractors.append(f"1/{2 ** (-wrong2_exp)}")
        # Off by one in final exponent
        if total_exp + 1 >= 0:
            distractors.append(str(2 ** (total_exp + 1)))
        else:
            distractors.append(f"1/{2 ** (-(total_exp + 1))}")
        if total_exp - 1 >= 0:
            distractors.append(str(2 ** (total_exp - 1)))
        else:
            distractors.append(f"1/{2 ** (-(total_exp - 1))}")
        # Multiplied exponents of 4 by 3 instead of 2
        wrong5_exp = a + 3 * b - 3 * c
        if wrong5_exp >= 0:
            distractors.append(str(2 ** wrong5_exp))
        else:
            distractors.append(f"1/{2 ** (-wrong5_exp)}")

        options, correct_index = self._make_numeric_distractors(correct, distractors)

        question = f"Calcola il valore di 2^{a} × 4^{b} / 8^{c}"
        explanation = (
            f"Convertiamo tutto in base 2: 4^{b} = 2^{2 * b}, 8^{c} = 2^{3 * c}. "
            f"Quindi 2^{a} × 2^{2 * b} / 2^{3 * c} = 2^({a} + {2 * b} - {3 * c}) = "
            f"2^{total_exp} = {correct}."
        )
        did_you_know = (
            "Per semplificare prodotti e quozienti di potenze, converti tutto alla stessa base. "
            "4 = 2², 8 = 2³, 16 = 2⁴, 32 = 2⁵. Poi somma/sottrai gli esponenti."
        )

        return {
            "question": question,
            "options": options,
            "correct_index": correct_index,
            "explanation": explanation,
            "did_you_know": did_you_know,
        }

    def _scientific_notation_order(self) -> dict:
        """Order numbers in scientific notation — find the largest."""
        # Generate 5 numbers with different representations but close values
        base_exp = random.randint(3, 7)

        # Create values that look similar but differ
        entries = []
        values = set()
        attempts = 0
        while len(entries) < 5 and attempts < 50:
            attempts += 1
            form = random.choice(["scientific", "shifted", "plain"])
            if form == "scientific":
                m = round(random.uniform(1.0, 9.9), 1)
                e = base_exp + random.choice([-1, 0, 1])
                val = m * (10 ** e)
                display = f"{m} × 10^{e}"
            elif form == "shifted":
                # Like 32 × 10^3 instead of 3.2 × 10^4
                m = round(random.uniform(10, 999), 0)
                e = base_exp - len(str(int(m))) + 1 + random.choice([-1, 0, 1])
                val = m * (10 ** e)
                display = f"{int(m)} × 10^{e}"
            else:
                val = random.randint(int(10 ** (base_exp - 1)), int(10 ** (base_exp + 1)))
                display = f"{val:,}".replace(",", ".")
                val = float(val)

            # Check for approximate uniqueness
            too_close = any(abs(val - v) / max(abs(v), 1) < 0.01 for v in values)
            if not too_close and display not in [e_d for _, e_d in entries]:
                entries.append((val, display))
                values.add(val)

        # If we couldn't generate enough, fill with guaranteed distinct values
        while len(entries) < 5:
            filler_val = random.uniform(10 ** (base_exp - 1), 10 ** (base_exp + 1))
            filler_display = f"{filler_val:.1f}"
            if filler_display not in [e_d for _, e_d in entries]:
                entries.append((filler_val, filler_display))

        # Find the largest
        max_idx = max(range(len(entries)), key=lambda i: entries[i][0])
        correct = entries[max_idx][1]

        # Options are the displays
        all_displays = [e[1] for e in entries]
        # correct is at position max_idx; shuffle
        options = list(all_displays)
        correct_index = max_idx
        options, correct_index = Exercise.shuffle_options(options, correct_index)

        numbers_str = ", ".join(all_displays)
        question = f"Quale dei seguenti numeri è il più grande?\n{numbers_str}"

        sorted_entries = sorted(entries, key=lambda e: e[0], reverse=True)
        order_str = " > ".join(e[1] for e in sorted_entries)
        explanation = (
            f"Convertendo tutti i numeri nella stessa notazione, l'ordine è: {order_str}. "
            f"Il più grande è {correct}."
        )
        did_you_know = (
            "Per confrontare numeri in notazione scientifica, prima confronta gli esponenti. "
            "Se gli esponenti sono uguali, confronta le mantisse. "
            "Attenzione a forme come 32 × 10³ = 3.2 × 10⁴!"
        )

        return {
            "question": question,
            "options": options,
            "correct_index": correct_index,
            "explanation": explanation,
            "did_you_know": did_you_know,
        }

    # ================================================================
    #  LEVEL 3 — Complex Mental Arithmetic (4 templates)
    # ================================================================

    def _successive_percentage(self) -> dict:
        """Successive percentage changes on a price."""
        price = random.choice([100, 120, 150, 180, 200, 250, 300, 400, 500])
        a = random.choice([10, 15, 20, 25, 30, 40, 50])
        b = random.choice([10, 15, 20, 25, 30, 40, 50])

        # Increase by a%, then decrease by b%
        after_increase = price * (1 + a / 100)
        final = after_increase * (1 - b / 100)
        final = round(final, 2)

        if final == int(final):
            correct = f"{int(final)}€"
        else:
            correct = f"{final:.2f}€"

        # Distractors
        # Just add/subtract percentages (common error)
        naive = price * (1 + (a - b) / 100)
        d1 = f"{naive:.2f}€" if naive != int(naive) else f"{int(naive)}€"

        # Apply both to original (common error)
        wrong2 = price + price * a / 100 - price * b / 100
        d2 = f"{wrong2:.2f}€" if wrong2 != int(wrong2) else f"{int(wrong2)}€"

        # Decrease then increase (order swap)
        after_decrease = price * (1 - b / 100)
        reverse_final = after_decrease * (1 + a / 100)
        reverse_final = round(reverse_final, 2)
        d3 = f"{reverse_final:.2f}€" if reverse_final != int(reverse_final) else f"{int(reverse_final)}€"

        # Off by a fixed amount
        d4 = f"{int(final) + 5}€" if final == int(final) else f"{final + 5:.2f}€"
        d5 = f"{max(1, int(final) - 5)}€" if final == int(final) else f"{max(0.01, final - 5):.2f}€"

        options, correct_index = self._make_numeric_distractors(
            correct, [d1, d2, d3, d4, d5]
        )

        question = (
            f"Un prodotto costa {price}€. Dopo un aumento del {a}% e poi uno sconto "
            f"del {b}%, qual è il prezzo finale?"
        )
        explanation = (
            f"Dopo l'aumento del {a}%: {price} × {1 + a / 100} = {after_increase:.2f}€. "
            f"Dopo lo sconto del {b}%: {after_increase:.2f} × {1 - b / 100} = {final}€. "
            f"Attenzione: non si possono semplicemente sottrarre le percentuali!"
        )
        did_you_know = (
            "Un aumento del 20% seguito da uno sconto del 20% NON riporta al prezzo originale! "
            "Il risultato è 1.20 × 0.80 = 0.96, cioè una perdita del 4%. "
            "In generale, +a% poi -a% dà una perdita di (a/100)²."
        )

        return {
            "question": question,
            "options": options,
            "correct_index": correct_index,
            "explanation": explanation,
            "did_you_know": did_you_know,
        }

    def _nested_fraction_compute(self) -> dict:
        """Compute nested fraction expressions like (a/b di X) + (c/d di Y)."""
        nice_values = [60, 80, 100, 120, 150, 200]
        x = random.choice(nice_values)
        y = random.choice(nice_values)

        frac_pairs = [(2, 3), (3, 4), (1, 4), (1, 3), (2, 5), (3, 5), (1, 2), (5, 6)]
        a, b = random.choice(frac_pairs)
        c, d = random.choice(frac_pairs)

        # Ensure whole results
        while (x * a) % b != 0:
            x = random.choice(nice_values)
        while (y * c) % d != 0:
            y = random.choice(nice_values)

        op = random.choice(["+", "-"])
        part1 = x * a // b
        part2 = y * c // d

        if op == "+":
            result = part1 + part2
        else:
            result = part1 - part2

        correct = str(result)

        # Distractors: swap fractions, arithmetic errors
        d1 = str(part1 + part2 if op == "-" else part1 - part2)  # wrong operation
        d2 = str(x * c // d + y * a // b if op == "+" else x * c // d - y * a // b)  # swapped fractions
        d3 = str(result + part1)  # added extra
        d4 = str(abs(result - 1))  # off by 1
        d5 = str(x * a // b)  # only first part

        options, correct_index = self._make_numeric_distractors(
            correct, [d1, d2, d3, d4, d5]
        )

        question = f"Calcola: ({a}/{b} di {x}) {op} ({c}/{d} di {y})"
        explanation = (
            f"{a}/{b} di {x} = {part1}. "
            f"{c}/{d} di {y} = {part2}. "
            f"Quindi {part1} {op} {part2} = {result}."
        )
        did_you_know = (
            "\"Di\" in matematica significa moltiplicazione: \"2/3 di 120\" = 2/3 × 120 = 80. "
            "Scomponi: prima dividi per il denominatore, poi moltiplica per il numeratore."
        )

        return {
            "question": question,
            "options": options,
            "correct_index": correct_index,
            "explanation": explanation,
            "did_you_know": did_you_know,
        }

    def _estimation_product(self) -> dict:
        """Near-round-number estimation via (a-e)(a+e) = a^2 - e^2."""
        a = random.choice([100, 200, 500, 1000])
        epsilon = random.choice([1, 2, 3, 4, 5, 7])
        n1 = a - epsilon
        n2 = a + epsilon

        result = n1 * n2  # = a^2 - epsilon^2
        a_sq = a * a
        eps_sq = epsilon * epsilon

        correct = str(result)

        # Distractors
        d1 = str(a_sq)  # forgot to subtract epsilon^2
        d2 = str(a_sq + eps_sq)  # added instead of subtracted
        d3 = str(a_sq - epsilon)  # subtracted epsilon instead of epsilon^2
        d4 = str(result + 2)  # off by 2
        d5 = str(result - 2)  # off by 2

        options, correct_index = self._make_numeric_distractors(
            correct, [d1, d2, d3, d4, d5]
        )

        question = f"Calcola il valore esatto di {n1} × {n2}"
        explanation = (
            f"Usando l'identità (a - b)(a + b) = a² - b²: "
            f"{n1} × {n2} = ({a} - {epsilon})({a} + {epsilon}) = "
            f"{a}² - {epsilon}² = {a_sq} - {eps_sq} = {result}."
        )
        did_you_know = (
            "Il prodotto notevole (a-b)(a+b) = a²-b² è utilissimo per il calcolo mentale. "
            "Ad esempio: 97 × 103 = (100-3)(100+3) = 10000 - 9 = 9991."
        )

        return {
            "question": question,
            "options": options,
            "correct_index": correct_index,
            "explanation": explanation,
            "did_you_know": did_you_know,
        }

    def _percentage_reverse(self) -> dict:
        """Find original price from final price after percentage change."""
        p = random.choice([10, 15, 20, 25, 30, 40, 50])
        # Choose original so that final is a nice number
        original = random.choice([80, 100, 120, 150, 160, 200, 250, 300, 400, 500])
        final = original * (100 + p) / 100
        final = round(final, 2)

        if final == int(final):
            final_str = f"{int(final)}"
        else:
            final_str = f"{final:.2f}"

        correct = f"{original}€"

        # Distractors
        # Common error: subtract p% from final
        wrong_subtract = final * (100 - p) / 100
        d1 = f"{wrong_subtract:.2f}€" if wrong_subtract != int(wrong_subtract) else f"{int(wrong_subtract)}€"
        # Another error: subtract the absolute increase from final
        increase = final - original
        d2 = f"{int(final - increase * 0.8)}€"  # slightly wrong
        # Just subtract flat percentage
        d3 = f"{int(final - p)}€"
        # Off by common factor
        d4 = f"{original + 10}€"
        d5 = f"{max(1, original - 10)}€"

        options, correct_index = self._make_numeric_distractors(
            correct, [d1, d2, d3, d4, d5]
        )

        question = (
            f"Dopo un aumento del {p}%, il prezzo è {final_str}€. "
            f"Qual era il prezzo originale?"
        )
        explanation = (
            f"Se il prezzo originale è x, dopo un aumento del {p}% diventa "
            f"x × {1 + p / 100}. Quindi x × {1 + p / 100} = {final_str}, "
            f"da cui x = {final_str} / {1 + p / 100} = {original}€. "
            f"Errore comune: sottrarre il {p}% dal prezzo finale ({final_str} × 0.{100 - p} = "
            f"{wrong_subtract:.2f}€) — sbagliato!"
        )
        did_you_know = (
            "Per trovare il prezzo originale dopo un aumento del p%, "
            "dividi il prezzo finale per (1 + p/100), NON sottrarre p%. "
            "Ad esempio, se dopo +20% il prezzo è 120€, "
            "l'originale è 120/1.2 = 100€, non 120 - 24 = 96€."
        )

        return {
            "question": question,
            "options": options,
            "correct_index": correct_index,
            "explanation": explanation,
            "did_you_know": did_you_know,
        }
