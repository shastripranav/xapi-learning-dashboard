from fastapi import APIRouter, HTTPException

from ..analytics.aggregator import COURSE_METADATA, get_statements_df
from ..analytics.completion import course_completion_rates

router = APIRouter(prefix="/api/courses", tags=["courses"])


@router.get("")
def list_courses():
    df = get_statements_df()
    if df.empty:
        return []

    rates = course_completion_rates(df)
    courses = []

    for cid, data in rates.items():
        course_df = df[df["activity_id"] == cid]
        scores = course_df[course_df["score"].notna()]["score"]
        durations = course_df[course_df["duration_minutes"].notna()]["duration_minutes"]
        meta = COURSE_METADATA.get(cid, {})

        courses.append({
            "course_id": cid,
            "course_name": data["course_name"],
            "domain": meta.get("domain", ""),
            "difficulty": meta.get("difficulty", ""),
            "enrollment_count": data["enrolled"],
            "completion_count": data["completed"],
            "completion_rate": data["rate"],
            "avg_score": round(float(scores.mean()), 3) if len(scores) > 0 else 0,
            "avg_duration_minutes": round(float(durations.mean()), 1) if len(durations) > 0 else 0,
        })

    courses.sort(key=lambda c: c["enrollment_count"], reverse=True)
    return courses


@router.get("/{course_id}")
def get_course(course_id: str):
    df = get_statements_df()
    course_df = df[df["activity_id"] == course_id]
    if course_df.empty:
        raise HTTPException(status_code=404, detail="Course not found")

    rates = course_completion_rates(df)
    rate_data = rates.get(course_id, {"enrolled": 0, "completed": 0, "rate": 0})
    meta = COURSE_METADATA.get(course_id, {})
    scores = course_df[course_df["score"].notna()]["score"]

    # weekly completion trend
    completed_df = course_df[course_df["verb"].isin({"completed", "passed"})].copy()
    completed_df["week"] = completed_df["timestamp"].dt.isocalendar().week
    weekly = completed_df.groupby("week").size().reset_index(name="completions")
    weekly_trend = [
        {"week": int(w), "completions": int(c)}
        for w, c in zip(weekly["week"], weekly["completions"])
    ]

    return {
        "course_id": course_id,
        "course_name": rate_data.get("course_name", course_id),
        "domain": meta.get("domain", ""),
        "difficulty": meta.get("difficulty", ""),
        "enrollment_count": rate_data["enrolled"],
        "completion_count": rate_data["completed"],
        "completion_rate": rate_data["rate"],
        "avg_score": round(float(scores.mean()), 3) if len(scores) > 0 else 0,
        "total_statements": len(course_df),
        "unique_learners": course_df["actor_email"].nunique(),
        "weekly_completions": weekly_trend,
    }


@router.get("/{course_id}/scores")
def get_score_distribution(course_id: str):
    """Score histogram data — buckets of 10 (0-10, 10-20, ... 90-100)."""
    df = get_statements_df()
    course_scores = df[(df["activity_id"] == course_id) & (df["score"].notna())]["score"]
    if course_scores.empty:
        return []

    buckets = []
    for low in range(0, 100, 10):
        high = low + 10
        count = int(((course_scores * 100 >= low) & (course_scores * 100 < high)).sum())
        buckets.append({"range": f"{low}-{high}", "count": count})

    # catch perfect 100s
    perfect = int((course_scores * 100 >= 100).sum())
    if perfect > 0 and buckets:
        buckets[-1]["count"] += perfect

    return buckets


@router.get("/{course_id}/dropoff")
def get_dropoff_analysis(course_id: str):
    """Module-level drop-off: what % of starters reach each module stage."""
    df = get_statements_df()
    course_df = df[df["activity_id"] == course_id]
    if course_df.empty:
        return []

    meta = COURSE_METADATA.get(course_id, {})
    n_modules = meta.get("modules", 8)

    # FIXME: xAPI doesn't natively track module-level progress in a single activity
    # We approximate using statement count per learner as a proxy for depth
    per_learner = course_df.groupby("actor_email").size()
    total_starters = len(per_learner)

    stages = []
    for i in range(1, n_modules + 1):
        threshold = i * 1.5
        reached = int((per_learner >= threshold).sum())
        pct = round(reached / total_starters, 3) if total_starters > 0 else 0
        stages.append({
            "module": f"Module {i}",
            "learners_reached": reached,
            "pct_of_starters": pct,
        })

    return stages
