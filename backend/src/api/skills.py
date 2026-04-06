from fastapi import APIRouter

from ..analytics.aggregator import get_statements_df
from ..analytics.skills import org_skill_averages, skill_heatmap_data

router = APIRouter(prefix="/api/skills", tags=["skills"])


@router.get("")
def list_skills():
    df = get_statements_df()
    if df.empty:
        return []
    return org_skill_averages(df)


@router.get("/heatmap")
def get_heatmap():
    df = get_statements_df()
    if df.empty:
        return {"skills": [], "learners": []}
    return skill_heatmap_data(df)


@router.get("/distribution")
def get_distribution():
    """Score distributions per skill — for box plots."""
    df = get_statements_df()
    if df.empty:
        return []

    from ..analytics.skills import get_skill_course_map, learner_skill_scores

    skill_map = get_skill_course_map()
    all_emails = df["actor_email"].unique()

    distributions: dict[str, list[float]] = {s: [] for s in skill_map}
    for email in all_emails:
        for entry in learner_skill_scores(df, email):
            if entry["score"] > 0:
                distributions[entry["skill"]].append(entry["score"])

    results = []
    for skill, scores in distributions.items():
        if not scores:
            continue
        sorted_scores = sorted(scores)
        n = len(sorted_scores)
        results.append({
            "skill": skill,
            "min": round(sorted_scores[0], 3),
            "q1": round(sorted_scores[n // 4], 3),
            "median": round(sorted_scores[n // 2], 3),
            "q3": round(sorted_scores[3 * n // 4], 3),
            "max": round(sorted_scores[-1], 3),
            "count": n,
        })

    return sorted(results, key=lambda x: x["median"])
