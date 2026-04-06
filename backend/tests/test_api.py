"""API endpoint integration tests using FastAPI TestClient."""
from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from src.analytics.aggregator import invalidate_cache, set_course_metadata
from src.course_catalog import COURSES
from src.db import clear_statements, close_db, get_db, insert_statements
from src.main import app
from src.xapi.parser import parse_batch

client = TestClient(app)

DEMO_PATH = Path(__file__).parent.parent / "data" / "demo_statements.json"


@pytest.fixture(autouse=True)
def setup_db():
    get_db()
    clear_statements()
    set_course_metadata(COURSES)
    _load_subset()
    yield
    close_db()


def _load_subset():
    """Load a small subset of demo data for API tests."""
    if not DEMO_PATH.exists():
        return
    with open(DEMO_PATH) as f:
        raw = json.load(f)
    parsed = parse_batch(raw[:500])
    rows = [
        {
            "actor_email": s.actor_email,
            "actor_name": s.actor_name,
            "verb": s.verb,
            "activity_id": s.activity_id,
            "activity_name": s.activity_name,
            "score": s.score,
            "completion": 1 if s.completion else 0 if s.completion is not None else None,
            "duration_minutes": s.duration_minutes,
            "timestamp": s.timestamp.isoformat(),
            "raw_json": None,
        }
        for s in parsed
    ]
    insert_statements(rows)
    invalidate_cache()


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_overview_endpoint():
    resp = client.get("/api/overview")
    assert resp.status_code == 200
    data = resp.json()
    assert "total_learners" in data
    assert data["total_learners"] > 0


def test_funnel_endpoint():
    resp = client.get("/api/overview/funnel")
    assert resp.status_code == 200
    data = resp.json()
    assert data["registered"] >= data["completed"]


def test_learner_list_pagination():
    resp = client.get("/api/learners?page=1&limit=5")
    assert resp.status_code == 200
    data = resp.json()
    assert "learners" in data
    assert len(data["learners"]) <= 5
    assert data["total"] > 0


def test_course_list():
    resp = client.get("/api/courses")
    assert resp.status_code == 200
    courses = resp.json()
    assert len(courses) > 0
    assert "completion_rate" in courses[0]


def test_skills_heatmap():
    resp = client.get("/api/skills/heatmap")
    assert resp.status_code == 200
    data = resp.json()
    assert "skills" in data
    assert "learners" in data


def test_engagement_scores():
    resp = client.get("/api/engagement/scores")
    assert resp.status_code == 200
    scores = resp.json()
    assert len(scores) > 0
    assert "total_score" in scores[0]


def test_data_source_status():
    resp = client.get("/api/data-source/status")
    assert resp.status_code == 200
    data = resp.json()
    assert "statement_count" in data
