"""Tests for Daily Session mode (TOLC-49)."""
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

def test_daily_session_route_returns_200(client):
    """GET /daily-session should return 200."""
    resp = client.get("/daily-session")
    assert resp.status_code == 200


def test_daily_session_route_returns_html(client):
    """Response should be HTML."""
    resp = client.get("/daily-session")
    assert "text/html" in resp.content_type


def test_daily_session_contains_title(client):
    """Page should contain the session title."""
    resp = client.get("/daily-session")
    assert "Sessione di Oggi".encode() in resp.data


def test_daily_session_contains_exercise_area(client):
    """Page should contain the exercise area element."""
    resp = client.get("/daily-session")
    assert b"exercise-area" in resp.data


def test_daily_session_contains_session_report(client):
    """Page should contain the session report element."""
    resp = client.get("/daily-session")
    assert b"session-report" in resp.data


def test_daily_session_contains_progress_bar(client):
    """Page should contain the progress bar."""
    resp = client.get("/daily-session")
    assert b"session-progress" in resp.data


def test_daily_session_loads_js(client):
    """Page should load daily_session.js."""
    resp = client.get("/daily-session")
    assert b"daily_session.js" in resp.data


# --- API Endpoint Tests ---

def test_api_returns_exercises(client):
    """API should return a list of exercises."""
    resp = client.get("/api/daily-session/exercises")
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)
    assert len(data) == 15  # default count


def test_api_respects_count_param(client):
    """API should respect the count query param."""
    resp = client.get("/api/daily-session/exercises?count=5")
    data = resp.get_json()
    assert len(data) == 5


def test_api_count_capped_at_20(client):
    """API should cap count at 20."""
    resp = client.get("/api/daily-session/exercises?count=50")
    data = resp.get_json()
    assert len(data) <= 20


def test_api_count_minimum_1(client):
    """API should enforce minimum count of 1."""
    resp = client.get("/api/daily-session/exercises?count=0")
    data = resp.get_json()
    assert len(data) >= 1


def test_api_handles_session_param(client):
    """API should handle a session param with type/difficulty items."""
    session = [
        {"type": "solve", "difficulty": 1, "reason": "overdue"},
        {"type": "graph", "difficulty": 2, "reason": "new"},
    ]
    url = "/api/daily-session/exercises?count=10&session=" + json.dumps(session)
    resp = client.get(url)
    data = resp.get_json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["type"] == "solve"
    assert data[0]["difficulty"] == 1
    assert data[0]["reason"] == "overdue"
    assert data[1]["type"] == "graph"
    assert data[1]["difficulty"] == 2


def test_api_exercises_have_type_field(client):
    """Each exercise should have a type field."""
    resp = client.get("/api/daily-session/exercises?count=3")
    data = resp.get_json()
    for ex in data:
        assert "type" in ex
        assert ex["type"] in exercise_registry


def test_api_exercises_have_difficulty_field(client):
    """Each exercise should have a difficulty field."""
    resp = client.get("/api/daily-session/exercises?count=3")
    data = resp.get_json()
    for ex in data:
        assert "difficulty" in ex
        assert ex["difficulty"] in (1, 2, 3)


def test_api_exercises_have_question(client):
    """Each exercise should have a question field."""
    resp = client.get("/api/daily-session/exercises?count=3")
    data = resp.get_json()
    for ex in data:
        assert "question" in ex
        assert len(ex["question"]) > 0


def test_api_exercises_have_options_or_steps(client):
    """Each exercise should have options or steps."""
    resp = client.get("/api/daily-session/exercises?count=5")
    data = resp.get_json()
    for ex in data:
        assert "options" in ex or "steps" in ex


def test_api_exercises_have_correct_index(client):
    """Each exercise should have correct_index."""
    resp = client.get("/api/daily-session/exercises?count=5")
    data = resp.get_json()
    for ex in data:
        assert "correct_index" in ex


def test_api_fallback_without_session(client):
    """Without session param, should generate random exercises."""
    resp = client.get("/api/daily-session/exercises?count=10")
    data = resp.get_json()
    assert len(data) == 10
    for ex in data:
        assert "type" in ex
        assert "reason" in ex
        assert ex["reason"] == "practice"


def test_api_empty_session_returns_empty(client):
    """An empty session array should return an empty list."""
    url = "/api/daily-session/exercises?session=" + json.dumps([])
    resp = client.get(url)
    data = resp.get_json()
    assert isinstance(data, list)
    assert len(data) == 0


def test_api_invalid_session_json_falls_back(client):
    """Invalid JSON in session param should trigger fallback."""
    resp = client.get("/api/daily-session/exercises?count=3&session=not-json")
    data = resp.get_json()
    assert isinstance(data, list)
    assert len(data) == 3


def test_api_skips_unknown_types_in_session(client):
    """Unknown exercise types in session should be skipped."""
    session = [
        {"type": "solve", "difficulty": 1, "reason": "overdue"},
        {"type": "nonexistent_type", "difficulty": 2, "reason": "new"},
        {"type": "graph", "difficulty": 2, "reason": "review"},
    ]
    url = "/api/daily-session/exercises?session=" + json.dumps(session)
    resp = client.get(url)
    data = resp.get_json()
    assert len(data) == 2
    types = [ex["type"] for ex in data]
    assert "nonexistent_type" not in types


def test_api_clamps_difficulty(client):
    """Difficulty should be clamped to 1-3."""
    session = [
        {"type": "solve", "difficulty": 0, "reason": "overdue"},
        {"type": "solve", "difficulty": 5, "reason": "review"},
    ]
    url = "/api/daily-session/exercises?session=" + json.dumps(session)
    resp = client.get(url)
    data = resp.get_json()
    assert data[0]["difficulty"] == 1
    assert data[1]["difficulty"] == 3


# --- Dashboard Badge Tests ---

def test_dashboard_contains_daily_badge(client):
    """Dashboard should contain the SRS daily badge element."""
    resp = client.get("/")
    assert b"srs-daily-badge" in resp.data
    assert b"daily-badge-text" in resp.data


# --- Navigation Tests ---

def test_nav_contains_session_link(client):
    """Navigation should contain a link to /daily-session."""
    resp = client.get("/")
    assert b"/daily-session" in resp.data
    assert "Sessione".encode() in resp.data
