"""Dashboard chart data"""

import pandas as pd

from achievements import calculate_streak


def summarize_practices(practices, today=None):
    # caculate the number and the chart
    """
    Summarise the totals, the last seven days and the types
    """
    if today is None:
        today = pd.Timestamp.today().normalize()
    else:
        today = pd.Timestamp(today).normalize()

    days = pd.date_range(end=today, periods=7)
    summary = {
        "practice_count": 0,
        "total_minutes": 0,
        "last_7_minutes": 0,
        "average_minutes": 0,
        "streak_days": 0,
        "day_labels": [day.strftime("%a\n%m/%d") for day in days],
        "day_minutes": [0] * 7,
        "training_types": [],
        "type_minutes": [],
    }
    if not practices:
        return summary

    # get the summary and agg
    records = pd.DataFrame(practices)
    records["date"] = pd.to_datetime(records["date"], format="%Y-%m-%d %H:%M")
    summary["practice_count"] = len(records)
    summary["total_minutes"] = int(records["duration"].sum())
    summary["average_minutes"] = round(records["duration"].mean(), 1)
    summary["streak_days"] = calculate_streak(
        records["date"].dt.strftime("%Y-%m-%d").tolist(), today.date()
    )
    # fill empty dates with 0; otherwise the seven-day graph skips them
    daily = records.groupby(records["date"].dt.normalize())["duration"].sum()
    daily = daily.reindex(days, fill_value=0)
    summary["day_minutes"] = [int(value) for value in daily.tolist()]
    summary["last_7_minutes"] = int(daily.sum())

    by_type = records.groupby("training_type")["duration"].sum()
    by_type = by_type.sort_values(ascending=False).head(5)
    summary["training_types"] = by_type.index.tolist()
    summary["type_minutes"] = [int(value) for value in by_type.tolist()]
    return summary
