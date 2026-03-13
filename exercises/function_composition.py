import math
import random

from exercises.base import Exercise


class FunctionComposition(Exercise):
    """Composizione di Funzioni: exercises on f(g(x)), decomposition, and domain."""

    _DID_YOU_KNOW = [
        "La composizione di funzioni non è commutativa: f(g(x)) ≠ g(f(x)) in generale!",
        "La notazione f∘g si legge 'f composto g' e significa applicare prima g, poi f.",
        "Il dominio di f∘g è l'insieme dei valori x nel dominio di g tali che g(x) sia nel dominio di f.",
        "Ogni funzione invertibile soddisfa f(f⁻¹(x)) = x, cioè f∘f⁻¹ = identità.",
        "Nella vita reale, la composizione appare ovunque: la temperatura dipende dall'altitudine, che dipende dalla posizione.",
    ]

    # -------------------------------------------------------------- public

    def generate(self, difficulty: int) -> dict:
        difficulty = max(1, min(3, difficulty))

        if difficulty == 1:
            templates = [
                self._evaluate_composition,
                self._identify_composition_formula,
            ]
        elif difficulty == 2:
            templates = [
                self._composition_from_table,
                self._order_matters,
                self._decompose_function,
            ]
        else:
            templates = [
                self._domain_of_composition,
                self._triple_composition,
            ]

        result = random.choice(templates)()
        result["difficulty"] = difficulty
        return result

    # -------------------------------------------------------------- helpers

    def _random_did_you_know(self) -> str:
        return random.choice(self._DID_YOU_KNOW)

    @staticmethod
    def _make_distinct_options(correct: str, distractors: list[str]) -> tuple[list[str], int]:
        """Build a list of 5 distinct options from the correct answer and distractors.

        Filters out duplicates of the correct answer, then pads with generated
        variants if fewer than 4 unique distractors are available.
        """
        seen = {correct}
        unique_distractors = []
        for d in distractors:
            if d not in seen:
                seen.add(d)
                unique_distractors.append(d)
            if len(unique_distractors) == 4:
                break

        # Pad if needed
        attempt = 0
        while len(unique_distractors) < 4 and attempt < 50:
            attempt += 1
            # Try numeric perturbation of correct answer
            try:
                val = float(correct)
                offset = random.choice([-3, -2, -1, 1, 2, 3]) * (attempt // 5 + 1)
                candidate = str(int(val + offset)) if val == int(val) else str(round(val + offset, 2))
            except (ValueError, OverflowError):
                candidate = f"Opzione {len(unique_distractors) + 2}"
            if candidate not in seen:
                seen.add(candidate)
                unique_distractors.append(candidate)

        options = [correct] + unique_distractors[:4]
        correct_index = 0
        return options, correct_index

    # -------------------------------------------------------------- L1

    def _evaluate_composition(self) -> dict:
        """L1: Evaluate f(g(a)) numerically for simple functions."""
        # Define function pairs: (name, display, lambda, safe_inputs)
        func_defs = [
            ("2x+1", lambda x: 2 * x + 1),
            ("3x-2", lambda x: 3 * x - 2),
            ("x+5", lambda x: x + 5),
            ("x²", lambda x: x ** 2),
            ("2x²", lambda x: 2 * x ** 2),
            ("x²+1", lambda x: x ** 2 + 1),
            ("x+3", lambda x: x + 3),
            ("4x", lambda x: 4 * x),
        ]

        # Pick two different functions
        f_def, g_def = random.sample(func_defs, 2)
        f_name, f_fn = f_def
        g_name, g_fn = g_def

        a = random.randint(1, 5)

        # Compute f(g(a))
        g_a = g_fn(a)
        fg_a = f_fn(g_a)

        # Distractors
        f_a = f_fn(a)
        gf_a = g_fn(f_a)  # g(f(a))
        sum_val = f_a + g_fn(a)  # f(a) + g(a)
        prod_val = f_a * g_fn(a)  # f(a) * g(a)
        off_by_one = fg_a + random.choice([-1, 1])

        correct = str(int(fg_a))
        distractors = [
            str(int(gf_a)),
            str(int(sum_val)),
            str(int(prod_val)),
            str(int(off_by_one)),
        ]

        options, correct_index = self._make_distinct_options(correct, distractors)
        options, correct_index = self.shuffle_options(options, correct_index)

        return {
            "question": (
                f"Se f(x) = {f_name} e g(x) = {g_name}, "
                f"quanto vale f(g({a}))?"
            ),
            "options": options,
            "correct_index": correct_index,
            "explanation": (
                f"Calcoliamo passo per passo: prima g({a}) = {int(g_a)}, "
                f"poi f({int(g_a)}) = {int(fg_a)}. "
                f"Quindi f(g({a})) = {correct}."
            ),
            "did_you_know": self._random_did_you_know(),
        }

    def _identify_composition_formula(self) -> dict:
        """L1: Identify f(g(x)) as a formula given f and g."""
        # Define function pairs with their symbolic compositions
        compositions = [
            {
                "f_name": "2x+1", "g_name": "x²",
                "fg": "2x²+1", "gf": "(2x+1)²",
                "prod": "x²(2x+1)", "add": "x²+2x+1",
                "partial": "2x²",
            },
            {
                "f_name": "x+3", "g_name": "x²",
                "fg": "x²+3", "gf": "(x+3)²",
                "prod": "x²(x+3)", "add": "x²+x+3",
                "partial": "x²+1",
            },
            {
                "f_name": "3x", "g_name": "x+2",
                "fg": "3(x+2)", "gf": "3x+2",
                "prod": "3x(x+2)", "add": "3x+x+2",
                "partial": "3x+6",
            },
            {
                "f_name": "x²", "g_name": "x+1",
                "fg": "(x+1)²", "gf": "x²+1",
                "prod": "x²(x+1)", "add": "x²+x+1",
                "partial": "x²+2",
            },
            {
                "f_name": "2x", "g_name": "x²-1",
                "fg": "2(x²-1)", "gf": "(2x)²-1",
                "prod": "2x(x²-1)", "add": "2x+x²-1",
                "partial": "2x²-1",
            },
            {
                "f_name": "x+4", "g_name": "3x",
                "fg": "3x+4", "gf": "3(x+4)",
                "prod": "3x(x+4)", "add": "3x+x+4",
                "partial": "3x+1",
            },
        ]

        comp = random.choice(compositions)
        correct = comp["fg"]
        distractors = [comp["gf"], comp["prod"], comp["add"], comp["partial"]]

        options, correct_index = self._make_distinct_options(correct, distractors)
        options, correct_index = self.shuffle_options(options, correct_index)

        return {
            "question": (
                f"Se f(x) = {comp['f_name']} e g(x) = {comp['g_name']}, "
                f"qual è l'espressione di f(g(x))?"
            ),
            "options": options,
            "correct_index": correct_index,
            "explanation": (
                f"Per calcolare f(g(x)), sostituiamo g(x) = {comp['g_name']} "
                f"al posto di x in f(x) = {comp['f_name']}. "
                f"Otteniamo f(g(x)) = {correct}. "
                f"Attenzione: g(f(x)) = {comp['gf']} è diverso!"
            ),
            "did_you_know": self._random_did_you_know(),
        }

    # -------------------------------------------------------------- L2

    def _composition_from_table(self) -> dict:
        """L2: Given tables for f and g, compute f(g(a))."""
        xs = [1, 2, 3, 4]

        # Generate random function values ensuring no collisions that make problem unsolvable
        g_vals = random.sample(range(1, 5), 4)  # g maps xs -> permutation of 1..4
        f_vals = [random.randint(1, 9) for _ in xs]

        g_table = dict(zip(xs, g_vals))
        f_table = dict(zip(xs, f_vals))

        # Pick input where g(a) is in domain of f
        a = random.choice(xs)
        g_a = g_table[a]
        fg_a = f_table[g_a]

        # Build table display
        g_rows = "  ".join(f"g({x}) = {g_table[x]}" for x in xs)
        f_rows = "  ".join(f"f({x}) = {f_table[x]}" for x in xs)

        # Distractors
        f_a = f_table[a]
        gf_a = g_table.get(f_a, random.randint(1, 9))  # g(f(a)) if possible
        sum_val = f_a + g_a
        wrong_lookup = f_table.get(a, random.randint(1, 9))  # f(a) instead of f(g(a))

        correct = str(fg_a)
        distractors = [
            str(gf_a),
            str(sum_val),
            str(wrong_lookup),
            str(fg_a + random.choice([-2, -1, 1, 2])),
        ]

        options, correct_index = self._make_distinct_options(correct, distractors)
        options, correct_index = self.shuffle_options(options, correct_index)

        return {
            "question": (
                f"Date le seguenti tabelle:\n"
                f"{g_rows}\n"
                f"{f_rows}\n"
                f"Quanto vale f(g({a}))?"
            ),
            "options": options,
            "correct_index": correct_index,
            "explanation": (
                f"Dalla tabella, g({a}) = {g_a}. "
                f"Poi cerchiamo f({g_a}) = {fg_a}. "
                f"Quindi f(g({a})) = {correct}."
            ),
            "did_you_know": self._random_did_you_know(),
        }

    def _order_matters(self) -> dict:
        """L2: Distinguish f(g(x)) from g(f(x)) — order matters."""
        pairs = [
            {
                "f_name": "x²", "g_name": "x+3",
                "fg": "(x+3)²", "gf": "x²+3",
                "prod": "x²(x+3)", "add": "x²+x+3",
                "wrong": "(x+3)³",
            },
            {
                "f_name": "2x", "g_name": "x-1",
                "fg": "2(x-1)", "gf": "2x-1",
                "prod": "2x(x-1)", "add": "2x+x-1",
                "wrong": "2(x+1)",
            },
            {
                "f_name": "x+5", "g_name": "3x",
                "fg": "3x+5", "gf": "3(x+5)",
                "prod": "3x(x+5)", "add": "3x+x+5",
                "wrong": "3x+3",
            },
            {
                "f_name": "x²+1", "g_name": "2x",
                "fg": "(2x)²+1", "gf": "2(x²+1)",
                "prod": "2x(x²+1)", "add": "x²+2x+1",
                "wrong": "4x+1",
            },
            {
                "f_name": "3x+2", "g_name": "x²",
                "fg": "3x²+2", "gf": "(3x+2)²",
                "prod": "x²(3x+2)", "add": "x²+3x+2",
                "wrong": "3x²+1",
            },
        ]

        pair = random.choice(pairs)
        correct = pair["fg"]
        distractors = [pair["gf"], pair["prod"], pair["add"], pair["wrong"]]

        options, correct_index = self._make_distinct_options(correct, distractors)
        options, correct_index = self.shuffle_options(options, correct_index)

        return {
            "question": (
                f"Se f(x) = {pair['f_name']} e g(x) = {pair['g_name']}, "
                f"quale delle seguenti espressioni corrisponde a f(g(x))?"
            ),
            "options": options,
            "correct_index": correct_index,
            "explanation": (
                f"Per f(g(x)), applichiamo prima g e poi f. "
                f"Sostituiamo g(x) = {pair['g_name']} in f: "
                f"f(g(x)) = {correct}. "
                f"Nota: g(f(x)) = {pair['gf']} è diverso! L'ordine conta."
            ),
            "did_you_know": self._random_did_you_know(),
        }

    def _decompose_function(self) -> dict:
        """L2: Decompose h(x) = f(g(x)) into f and g."""
        decompositions = [
            {
                "h": "√(2x+1)",
                "correct_f": "f(x) = √x",
                "correct_g": "g(x) = 2x+1",
                "distractors": [
                    "f(x) = 2x+1, g(x) = √x",
                    "f(x) = √(2x), g(x) = x+1",
                    "f(x) = x+1, g(x) = √(2x)",
                    "f(x) = 2√x, g(x) = x+1",
                ],
            },
            {
                "h": "(3x-2)²",
                "correct_f": "f(x) = x²",
                "correct_g": "g(x) = 3x-2",
                "distractors": [
                    "f(x) = 3x-2, g(x) = x²",
                    "f(x) = (3x)², g(x) = x-2",
                    "f(x) = x-2, g(x) = (3x)²",
                    "f(x) = 9x², g(x) = x-2",
                ],
            },
            {
                "h": "ln(x²+4)",
                "correct_f": "f(x) = ln(x)",
                "correct_g": "g(x) = x²+4",
                "distractors": [
                    "f(x) = x²+4, g(x) = ln(x)",
                    "f(x) = ln(x²), g(x) = x+4",
                    "f(x) = x+4, g(x) = ln(x²)",
                    "f(x) = ln(x+4), g(x) = x²",
                ],
            },
            {
                "h": "e^(x+3)",
                "correct_f": "f(x) = eˣ",
                "correct_g": "g(x) = x+3",
                "distractors": [
                    "f(x) = x+3, g(x) = eˣ",
                    "f(x) = e³, g(x) = eˣ",
                    "f(x) = eˣ⁺¹, g(x) = x+2",
                    "f(x) = 3eˣ, g(x) = x",
                ],
            },
            {
                "h": "1/(x²-1)",
                "correct_f": "f(x) = 1/x",
                "correct_g": "g(x) = x²-1",
                "distractors": [
                    "f(x) = x²-1, g(x) = 1/x",
                    "f(x) = 1/x², g(x) = x-1",
                    "f(x) = x-1, g(x) = 1/x²",
                    "f(x) = 1/(x-1), g(x) = x²",
                ],
            },
        ]

        decomp = random.choice(decompositions)
        correct_label = f"{decomp['correct_f']}, {decomp['correct_g']}"

        options, correct_index = self._make_distinct_options(
            correct_label, decomp["distractors"]
        )
        options, correct_index = self.shuffle_options(options, correct_index)

        return {
            "question": (
                f"La funzione h(x) = {decomp['h']} può essere scritta come f(g(x)). "
                f"Quali sono f e g?"
            ),
            "options": options,
            "correct_index": correct_index,
            "explanation": (
                f"Per decomporre h(x) = {decomp['h']}, identifichiamo la funzione "
                f"'esterna' e quella 'interna'. "
                f"La funzione esterna è {decomp['correct_f']} e quella interna è "
                f"{decomp['correct_g']}. "
                f"Verificando: f(g(x)) = {decomp['h']} ✓."
            ),
            "did_you_know": self._random_did_you_know(),
        }

    # -------------------------------------------------------------- L3

    def _domain_of_composition(self) -> dict:
        """L3: Find the domain of f(g(x))."""
        domain_problems = [
            {
                "f_name": "ln(x)",
                "g_name": "x²-4",
                "fg_name": "ln(x²-4)",
                "condition": "x² - 4 > 0, cioè x < -2 oppure x > 2",
                "correct": "(-∞, -2) ∪ (2, +∞)",
                "distractors": [
                    "(-2, 2)",
                    "(-∞, -4) ∪ (4, +∞)",
                    "ℝ \\ {-2, 2}",
                    "[-2, 2]",
                ],
            },
            {
                "f_name": "√x",
                "g_name": "3x-6",
                "fg_name": "√(3x-6)",
                "condition": "3x - 6 ≥ 0, cioè x ≥ 2",
                "correct": "[2, +∞)",
                "distractors": [
                    "(2, +∞)",
                    "[0, +∞)",
                    "(-∞, 2]",
                    "[6, +∞)",
                ],
            },
            {
                "f_name": "1/x",
                "g_name": "x-5",
                "fg_name": "1/(x-5)",
                "condition": "x - 5 ≠ 0, cioè x ≠ 5",
                "correct": "ℝ \\ {5}",
                "distractors": [
                    "ℝ \\ {0}",
                    "(5, +∞)",
                    "(-∞, 5)",
                    "ℝ \\ {-5}",
                ],
            },
            {
                "f_name": "√x",
                "g_name": "4-x²",
                "fg_name": "√(4-x²)",
                "condition": "4 - x² ≥ 0, cioè -2 ≤ x ≤ 2",
                "correct": "[-2, 2]",
                "distractors": [
                    "(-2, 2)",
                    "(-∞, -2] ∪ [2, +∞)",
                    "[0, 2]",
                    "[-4, 4]",
                ],
            },
            {
                "f_name": "ln(x)",
                "g_name": "x+1",
                "fg_name": "ln(x+1)",
                "condition": "x + 1 > 0, cioè x > -1",
                "correct": "(-1, +∞)",
                "distractors": [
                    "[0, +∞)",
                    "(-∞, -1)",
                    "[-1, +∞)",
                    "(1, +∞)",
                ],
            },
            {
                "f_name": "1/x",
                "g_name": "x²-9",
                "fg_name": "1/(x²-9)",
                "condition": "x² - 9 ≠ 0, cioè x ≠ -3 e x ≠ 3",
                "correct": "ℝ \\ {-3, 3}",
                "distractors": [
                    "ℝ \\ {9}",
                    "(-3, 3)",
                    "(-∞, -3) ∪ (3, +∞)",
                    "ℝ \\ {0}",
                ],
            },
        ]

        problem = random.choice(domain_problems)
        correct = problem["correct"]

        options, correct_index = self._make_distinct_options(
            correct, problem["distractors"]
        )
        options, correct_index = self.shuffle_options(options, correct_index)

        return {
            "question": (
                f"Se f(x) = {problem['f_name']} e g(x) = {problem['g_name']}, "
                f"qual è il dominio di f(g(x)) = {problem['fg_name']}?"
            ),
            "options": options,
            "correct_index": correct_index,
            "explanation": (
                f"Per trovare il dominio di f(g(x)) = {problem['fg_name']}, "
                f"dobbiamo imporre che g(x) appartenga al dominio di f. "
                f"Serve che {problem['condition']}. "
                f"Il dominio è quindi {correct}."
            ),
            "did_you_know": self._random_did_you_know(),
        }

    def _triple_composition(self) -> dict:
        """L3: Compute f(g(h(a))) step by step with three functions."""
        # Simple functions for triple composition
        func_pool = [
            ("2x+1", lambda x: 2 * x + 1),
            ("x-3", lambda x: x - 3),
            ("x+2", lambda x: x + 2),
            ("3x", lambda x: 3 * x),
            ("x²", lambda x: x ** 2),
            ("x+5", lambda x: x + 5),
            ("2x-1", lambda x: 2 * x - 1),
            ("4x", lambda x: 4 * x),
        ]

        f_def, g_def, h_def = random.sample(func_pool, 3)
        f_name, f_fn = f_def
        g_name, g_fn = g_def
        h_name, h_fn = h_def

        a = random.randint(1, 4)

        h_a = h_fn(a)
        gh_a = g_fn(h_a)
        fgh_a = f_fn(gh_a)

        # Distractors: wrong orders and partial computations
        f_a = f_fn(a)
        g_a = g_fn(a)
        gfh = g_fn(f_fn(h_fn(a)))  # wrong order
        hgf = h_fn(g_fn(f_fn(a)))  # reversed order
        partial = g_fn(h_fn(a))  # only g(h(a)) without f

        correct = str(int(fgh_a))
        distractors = [
            str(int(gfh)),
            str(int(hgf)),
            str(int(partial)),
            str(int(fgh_a + random.choice([-2, -1, 1, 2]))),
        ]

        options, correct_index = self._make_distinct_options(correct, distractors)
        options, correct_index = self.shuffle_options(options, correct_index)

        return {
            "question": (
                f"Se f(x) = {f_name}, g(x) = {g_name} e h(x) = {h_name}, "
                f"quanto vale f(g(h({a})))?"
            ),
            "options": options,
            "correct_index": correct_index,
            "explanation": (
                f"Calcoliamo dall'interno verso l'esterno:\n"
                f"h({a}) = {int(h_a)}\n"
                f"g({int(h_a)}) = {int(gh_a)}\n"
                f"f({int(gh_a)}) = {int(fgh_a)}\n"
                f"Quindi f(g(h({a}))) = {correct}."
            ),
            "did_you_know": self._random_did_you_know(),
        }
