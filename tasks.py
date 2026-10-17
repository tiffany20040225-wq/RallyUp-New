"""daily and weekly goals"""

from datetime import date, timedelta


def get_multiTasks(practices, today=None):
    """
    Count today's and this week's practice separately for the three fixed goals
    """
    if today is None:
        today = date.today()
    monday = today - timedelta(days=today.weekday())

    minutes_today = 0
    minutes_this_week = 0
    types_this_week = set()
    for practice in practices:
        practice_day = date.fromisoformat(practice["date"][:10])
        if practice_day == today:
            minutes_today =minutes_today+ practice["duration"]
        if monday <= practice_day <= today:
            minutes_this_week =minutes_this_week+ practice["duration"]
            types_this_week.add(practice["training_type"].casefold())
    
    # the three task showing
    return [
        {
            "name": "Daily Warm-Up",
            "description": "Practice for 30 minutes today",
            "progress": minutes_today,
            "target": 30,
            "unit": "min",
        },
        {
            "name": "Weekly Rally",
            "description": "Practice for 120 minutes this week",
            "progress": minutes_this_week,
            "target": 120,
            "unit": "min",
        },
        {
            "name": "Skill Mix",
            "description": "Try 3 training types this week",
            "progress": len(types_this_week),
            "target": 3,
            "unit": "types",
        },
    ]
