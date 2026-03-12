import math
import random
from fractions import Fraction

from exercises.base import Exercise


class ProbabilityGame(Exercise):
    """Probabilita' Visuale: visualize sample spaces and compute probabilities."""

    # ------------------------------------------------------------------ colours
    _GREEN = "#27ae60"
    _RED = "#e74c3c"
    _BLUE = "#2980b9"
    _GREY = "#95a5a6"
    _DARK = "#2c3e50"

    # ------------------------------------------------------------------ public
    def generate(self, difficulty: int) -> dict:
        difficulty = max(1, min(3, difficulty))

        if difficulty == 1:
            templates = [
                self._die_single_value,
                self._die_single_even_odd,
                self._die_single_greater,
                self._card_single_suit,
                self._card_single_figure,
                self._urn_single_color,
            ]
        elif difficulty == 2:
            templates = [
                self._two_dice_sum,
                self._two_dice_both_even,
                self._two_cards_same_suit,
                self._urn_two_draws_no_replacement,
                self._urn_two_draws_with_replacement,
                self._at_least_one_six,
                self._comb_permutazioni_semplici,
                self._comb_combinazioni,
                self._comb_principio_conteggio,
                self._comb_disposizioni,
            ]
        else:
            templates = [
                self._conditional_die,
                self._conditional_cards,
                self._conditional_urn,
                self._bayes_urn,
                self._comb_combinazioni_con_condizione,
                self._comb_inclusione_esclusione,
                self._comb_permutazioni_con_ripetizione,
                self._comb_probabilita_combinatorica,
            ]

        template_fn = random.choice(templates)
        return template_fn(difficulty)

    # ------------------------------------------------------------------ SVG helpers
    @staticmethod
    def _svg_wrap(inner: str, width: int = 400, height: int = 300) -> str:
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'viewBox="0 0 {width} {height}" '
            f'width="{width}" height="{height}" '
            f'style="font-family:sans-serif;font-size:12px;">'
            f"{inner}</svg>"
        )

    @classmethod
    def _svg_branch(cls, x1, y1, x2, y2, label, color=None, bold=False):
        c = color or cls._DARK
        sw = "2" if bold else "1.2"
        fw = "bold" if bold else "normal"
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        return (
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="{c}" stroke-width="{sw}"/>'
            f'<text x="{mx - 5}" y="{my - 5}" fill="{c}" '
            f'font-weight="{fw}" font-size="11">{label}</text>'
        )

    @classmethod
    def _svg_node(cls, x, y, label, color=None, radius=14):
        c = color or cls._GREY
        return (
            f'<circle cx="{x}" cy="{y}" r="{radius}" fill="{c}" opacity="0.25"/>'
            f'<text x="{x}" y="{y + 4}" text-anchor="middle" '
            f'fill="{cls._DARK}" font-size="10" font-weight="bold">{label}</text>'
        )

    def _build_single_event_tree(self, outcomes, probs, favourable_set, root_label="Evento"):
        """Build an SVG tree for a single event with multiple outcomes."""
        n = len(outcomes)
        w = max(400, n * 70)
        h = 180
        root_x, root_y = w // 2, 30
        parts = [self._svg_node(root_x, root_y, root_label, self._BLUE)]

        spacing = min(70, (w - 40) / max(n - 1, 1))
        start_x = root_x - spacing * (n - 1) / 2

        for i, (out, p) in enumerate(zip(outcomes, probs)):
            cx = start_x + i * spacing
            cy = 140
            is_fav = i in favourable_set
            color = self._GREEN if is_fav else self._RED
            parts.append(self._svg_branch(root_x, root_y + 14, cx, cy - 14, str(p), color, is_fav))
            parts.append(self._svg_node(cx, cy, str(out), color))

        return self._svg_wrap("".join(parts), w, h)

    def _build_two_event_tree(self, event1_outcomes, event1_probs,
                              event2_outcomes_fn, event2_probs_fn,
                              is_favourable_fn, label1="E1", label2="E2"):
        """Build an SVG tree for two sequential events."""
        n1 = len(event1_outcomes)
        n2_max = max(len(event2_outcomes_fn(o)) for o in event1_outcomes)
        w = max(500, n1 * n2_max * 55)
        h = 300
        root_x, root_y = w // 2, 25
        parts = [self._svg_node(root_x, root_y, label1, self._BLUE)]

        block_w = w / n1
        for i, (o1, p1) in enumerate(zip(event1_outcomes, event1_probs)):
            mid_x = block_w * i + block_w / 2
            mid_y = 110
            parts.append(self._svg_branch(root_x, root_y + 14, mid_x, mid_y - 14, str(p1)))
            parts.append(self._svg_node(mid_x, mid_y, str(o1), self._BLUE))

            e2_outcomes = event2_outcomes_fn(o1)
            e2_probs = event2_probs_fn(o1)
            n2 = len(e2_outcomes)
            sub_spacing = min(50, (block_w - 10) / max(n2 - 1, 1))
            sub_start = mid_x - sub_spacing * (n2 - 1) / 2

            for j, (o2, p2) in enumerate(zip(e2_outcomes, e2_probs)):
                leaf_x = sub_start + j * sub_spacing
                leaf_y = 250
                is_fav = is_favourable_fn(o1, o2)
                color = self._GREEN if is_fav else self._RED
                parts.append(self._svg_branch(mid_x, mid_y + 14, leaf_x, leaf_y - 14,
                                              str(p2), color, is_fav))
                parts.append(self._svg_node(leaf_x, leaf_y, str(o2), color, 12))

        return self._svg_wrap("".join(parts), w, h)

    @staticmethod
    def _frac_str(f: Fraction) -> str:
        if f.denominator == 1:
            return str(f.numerator)
        return f"{f.numerator}/{f.denominator}"

    def _make_distractors(self, correct: Fraction, count: int = 4) -> list:
        """Generate plausible wrong answers near the correct fraction."""
        distractors = set()
        attempts = 0
        candidates = []

        n, d = correct.numerator, correct.denominator
        candidates.extend([
            Fraction(n + 1, d) if n + 1 <= d else None,
            Fraction(max(n - 1, 0), d) if n - 1 >= 0 else None,
            Fraction(n, d + 1),
            Fraction(n, max(d - 1, 1)) if d > 1 else None,
            Fraction(d - n, d) if d - n > 0 else None,
            Fraction(n * 2, d * 2 + 1) if n * 2 <= d * 2 + 1 else None,
            Fraction(n + 1, d + 1) if n + 1 <= d + 1 else None,
            Fraction(1, d),
            Fraction(n, d * 2),
            Fraction(min(n + 2, d), d),
        ])

        for c in candidates:
            if c is not None and Fraction(0) <= c <= Fraction(1) and c != correct:
                distractors.add(c)
            if len(distractors) >= count:
                break

        while len(distractors) < count and attempts < 50:
            attempts += 1
            rand_n = random.randint(0, d + 2)
            rand_d = random.randint(max(1, d - 2), d + 3)
            f = Fraction(rand_n, rand_d)
            if Fraction(0) <= f <= Fraction(1) and f != correct:
                distractors.add(f)

        return list(distractors)[:count]

    def _make_int_distractors(self, correct: int, count: int = 4) -> list:
        """Generate plausible wrong integer answers near the correct value."""
        distractors = set()
        candidates = []

        candidates.extend([
            correct + 1,
            correct - 1 if correct > 1 else correct + 2,
            correct * 2,
            correct // 2 if correct > 2 else correct + 3,
            correct + random.randint(2, 5),
            correct - random.randint(2, min(5, max(2, correct - 1))) if correct > 3 else correct + random.randint(3, 7),
            correct * 3,
            correct + 10,
        ])

        for c in candidates:
            if c > 0 and c != correct:
                distractors.add(c)
            if len(distractors) >= count:
                break

        attempts = 0
        while len(distractors) < count and attempts < 50:
            attempts += 1
            delta = random.randint(1, max(10, correct))
            val = correct + random.choice([-1, 1]) * delta
            if val > 0 and val != correct:
                distractors.add(val)

        return list(distractors)[:count]

    def _build_int_result(self, question, correct_int, distractors_int, svg, explanation, did_you_know):
        """Build result dict for combinatorics problems with integer answers."""
        options = [str(correct_int)] + [str(d) for d in distractors_int]
        correct_index = 0
        options, correct_index = self.shuffle_options(options, correct_index)

        return {
            "question": question,
            "options": options,
            "correct_index": correct_index,
            "graph_data": svg,
            "explanation": explanation,
            "did_you_know": did_you_know,
        }

    def _build_result(self, question, correct, distractors, svg, explanation, did_you_know):
        options = [self._frac_str(correct)] + [self._frac_str(d) for d in distractors]
        correct_index = 0
        options, correct_index = self.shuffle_options(options, correct_index)

        return {
            "question": question,
            "options": options,
            "correct_index": correct_index,
            "graph_data": svg,
            "explanation": explanation,
            "did_you_know": did_you_know,
        }

    # ==================================================================
    #  LEVEL 1 TEMPLATES (single event)
    # ==================================================================

    # Template 1: Single die - specific value
    def _die_single_value(self, difficulty: int) -> dict:
        target = random.randint(1, 6)
        correct = Fraction(1, 6)
        outcomes = list(range(1, 7))
        probs = [Fraction(1, 6)] * 6
        fav = {target - 1}

        svg = self._build_single_event_tree(outcomes, probs, fav, "Dado")
        distractors = self._make_distractors(correct)

        return self._build_result(
            question=f"Si lancia un dado a 6 facce. Qual e' la probabilita' di ottenere {target}?",
            correct=correct,
            distractors=distractors,
            svg=svg,
            explanation=(
                f"Lo spazio campionario ha 6 risultati equiprobabili: {{1, 2, 3, 4, 5, 6}}. "
                f"L'evento favorevole e' {{{target}}}, quindi P = 1/6."
            ),
            did_you_know=(
                "In un dado equilibrato, ogni faccia ha probabilita' 1/6. "
                "La somma di tutte le probabilita' e' sempre 1."
            ),
        )

    # Template 2: Single die - even or odd
    def _die_single_even_odd(self, difficulty: int) -> dict:
        is_even = random.choice([True, False])
        label = "pari" if is_even else "dispari"
        target_set = {2, 4, 6} if is_even else {1, 3, 5}
        correct = Fraction(3, 6)
        outcomes = list(range(1, 7))
        probs = [Fraction(1, 6)] * 6
        fav = {i for i, v in enumerate(outcomes) if v in target_set}

        svg = self._build_single_event_tree(outcomes, probs, fav, "Dado")
        distractors = self._make_distractors(correct)

        return self._build_result(
            question=f"Si lancia un dado a 6 facce. Qual e' la probabilita' di ottenere un numero {label}?",
            correct=correct,
            distractors=distractors,
            svg=svg,
            explanation=(
                f"I numeri {label} su un dado sono {sorted(target_set)}. "
                f"Sono 3 su 6 risultati possibili, quindi P = 3/6 = 1/2."
            ),
            did_you_know=(
                "Quando l'evento copre esattamente meta' dello spazio campionario, "
                "la probabilita' e' 1/2. Questo accade per pari/dispari su un dado."
            ),
        )

    # Template 3: Single die - greater than N
    def _die_single_greater(self, difficulty: int) -> dict:
        threshold = random.randint(2, 5)
        favourable = [v for v in range(1, 7) if v > threshold]
        correct = Fraction(len(favourable), 6)
        outcomes = list(range(1, 7))
        probs = [Fraction(1, 6)] * 6
        fav = {i for i, v in enumerate(outcomes) if v > threshold}

        svg = self._build_single_event_tree(outcomes, probs, fav, "Dado")
        distractors = self._make_distractors(correct)

        return self._build_result(
            question=(
                f"Si lancia un dado a 6 facce. Qual e' la probabilita' "
                f"di ottenere un numero maggiore di {threshold}?"
            ),
            correct=correct,
            distractors=distractors,
            svg=svg,
            explanation=(
                f"I numeri maggiori di {threshold} sono {favourable}. "
                f"Sono {len(favourable)} su 6, quindi P = {len(favourable)}/6"
                f"{' = ' + self._frac_str(correct) if correct != Fraction(len(favourable), 6) else ''}."
            ),
            did_you_know=(
                "Per calcolare P(X > k), conta i risultati favorevoli e dividi "
                "per il numero totale di risultati possibili."
            ),
        )

    # Template 4: Single card draw - suit
    def _card_single_suit(self, difficulty: int) -> dict:
        suits = ["cuori", "quadri", "fiori", "picche"]
        suit = random.choice(suits)
        correct = Fraction(13, 52)
        suit_symbols = {"cuori": "\u2665", "quadri": "\u2666", "fiori": "\u2663", "picche": "\u2660"}
        all_symbols = [suit_symbols[s] for s in suits]
        probs = [Fraction(13, 52)] * 4
        fav = {suits.index(suit)}

        svg = self._build_single_event_tree(all_symbols, probs, fav, "Carta")
        distractors = self._make_distractors(correct)

        return self._build_result(
            question=(
                f"Si estrae una carta da un mazzo di 52. "
                f"Qual e' la probabilita' che sia di {suit}?"
            ),
            correct=correct,
            distractors=distractors,
            svg=svg,
            explanation=(
                f"In un mazzo da 52 carte ci sono 13 carte di {suit}. "
                f"P = 13/52 = 1/4."
            ),
            did_you_know=(
                "Un mazzo standard ha 52 carte: 4 semi (cuori, quadri, fiori, picche) "
                "con 13 carte ciascuno (A, 2-10, J, Q, K)."
            ),
        )

    # Template 5: Single card draw - figure (J, Q, K)
    def _card_single_figure(self, difficulty: int) -> dict:
        correct = Fraction(12, 52)
        outcomes = ["A", "2-10", "J", "Q", "K"]
        probs = [Fraction(4, 52), Fraction(36, 52), Fraction(4, 52), Fraction(4, 52), Fraction(4, 52)]
        fav = {2, 3, 4}

        svg = self._build_single_event_tree(outcomes, probs, fav, "Carta")
        distractors = self._make_distractors(correct)

        return self._build_result(
            question=(
                "Si estrae una carta da un mazzo di 52. "
                "Qual e' la probabilita' che sia una figura (J, Q o K)?"
            ),
            correct=correct,
            distractors=distractors,
            svg=svg,
            explanation=(
                "Le figure sono J, Q, K in ciascuno dei 4 semi: 3 x 4 = 12 carte. "
                "P = 12/52 = 3/13."
            ),
            did_you_know=(
                "Le figure (Jack, Queen, King) rappresentano personaggi storici "
                "in molte tradizioni di carte. Ci sono 12 figure su 52 carte."
            ),
        )

    # Template 6: Urn - single color extraction
    def _urn_single_color(self, difficulty: int) -> dict:
        colors = ["rosse", "blu", "verdi"]
        counts = [random.randint(2, 6) for _ in range(3)]
        total = sum(counts)
        target_idx = random.randint(0, 2)
        target_color = colors[target_idx]
        correct = Fraction(counts[target_idx], total)

        probs = [Fraction(c, total) for c in counts]
        fav = {target_idx}
        color_labels = [f"{colors[i]}({counts[i]})" for i in range(3)]

        svg = self._build_single_event_tree(color_labels, probs, fav, "Urna")
        distractors = self._make_distractors(correct)

        return self._build_result(
            question=(
                f"Un'urna contiene {counts[0]} palline rosse, {counts[1]} blu e {counts[2]} verdi. "
                f"Si estrae una pallina a caso. Qual e' la probabilita' che sia {target_color}?"
            ),
            correct=correct,
            distractors=distractors,
            svg=svg,
            explanation=(
                f"Ci sono {counts[target_idx]} palline {target_color} su {total} totali. "
                f"P = {counts[target_idx]}/{total}"
                f"{' = ' + self._frac_str(correct) if correct != Fraction(counts[target_idx], total) else ''}."
            ),
            did_you_know=(
                "Il modello dell'urna e' alla base della probabilita' classica: "
                "P(evento) = casi favorevoli / casi possibili."
            ),
        )

    # ==================================================================
    #  LEVEL 2 TEMPLATES (two sequential events)
    # ==================================================================

    # Template 7: Two dice - sum equals target
    def _two_dice_sum(self, difficulty: int) -> dict:
        target_sum = random.choice([5, 6, 7, 8, 9])
        favourable = [(a, b) for a in range(1, 7) for b in range(1, 7) if a + b == target_sum]
        correct = Fraction(len(favourable), 36)

        outcomes1 = list(range(1, 7))
        probs1 = [Fraction(1, 6)] * 6

        def e2_out(o1):
            return list(range(1, 7))

        def e2_probs(o1):
            return [Fraction(1, 6)] * 6

        def is_fav(o1, o2):
            return o1 + o2 == target_sum

        svg = self._build_two_event_tree(
            [1, 2, 3], [Fraction(1, 6)] * 3,
            lambda o1: [1, 2, 3],
            lambda o1: [Fraction(1, 6)] * 3,
            is_fav, "D1", "D2"
        )

        distractors = self._make_distractors(correct)
        pairs_str = ", ".join(f"({a},{b})" for a, b in favourable)

        return self._build_result(
            question=(
                f"Si lanciano due dadi a 6 facce. "
                f"Qual e' la probabilita' che la somma sia {target_sum}?"
            ),
            correct=correct,
            distractors=distractors,
            svg=svg,
            explanation=(
                f"Lo spazio campionario ha 6x6 = 36 coppie. "
                f"Le coppie con somma {target_sum} sono: {pairs_str}. "
                f"Sono {len(favourable)} su 36, quindi P = {self._frac_str(correct)}."
            ),
            did_you_know=(
                "La somma piu' probabile con due dadi e' 7, con probabilita' 6/36 = 1/6. "
                "Le somme vicine a 7 sono piu' probabili di quelle estreme (2 o 12)."
            ),
        )

    # Template 8: Two dice - both even
    def _two_dice_both_even(self, difficulty: int) -> dict:
        correct = Fraction(9, 36)

        def is_fav(o1, o2):
            return o1 % 2 == 0 and o2 % 2 == 0

        svg = self._build_two_event_tree(
            ["P", "D"], [Fraction(1, 2)] * 2,
            lambda o1: ["P", "D"],
            lambda o1: [Fraction(1, 2)] * 2,
            lambda o1, o2: o1 == "P" and o2 == "P",
            "D1", "D2"
        )

        distractors = self._make_distractors(correct)

        return self._build_result(
            question=(
                "Si lanciano due dadi a 6 facce. "
                "Qual e' la probabilita' che entrambi diano un numero pari?"
            ),
            correct=correct,
            distractors=distractors,
            svg=svg,
            explanation=(
                "P(pari su un dado) = 3/6 = 1/2. "
                "I dadi sono indipendenti, quindi P(entrambi pari) = 1/2 x 1/2 = 1/4 = 9/36."
            ),
            did_you_know=(
                "Per eventi indipendenti: P(A e B) = P(A) x P(B). "
                "Due lanci di dado sono sempre eventi indipendenti."
            ),
        )

    # Template 9: Two cards same suit (with replacement)
    def _two_cards_same_suit(self, difficulty: int) -> dict:
        suit = random.choice(["cuori", "quadri", "fiori", "picche"])
        correct = Fraction(13, 52) * Fraction(12, 51)

        svg_parts = []
        svg_parts.append(self._svg_node(200, 25, "Mazzo", self._BLUE))
        svg_parts.append(self._svg_branch(200, 39, 100, 96, "13/52", self._GREEN, True))
        svg_parts.append(self._svg_branch(200, 39, 300, 96, "39/52", self._RED, False))
        svg_parts.append(self._svg_node(100, 110, suit[:3], self._GREEN))
        svg_parts.append(self._svg_node(300, 110, "altro", self._RED))
        svg_parts.append(self._svg_branch(100, 124, 60, 236, "12/51", self._GREEN, True))
        svg_parts.append(self._svg_branch(100, 124, 140, 236, "39/51", self._RED, False))
        svg_parts.append(self._svg_node(60, 250, suit[:3], self._GREEN, 12))
        svg_parts.append(self._svg_node(140, 250, "altro", self._RED, 12))
        svg = self._svg_wrap("".join(svg_parts))

        distractors = self._make_distractors(correct)

        return self._build_result(
            question=(
                f"Si estraggono 2 carte da un mazzo di 52, senza rimettere la prima. "
                f"Qual e' la probabilita' che entrambe siano di {suit}?"
            ),
            correct=correct,
            distractors=distractors,
            svg=svg,
            explanation=(
                f"Prima carta di {suit}: 13/52. "
                f"Seconda carta di {suit} (senza rimpiazzo): 12/51. "
                f"P = 13/52 x 12/51 = {self._frac_str(correct)}."
            ),
            did_you_know=(
                "Senza rimpiazzo, la seconda estrazione dipende dalla prima: "
                "il mazzo ha una carta in meno. Questo rende gli eventi dipendenti."
            ),
        )

    # Template 10: Urn - two draws without replacement
    def _urn_two_draws_no_replacement(self, difficulty: int) -> dict:
        r = random.randint(3, 6)
        b = random.randint(3, 6)
        total = r + b
        target = random.choice(["rosse", "blu"])
        t_count = r if target == "rosse" else b

        correct = Fraction(t_count, total) * Fraction(t_count - 1, total - 1)

        svg_parts = []
        svg_parts.append(self._svg_node(200, 25, "Urna", self._BLUE))
        p1 = Fraction(t_count, total)
        p1c = Fraction(total - t_count, total)
        svg_parts.append(self._svg_branch(200, 39, 100, 96, self._frac_str(p1), self._GREEN, True))
        svg_parts.append(self._svg_branch(200, 39, 300, 96, self._frac_str(p1c), self._RED, False))
        svg_parts.append(self._svg_node(100, 110, target[:3], self._GREEN))
        svg_parts.append(self._svg_node(300, 110, "altra", self._RED))

        p2 = Fraction(t_count - 1, total - 1)
        p2c = Fraction(total - t_count, total - 1)
        svg_parts.append(self._svg_branch(100, 124, 60, 236, self._frac_str(p2), self._GREEN, True))
        svg_parts.append(self._svg_branch(100, 124, 140, 236, self._frac_str(p2c), self._RED, False))
        svg_parts.append(self._svg_node(60, 250, target[:3], self._GREEN, 12))
        svg_parts.append(self._svg_node(140, 250, "altra", self._RED, 12))
        svg = self._svg_wrap("".join(svg_parts))

        distractors = self._make_distractors(correct)

        return self._build_result(
            question=(
                f"Un'urna contiene {r} palline rosse e {b} blu. "
                f"Si estraggono 2 palline senza rimpiazzo. "
                f"Qual e' la probabilita' che siano entrambe {target}?"
            ),
            correct=correct,
            distractors=distractors,
            svg=svg,
            explanation=(
                f"Prima estrazione {target}: {t_count}/{total}. "
                f"Seconda {target} (senza rimpiazzo): {t_count - 1}/{total - 1}. "
                f"P = {t_count}/{total} x {t_count - 1}/{total - 1} = {self._frac_str(correct)}."
            ),
            did_you_know=(
                "Estrazione senza rimpiazzo: dopo ogni estrazione, il totale diminuisce. "
                "La probabilita' della seconda estrazione dipende dalla prima."
            ),
        )

    # Template 11: Urn - two draws with replacement
    def _urn_two_draws_with_replacement(self, difficulty: int) -> dict:
        r = random.randint(2, 5)
        b = random.randint(2, 5)
        total = r + b
        target = random.choice(["rosse", "blu"])
        t_count = r if target == "rosse" else b

        p_single = Fraction(t_count, total)
        correct = p_single * p_single

        svg_parts = []
        svg_parts.append(self._svg_node(200, 25, "Urna", self._BLUE))
        svg_parts.append(self._svg_branch(200, 39, 100, 96, self._frac_str(p_single), self._GREEN, True))
        p_other = Fraction(total - t_count, total)
        svg_parts.append(self._svg_branch(200, 39, 300, 96, self._frac_str(p_other), self._RED, False))
        svg_parts.append(self._svg_node(100, 110, target[:3], self._GREEN))
        svg_parts.append(self._svg_node(300, 110, "altra", self._RED))

        svg_parts.append(self._svg_branch(100, 124, 60, 236, self._frac_str(p_single), self._GREEN, True))
        svg_parts.append(self._svg_branch(100, 124, 140, 236, self._frac_str(p_other), self._RED, False))
        svg_parts.append(self._svg_node(60, 250, target[:3], self._GREEN, 12))
        svg_parts.append(self._svg_node(140, 250, "altra", self._RED, 12))
        svg = self._svg_wrap("".join(svg_parts))

        distractors = self._make_distractors(correct)

        return self._build_result(
            question=(
                f"Un'urna contiene {r} palline rosse e {b} blu. "
                f"Si estraggono 2 palline CON rimpiazzo. "
                f"Qual e' la probabilita' che siano entrambe {target}?"
            ),
            correct=correct,
            distractors=distractors,
            svg=svg,
            explanation=(
                f"Con rimpiazzo, ogni estrazione ha la stessa probabilita': {self._frac_str(p_single)}. "
                f"P = {self._frac_str(p_single)} x {self._frac_str(p_single)} = {self._frac_str(correct)}."
            ),
            did_you_know=(
                "Con rimpiazzo, le estrazioni sono indipendenti: la pallina viene rimessa "
                "nell'urna, quindi le probabilita' non cambiano."
            ),
        )

    # Template 12: At least one 6 with two dice
    def _at_least_one_six(self, difficulty: int) -> dict:
        p_no_six = Fraction(5, 6) * Fraction(5, 6)
        correct = Fraction(1, 1) - p_no_six

        svg_parts = []
        svg_parts.append(self._svg_node(200, 25, "D1", self._BLUE))
        svg_parts.append(self._svg_branch(200, 39, 100, 96, "1/6", self._GREEN, True))
        svg_parts.append(self._svg_branch(200, 39, 300, 96, "5/6", self._GREY, False))
        svg_parts.append(self._svg_node(100, 110, "6", self._GREEN))
        svg_parts.append(self._svg_node(300, 110, "non 6", self._GREY))

        svg_parts.append(self._svg_branch(100, 124, 60, 236, "1/6", self._GREEN, True))
        svg_parts.append(self._svg_branch(100, 124, 140, 236, "5/6", self._GREEN, True))
        svg_parts.append(self._svg_node(60, 250, "6", self._GREEN, 12))
        svg_parts.append(self._svg_node(140, 250, "non 6", self._GREEN, 12))

        svg_parts.append(self._svg_branch(300, 124, 260, 236, "1/6", self._GREEN, True))
        svg_parts.append(self._svg_branch(300, 124, 340, 236, "5/6", self._RED, False))
        svg_parts.append(self._svg_node(260, 250, "6", self._GREEN, 12))
        svg_parts.append(self._svg_node(340, 250, "non 6", self._RED, 12))
        svg = self._svg_wrap("".join(svg_parts))

        distractors = self._make_distractors(correct)

        return self._build_result(
            question=(
                "Si lanciano due dadi. Qual e' la probabilita' "
                "di ottenere almeno un 6?"
            ),
            correct=correct,
            distractors=distractors,
            svg=svg,
            explanation=(
                "Usiamo il complementare: P(almeno un 6) = 1 - P(nessun 6). "
                "P(nessun 6) = 5/6 x 5/6 = 25/36. "
                f"P(almeno un 6) = 1 - 25/36 = {self._frac_str(correct)}."
            ),
            did_you_know=(
                "Il trucco 'almeno uno' = 1 - P(nessuno) e' fondamentale: "
                "e' quasi sempre piu' facile calcolare il complementare."
            ),
        )

    # ==================================================================
    #  LEVEL 3 TEMPLATES (conditional probability)
    # ==================================================================

    # Template 13: Conditional probability with die
    def _conditional_die(self, difficulty: int) -> dict:
        threshold = random.choice([3, 4])
        target = random.choice(["pari", "dispari"])
        given_set = set(range(threshold + 1, 7))
        if target == "pari":
            target_set = {2, 4, 6}
        else:
            target_set = {1, 3, 5}

        both = given_set & target_set
        correct = Fraction(len(both), len(given_set))

        outcomes = list(range(1, 7))
        probs = [Fraction(1, 6)] * 6
        fav_given = {i for i, v in enumerate(outcomes) if v in given_set}
        fav_both = {i for i, v in enumerate(outcomes) if v in both}

        inner = []
        inner.append(self._svg_node(200, 25, "Dado", self._BLUE))
        spacing = 55
        start_x = 200 - spacing * 2.5
        for i, v in enumerate(outcomes):
            cx = start_x + i * spacing
            cy = 100
            if v in both:
                color = self._GREEN
            elif v in given_set:
                color = self._BLUE
            else:
                color = self._RED
            inner.append(self._svg_branch(200, 39, cx, cy - 14, "1/6", color, v in both))
            inner.append(self._svg_node(cx, cy, str(v), color))

        inner.append(
            f'<text x="200" y="150" text-anchor="middle" fill="{self._DARK}" font-size="11">'
            f'Blu = dato (>{threshold}) | Verde = favorevole ({target} e >{threshold})</text>'
        )
        svg = self._svg_wrap("".join(inner), 400, 170)

        distractors = self._make_distractors(correct)

        return self._build_result(
            question=(
                f"Si lancia un dado. Sapendo che il risultato e' maggiore di {threshold}, "
                f"qual e' la probabilita' che sia {target}?"
            ),
            correct=correct,
            distractors=distractors,
            svg=svg,
            explanation=(
                f"Dato che il risultato e' > {threshold}, lo spazio si riduce a {sorted(given_set)}. "
                f"Tra questi, i numeri {target} sono {sorted(both)}. "
                f"P({target} | > {threshold}) = {len(both)}/{len(given_set)} = {self._frac_str(correct)}."
            ),
            did_you_know=(
                "La probabilita' condizionata P(A|B) = P(A e B) / P(B) restringe "
                "lo spazio campionario ai soli casi in cui B si e' verificato."
            ),
        )

    # Template 14: Conditional probability with cards
    def _conditional_cards(self, difficulty: int) -> dict:
        condition = random.choice(["rossa", "nera"])
        if condition == "rossa":
            given_count = 26
            figure_in_given = 6
        else:
            given_count = 26
            figure_in_given = 6

        correct = Fraction(figure_in_given, given_count)

        svg_parts = []
        svg_parts.append(self._svg_node(200, 25, "Mazzo", self._BLUE))
        svg_parts.append(self._svg_branch(200, 39, 100, 96, "26/52", self._BLUE, True))
        svg_parts.append(self._svg_branch(200, 39, 300, 96, "26/52", self._RED, False))
        svg_parts.append(self._svg_node(100, 110, condition[:3], self._BLUE))
        svg_parts.append(self._svg_node(300, 110, "altra", self._RED))

        svg_parts.append(self._svg_branch(100, 124, 50, 236, f"{figure_in_given}/26", self._GREEN, True))
        svg_parts.append(self._svg_branch(100, 124, 150, 236, f"{given_count - figure_in_given}/26", self._GREY, False))
        svg_parts.append(self._svg_node(50, 250, "fig.", self._GREEN, 12))
        svg_parts.append(self._svg_node(150, 250, "non fig.", self._GREY, 12))
        svg = self._svg_wrap("".join(svg_parts))

        distractors = self._make_distractors(correct)

        return self._build_result(
            question=(
                f"Si estrae una carta da un mazzo di 52. "
                f"Sapendo che la carta e' {condition}, qual e' la probabilita' che sia una figura?"
            ),
            correct=correct,
            distractors=distractors,
            svg=svg,
            explanation=(
                f"Le carte {condition} sono 26. Tra queste, le figure sono "
                f"J, Q, K di 2 semi = 6 carte. "
                f"P(figura | {condition}) = 6/26 = {self._frac_str(correct)}."
            ),
            did_you_know=(
                "Nella probabilita' condizionata, il 'dato che' restringe "
                "l'universo di riferimento. Non confondiamo P(A|B) con P(A e B)!"
            ),
        )

    # Template 15: Conditional probability with urn
    def _conditional_urn(self, difficulty: int) -> dict:
        r = random.randint(3, 6)
        b = random.randint(3, 6)
        total = r + b

        first_color = random.choice(["rossa", "blu"])
        second_color = random.choice(["rossa", "blu"])
        first_count = r if first_color == "rossa" else b
        if first_color == second_color:
            second_count = first_count - 1
        else:
            second_count = (r if second_color == "rossa" else b)

        correct = Fraction(second_count, total - 1)

        svg_parts = []
        svg_parts.append(self._svg_node(200, 25, "Urna", self._BLUE))
        p1 = Fraction(first_count, total)
        svg_parts.append(self._svg_branch(200, 39, 200, 96, self._frac_str(p1), self._BLUE, True))
        svg_parts.append(self._svg_node(200, 110, f"1a={first_color[:3]}", self._BLUE))

        p2_fav = Fraction(second_count, total - 1)
        p2_other = Fraction(total - 1 - second_count, total - 1)
        svg_parts.append(self._svg_branch(200, 124, 120, 236, self._frac_str(p2_fav), self._GREEN, True))
        svg_parts.append(self._svg_branch(200, 124, 280, 236, self._frac_str(p2_other), self._RED, False))
        svg_parts.append(self._svg_node(120, 250, second_color[:3], self._GREEN, 12))
        svg_parts.append(self._svg_node(280, 250, "altra", self._RED, 12))
        svg = self._svg_wrap("".join(svg_parts))

        distractors = self._make_distractors(correct)

        remaining_total = total - 1
        return self._build_result(
            question=(
                f"Un'urna contiene {r} palline rosse e {b} blu. "
                f"Si estrae una pallina {first_color}, senza rimetterla. "
                f"Qual e' la probabilita' che la seconda sia {second_color}?"
            ),
            correct=correct,
            distractors=distractors,
            svg=svg,
            explanation=(
                f"Dopo aver estratto una pallina {first_color}, nell'urna restano {remaining_total} palline "
                f"di cui {second_count} {second_color}. "
                f"P(2a {second_color} | 1a {first_color}) = {second_count}/{remaining_total} = {self._frac_str(correct)}."
            ),
            did_you_know=(
                "La probabilita' condizionata nell'urna senza rimpiazzo: "
                "dopo la prima estrazione, il contenuto dell'urna cambia e "
                "le probabilita' si aggiornano di conseguenza."
            ),
        )

    # Template 16: Bayes-style urn (two urns)
    def _bayes_urn(self, difficulty: int) -> dict:
        r1 = random.randint(2, 5)
        b1 = random.randint(2, 5)
        t1 = r1 + b1
        r2 = random.randint(2, 5)
        b2 = random.randint(2, 5)
        t2 = r2 + b2

        target = random.choice(["rossa", "blu"])
        tc1 = r1 if target == "rossa" else b1
        tc2 = r2 if target == "rossa" else b2

        p_u1 = Fraction(1, 2)
        p_u2 = Fraction(1, 2)
        p_target_u1 = Fraction(tc1, t1)
        p_target_u2 = Fraction(tc2, t2)
        correct = p_u1 * p_target_u1 + p_u2 * p_target_u2

        svg_parts = []
        svg_parts.append(self._svg_node(200, 20, "Scelta", self._BLUE))
        svg_parts.append(self._svg_branch(200, 34, 100, 76, "1/2", self._BLUE))
        svg_parts.append(self._svg_branch(200, 34, 300, 76, "1/2", self._BLUE))
        svg_parts.append(self._svg_node(100, 90, f"U1", self._BLUE))
        svg_parts.append(self._svg_node(300, 90, f"U2", self._BLUE))

        svg_parts.append(self._svg_branch(100, 104, 55, 216, self._frac_str(p_target_u1), self._GREEN, True))
        svg_parts.append(self._svg_branch(100, 104, 145, 216, self._frac_str(Fraction(t1 - tc1, t1)), self._RED))
        svg_parts.append(self._svg_node(55, 230, target[:3], self._GREEN, 12))
        svg_parts.append(self._svg_node(145, 230, "altra", self._RED, 12))

        svg_parts.append(self._svg_branch(300, 104, 255, 216, self._frac_str(p_target_u2), self._GREEN, True))
        svg_parts.append(self._svg_branch(300, 104, 345, 216, self._frac_str(Fraction(t2 - tc2, t2)), self._RED))
        svg_parts.append(self._svg_node(255, 230, target[:3], self._GREEN, 12))
        svg_parts.append(self._svg_node(345, 230, "altra", self._RED, 12))
        svg = self._svg_wrap("".join(svg_parts), 400, 260)

        distractors = self._make_distractors(correct)

        return self._build_result(
            question=(
                f"Ci sono due urne. L'urna 1 ha {r1} rosse e {b1} blu. "
                f"L'urna 2 ha {r2} rosse e {b2} blu. "
                f"Si sceglie un'urna a caso (prob. 1/2 ciascuna) e si estrae una pallina. "
                f"Qual e' la probabilita' che sia {target}?"
            ),
            correct=correct,
            distractors=distractors,
            svg=svg,
            explanation=(
                f"P({target}) = P(U1) x P({target}|U1) + P(U2) x P({target}|U2) "
                f"= 1/2 x {self._frac_str(p_target_u1)} + 1/2 x {self._frac_str(p_target_u2)} "
                f"= {self._frac_str(correct)}."
            ),
            did_you_know=(
                "Questa e' la legge della probabilita' totale: "
                "P(A) = somma di P(B_i) x P(A|B_i) su tutte le partizioni B_i. "
                "E' la base del teorema di Bayes."
            ),
        )

    # ==================================================================
    #  LEVEL 2 COMBINATORICS TEMPLATES
    # ==================================================================

    # Template C1: Permutazioni semplici
    def _comb_permutazioni_semplici(self, difficulty: int) -> dict:
        n = random.randint(3, 7)
        correct = math.factorial(n)

        oggetti_map = {
            3: ("3 libri", "libri"),
            4: ("4 persone", "persone"),
            5: ("5 lettere distinte", "lettere"),
            6: ("6 studenti", "studenti"),
            7: ("7 colori", "colori"),
        }
        oggetti_desc, oggetti_tipo = oggetti_map[n]

        distractors = self._make_int_distractors(correct)

        return self._build_int_result(
            question=(
                f"In quanti modi diversi si possono disporre in fila {oggetti_desc}?"
            ),
            correct_int=correct,
            distractors_int=distractors,
            svg="",
            explanation=(
                f"Il numero di permutazioni di {n} oggetti distinti e' {n}! = {correct}. "
                f"Si moltiplica: {' x '.join(str(i) for i in range(n, 0, -1))} = {correct}."
            ),
            did_you_know=(
                "Il fattoriale n! cresce molto rapidamente: 10! = 3.628.800. "
                "Le permutazioni contano tutti i possibili ordinamenti di un insieme."
            ),
        )

    # Template C2: Combinazioni
    def _comb_combinazioni(self, difficulty: int) -> dict:
        n = random.randint(5, 10)
        k = random.randint(2, min(4, n - 1))
        correct = math.comb(n, k)

        scenari = [
            (f"un gruppo di {n} amici", f"{k}", "amici"),
            (f"un insieme di {n} oggetti", f"{k}", "oggetti"),
            (f"una classe di {n} studenti", f"{k}", "studenti"),
        ]
        scenario = random.choice(scenari)

        distractors = self._make_int_distractors(correct)

        return self._build_int_result(
            question=(
                f"Da {scenario[0]}, in quanti modi si possono scegliere {scenario[1]} {scenario[2]}?"
            ),
            correct_int=correct,
            distractors_int=distractors,
            svg="",
            explanation=(
                f"Il numero di combinazioni C({n},{k}) = {n}! / ({k}! x ({n}-{k})!) = {correct}. "
                f"L'ordine di scelta non conta."
            ),
            did_you_know=(
                "Le combinazioni C(n,k) si chiamano anche coefficienti binomiali e "
                "compaiono nel triangolo di Tartaglia (o di Pascal). "
                "Vale sempre C(n,k) = C(n, n-k)."
            ),
        )

    # Template C3: Principio fondamentale del conteggio
    def _comb_principio_conteggio(self, difficulty: int) -> dict:
        scenari = [
            {
                "desc": "Un codice e' formato da {n} cifre decimali (0-9). Quante combinazioni diverse sono possibili?",
                "base": 10,
                "n_range": (2, 4),
                "calc_desc": "Ogni posizione ha {base} scelte possibili, quindi il totale e' {base}^{n} = {ans}.",
            },
            {
                "desc": "Un menu' offre {a} primi e {b} secondi. Quanti pasti diversi (un primo + un secondo) si possono comporre?",
                "type": "product",
                "a_range": (3, 7),
                "b_range": (3, 7),
                "calc_desc": "Per il principio del conteggio: {a} x {b} = {ans}.",
            },
            {
                "desc": "Per andare da A a B ci sono {a} strade, e da B a C ci sono {b} strade. Quanti percorsi diversi A-B-C esistono?",
                "type": "product",
                "a_range": (2, 5),
                "b_range": (2, 5),
                "calc_desc": "Per il principio del conteggio: {a} x {b} = {ans}.",
            },
        ]
        scenario = random.choice(scenari)

        if scenario.get("type") == "product":
            a = random.randint(*scenario["a_range"])
            b = random.randint(*scenario["b_range"])
            correct = a * b
            question = scenario["desc"].format(a=a, b=b)
            calc = scenario["calc_desc"].format(a=a, b=b, ans=correct)
        else:
            base = scenario["base"]
            n = random.randint(*scenario["n_range"])
            correct = base ** n
            question = scenario["desc"].format(n=n)
            calc = scenario["calc_desc"].format(base=base, n=n, ans=correct)

        distractors = self._make_int_distractors(correct)

        return self._build_int_result(
            question=question,
            correct_int=correct,
            distractors_int=distractors,
            svg="",
            explanation=(
                f"Applichiamo il principio fondamentale del conteggio. {calc}"
            ),
            did_you_know=(
                "Il principio fondamentale del conteggio afferma che se un'operazione "
                "puo' essere compiuta in m modi, e un'altra in n modi, le due operazioni "
                "insieme possono essere compiute in m x n modi."
            ),
        )

    # Template C4: Disposizioni semplici
    def _comb_disposizioni(self, difficulty: int) -> dict:
        n = random.randint(5, 9)
        k = random.randint(2, min(4, n - 1))
        correct = math.perm(n, k)

        scenari = [
            (f"un gruppo di {n} atleti", f"i primi {k} classificati (1o, 2o, ..., {k}o posto)", "atleti"),
            (f"{n} candidati", f"presidente, vicepresidente" + (f" e segretario" if k >= 3 else ""), "candidati"),
            (f"un insieme di {n} colori", f"una sequenza ordinata di {k} colori", "colori"),
        ]
        # Adjust k for the candidati scenario
        if k == 2:
            scenario = random.choice(scenari)
        elif k >= 3:
            scenario = random.choice(scenari)
        else:
            scenario = scenari[0]

        distractors = self._make_int_distractors(correct)

        return self._build_int_result(
            question=(
                f"Da {scenario[0]}, in quanti modi si possono scegliere {scenario[1]}?"
            ),
            correct_int=correct,
            distractors_int=distractors,
            svg="",
            explanation=(
                f"Le disposizioni semplici D({n},{k}) = {n}! / ({n}-{k})! = {correct}. "
                f"L'ordine conta: si scelgono {k} elementi da {n} e l'ordine e' importante."
            ),
            did_you_know=(
                "La differenza tra combinazioni e disposizioni sta nell'ordine: "
                "le disposizioni D(n,k) = C(n,k) x k! perche' ogni gruppo di k elementi "
                "puo' essere ordinato in k! modi diversi."
            ),
        )

    # ==================================================================
    #  LEVEL 3 COMBINATORICS TEMPLATES
    # ==================================================================

    # Template C5: Combinazioni con condizione
    def _comb_combinazioni_con_condizione(self, difficulty: int) -> dict:
        n_total = random.randint(7, 12)
        k_choose = random.randint(3, min(5, n_total - 2))
        n_fixed = random.randint(1, min(2, k_choose - 1))

        remaining_choose = k_choose - n_fixed
        remaining_pool = n_total - n_fixed
        correct = math.comb(remaining_pool, remaining_choose)

        scenari = [
            {
                "question": (
                    f"Da un gruppo di {n_total} persone si deve formare un comitato di {k_choose}. "
                    f"Se {n_fixed} {'persona deve' if n_fixed == 1 else 'persone devono'} "
                    f"essere {'inclusa' if n_fixed == 1 else 'incluse'} obbligatoriamente, "
                    f"quanti comitati diversi si possono formare?"
                ),
            },
            {
                "question": (
                    f"Una squadra di {k_choose} giocatori deve essere scelta da {n_total} disponibili. "
                    f"Se il capitano" + (f" e il vice" if n_fixed == 2 else "") +
                    f" {'deve' if n_fixed == 1 else 'devono'} far parte della squadra, "
                    f"quante squadre diverse sono possibili?"
                ),
            },
        ]
        scenario = random.choice(scenari)

        distractors = self._make_int_distractors(correct)

        return self._build_int_result(
            question=scenario["question"],
            correct_int=correct,
            distractors_int=distractors,
            svg="",
            explanation=(
                f"Con {n_fixed} {'persona fissa' if n_fixed == 1 else 'persone fisse'}, "
                f"restano {remaining_choose} posti da assegnare scegliendo "
                f"tra {remaining_pool} persone rimanenti. "
                f"C({remaining_pool},{remaining_choose}) = {correct}."
            ),
            did_you_know=(
                "Quando alcuni elementi sono fissati, il problema si riduce: "
                "si fissano quelli obbligatori e si calcolano le combinazioni "
                "per i posti rimanenti. E' una tecnica molto usata nei problemi TOLC."
            ),
        )

    # Template C6: Principio di inclusione-esclusione
    def _comb_inclusione_esclusione(self, difficulty: int) -> dict:
        scenari = [
            {
                "n": 100,
                "a": 2,
                "b": 3,
                "desc": "Quanti numeri interi da 1 a {n} sono divisibili per {a} o per {b}?",
            },
            {
                "n": 100,
                "a": 2,
                "b": 5,
                "desc": "Quanti numeri interi da 1 a {n} sono divisibili per {a} o per {b}?",
            },
            {
                "n": 50,
                "a": 3,
                "b": 5,
                "desc": "Quanti numeri interi da 1 a {n} sono divisibili per {a} o per {b}?",
            },
        ]
        scenario = random.choice(scenari)
        n = scenario["n"]
        a = scenario["a"]
        b = scenario["b"]
        lcm_ab = (a * b) // math.gcd(a, b)

        div_a = n // a
        div_b = n // b
        div_ab = n // lcm_ab
        correct = div_a + div_b - div_ab

        question = scenario["desc"].format(n=n, a=a, b=b)
        distractors = self._make_int_distractors(correct)

        return self._build_int_result(
            question=question,
            correct_int=correct,
            distractors_int=distractors,
            svg="",
            explanation=(
                f"Per il principio di inclusione-esclusione: "
                f"|A ∪ B| = |A| + |B| - |A ∩ B|. "
                f"Divisibili per {a}: {div_a}. "
                f"Divisibili per {b}: {div_b}. "
                f"Divisibili per entrambi (mcm={lcm_ab}): {div_ab}. "
                f"Totale = {div_a} + {div_b} - {div_ab} = {correct}."
            ),
            did_you_know=(
                "Il principio di inclusione-esclusione evita il doppio conteggio: "
                "quando si contano elementi in A o B, quelli in A e B vengono contati "
                "due volte, quindi vanno sottratti una volta."
            ),
        )

    # Template C7: Permutazioni con ripetizione (anagrammi)
    def _comb_permutazioni_con_ripetizione(self, difficulty: int) -> dict:
        parole = [
            ("MAMMA", {"M": 3, "A": 2}),
            ("NONNA", {"N": 3, "O": 1, "A": 1}),
            ("BABBO", {"B": 3, "A": 1, "O": 1}),
            ("LATTE", {"L": 1, "A": 1, "T": 2, "E": 1}),
            ("PALLA", {"P": 1, "A": 2, "L": 2}),
            ("TETTO", {"T": 3, "E": 1, "O": 1}),
            ("CACAO", {"C": 2, "A": 2, "O": 1}),
        ]
        parola, freq = random.choice(parole)
        n = sum(freq.values())
        denominatore = 1
        for count in freq.values():
            denominatore *= math.factorial(count)
        correct = math.factorial(n) // denominatore

        freq_str = ", ".join(f"{letter}={count}" for letter, count in freq.items() if count > 1)
        denom_str = " x ".join(f"{count}!" for count in freq.values() if count > 1)

        distractors = self._make_int_distractors(correct)

        return self._build_int_result(
            question=(
                f"Quanti anagrammi diversi (anche senza senso) si possono formare "
                f"con le lettere della parola {parola}?"
            ),
            correct_int=correct,
            distractors_int=distractors,
            svg="",
            explanation=(
                f"La parola {parola} ha {n} lettere con ripetizioni ({freq_str}). "
                f"Il numero di anagrammi e' {n}! / ({denom_str}) = "
                f"{math.factorial(n)} / {denominatore} = {correct}."
            ),
            did_you_know=(
                "Le permutazioni con ripetizione si calcolano come n! / (n1! x n2! x ... x nk!) "
                "dove n1, n2, ... sono le frequenze di ciascun elemento ripetuto. "
                "Questo perche' scambiare elementi identici non produce un nuovo anagramma."
            ),
        )

    # Template C8: Probabilita' combinatorica (carte)
    def _comb_probabilita_combinatorica(self, difficulty: int) -> dict:
        scenari = [
            {
                "k": 3,
                "desc": "Si estraggono {k} carte da un mazzo di 52. Qual e' la probabilita' che siano tutte rosse (cuori o quadri)?",
                "fav_n": 26,
                "total_n": 52,
            },
            {
                "k": 2,
                "desc": "Si estraggono {k} carte da un mazzo di 52. Qual e' la probabilita' che siano tutte figure (J, Q, K)?",
                "fav_n": 12,
                "total_n": 52,
            },
            {
                "k": 4,
                "desc": "Si estraggono {k} carte da un mazzo di 52. Qual e' la probabilita' che siano tutte dello stesso seme?",
                "type": "same_suit",
                "total_n": 52,
            },
        ]
        scenario = random.choice(scenari)
        k = scenario["k"]

        if scenario.get("type") == "same_suit":
            fav = 4 * math.comb(13, k)
            total = math.comb(52, k)
            correct = Fraction(fav, total)
            calc_explanation = (
                f"Modi di scegliere {k} carte dallo stesso seme: 4 x C(13,{k}) = 4 x {math.comb(13, k)} = {fav}. "
                f"Modi totali di scegliere {k} carte: C(52,{k}) = {total}. "
                f"P = {fav}/{total} = {self._frac_str(correct)}."
            )
        else:
            fav_n = scenario["fav_n"]
            total_n = scenario["total_n"]
            fav = math.comb(fav_n, k)
            total = math.comb(total_n, k)
            correct = Fraction(fav, total)
            calc_explanation = (
                f"Modi favorevoli: C({fav_n},{k}) = {fav}. "
                f"Modi totali: C({total_n},{k}) = {total}. "
                f"P = {fav}/{total} = {self._frac_str(correct)}."
            )

        question = scenario["desc"].format(k=k)
        distractors = self._make_distractors(correct)

        return self._build_result(
            question=question,
            correct=correct,
            distractors=distractors,
            svg="",
            explanation=calc_explanation,
            did_you_know=(
                "La probabilita' combinatorica usa il rapporto tra combinazioni favorevoli "
                "e combinazioni totali: P = C(favorevoli) / C(totali). "
                "E' l'approccio classico per problemi di estrazione senza rimpiazzo."
            ),
        )
