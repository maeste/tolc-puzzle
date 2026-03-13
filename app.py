from flask import Flask, render_template, jsonify, request
from exercises.base import Exercise

app = Flask(__name__)

EXERCISE_TYPES = {
    "trap": {"name": "Trova la Trappola", "icon": "🔍", "desc": "Trova l'errore nascosto nei calcoli"},
    "word": {"name": "Traduci la Storia", "icon": "📖", "desc": "Traduci problemi in equazioni"},
    "graph": {"name": "Che Funzione Sono?", "icon": "📈", "desc": "Associa funzioni e grafici"},
    "logic": {"name": "Detective Logico", "icon": "🕵️", "desc": "Risolvi puzzle di logica formale"},
    "probability": {"name": "Probabilità Visuale", "icon": "🎲", "desc": "Visualizza spazi campionari"},
    "geometry": {"name": "Sherlock Geometrico", "icon": "📐", "desc": "Combina proprietà geometriche"},
    "estimation": {"name": "Stima Flash", "icon": "⚡", "desc": "Stima ordini di grandezza"},
    "solve": {"name": "Calcola e Risolvi", "icon": "🧮", "desc": "Risolvi equazioni e espressioni"},
    "statistics": {"name": "Statistica", "icon": "📊", "desc": "Media, mediana, varianza e altro"},
    "analytic_geo": {"name": "Geometria Analitica", "icon": "📏", "desc": "Rette, distanze e circonferenze nel piano"},
    "inequalities": {"name": "Disequazioni", "icon": "⚖️", "desc": "Disequazioni di 1° e 2° grado, razionali"},
    "simplification": {"name": "Semplifica l'Espressione", "icon": "✏️", "desc": "Semplifica espressioni e identifica la forma equivalente"},
    "always_true": {"name": "Sempre o Mai Vero?", "icon": "🤔", "desc": "Ragiona su proprietà matematiche: sempre, mai o talvolta vere?"},
    "proportional": {"name": "Ragionamento Proporzionale", "icon": "🔄", "desc": "Ragiona su come cambiano le grandezze in una formula"},
    "cross_topic": {"name": "Domande Trasversali", "icon": "🔗", "desc": "Domande che combinano più aree tematiche"},
    "number_sense": {"name": "Senso Numerico", "icon": "🔢", "desc": "Percentuali, frazioni, potenze e notazione scientifica"},
    "which_satisfies": {"name": "Quale Soddisfa?", "icon": "🎯", "desc": "Identifica quale oggetto matematico soddisfa una proprietà"},
    "composition": {"name": "Composizione di Funzioni", "icon": "🔗", "desc": "Esercizi sulla composizione f(g(x)), decomposizione e dominio"},
    "strategy": {"name": "Scelta Strategica", "icon": "🧭", "desc": "Scegli la strategia più efficiente per risolvere il problema"},
}

exercise_registry = {}

# TOLC-B Realistic Exam Question Distribution (20 questions total)
# Based on analysis of 40 real TOLC-B questions.
#
# Category breakdown:
#   Aritmetica/Numeri (~15%):  number_sense (2) + estimation (1)       = 3 questions
#   Algebra (~20%):            solve (2) + inequalities (1) + simpl(1) = 4 questions
#   Geometria (~20%):          geometry (2) + analytic_geo (2)         = 4 questions
#   Funzioni/Grafici (~20%):   word (1) + graph (2) + composition (1) = 4 questions
#   Meta-ragionamento (~10%):  which_satisfies (2)                     = 2 questions
#   Prob+Stat+Logica (~15%):   probability (1) + statistics (1) + logic(1) = 3 questions
#                                                                 Total = 20 questions
#
# Excluded types (still available in learning mode via EXERCISE_TYPES):
#   trap         -- format doesn't exist in real TOLC-B
#   always_true  -- competency embedded in other question types
#   proportional -- competency embedded in other question types
#   cross_topic  -- integration happens naturally in real TOLC-B
REALISTIC_EXAM_WEIGHTS = {
    "number_sense": 2,     # Aritmetica pura
    "solve": 2,            # Algebra: equazioni
    "inequalities": 1,     # Algebra: disequazioni
    "simplification": 1,   # Algebra: semplificazione espressioni
    "which_satisfies": 2,  # Meta-formato "quale soddisfa?" (~10%)
    "geometry": 2,         # Geometria euclidea (SVG)
    "analytic_geo": 2,     # Geometria analitica
    "word": 1,             # Word problems
    "composition": 1,      # Composizione di funzioni
    "probability": 1,      # Probabilità
    "statistics": 1,       # Statistica
    "logic": 1,            # Logica
    "graph": 2,            # Grafici di funzioni (SVG)
    "estimation": 1,       # Stima ordini di grandezza
}


def register_exercise(type_key, cls):
    exercise_registry[type_key] = cls


from exercises.word_modeler import WordModeler
register_exercise("word", WordModeler)

from exercises.trap_calculator import TrapCalculator
register_exercise("trap", TrapCalculator)

from exercises.graph_reader import GraphReader
register_exercise("graph", GraphReader)

from exercises.logic_puzzle import LogicPuzzle
register_exercise("logic", LogicPuzzle)

from exercises.probability_game import ProbabilityGame
register_exercise("probability", ProbabilityGame)

from exercises.geometry_sherlock import GeometrySherlock
register_exercise("geometry", GeometrySherlock)

from exercises.estimation_blitz import EstimationBlitz
register_exercise("estimation", EstimationBlitz)

from exercises.solve_exercise import SolveExercise
register_exercise("solve", SolveExercise)

from exercises.statistics_exercise import StatisticsExercise
register_exercise("statistics", StatisticsExercise)

