from datetime import datetime, timedelta, timezone

from fastapi import APIRouter

from ..analytics.aggregator import daily_activity, get_statements_df
from ..analytics.completion import completion_funnel, course_completion_rates

router = APIRouter(prefix="/api/overview", tags=["overview"])


@router.get("")
def get_overview():
    """KPI cards and summary stats for the overview page."""
    df = get_statements_df()
    if df.empty:
        return {"total_learners": 0, "active_30d": 0, "avg_completion_rate": 0, "avg_score": 0}

    now = datetime.now(timezone.utc)
    cutoff_30d = now - timedelta(days=30)
    cutoff_prev = now - timedelta(days=60)

    total_learners = df["actor_email"].nunique()

    recent = df[df["timestamp"] >= cutoff_30d]
    active_30d = recent["actor_email"].nunique()

    prev_period = df[(df["timestamp"] >= cutoff_prev) & (df["timestamp"] < cutoff_30d)]
    prev_active = prev_period["actor_email"].nunique()

    rates = course_completion_rates(df)
    avg_rate = sum(r["rate"] for r in rates.values()) / len(rates) if rates else 0

    scores = df[df["score"].notna()]["score"]
    avg_score = float(scores.mean()) if len(scores) > 0 else 0

    prev_scores = prev_period[prev_period["score"].notna()]["score"]
    prev_avg_score = float(prev_scores.mean()) if len(prev_scores) > 0 else avg_score

    return {
        "total_learners": total_learners,
        "active_30d": active_30d,
        "active_trend": active_30d - prev_active,
        "avg_completion_rate": round(avg_rate, 4),
        "avg_score": round(avg_score, 4),
        "score_trend": round(avg_score - prev_avg_score, 4),
    }


@router.get("/funnel")
def get_funnel():
    df = get_statements_df()
    if df.empty:
        return {
            "total_learners": 0,
            "registered": 0,
            "started": 0,
            "in_progress": 0,
            "completed": 0,
        }
    return completion_funnel(df)


@router.get("/timeline")
def get_timeline(days: int = 90):
    df = get_statements_df()
    return daily_activity(df, days=days)


@router.get("/top-courses")
def get_top_courses(limit: int = 5):
    df = get_statements_df()
    if df.empty:
        return []

    rates = course_completion_rates(df)
    courses = []
    for cid, data in rates.items():
        scores = df[(df["activity_id"] == cid) & (df["score"].notna())]["score"]
        avg_sc = float(scores.mean()) if len(scores) > 0 else 0

        courses.append({
            "course_id": cid,
            "course_name": data["course_name"],
            "enrolled": data["enrolled"],
            "completed": data["completed"],
            "completion_rate": data["rate"],
            "avg_score": round(avg_sc, 3),
        })

    courses.sort(key=lambda c: c["enrolled"], reverse=True)
    return courses[:limit]
