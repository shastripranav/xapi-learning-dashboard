from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, Query

from ..analytics.aggregator import get_statements_df
from ..analytics.completion import learner_completion_summary
from ..analytics.engagement import calculate_engagement_scores
from ..analytics.risk import identify_at_risk
from ..analytics.skills import learner_skill_scores

router = APIRouter(prefix="/api/learners", tags=["learners"])

INACTIVE_DAYS = 14


@router.get("")
def list_learners(
    search: str = Query("", description="Search by name or email"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
):
    """Paginated learner list with search."""
    df = get_statements_df()
    if df.empty:
        return {"learners": [], "total": 0, "page": page, "limit": limit}

    engagement = {e["email"]: e["total_score"] for e in calculate_engagement_scores(df)}
    at_risk_set = {r["email"] for r in identify_at_risk(df)}

    now = datetime.now(timezone.utc)
    learners = []

    for email, group in df.groupby("actor_email"):
        name = group["actor_name"].iloc[0]

        if search:
            q = search.lower()
            if q not in name.lower() and q not in email.lower():
                continue

        done = group[group["verb"].isin({"completed", "passed"})]
        completed_courses = done["activity_id"].nunique()
        scores = group[group["score"].notna()]["score"]
        avg_score = float(scores.mean()) if len(scores) > 0 else 0
        last_active = group["timestamp"].max()
        days_inactive = (now - last_active).days

        if email in at_risk_set:
            status = "at-risk"
        elif days_inactive > INACTIVE_DAYS:
            status = "inactive"
        else:
            status = "active"

        learners.append({
            "email": email,
            "name": name,
            "courses_completed": completed_courses,
            "avg_score": round(avg_score, 3),
            "last_active": last_active.isoformat(),
            "engagement_score": engagement.get(email, 0),
            "status": status,
        })

    learners.sort(key=lambda x: x["name"])
    total = len(learners)
    start = (page - 1) * limit
    return {"learners": learners[start:start + limit], "total": total, "page": page, "limit": limit}


@router.get("/{email}")
def get_learner(email: str):
    df = get_statements_df()
    learner_df = df[df["actor_email"] == email]
    if learner_df.empty:
        raise HTTPException(status_code=404, detail="Learner not found")

    name = learner_df["actor_name"].iloc[0]
    engagement = calculate_engagement_scores(df)
    eng = next((e for e in engagement if e["email"] == email), None)

    return {
        "email": email,
        "name": name,
        "statement_count": len(learner_df),
        "first_activity": learner_df["timestamp"].min().isoformat(),
        "last_activity": learner_df["timestamp"].max().isoformat(),
        "engagement": eng,
    }


@router.get("/{email}/skills")
def get_learner_skills(email: str):
    df = get_statements_df()
    if df[df["actor_email"] == email].empty:
        raise HTTPException(status_code=404, detail="Learner not found")

    skills = learner_skill_scores(df, email)

    # cohort averages for overlay
    all_emails = df["actor_email"].unique()
    skill_totals: dict[str, list[float]] = {}
    for e in all_emails:
        for s in learner_skill_scores(df, e):
            if s["score"] > 0:
                skill_totals.setdefault(s["skill"], []).append(s["score"])

    cohort_avg = {
        sk: round(sum(v) / len(v), 3) for sk, v in skill_totals.items()
    }

    return {"learner_skills": skills, "cohort_avg": cohort_avg}


@router.get("/{email}/activity")
def get_learner_activity(email: str, limit: int = 20):
    df = get_statements_df()
    learner_df = df[df["actor_email"] == email].sort_values("timestamp", ascending=False)
    if learner_df.empty:
        raise HTTPException(status_code=404, detail="Learner not found")

    recent = learner_df.head(limit)
    return [
        {
            "verb": row["verb"],
            "activity_name": row["activity_name"],
            "score": row["score"] if row["score"] == row["score"] else None,
            "timestamp": row["timestamp"].isoformat(),
        }
        for _, row in recent.iterrows()
    ]


@router.get("/{email}/progress")
def get_learner_progress(email: str):
    df = get_statements_df()
    if df[df["actor_email"] == email].empty:
        raise HTTPException(status_code=404, detail="Learner not found")
    return learner_completion_summary(df, email)
