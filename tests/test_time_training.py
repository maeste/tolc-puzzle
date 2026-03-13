"""Tests for Time Training mode (TOLC-45)."""
import json

import pytest

from app import app, EXERCISE_TYPES, exercise_registry


@pytest.fixture
def client():
    """Flask test client."""
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


# --- Route Tests ---

def test_time_training_route_returns_200(client):
    """GET /time-training should return 200."""
    resp = client.get("/time-training")
    assert resp.status_code == 200


def test_time_training_route_returns_html(client):
    """Response should be HTML."""
    resp = client.get("/time-training")
    assert b"text/html" in resp.content_type.encode()


def test_time_training_contains_title(client):
    """Page should contain the training title."""
    resp = client.get("/time-training")
    assert "Allenamento Gestione Tempo".encode() in resp.data


def test_time_training_contains_settings(client):
    """Page should contain settings controls."""
    resp = client.get("/time-training")
    html = resp.data.decode()
    assert "numQuestions" in html
    assert "timeout" in html


def test_time_training_contains_timer_element(client):
    """Page should contain the timer display."""
    resp = client.get("/time-training")
    html = resp.data.decode()
    assert "tt-timer-circle" in html
    assert "tt-timer-text" in html


def test_time_training_contains_start_button(client):
    """Page should contain the start button."""
    resp = client.get("/time-training")
    assert "btn-start-tt".encode() in resp.data


def test_time_training_contains_exercise_types(client):
    """Page should render exercise type checkboxes."""
    resp = client.get("/time-training")
    html = resp.data.decode()
    # Should contain at least a few exercise types
    assert "tt-type-checkboxes" in html
    for key in ["solve", "graph", "logic"]:
        assert key in html


def test_time_training_contains_results_section(client):
    """Page should contain the results screen (hidden initially)."""
    resp = client.get("/time-training")
    html = resp.data.decode()
    assert "tt-results" in html
    assert "tt-scatter-plot" in html


def test_time_training_loads_js(client):
    """Page should load the time_training.js script."""
    resp = client.get("/time-training")
    assert b"time_training.js" in resp.data


def test_time_training_js_file_exists(client):
    """The JS file should be accessible via static route."""
    resp = client.get("/static/js/time_training.js")
    assert resp.status_code == 200


# --- Exercise API Integration ---

def test_exercise_api_works_for_all_registered_types(client):
    """Each registered exercise type should return valid JSON from the API."""
    for ex_type in exercise_registry:
        resp = client.get(f"/api/exercise/{ex_type}?difficulty=2")
        assert resp.status_code == 200, f"Failed for type: {ex_type}"
        data = resp.get_json()
        assert "question" in data, f"No question for type: {ex_type}"


def test_exercise_api_returns_correct_index(client):
    """Exercises should include correct_index."""
    for ex_type in list(exercise_registry.keys())[:5]:
        resp = client.get(f"/api/exercise/{ex_type}?difficulty=1")
        data = resp.get_json()
        assert "correct_index" in data or "steps" in data, f"Missing correct_index for {ex_type}"


# --- EV Calculation Logic (Python equivalents) ---

def _calculate_ev(remaining_options):
    """Calculate expected value of guessing with remaining options.

    TOLC scoring: +1 correct, -0.25 wrong.
    EV = (1/N)*1 + ((N-1)/N)*(-0.25)
    """
    if remaining_options <= 0:
        return float("-inf")
    return (1 / remaining_options) * 1 + ((remaining_options - 1) / remaining_options) * (-0.25)


def test_ev_5_options_is_zero():
    """With 5 options (no elimination), EV = 0 (break-even)."""
    ev = _calculate_ev(5)
    assert ev == pytest.approx(0.0)


def test_ev_4_options_is_slightly_positive():
    """With 4 options (1 eliminated), EV is slightly positive but below threshold."""
    ev = _calculate_ev(4)
    assert ev > 0
    assert ev < 0.1  # small positive, JS only shows hint at >= 2 eliminated


def test_ev_3_options_is_positive():
    """With 3 options (2 eliminated), EV should be positive."""
    ev = _calculate_ev(3)
    assert ev > 0


def test_ev_2_options_is_positive():
    """With 2 options (3 eliminated), EV should be highly positive."""
    ev = _calculate_ev(2)
    assert ev > 0
    assert ev > _calculate_ev(3)


def test_ev_1_option_is_one():
    """With 1 option (4 eliminated), EV should be 1 (certain correct)."""
    ev = _calculate_ev(1)
    assert ev == pytest.approx(1.0)


# --- TOLC Scoring Logic ---

def _tolc_score(correct, wrong, skipped):
    """Calculate TOLC score: +1 correct, -0.25 wrong, 0 skip."""
    return correct * 1 + wrong * (-0.25) + skipped * 0


def test_tolc_score_all_correct():
    """All correct should give max score."""
    assert _tolc_score(20, 0, 0) == 20.0


def test_tolc_score_all_wrong():
    """All wrong should give -5."""
    assert _tolc_score(0, 20, 0) == -5.0


def test_tolc_score_all_skipped():
    """All skipped should give 0."""
    assert _tolc_score(0, 0, 20) == 0.0


def test_tolc_score_mixed():
    """Mixed results should calculate correctly."""
    # 10 correct, 5 wrong, 5 skipped
    score = _tolc_score(10, 5, 5)
    assert score == pytest.approx(10 - 1.25)


# --- Strategy Feedback Logic ---

def _get_feedback(result, difficulty, time_spent, timeout, eliminated_count):
    """Python equivalent of JS getQuestionFeedback."""
    if result == "skip" and difficulty == 3:
        return "Buona scelta"
    if result == "correct" and time_spent < timeout * 0.4:
        return "Ottimo ritmo!"
    if result == "wrong" and time_spent > timeout * 0.7:
        return "Troppo tempo"
    if result == "correct" and eliminated_count >= 2:
        return "Eliminazione + risposta"
    if result == "skip" and time_spent >= timeout * 0.95:
        return "Tempo scaduto"
    return ""


def test_feedback_skip_hard_question():
    """Skipping a hard question should be positive feedback."""
    fb = _get_feedback("skip", 3, 60, 150, 0)
    assert "Buona scelta" in fb


def test_feedback_fast_correct():
    """Fast correct answer gets positive feedback."""
    fb = _get_feedback("correct", 2, 40, 150, 0)
    assert "Ottimo ritmo" in fb


def test_feedback_slow_wrong():
    """Slow wrong answer gets warning."""
    fb = _get_feedback("wrong", 2, 120, 150, 0)
    assert "Troppo tempo" in fb


def test_feedback_elimination_guess():
    """Correct after elimination gets strategy praise."""
    fb = _get_feedback("correct", 2, 100, 150, 2)
    assert "Eliminazione" in fb


def test_feedback_timeout():
    """Timed-out question gets timeout feedback."""
    fb = _get_feedback("skip", 2, 148, 150, 0)
    assert "Tempo scaduto" in fb


def test_feedback_normal_answer():
    """Normal answer without special condition returns empty."""
    fb = _get_feedback("correct", 2, 90, 150, 0)
    assert fb == ""


# --- Dashboard Link ---

def test_dashboard_has_time_training_link(client):
    """Dashboard should contain a link to time training."""
    resp = client.get("/")
    assert b"/time-training" in resp.data


# --- Navigation ---

def test_base_nav_has_tempo_link(client):
    """Base template nav should include Tempo link."""
    resp = client.get("/time-training")
    assert b"Tempo" in resp.data
