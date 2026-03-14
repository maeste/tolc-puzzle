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
                self._division_remainder_basic,
                self._sequence_arithmetic_nth_term,
                self._sequence_geometric_nth_term,
            ]
        elif difficulty == 2:
            templates = [
                self._order_of_magnitude_sum,
                self._percentage_time_conversion,
                self._power_rules_numeric,
                self._scientific_notation_order,
                self._division_remainder_find_number,
                self._division_remainder_properties,
                self._sequence_arithmetic_sum,
                self._sequence_geometric_sum,
                self._sequence_find_ratio_or_difference,
            ]
        else:
            templates = [
                self._successive_percentage,
                self._nested_fraction_compute,
                self._estimation_product,
                self._percentage_reverse,
                self._division_remainder_word_problem,
                self._sequence_geometric_convergence,
                self._sequence_mixed_problem,
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

    # ================================================================
    #  Division with Remainder (4 templates across L1, L2, L3)
    # ================================================================

    def _division_remainder_basic(self) -> dict:
        """L1 — Basic remainder calculation."""
        b = random.randint(3, 13)
        a = random.randint(20, 200)
        # Ensure there is a non-zero remainder for a more interesting question
        while a % b == 0:
            a = random.randint(20, 200)

        remainder = a % b
        quotient = a // b

        correct = str(remainder)

        # Distractors based on common errors
        distractors = [
            str(quotient),                          # confuse quotient with remainder
            str(remainder + 1),                     # off-by-one high
            str(max(0, remainder - 1)),             # off-by-one low
            str(b - remainder),                     # complement to divisor
            str(abs(a - b)),                        # wrong operation: subtraction
            str(quotient + 1),                      # quotient off-by-one
        ]

        options, correct_index = self._make_numeric_distractors(correct, distractors)

        question = f"Qual è il resto della divisione di {a} per {b}?"
        explanation = (
            f"Calcola {a} ÷ {b} = {quotient} con resto {remainder}. "
            f"Verifica: {quotient} × {b} + {remainder} = "
            f"{quotient * b} + {remainder} = {a}."
        )
        did_you_know = (
            "Il resto della divisione di a per b è sempre compreso tra 0 e b−1. "
            "Si può calcolare come a − (a ÷ b) × b, dove la divisione è intera."
        )

        return {
            "question": question,
            "options": options,
            "correct_index": correct_index,
            "explanation": explanation,
            "did_you_know": did_you_know,
        }

    def _division_remainder_find_number(self) -> dict:
        """L2 — Find the number given divisor and remainder."""
        d = random.randint(4, 12)
        r = random.randint(1, d - 1)
        k = random.randint(3, 15)
        n = k * d + r

        correct = str(n)

        # Distractors: numbers that give different remainders
        distractors = []
        # Number with remainder r+1 (or r-1)
        distractors.append(str(k * d + min(r + 1, d - 1)))
        distractors.append(str(k * d + max(r - 1, 0)))
        # The quotient itself
        distractors.append(str(k))
        # A multiple of d (remainder 0)
        distractors.append(str(k * d))
        # Different k, same structure but wrong
        distractors.append(str((k + 1) * d + r + 1))
        distractors.append(str((k - 1) * d))

        options, correct_index = self._make_numeric_distractors(correct, distractors)

        question = f"Quale dei seguenti numeri, diviso per {d}, dà resto {r}?"
        explanation = (
            f"Un numero che diviso per {d} dà resto {r} ha la forma "
            f"k × {d} + {r}. Con k = {k}: {k} × {d} + {r} = {n}. "
            f"Verifica: {n} ÷ {d} = {k} con resto {r}."
        )
        did_you_know = (
            "Tutti i numeri che danno lo stesso resto r quando divisi per d "
            "formano una classe di equivalenza modulo d. "
            "Si scrivono come n ≡ r (mod d)."
        )

        return {
            "question": question,
            "options": options,
            "correct_index": correct_index,
            "explanation": explanation,
            "did_you_know": did_you_know,
        }

    def _division_remainder_word_problem(self) -> dict:
        """L3 — Word problem involving division with remainder."""
        contexts = [
            {
                "items": "studenti",
                "groups": "gruppi",
                "group_word": "gruppo",
                "container": "da",
                "remainder_verb": "restano",
                "template": (
                    "Ci sono {n} {items} da dividere in {groups} {container} {g}. "
                    "Quanti {groups} completi si formano e quanti {items} {remainder_verb}?"
                ),
            },
            {
                "items": "biscotti",
                "groups": "sacchetti",
                "group_word": "sacchetto",
                "container": "da",
                "remainder_verb": "avanzano",
                "template": (
                    "Si devono confezionare {n} {items} in {groups} {container} {g}. "
                    "Quanti {groups} completi si riempiono e quanti {items} {remainder_verb}?"
                ),
            },
            {
                "items": "pagine",
                "groups": "capitoli",
                "group_word": "capitolo",
                "container": "da",
                "remainder_verb": "restano",
                "template": (
                    "Un libro ha {n} {items} da distribuire in {groups} {container} {g} {items} ciascuno. "
                    "Quanti {groups} completi ci sono e quante {items} {remainder_verb}?"
                ),
            },
        ]

        ctx = random.choice(contexts)
        g = random.randint(4, 9)
        n = random.randint(30, 120)
        # Ensure non-zero remainder
        while n % g == 0:
            n = random.randint(30, 120)

        q = n // g
        r = n % g

        correct = f"{q} {ctx['groups']} completi, {r} {ctx['items']} {ctx['remainder_verb']}"

        # Distractors based on common errors
        distractors = [
            # Swap quotient and remainder
            f"{r} {ctx['groups']} completi, {q} {ctx['items']} {ctx['remainder_verb']}",
            # Off-by-one on groups (round up)
            f"{q + 1} {ctx['groups']} completi, {0} {ctx['items']} {ctx['remainder_verb']}",
            # Off-by-one on remainder
            f"{q} {ctx['groups']} completi, {r + 1} {ctx['items']} {ctx['remainder_verb']}",
            # Wrong operation: subtraction
            f"{q - 1} {ctx['groups']} completi, {r + g} {ctx['items']} {ctx['remainder_verb']}",
            # Remainder = g - r (complement error)
            f"{q} {ctx['groups']} completi, {g - r} {ctx['items']} {ctx['remainder_verb']}",
        ]

        # Filter out duplicates of the correct answer
        unique_distractors = []
        seen = {correct}
        for dist in distractors:
            if dist not in seen:
                seen.add(dist)
                unique_distractors.append(dist)

        # Pad if needed
        fallback_idx = 2
        while len(unique_distractors) < 4:
            fb = f"{q + fallback_idx} {ctx['groups']} completi, {max(0, r - fallback_idx)} {ctx['items']} {ctx['remainder_verb']}"
            if fb not in seen:
                seen.add(fb)
                unique_distractors.append(fb)
            fallback_idx += 1

        options = [correct] + unique_distractors[:4]
        correct_index = 0
        options, correct_index = Exercise.shuffle_options(options, correct_index)

        question = ctx["template"].format(
            n=n, items=ctx["items"], groups=ctx["groups"],
            container=ctx["container"], g=g, remainder_verb=ctx["remainder_verb"],
        )
        explanation = (
            f"{n} ÷ {g} = {q} con resto {r}. "
            f"Si formano {q} {ctx['groups']} completi e {ctx['remainder_verb']} "
            f"{r} {ctx['items']}. "
            f"Verifica: {q} × {g} + {r} = {q * g} + {r} = {n}."
        )
        did_you_know = (
            "Nei problemi di divisione con resto nella vita reale, il resto "
            "indica gli elementi che non riempiono completamente un gruppo. "
            "Se servono gruppi per tutti, bisogna arrotondare per eccesso il quoziente."
        )

        return {
            "question": question,
            "options": options,
            "correct_index": correct_index,
            "explanation": explanation,
            "did_you_know": did_you_know,
        }

    # ================================================================
    #  Arithmetic & Geometric Sequences (7 templates across L1, L2, L3)
    # ================================================================

    # --- L1 ---

    def _sequence_arithmetic_nth_term(self) -> dict:
        """L1 — Find the n-th term of an arithmetic sequence."""
        a1 = random.randint(2, 20)
        d = random.randint(2, 8)
        n = random.randint(5, 15)

        correct_val = a1 + (n - 1) * d
        correct = str(correct_val)

        # Distractors
        distractors = [
            str(a1 + n * d),           # off-by-one: using n instead of n-1
            str(a1 * d),               # a1 * d
            str(a1 + (n - 2) * d),     # off-by-one low
            str(a1 * n + d),           # wrong formula
            str((n - 1) * d),          # forgot a1
        ]

        options, correct_index = self._make_numeric_distractors(correct, distractors)

        question = (
            f"In una progressione aritmetica con primo termine a₁ = {a1} "
            f"e ragione d = {d}, qual è il {n}-esimo termine?"
        )
        explanation = (
            f"La formula del termine n-esimo è aₙ = a₁ + (n−1)·d. "
            f"Quindi a_{n} = {a1} + ({n}−1)·{d} = {a1} + {(n - 1) * d} = {correct_val}."
        )
        did_you_know = (
            "In una progressione aritmetica ogni termine si ottiene sommando "
            "la ragione d al termine precedente. La formula generale è "
            "aₙ = a₁ + (n−1)·d."
        )

        return {
            "question": question,
            "options": options,
            "correct_index": correct_index,
            "explanation": explanation,
            "did_you_know": did_you_know,
        }

    def _sequence_geometric_nth_term(self) -> dict:
        """L1 — Find the n-th term of a geometric sequence."""
        a1 = random.randint(2, 5)
        r = random.randint(2, 4)
        n = random.randint(4, 7)

        correct_val = a1 * r ** (n - 1)
        correct = str(correct_val)

        # Distractors
        distractors = [
            str(a1 * r ** n),              # off-by-one: r^n instead of r^(n-1)
            str(a1 * r ** (n - 2)),        # off-by-one low
            str(a1 * (r + 1) ** (n - 1)),  # wrong ratio
            str(a1 * n * r),              # linear approximation
            str(r ** (n - 1)),            # forgot a1
        ]

        options, correct_index = self._make_numeric_distractors(correct, distractors)

        question = (
            f"In una progressione geometrica con primo termine a₁ = {a1} "
            f"e ragione r = {r}, qual è il {n}-esimo termine?"
        )
        explanation = (
            f"La formula del termine n-esimo è aₙ = a₁ · r^(n−1). "
            f"Quindi a_{n} = {a1} · {r}^({n}−1) = {a1} · {r ** (n - 1)} = {correct_val}."
        )
        did_you_know = (
            "In una progressione geometrica ogni termine si ottiene moltiplicando "
            "il precedente per la ragione r. La formula generale è "
            "aₙ = a₁ · r^(n−1). Attenzione: l'esponente è n−1, non n!"
        )

        return {
            "question": question,
            "options": options,
            "correct_index": correct_index,
            "explanation": explanation,
            "did_you_know": did_you_know,
        }

    # --- L2 ---

    def _sequence_arithmetic_sum(self) -> dict:
        """L2 — Sum of first n terms of an arithmetic sequence (word problem)."""
        a1 = random.randint(1, 10)
        d = random.randint(1, 5)
        n = random.randint(5, 12)

        a_n = a1 + (n - 1) * d
        s_n = n * (2 * a1 + (n - 1) * d) // 2
        correct = str(s_n)

        # Distractors
        distractors = [
            str(n * a1),                                   # forgetting d
            str((n - 1) * (2 * a1 + (n - 1) * d) // 2),  # off-by-one on n
            str(a_n * n),                                  # wrong: last term * n
            str(a1 + a_n),                                 # forgetting n/2
            str(n * (a1 + a_n)),                           # forgetting /2
        ]

        options, correct_index = self._make_numeric_distractors(correct, distractors)

        question = (
            f"Uno studente risparmia {a1}€ il primo mese, e ogni mese successivo "
            f"risparmia {d}€ in più. Quanto ha risparmiato in totale dopo {n} mesi?"
        )
        explanation = (
            f"È una progressione aritmetica con a₁ = {a1}, d = {d}, n = {n}. "
            f"L'ultimo termine è a_{n} = {a1} + ({n}−1)·{d} = {a_n}. "
            f"La somma è Sₙ = n·(a₁ + aₙ)/2 = {n}·({a1} + {a_n})/2 = {s_n}€."
        )
        did_you_know = (
            "La somma dei primi n termini di una progressione aritmetica è "
            "Sₙ = n·(a₁ + aₙ)/2 = n·(2a₁ + (n−1)d)/2. "
            "Gauss scoprì questa formula da bambino sommando i numeri da 1 a 100!"
        )

        return {
            "question": question,
            "options": options,
            "correct_index": correct_index,
            "explanation": explanation,
            "did_you_know": did_you_know,
        }

    def _sequence_geometric_sum(self) -> dict:
        """L2 — Sum of first n terms of a geometric sequence (word problem)."""
        a1 = random.randint(1, 5)
        r = random.choice([2, 3])
        n = random.randint(4, 7)

        s_n = a1 * (r ** n - 1) // (r - 1)
        last_term = a1 * r ** (n - 1)
        correct = str(s_n)

        # Distractors
        distractors = [
            str(a1 * r ** n),                              # just last term * r (overshoot)
            str(a1 * (r ** (n - 1) - 1) // (r - 1)),     # off-by-one on n
            str(a1 * r * n),                               # linear approximation
            str(a1 * (r ** n + 1) // (r + 1)),            # wrong formula
            str(last_term),                                # just the last term
        ]

        options, correct_index = self._make_numeric_distractors(correct, distractors)

        verb = "raddoppia" if r == 2 else "triplica"
        question = (
            f"Una popolazione di batteri {verb} ogni ora. Inizialmente sono {a1}. "
            f"Quanti batteri ci sono in totale (somma cumulativa) dopo {n} ore?"
        )
        explanation = (
            f"È una progressione geometrica con a₁ = {a1}, r = {r}, n = {n}. "
            f"La somma è Sₙ = a₁·(rⁿ − 1)/(r − 1) = "
            f"{a1}·({r}^{n} − 1)/({r} − 1) = "
            f"{a1}·{r ** n - 1}/{r - 1} = {s_n}."
        )
        did_you_know = (
            "La somma di una progressione geometrica è Sₙ = a₁·(rⁿ − 1)/(r − 1). "
            "La crescita geometrica è sorprendentemente rapida: "
            "raddoppiando ogni giorno, un centesimo diventa oltre 10 milioni in 30 giorni!"
        )

        return {
            "question": question,
            "options": options,
            "correct_index": correct_index,
            "explanation": explanation,
            "did_you_know": did_you_know,
        }

    def _sequence_find_ratio_or_difference(self) -> dict:
        """L2 — Find common difference or ratio given two terms."""
        variant = random.choice(["arithmetic", "geometric"])

        if variant == "arithmetic":
            d = random.randint(2, 8)
            a1 = random.randint(1, 20)
            n1 = random.randint(2, 5)
            n2 = n1 + random.randint(2, 6)
            v1 = a1 + (n1 - 1) * d
            v2 = a1 + (n2 - 1) * d

            correct = str(d)

            # Distractors
            distractors = [
                str(v2 - v1),                # forgot to divide by gap
                str(abs(v2 // v1)) if v1 != 0 else "1",  # confused with ratio
                str(d + 1),                  # off-by-one
                str(d - 1) if d > 1 else "0",  # off-by-one
                str((v2 - v1) // (n2 - n1 + 1)),  # wrong gap
            ]

            options, correct_index = self._make_numeric_distractors(correct, distractors)

            question = (
                f"In una progressione aritmetica, il {n1}-esimo termine è {v1} "
                f"e il {n2}-esimo termine è {v2}. Trova la ragione d."
            )
            explanation = (
                f"La differenza tra il {n2}-esimo e il {n1}-esimo termine è "
                f"{v2} − {v1} = {v2 - v1}. Il numero di passi è {n2} − {n1} = {n2 - n1}. "
                f"Quindi d = {v2 - v1}/{n2 - n1} = {d}."
            )
            did_you_know = (
                "Per trovare la ragione di una progressione aritmetica dati due termini, "
                "basta dividere la differenza dei valori per la differenza degli indici: "
                "d = (aₘ − aₙ)/(m − n)."
            )
        else:
            # Geometric: pick r and terms so that the ratio is integer
            r = random.randint(2, 4)
            a1 = random.randint(1, 5)
            n1 = 2
            n2 = n1 + random.choice([2, 3])
            v1 = a1 * r ** (n1 - 1)
            v2 = a1 * r ** (n2 - 1)
            gap = n2 - n1

            correct = str(r)

            # Distractors
            distractors = [
                str(v2 // v1) if v1 != 0 else "1",  # forgot to take root
                str(v2 - v1),                          # confused with difference
                str(r + 1),                            # off-by-one
                str(r - 1) if r > 1 else "1",         # off-by-one
                str(r * r),                            # squared ratio
            ]

            options, correct_index = self._make_numeric_distractors(correct, distractors)

            question = (
                f"In una progressione geometrica, il {n1}-esimo termine è {v1} "
                f"e il {n2}-esimo termine è {v2}. Trova la ragione r."
            )
            explanation = (
                f"Il rapporto tra il {n2}-esimo e il {n1}-esimo termine è "
                f"{v2}/{v1} = {v2 // v1}. Il numero di passi è {n2} − {n1} = {gap}. "
                f"Quindi r^{gap} = {v2 // v1}, da cui r = {r}."
            )
            did_you_know = (
                "Per trovare la ragione di una progressione geometrica dati due termini, "
                "calcola il rapporto dei valori e poi estrai la radice appropriata: "
                "r = (aₘ/aₙ)^(1/(m−n))."
            )

        return {
            "question": question,
            "options": options,
            "correct_index": correct_index,
            "explanation": explanation,
            "did_you_know": did_you_know,
        }

    # --- L3 ---

    def _sequence_geometric_convergence(self) -> dict:
        """L3 — Sum of infinite geometric series with |r| < 1."""
        # Use fractions to avoid floating point issues
        ratio_choices = [
            (1, 2, "1/2", "50%"),
            (1, 3, "1/3", "33%"),
            (2, 3, "2/3", "67%"),
            (1, 4, "1/4", "25%"),
            (3, 4, "3/4", "75%"),
        ]
        r_num, r_den, r_str, r_percent = random.choice(ratio_choices)
        a1 = random.randint(1, 10)

        # S_inf = a1 / (1 - r) = a1 / ((r_den - r_num) / r_den) = a1 * r_den / (r_den - r_num)
        numerator = a1 * r_den
        denominator = r_den - r_num

        if numerator % denominator == 0:
            correct_val = numerator // denominator
            correct = str(correct_val)
        else:
            f = Fraction(numerator, denominator)
            correct = f"{f.numerator}/{f.denominator}"

        # Distractors
        # a1/(1+r) instead of a1/(1-r)
        d1_num = a1 * r_den
        d1_den = r_den + r_num
        if d1_num % d1_den == 0:
            d1 = str(d1_num // d1_den)
        else:
            f1 = Fraction(d1_num, d1_den)
            d1 = f"{f1.numerator}/{f1.denominator}"

        # a1/r
        if a1 % r_num == 0 and r_den == 1:
            d2 = str(a1 * r_den // r_num)
        else:
            f2 = Fraction(a1 * r_den, r_num)
            d2 = f"{f2.numerator}/{f2.denominator}" if f2.denominator != 1 else str(f2.numerator)

        # a1*(1-r) = a1 * (r_den - r_num) / r_den
        d3_num = a1 * (r_den - r_num)
        d3_den = r_den
        if d3_num % d3_den == 0:
            d3 = str(d3_num // d3_den)
        else:
            f3 = Fraction(d3_num, d3_den)
            d3 = f"{f3.numerator}/{f3.denominator}"

        d4 = "la serie diverge"

        distractors = [d1, d2, d3, d4, str(a1)]

        options, correct_index = self._make_numeric_distractors(correct, distractors)

        question = (
            f"Calcola la somma della serie geometrica infinita con "
            f"a₁ = {a1} e r = {r_str}."
        )
        explanation = (
            f"Per una serie geometrica con |r| < 1, la somma è S∞ = a₁/(1−r). "
            f"Qui S∞ = {a1}/(1 − {r_str}) = {a1}/{denominator}/{r_den} = "
            f"{a1} · {r_den}/{denominator} = {correct}."
        )
        did_you_know = (
            "Una serie geometrica converge (ha somma finita) solo se |r| < 1. "
            "La formula S∞ = a₁/(1−r) è usata in finanza per calcolare "
            "il valore attuale di rendite perpetue."
        )

        return {
            "question": question,
            "options": options,
            "correct_index": correct_index,
            "explanation": explanation,
            "did_you_know": did_you_know,
        }

    def _sequence_mixed_problem(self) -> dict:
        """L3 — Identify sequence type and find the next term."""
        variant = random.choice(["arithmetic", "geometric"])

        if variant == "arithmetic":
            a1 = random.randint(1, 20)
            d = random.randint(2, 8)
            terms = [a1 + i * d for i in range(4)]
            next_term = a1 + 4 * d

            # What if it were geometric? Fake next term
            if terms[1] != 0 and terms[0] != 0:
                fake_ratio = terms[1] / terms[0]
                geometric_next = int(round(terms[3] * fake_ratio))
            else:
                geometric_next = next_term + d

            correct = str(next_term)
            distractors = [
                str(geometric_next),       # if mistaken for geometric
                str(next_term + 1),        # off-by-one
                str(next_term - 1),        # off-by-one
                str(next_term + d),        # skipped one term
                str(terms[3]),             # repeated last
            ]
        else:
            a1 = random.randint(2, 5)
            r = random.randint(2, 3)
            terms = [a1 * r ** i for i in range(4)]
            next_term = a1 * r ** 4

            # What if it were arithmetic? Fake next term
            fake_d = terms[1] - terms[0]
            arithmetic_next = terms[3] + fake_d

            correct = str(next_term)
            distractors = [
                str(arithmetic_next),      # if mistaken for arithmetic
                str(next_term * r),        # one too far
                str(terms[3] + terms[2]),  # addition instead of multiplication
                str(next_term + 1),        # off-by-one
                str(a1 * r ** 3),          # repeated last
            ]

        options, correct_index = self._make_numeric_distractors(correct, distractors)

        t_str = ", ".join(str(t) for t in terms)
        question = (
            f"Data la successione {t_str}, qual è il termine successivo?"
        )

        if variant == "arithmetic":
            explanation = (
                f"La differenza tra termini consecutivi è costante: "
                f"{terms[1]} − {terms[0]} = {d}. "
                f"È una progressione aritmetica con d = {d}. "
                f"Il termine successivo è {terms[3]} + {d} = {next_term}."
            )
        else:
            explanation = (
                f"Il rapporto tra termini consecutivi è costante: "
                f"{terms[1]}/{terms[0]} = {r}. "
                f"È una progressione geometrica con r = {r}. "
                f"Il termine successivo è {terms[3]} · {r} = {next_term}."
            )

        did_you_know = (
            "Per riconoscere il tipo di successione: se la differenza tra termini "
            "consecutivi è costante, è aritmetica; se il rapporto è costante, "
            "è geometrica. Controlla sempre entrambe le possibilità!"
        )

        return {
            "question": question,
            "options": options,
            "correct_index": correct_index,
            "explanation": explanation,
            "did_you_know": did_you_know,
        }

    def _division_remainder_properties(self) -> dict:
        """L2 — Properties of remainders with related divisors."""
        # Pick d1 and d2 where d2 divides d1
        pairs = [
            (6, 3), (6, 2), (8, 4), (8, 2), (10, 5), (10, 2),
            (12, 6), (12, 4), (12, 3), (12, 2), (9, 3), (15, 5), (15, 3),
        ]
        d1, d2 = random.choice(pairs)

        # Pick a remainder r1 for division by d1 (non-zero)
        r1 = random.randint(1, d1 - 1)

        # The remainder of n divided by d2 is r1 % d2
        correct_r2 = r1 % d2

        correct = str(correct_r2)

        # Distractors: other possible remainders for d2
        distractors = []
        for candidate in range(0, d2):
            if candidate != correct_r2:
                distractors.append(str(candidate))
        # Add some plausible wrong answers
        distractors.append(str(r1))           # use the original remainder
        distractors.append(str(d2 - correct_r2) if correct_r2 != 0 else str(d2 - 1))
        distractors.append(str(d1 - r1))      # complement in d1

        options, correct_index = self._make_numeric_distractors(correct, distractors)

        question = (
            f"Se il resto della divisione di n per {d1} è {r1}, "
            f"quale potrebbe essere il resto della divisione di n per {d2}?"
        )
        explanation = (
            f"Se n = k × {d1} + {r1} per qualche intero k, allora poiché {d1} è "
            f"divisibile per {d2}, abbiamo n = k × {d1} + {r1}. "
            f"Dividendo {r1} per {d2}: {r1} ÷ {d2} = {r1 // d2} con resto {correct_r2}. "
            f"Quindi il resto di n ÷ {d2} è {correct_r2}."
        )
        did_you_know = (
            "Se d2 divide d1, allora il resto di n diviso d2 dipende solo dal resto "
            "di n diviso d1. In particolare, se n ha resto r1 nella divisione per d1, "
            "allora il resto nella divisione per d2 è semplicemente r1 mod d2."
        )

        return {
            "question": question,
            "options": options,
            "correct_index": correct_index,
            "explanation": explanation,
            "did_you_know": did_you_know,
        }
