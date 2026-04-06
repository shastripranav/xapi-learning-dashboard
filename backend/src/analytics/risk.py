"""At-risk learner identification.

Flags learners based on three signals:
  1. Inactive: no activity in 14+ days
  2. Declining: score trending down over last 3 scored attempts
  3. Disengaged: engagement score below 30
"""

from datetime import datetime, timezone

import pandas as pd

from .engagement import calculate_engagement_scores

INACTIVE_THRESHOLD_DAYS = 14
ENGAGEMENT_THRESHOLD = 30.0


def identify_at_risk(df: pd.DataFrame) -> list[dict]:
    now = datetime.now(timezone.utc)
    engagement_scores = {
        e["email"]: e["total_score"]
        for e in calculate_engagement_scores(df)
    }

    at_risk = []

    for email, group in df.groupby("actor_email"):
        name = group["actor_name"].iloc[0]
        last_ts = group["timestamp"].max()
        days_since = (now - last_ts).days

        reasons = []

        if days_since >= INACTIVE_THRESHOLD_DAYS:
            reasons.append(f"Inactive for {days_since} days")

        scored = group[group["score"].notna()].sort_values("timestamp")
        if len(scored) >= 3:
            last_3 = scored.tail(3)["score"].tolist()
            if last_3[0] > last_3[1] > last_3[2]:
                reasons.append("Score declining over last 3 attempts")

        eng_score = engagement_scores.get(email, 0)
        if eng_score < ENGAGEMENT_THRESHOLD:
            reasons.append(f"Engagement score {eng_score:.0f} (below {ENGAGEMENT_THRESHOLD:.0f})")

        if reasons:
            trend = "declining" if any("declining" in r.lower() for r in reasons) else "stable"
            at_risk.append({
                "email": email,
                "name": name,
                "days_since_active": days_since,
                "score_trend": trend,
                "engagement_score": eng_score,
                "risk_reasons": reasons,
            })

    at_risk.sort(key=lambda x: len(x["risk_reasons"]), reverse=True)
    return at_risk