from exercises.analytic_geometry import AnalyticGeometry
register_exercise("analytic_geo", AnalyticGeometry)

from exercises.inequalities import InequalitiesExercise
register_exercise("inequalities", InequalitiesExercise)

from exercises.simplification import SimplificationExercise
register_exercise("simplification", SimplificationExercise)

from exercises.always_true import AlwaysTrueExercise
register_exercise("always_true", AlwaysTrueExercise)

from exercises.proportional_reasoning import ProportionalReasoning
register_exercise("proportional", ProportionalReasoning)

from exercises.cross_topic import CrossTopicExercise
register_exercise("cross_topic", CrossTopicExercise)

from exercises.number_sense import NumberSense
register_exercise("number_sense", NumberSense)

from exercises.which_satisfies import WhichSatisfies
register_exercise("which_satisfies", WhichSatisfies)

from exercises.function_composition import FunctionComposition
register_exercise("composition", FunctionComposition)

from exercises.strategy_selection import StrategySelection
register_exercise("strategy", StrategySelection)


@app.route("/")
def dashboard():
    return render_template("dashboard.html", exercise_types=EXERCISE_TYPES)


@app.route("/exercise/<exercise_type>")
def exercise_page(exercise_type):
    if exercise_type not in EXERCISE_TYPES:
        return render_template("404.html"), 404
    info = EXERCISE_TYPES[exercise_type]
    return render_template("exercise.html", exercise_type=exercise_type, info=info)


@app.route("/results")
def results():
    return render_template("results.html", exercise_types=EXERCISE_TYPES)


@app.route("/simulation")
def simulation():
    return render_template("simulation.html", exercise_types=EXERCISE_TYPES)


@app.route("/api/exercise/<exercise_type>")
def api_exercise(exercise_type):
    if exercise_type not in exercise_registry:
        return jsonify({"error": f"Tipo esercizio '{exercise_type}' non trovato"}), 404
    difficulty = request.args.get("difficulty", 1, type=int)
    difficulty = max(1, min(3, difficulty))
    ex = exercise_registry[exercise_type]()
    data = ex.generate(difficulty)
    return jsonify(data)


@app.route("/api/check", methods=["POST"])
def api_check():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Nessun dato ricevuto"}), 400
    exercise_type = data.get("type")
    if exercise_type not in exercise_registry:
        return jsonify({"error": f"Tipo esercizio '{exercise_type}' non trovato"}), 404
    ex = exercise_registry[exercise_type]()
    result = ex.check(data)
    return jsonify(result)


@app.route("/api/simulation/exercises")
def api_simulation_exercises():
    """Generate 20 exercises distributed across 9 types for TOLC-B simulation."""
    import random as _random
    distribution = [
        "trap", "trap",
        "word",
        "graph", "graph",
        "logic",
        "probability", "probability",
        "geometry", "geometry",
        "estimation",
        "solve", "solve",
        "statistics", "statistics",
        "simplification",
        "always_true",
        "proportional",
        "cross_topic", "cross_topic",
    ]
    _random.shuffle(distribution)
    exercises = []
    for ex_type in distribution:
        difficulty = _random.randint(1, 3)
        ex = exercise_registry[ex_type]()
        if ex_type == "geometry":
            data = ex.generate(difficulty, text_only=True)
        else:
            data = ex.generate(difficulty)
        data["type"] = ex_type
        data["difficulty"] = difficulty
        exercises.append(data)
    return jsonify(exercises)


@app.route("/time-training")
def time_training():
    return render_template("time_training.html", exercise_types=EXERCISE_TYPES)


@app.route("/realistic-exam")
def realistic_exam():
    return render_template("realistic_exam.html", exercise_types=EXERCISE_TYPES)


@app.route("/api/realistic-exam/exercises")
def api_realistic_exam_exercises():
    """Generate 20 exercises for realistic TOLC-B exam format.

    Uses REALISTIC_EXAM_WEIGHTS to build the question distribution,
    approximating real TOLC-B category frequencies.
    Includes SVG graph questions (graph, geometry types).
    """
    import random as _random
    # Build the flat distribution list from the weights config
    exam_types = []
    for ex_type, count in REALISTIC_EXAM_WEIGHTS.items():
        exam_types.extend([ex_type] * count)
    _random.shuffle(exam_types)
    exercises = []
    for ex_type in exam_types:
        difficulty = _random.choice([1, 2, 2, 2, 3])
        ex = exercise_registry[ex_type]()
        if ex_type in ("word", "estimation"):
            data = ex.generate(difficulty, exam_mode=True)
        elif ex_type == "geometry":
            data = ex.generate(difficulty, text_only=True)
        else:
            data = ex.generate(difficulty)
        data["type"] = ex_type
        data["difficulty"] = difficulty
        # Keep graph_data when present (SVG rendered client-side)
        # Some types (e.g. trap) use "steps" instead of "options";
        # normalise to "options" for consistent exam format.
        if "options" not in data and "steps" in data:
            data["options"] = data.pop("steps")
        # Ensure exactly 5 options
        if "options" not in data:
            data["options"] = []
        if len(data["options"]) < 5:
            while len(data["options"]) < 5:
                data["options"].append("Nessuna delle precedenti")
        elif len(data.get("options", [])) > 5:
            # Keep correct + first 4 wrong
            correct = data["options"][data["correct_index"]]
            others = [o for i, o in enumerate(data["options"]) if i != data["correct_index"]][:4]
            data["options"] = [correct] + others
            data["correct_index"] = 0
            data["options"], data["correct_index"] = Exercise.shuffle_options(data["options"], 0)
        exercises.append(data)
    return jsonify(exercises)


@app.route("/api/types")
def api_types():
    return jsonify(EXERCISE_TYPES)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
