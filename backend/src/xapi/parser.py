"""Convert raw xAPI JSON statements into ParsedStatement objects.

Handles the messy reality of xAPI — actors without names, missing scores,
duration in various ISO 8601 formats, etc.
"""

import re
from datetime import datetime

from ..models import ParsedStatement
from .verbs import resolve_verb


def parse_statement(raw: dict) -> ParsedStatement | None:
    verb = resolve_verb(raw.get("verb", {}))
    if verb is None:
        return None

    actor = raw.get("actor", {})
    email = _extract_email(actor)
    if not email:
        return None

    obj = raw.get("object", {})
    result = raw.get("result", {})
    score_obj = result.get("score", {})

    return ParsedStatement(
        actor_email=email,
        actor_name=actor.get("name", email.split("@")[0]),
        verb=verb,
        activity_id=obj.get("id", "unknown"),
        activity_name=_get_activity_name(obj),
        score=score_obj.get("scaled"),
        completion=result.get("completion"),
        duration_minutes=_parse_duration(result.get("duration")),
        timestamp=_parse_timestamp(raw.get("timestamp", "")),
        raw=raw,
    )


def parse_batch(raw_statements: list[dict]) -> list[ParsedStatement]:
    """Parse a list of raw xAPI statements, skipping any that fail."""
    parsed = []
    for stmt in raw_statements:
        try:
            p = parse_statement(stmt)
            if p is not None:
                parsed.append(p)
        except Exception:
            continue
    return parsed


def _extract_email(actor: dict) -> str | None:
    mbox = actor.get("mbox", "")
    if mbox.startswith("mailto:"):
        return mbox[7:]
    if "@" in mbox:
        return mbox
    account = actor.get("account", {})
    return account.get("name")


def _get_activity_name(obj: dict) -> str:
    defn = obj.get("definition", {})
    name = defn.get("name", {})
    # xAPI names are language-mapped
    if isinstance(name, dict):
        return name.get("en-US", name.get("en", next(iter(name.values()), "Unknown")))
    return str(name) if name else obj.get("id", "Unknown")


# ISO 8601 duration: PT1H30M, PT45M, PT2H, PT1H15M30S
_DURATION_RE = re.compile(
    r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+(?:\.\d+)?)S)?", re.IGNORECASE
)


def _parse_duration(duration_str: str | None) -> float | None:
    if not duration_str:
        return None
    m = _DURATION_RE.match(duration_str)
    if not m:
        return None
    hours = int(m.group(1) or 0)
    minutes = int(m.group(2) or 0)
    seconds = float(m.group(3) or 0)
    total = hours * 60 + minutes + seconds / 60
    return round(total, 2) if total > 0 else None


def _parse_timestamp(ts: str) -> datetime:
    if not ts:
        return datetime.now()
    ts = ts.replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(ts)
    except ValueError:
        return datetime.now()
