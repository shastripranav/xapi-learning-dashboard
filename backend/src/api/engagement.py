from fastapi import APIRouter

from ..analytics.aggregator import get_statements_df
from ..analytics.engagement import calculate_engagement_scores
from ..analytics.risk import identify_at_risk
from ..analytics.time_analysis import (
    peak_activity_hours,
    time_of_day_heatmap,
    time_on_task_by_course,
)

router = APIRouter(prefix="/api/engagement", tags=["engagement"])


@router.get("/scores")
def get_engagement_scores():
    df = get_statements_df()
    if df.empty:
        return []
    return calculate_engagement_scores(df)


@router.get("/at-risk")
def get_at_risk():
    df = get_statements_df()
    if df.empty:
        return []
    return identify_at_risk(df)


@router.get("/time-of-day")
def get_time_of_day():
    df = get_statements_df()
    if df.empty:
        return []
    return time_of_day_heatmap(df)


@router.get("/time-on-task")
def get_time_on_task():
    df = get_statements_df()
    if df.empty:
        return []
    return time_on_task_by_course(df)


@router.get("/peak-hours")
def get_peak_hours():
    df = get_statements_df()
    if df.empty:
        return []
    return peak_activity_hours(df)
