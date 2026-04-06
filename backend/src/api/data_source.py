"""Data source management — LRS connection, JSON upload, demo data loading."""

import json
import logging
from datetime import datetime, timezone
from pathlib import Path

from fastapi import APIRouter, HTTPException, UploadFile

from ..analytics.aggregator import invalidate_cache, set_course_metadata
from ..db import clear_statements, get_statement_count, insert_statements, set_metadata
from ..models import LRSConnection
from ..xapi.client import LRSClient
from ..xapi.parser import parse_batch

router = APIRouter(tags=["data-source"])
log = logging.getLogger(__name__)

DEMO_DATA_PATH = Path(__file__).parent.parent.parent / "data" / "demo_statements.json"


def _load_statements_to_db(raw_statements: list[dict]) -> int:
    parsed = parse_batch(raw_statements)
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
            "raw_json": json.dumps(s.raw) if s.raw else None,
        }
        for s in parsed
    ]
    insert_statements(rows)
    invalidate_cache()
    return len(rows)


@router.post("/api/load-demo")
def load_demo():
    """Load built-in demo dataset — the critical feature for GitHub visitors."""
    if not DEMO_DATA_PATH.exists():
        raise HTTPException(
            status_code=500,
            detail="Demo data not found. Run generate_demo_data.py first.",
        )

    clear_statements()

    with open(DEMO_DATA_PATH) as f:
        raw = json.load(f)

    count = _load_statements_to_db(raw)
    set_metadata("data_mode", "demo")
    set_metadata("last_sync", datetime.now(timezone.utc).isoformat())

    _init_course_metadata()
    log.info(f"Loaded {count} demo statements")
    return {"loaded": count, "mode": "demo"}


@router.post("/api/connect-lrs")
async def connect_lrs(conn: LRSConnection):
    client = LRSClient(conn.endpoint, conn.username, conn.password)
    try:
        ok = await client.test_connection()
        if not ok:
            raise HTTPException(status_code=400, detail="LRS connection failed")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Cannot reach LRS: {e}")

    try:
        statements = await client.fetch_statements()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Failed to fetch statements: {e}")

    clear_statements()
    count = _load_statements_to_db(statements)
    set_metadata("data_mode", "lrs")
    set_metadata("lrs_endpoint", conn.endpoint)
    set_metadata("last_sync", datetime.now(timezone.utc).isoformat())
    _init_course_metadata()

    return {"loaded": count, "mode": "lrs", "endpoint": conn.endpoint}


@router.post("/api/upload")
async def upload_statements(file: UploadFile):
    content = await file.read()
    try:
        raw = json.loads(content)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON file")

    if not isinstance(raw, list):
        raise HTTPException(status_code=400, detail="Expected a JSON array of statements")

    clear_statements()
    count = _load_statements_to_db(raw)
    set_metadata("data_mode", "upload")
    set_metadata("last_sync", datetime.now(timezone.utc).isoformat())
    _init_course_metadata()

    return {"loaded": count, "mode": "upload"}


@router.get("/api/data-source/status")
def data_source_status():
    from ..db import get_metadata

    return {
        "mode": get_metadata("data_mode") or "none",
        "statement_count": get_statement_count(),
        "last_sync": get_metadata("last_sync"),
        "lrs_endpoint": get_metadata("lrs_endpoint"),
    }


def _init_course_metadata():
    from ..course_catalog import COURSES
    set_course_metadata(COURSES)
