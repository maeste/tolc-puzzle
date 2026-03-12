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
}

exercise_registry = {}


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
        "word", "word",
        "graph", "graph",
        "logic", "logic",
        "probability", "probability",
        "geometry", "geometry",
        "estimation", "estimation",
        "solve", "solve", "solve",
        "statistics", "statistics", "statistics",
    ]
    _random.shuffle(distribution)
    exercises = []
    for ex_type in distribution:
        difficulty = _random.randint(1, 3)
        ex = exercise_registry[ex_type]()
        data = ex.generate(difficulty)
        data["type"] = ex_type
        data["difficulty"] = difficulty
        exercises.append(data)
    return jsonify(exercises)


@app.route("/realistic-exam")
def realistic_exam():
    return render_template("realistic_exam.html", exercise_types=EXERCISE_TYPES)


@app.route("/api/realistic-exam/exercises")
def api_realistic_exam_exercises():
    """Generate 20 text-only exercises for realistic TOLC-B exam format."""
    import random as _random
    # Use types that work well in text-only format (no graph type)
    text_types = [
        "trap", "trap",
        "word", "word",
        "logic", "logic",
        "solve", "solve", "solve",
        "statistics", "statistics",
        "analytic_geo", "analytic_geo",
        "inequalities", "inequalities",
        "probability", "probability",
        "geometry", "geometry",
        "estimation",
    ]
    _random.shuffle(text_types)
    exercises = []
    for ex_type in text_types:
        difficulty = _random.choice([1, 2, 2, 2, 3])
        ex = exercise_registry[ex_type]()
        data = ex.generate(difficulty)
        data["type"] = ex_type
        data["difficulty"] = difficulty
        # Remove graphical data for text-only format
        data.pop("graph_data", None)
        # Ensure exactly 5 options
        if len(data.get("options", [])) < 5:
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
