"""Shared fixtures for analytics tests."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from src.analytics.aggregator import set_course_metadata
from src.course_catalog import COURSES
from src.db import clear_statements, close_db, get_db, insert_statements
from src.xapi.parser import parse_batch


@pytest.fixture(autouse=True)
def clean_db():
    """Fresh DB for every test."""
    get_db()
    clear_statements()
    set_course_metadata(COURSES)
    yield
    close_db()


@pytest.fixture
def sample_statements():
    """Minimal set of statements for unit tests."""
    now = datetime.now(timezone.utc)
    py = ("course-python-101", "Python Fundamentals")
    cl = ("course-cloud-arch", "Cloud Architecture")
    base = [
        _stmt("alice@co.com", "Alice", "registered",
              *py, now - timedelta(days=30)),
        _stmt("alice@co.com", "Alice", "initialized",
              *py, now - timedelta(days=29)),
        _stmt("alice@co.com", "Alice", "experienced",
              *py, now - timedelta(days=28), duration_min=25),
        _stmt("alice@co.com", "Alice", "experienced",
              *py, now - timedelta(days=27), duration_min=30),
        _stmt("alice@co.com", "Alice", "completed",
              *py, now - timedelta(days=25), score=0.85,
              completion=True),
        _stmt("alice@co.com", "Alice", "passed",
              *py, now - timedelta(days=25), score=0.85),
        _stmt("bob@co.com", "Bob", "registered",
              *py, now - timedelta(days=20)),
        _stmt("bob@co.com", "Bob", "initialized",
              *py, now - timedelta(days=19)),
        _stmt("bob@co.com", "Bob", "experienced",
              *py, now - timedelta(days=18), duration_min=15),
        _stmt("bob@co.com", "Bob", "scored",
              *py, now - timedelta(days=5), score=0.55),
        _stmt("charlie@co.com", "Charlie", "registered",
              *cl, now - timedelta(days=60)),
        _stmt("charlie@co.com", "Charlie", "experienced",
              *cl, now - timedelta(days=50), duration_min=40),
        _stmt("charlie@co.com", "Charlie", "scored",
              *cl, now - timedelta(days=45), score=0.70),
        _stmt("charlie@co.com", "Charlie", "scored",
              *cl, now - timedelta(days=40), score=0.60),
        _stmt("charlie@co.com", "Charlie", "scored",
              *cl, now - timedelta(days=35), score=0.50),
    ]
    return base


@pytest.fixture
def loaded_db(sample_statements):
    parsed = parse_batch(sample_statements)
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
    from src.analytics.aggregator import invalidate_cache
    invalidate_cache()
    return rows


def _stmt(
    email, name, verb, course_id, course_name, ts,
    score=None, completion=None, duration_min=None,
):
    from src.xapi.verbs import SHORTNAME_TO_IRI
    stmt = {
        "actor": {"mbox": f"mailto:{email}", "name": name},
        "verb": {"id": SHORTNAME_TO_IRI[verb], "display": {"en-US": verb}},
        "object": {
            "id": course_id,
            "definition": {"name": {"en-US": course_name}},
        },
        "timestamp": ts.isoformat(),
    }
    if score is not None or completion is not None or duration_min is not None:
        result = {}
        if score is not None:
            result["score"] = {"scaled": score}
        if completion is not None:
            result["completion"] = completion
        if duration_min is not None:
            m = int(duration_min)
            result["duration"] = f"PT{m}M0S"
        stmt["result"] = result
    return stmt
