import random

from exercises.base import Exercise


class StrategySelection(Exercise):
    """Scelta Strategica: identifica la strategia più efficiente per risolvere un problema."""

    def generate(self, difficulty: int) -> dict:
        difficulty = max(1, min(3, difficulty))

        if difficulty == 1:
            templates = [
                self._eq_simple_linear,
                self._eq_factorable_quadratic,
                self._eq_irrational_roots_quadratic,
                self._eq_perfect_square_quadratic,
            ]
        elif difficulty == 2:
            templates = [
                self._expr_common_factor,
                self._expr_difference_of_squares,
                self._expr_sum_of_cubes,
                self._expr_completing_square,
            ]
        else:
            templates = [
                self._geo_collinear_points,
                self._geo_angle_from_sides,
                self._geo_area_polygon_coordinates,
                self._geo_perpendicular_bisector,
            ]

        template_fn = random.choice(templates)
        result = template_fn()
        result["difficulty"] = difficulty
        return result

    # ------------------------------------------------------------------ helpers

    @staticmethod
    def _make_strategy_options(
        correct: str, distractors: list[str]
    ) -> tuple[list[str], int]:
        """Build a list of 5 strategy options with the correct one included.

        Returns (options, correct_index) after shuffling.
        """
        pool = [d for d in distractors if d != correct]
        random.shuffle(pool)
        options = [correct] + pool[:4]
        random.shuffle(options)
        correct_index = options.index(correct)
        return options, correct_index

    # ======================================================================
    # LEVEL 1 — Equation solving strategy
    # ======================================================================

    def _eq_simple_linear(self) -> dict:
        a = random.choice([2, 3, 4, 5, 6, 7, 8])
        b = random.randint(1, 15)
        c = random.randint(1, 20)
        equation = f"{a}x + {b} = {c}"

        correct = "Isolamento della variabile"
        distractors = [
            "Isolamento della variabile",
            "Formula quadratica",
            "Fattorizzazione",
            "Completamento del quadrato",
            "Sostituzione",
            "Metodo grafico",
        ]

        options, correct_index = self._make_strategy_options(correct, distractors)

        return {
            "question": (
                f"Quale strategia è più efficiente per risolvere l'equazione "
                f"{equation}?"
            ),
            "options": options,
            "correct_index": correct_index,
            "explanation": (
                f"L'equazione {equation} è lineare di primo grado. "
                f"La strategia più efficiente è l'isolamento della variabile: "
                f"si sposta il termine noto a destra e si divide per il coefficiente. "
                f"Le altre strategie (formula quadratica, fattorizzazione, ecc.) "
                f"sono pensate per equazioni di grado superiore."
            ),
            "did_you_know": (
                "Le equazioni lineari si risolvono sempre in un solo passaggio "
                "algebrico: isolare la variabile."
            ),
            "approfondimento": False,
        }

    def _eq_factorable_quadratic(self) -> dict:
        r1 = random.randint(1, 9)
        r2 = random.randint(1, 9)
        if random.random() < 0.5:
            r1 = -r1
        # x^2 - (r1+r2)x + r1*r2 = 0
        b_coeff = -(r1 + r2)
        c_coeff = r1 * r2
        b_str = f"+ {b_coeff}" if b_coeff >= 0 else f"- {abs(b_coeff)}"
        c_str = f"+ {c_coeff}" if c_coeff >= 0 else f"- {abs(c_coeff)}"
        equation = f"x² {b_str}x {c_str} = 0"

        correct = "Fattorizzazione"
        distractors = [
            "Fattorizzazione",
            "Formula quadratica",
            "Completamento del quadrato",
            "Isolamento della variabile",
            "Sostituzione",
            "Metodo grafico",
        ]

        options, correct_index = self._make_strategy_options(correct, distractors)

        return {
            "question": (
                f"Quale strategia è più efficiente per risolvere l'equazione "
                f"{equation}?"
            ),
            "options": options,
            "correct_index": correct_index,
            "explanation": (
                f"L'equazione {equation} ha radici intere ({r1} e {r2}), "
                f"quindi si fattorizza facilmente come (x - {r1})(x - {r2}) = 0. "
                f"La fattorizzazione è più rapida della formula quadratica "
                f"quando le radici sono numeri interi semplici."
            ),
            "did_you_know": (
                "Per verificare se un'equazione quadratica è fattorizzabile con "
                "radici intere, cerca due numeri il cui prodotto sia il termine "
                "noto e la cui somma sia il coefficiente del termine di primo grado."
            ),
            "approfondimento": False,
        }

    def _eq_irrational_roots_quadratic(self) -> dict:
        a = random.choice([1, 2, 3])
        b = random.choice([1, 3, 5, 7])
        # ensure discriminant > 0 but not a perfect square
        while True:
            c = random.randint(1, 10)
            disc = b * b - 4 * a * c
            if disc < 0:
                c = random.randint(-10, -1)
                disc = b * b - 4 * a * c
            if disc > 0:
                sqrt_disc = disc ** 0.5
                if abs(sqrt_disc - round(sqrt_disc)) > 0.01:
                    break

        a_str = f"{a}x²" if a != 1 else "x²"
        b_str = f"+ {b}x" if b > 0 else f"- {abs(b)}x"
        c_str = f"+ {c}" if c >= 0 else f"- {abs(c)}"
        equation = f"{a_str} {b_str} {c_str} = 0"

        correct = "Formula quadratica"
        distractors = [
            "Formula quadratica",
            "Fattorizzazione",
            "Completamento del quadrato",
            "Isolamento della variabile",
            "Tentativi",
            "Metodo grafico",
        ]

        options, correct_index = self._make_strategy_options(correct, distractors)

        return {
            "question": (
                f"Quale strategia è più efficiente per risolvere l'equazione "
                f"{equation}?"
            ),
            "options": options,
            "correct_index": correct_index,
            "explanation": (
                f"L'equazione {equation} ha discriminante Δ = {disc}, che non è "
                f"un quadrato perfetto. Le radici sono irrazionali, quindi la "
                f"fattorizzazione con numeri interi non funziona. La formula "
                f"quadratica x = (-b ± √Δ) / 2a è la strategia più diretta."
            ),
            "did_you_know": (
                "La formula quadratica funziona sempre per equazioni di secondo "
                "grado, ma è particolarmente utile quando il discriminante non "
                "è un quadrato perfetto."
            ),
            "approfondimento": False,
        }

    def _eq_perfect_square_quadratic(self) -> dict:
        k = random.choice([2, 3, 4, 5, 6, 7])
        sign = random.choice([1, -1])
        # (x + sign*k)^2 = 0  =>  x^2 + 2*sign*k*x + k^2 = 0
        b_coeff = 2 * sign * k
        c_coeff = k * k
        b_str = f"+ {b_coeff}x" if b_coeff > 0 else f"- {abs(b_coeff)}x"
        equation = f"x² {b_str} + {c_coeff} = 0"

        correct = "Completamento del quadrato"
        distractors = [
            "Completamento del quadrato",
            "Formula quadratica",
            "Fattorizzazione",
            "Isolamento della variabile",
            "Sostituzione",
            "Tentativi",
        ]

        options, correct_index = self._make_strategy_options(correct, distractors)

        sign_str = "+" if sign > 0 else "-"

        return {
            "question": (
                f"Quale strategia è più efficiente per risolvere l'equazione "
                f"{equation}?"
            ),
            "options": options,
            "correct_index": correct_index,
            "explanation": (
                f"L'equazione {equation} è un quadrato perfetto: "
                f"(x {sign_str} {k})² = 0. Riconoscere questa struttura "
                f"tramite il completamento del quadrato è il metodo più rapido. "
                f"La formula quadratica funzionerebbe ma è inutilmente laboriosa."
            ),
            "did_you_know": (
                "Un trinomio a² ± 2ab + b² è sempre un quadrato perfetto. "
                "Riconoscerlo permette di risolvere l'equazione immediatamente."
            ),
            "approfondimento": False,
        }

    # ======================================================================
    # LEVEL 2 — Expression simplification strategy
    # ======================================================================

    def _expr_common_factor(self) -> dict:
        a = random.choice([2, 3, 4, 5, 6])
        b = random.randint(2, 8)
        c = random.randint(2, 8)
        expression = f"{a * b}x³ + {a * c}x²"

        correct = "Raccoglimento a fattore comune"
        distractors = [
            "Raccoglimento a fattore comune",
            "Prodotti notevoli",
            "Sostituzione",
            "Semplificazione diretta",
            "Scomposizione in fattori primi",
            "Divisione polinomiale",
        ]

        options, correct_index = self._make_strategy_options(correct, distractors)

        return {
            "question": (
                f"Quale strategia è più efficiente per semplificare l'espressione "
                f"{expression}?"
            ),
            "options": options,
            "correct_index": correct_index,
            "explanation": (
                f"Entrambi i termini contengono il fattore comune {a}x². "
                f"Raccogliendo: {a}x²({b}x + {c}). Il raccoglimento a fattore "
                f"comune è sempre il primo passo da tentare quando i termini "
                f"condividono fattori."
            ),
            "did_you_know": (
                "Il raccoglimento a fattore comune è il primo passo in qualsiasi "
                "scomposizione: cerca sempre il MCD dei coefficienti e la minima "
                "potenza delle variabili comuni."
            ),
            "approfondimento": False,
        }

    def _expr_difference_of_squares(self) -> dict:
        a = random.choice([2, 3, 4, 5, 6, 7])
        b = random.choice([1, 2, 3, 4, 5])
        a_sq = a * a
        b_sq = b * b
        expression = f"{a_sq}x² - {b_sq}"

        correct = "Prodotti notevoli"
        distractors = [
            "Prodotti notevoli",
            "Raccoglimento a fattore comune",
            "Scomposizione",
            "Sostituzione",
            "Semplificazione diretta",
            "Divisione polinomiale",
        ]

        options, correct_index = self._make_strategy_options(correct, distractors)

        return {
            "question": (
                f"Quale strategia è più efficiente per semplificare l'espressione "
                f"{expression}?"
            ),
            "options": options,
            "correct_index": correct_index,
            "explanation": (
                f"L'espressione {expression} è una differenza di quadrati: "
                f"({a}x)² - {b}². Si applica la formula a² - b² = (a+b)(a-b), "
                f"ottenendo ({a}x + {b})({a}x - {b}). I prodotti notevoli "
                f"sono la via più veloce per questo tipo di espressione."
            ),
            "did_you_know": (
                "La differenza di quadrati a² - b² = (a+b)(a-b) è uno dei "
                "prodotti notevoli più utili in algebra."
            ),
            "approfondimento": False,
        }

    def _expr_sum_of_cubes(self) -> dict:
        a = random.choice([1, 2, 3])
        b = random.choice([1, 2, 3])
        is_sum = random.choice([True, False])
        a_cube = a ** 3
        b_cube = b ** 3
        op = "+" if is_sum else "-"
        expression = f"{a_cube}x³ {op} {b_cube}"
        formula_name = "somma" if is_sum else "differenza"

        correct = "Prodotti notevoli"
        distractors = [
            "Prodotti notevoli",
            "Raccoglimento a fattore comune",
            "Sostituzione",
            "Scomposizione in fattori primi",
            "Semplificazione diretta",
            "Divisione polinomiale",
        ]

        options, correct_index = self._make_strategy_options(correct, distractors)

        return {
            "question": (
                f"Quale strategia è più efficiente per scomporre l'espressione "
                f"{expression}?"
            ),
            "options": options,
            "correct_index": correct_index,
            "explanation": (
                f"L'espressione {expression} è una {formula_name} di cubi. "
                f"Si applica la formula a³ ± b³ = (a ± b)(a² ∓ ab + b²). "
                f"Riconoscere i prodotti notevoli è la strategia più efficiente."
            ),
            "did_you_know": (
                "Le formule per somma e differenza di cubi sono: "
                "a³ + b³ = (a+b)(a²-ab+b²) e a³ - b³ = (a-b)(a²+ab+b²)."
            ),
            "approfondimento": False,
        }

    def _expr_completing_square(self) -> dict:
        a = random.choice([1, 2, 3])
        b = random.choice([2, 4, 6, 8, 10])
        c = random.randint(1, 10)
        a_str = f"{a}x²" if a != 1 else "x²"
        expression = f"{a_str} + {b}x + {c}"

        correct = "Completamento del quadrato"
        distractors = [
            "Completamento del quadrato",
            "Raccoglimento a fattore comune",
            "Prodotti notevoli",
            "Scomposizione",
            "Sostituzione",
            "Semplificazione diretta",
        ]

        options, correct_index = self._make_strategy_options(correct, distractors)

        return {
            "question": (
                f"Quale strategia è più efficiente per riscrivere l'espressione "
                f"{expression} in forma canonica (vertice della parabola)?"
            ),
            "options": options,
            "correct_index": correct_index,
            "explanation": (
                f"Per trovare la forma canonica di un trinomio di secondo grado, "
                f"il completamento del quadrato è la strategia specifica: "
                f"si riscrive come a(x - h)² + k. Questo rivela direttamente "
                f"il vertice della parabola."
            ),
            "did_you_know": (
                "Il completamento del quadrato trasforma ax² + bx + c nella "
                "forma a(x + b/2a)² + (c - b²/4a), utile per trovare il vertice."
            ),
            "approfondimento": False,
        }

    # ======================================================================
    # LEVEL 3 — Geometry problem approach
    # ======================================================================

    def _geo_collinear_points(self) -> dict:
        x1 = random.randint(-5, 5)
        y1 = random.randint(-5, 5)
        dx = random.choice([-3, -2, -1, 1, 2, 3])
        dy = random.choice([-3, -2, -1, 1, 2, 3])
        x2, y2 = x1 + dx, y1 + dy
        x3, y3 = x1 + 2 * dx, y1 + 2 * dy

        correct = "Geometria analitica (determinante)"
        distractors = [
            "Geometria analitica (determinante)",
            "Geometria euclidea sintetica",
            "Approccio trigonometrico",
            "Approccio algebrico diretto",
            "Approccio vettoriale",
            "Metodo grafico",
        ]

        options, correct_index = self._make_strategy_options(correct, distractors)

        return {
            "question": (
                f"Per verificare se i punti A({x1},{y1}), B({x2},{y2}), "
                f"C({x3},{y3}) sono allineati, quale approccio è più efficiente?"
            ),
            "options": options,
            "correct_index": correct_index,
            "explanation": (
                f"Per verificare la collinearità di tre punti, il metodo più "
                f"efficiente è calcolare il determinante della matrice 3×3 "
                f"formata dalle coordinate. Se il determinante è zero, i punti "
                f"sono allineati. È un singolo calcolo numerico, molto più "
                f"rapido di calcolare pendenze o distanze."
            ),
            "did_you_know": (
                "Il determinante |x1(y2-y3) + x2(y3-y1) + x3(y1-y2)| è anche "
                "il doppio dell'area del triangolo formato dai tre punti. "
                "Se vale zero, i punti sono allineati."
            ),
            "approfondimento": True,
        }

    def _geo_angle_from_sides(self) -> dict:
        # Generate a valid triangle with integer sides
        while True:
            a = random.randint(3, 12)
            b = random.randint(3, 12)
            c = random.randint(3, 12)
            if a + b > c and a + c > b and b + c > a:
                break

        correct = "Approccio trigonometrico (teorema del coseno)"
        distractors = [
            "Approccio trigonometrico (teorema del coseno)",
            "Geometria analitica (determinante)",
            "Geometria euclidea sintetica",
            "Approccio algebrico diretto",
            "Approccio vettoriale",
            "Metodo grafico",
        ]

        options, correct_index = self._make_strategy_options(correct, distractors)

        return {
            "question": (
                f"Per trovare l'angolo opposto al lato di lunghezza {c} "
                f"in un triangolo con lati {a}, {b}, {c}, quale approccio "
                f"è più efficiente?"
            ),
            "options": options,
            "correct_index": correct_index,
            "explanation": (
                f"Conoscendo tutti e tre i lati di un triangolo, il teorema "
                f"del coseno è la strategia diretta: cos(C) = (a² + b² - c²) / (2ab). "
                f"Un singolo calcolo fornisce l'angolo. La geometria sintetica "
                f"richiederebbe costruzioni ausiliarie, mentre il metodo "
                f"vettoriale è equivalente ma più laborioso."
            ),
            "did_you_know": (
                "Il teorema del coseno generalizza il teorema di Pitagora: "
                "quando l'angolo è 90°, cos(90°) = 0 e si ottiene a² + b² = c²."
            ),
            "approfondimento": True,
        }

    def _geo_area_polygon_coordinates(self) -> dict:
        n = random.choice([4, 5, 6])
        shape_names = {4: "quadrilatero", 5: "pentagono", 6: "esagono"}
        shape = shape_names[n]

        # Generate n vertices
        vertices = []
        for i in range(n):
            angle = 2 * 3.14159 * i / n
            r = random.randint(3, 7)
            x = round(r * (1 if i % 2 == 0 else -1) + random.randint(-2, 2))
            y = round(r * (1 if i < n // 2 else -1) + random.randint(-2, 2))
            vertices.append((x, y))

        vertices_str = ", ".join(f"({x},{y})" for x, y in vertices)

        correct = "Geometria analitica (formula di Gauss)"
        distractors = [
            "Geometria analitica (formula di Gauss)",
            "Geometria euclidea sintetica",
            "Approccio trigonometrico",
            "Scomposizione in triangoli",
            "Approccio vettoriale",
            "Metodo grafico",
        ]

        options, correct_index = self._make_strategy_options(correct, distractors)

        return {
            "question": (
                f"Per calcolare l'area di un {shape} con vertici "
                f"{vertices_str}, quale approccio è più efficiente?"
            ),
            "options": options,
            "correct_index": correct_index,
            "explanation": (
                f"Quando si hanno le coordinate dei vertici di un poligono, "
                f"la formula di Gauss (formula del laccio) calcola l'area "
                f"direttamente: A = ½|Σ(xᵢyᵢ₊₁ - xᵢ₊₁yᵢ)|. È un calcolo "
                f"sistematico e veloce, senza bisogno di scomporre il poligono "
                f"o usare trigonometria."
            ),
            "did_you_know": (
                "La formula di Gauss (o formula del laccio/shoelace) funziona "
                "per qualsiasi poligono semplice dato per coordinate, "
                "indipendentemente dal numero di lati."
            ),
            "approfondimento": True,
        }

    def _geo_perpendicular_bisector(self) -> dict:
        x1 = random.randint(-6, 6)
        y1 = random.randint(-6, 6)
        x2 = random.randint(-6, 6)
        y2 = random.randint(-6, 6)
        while x1 == x2 and y1 == y2:
            x2 = random.randint(-6, 6)
            y2 = random.randint(-6, 6)

        correct = "Geometria analitica (determinante)"
        distractors = [
            "Geometria analitica (determinante)",
            "Geometria euclidea sintetica",
            "Approccio trigonometrico",
            "Approccio algebrico diretto",
            "Approccio vettoriale",
            "Metodo grafico",
        ]

        options, correct_index = self._make_strategy_options(correct, distractors)

        return {
            "question": (
                f"Per trovare l'equazione dell'asse del segmento con estremi "
                f"A({x1},{y1}) e B({x2},{y2}), quale approccio è più efficiente?"
            ),
            "options": options,
            "correct_index": correct_index,
            "explanation": (
                f"L'asse di un segmento è il luogo dei punti equidistanti "
                f"dagli estremi. In geometria analitica, basta imporre la "
                f"condizione (x-x₁)² + (y-y₁)² = (x-x₂)² + (y-y₂)² e "
                f"semplificare. Si ottiene direttamente l'equazione della retta "
                f"senza bisogno di calcolare pendenza e punto medio separatamente."
            ),
            "did_you_know": (
                "L'asse del segmento è perpendicolare al segmento e passa "
                "per il suo punto medio. In geometria analitica, la condizione "
                "di equidistanza porta direttamente all'equazione."
            ),
            "approfondimento": True,
        }
