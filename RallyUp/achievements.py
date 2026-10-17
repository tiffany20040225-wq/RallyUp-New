"""functions about achievements and traning days"""

from datetime import date, datetime, timedelta


# achievement list
ACHIEVEMENTS = [
    {"name": "First Practice", "goal": "Log your first practice", "title": "Court Rookie"},
    {"name": "5 Practices", "goal": "Log 5 practices", "title": "Rally Regular"},
    {"name": "120 Minutes", "goal": "Practice for 120 minutes", "title": "Dedicated Player"},
    {"name": "3 Training Types", "goal": "Try 3 training types", "title": "All-Rounder"},
    {"name": "3-Day Streak", "goal": "Practice on 3 days in a row", "title": "Habit Hitter"},
    {"name": "500 XP", "goal": "Earn 500 XP", "title": "XP Ace"},
    {"name": "7-Day Streak", "goal": "Practice on 7 days in a row", "title": "Court Champion"},
]


def calculate_streak(saved_dates, today=None):
    """
    count consecutive practice dates, starting from today or yesterday, if uese practice twice one day, it will calculate one
    """
    if today is None:
        today = date.today()
    practice_days = set()
    for saved_date in saved_dates:
        practice_days.add(datetime.strptime(saved_date[:10], "%Y-%m-%d").date())

    day = today
    if day not in practice_days:
        day = today - timedelta(days=1)
    streak = 0
    while day in practice_days:
        streak += 1
        day -= timedelta(days=1)
    return streak


def get_current_title(unlocked):
    """
    Use the last unlocked title in the achievement list
    """
    title = "New Player"
    for achievement in ACHIEVEMENTS:
        if achievement["name"] in unlocked:
            title = achievement["title"]
    return title


def title_4Achievement(name):
    """
    get the achievement title
    """
    for achievement in ACHIEVEMENTS:
        if achievement["name"] == name:
            return achievement["title"]
    return ""


def check_achievements(connection, user_id, unlocked_date):
    """
    1.Check totals and streaks, then return only newly inserted
    achievements
    2.Reuse save_practice's connection so these writes stay in its
    transaction
    3.There is no separate connect() or commit() here; errors go back to
    save_practice
    """
    totals = connection.execute(
        "SELECT COUNT(*), COALESCE(SUM(duration), 0), COUNT(DISTINCT LOWER(training_type)) "
        "FROM practices WHERE user_id = ?",
        (user_id,),
    ).fetchone()
    practice_count, total_minutes, type_count = totals
    # get the total_xp
    total_xp = connection.execute(
        "SELECT total_xp FROM users WHERE id = ?", (user_id,)
    ).fetchone()[0]
    # get the dates, not the number of sessions, for the streak
    dates = connection.execute(
        "SELECT date FROM practices WHERE user_id = ?", (user_id,)
    ).fetchall()
    streak = calculate_streak([row[0] for row in dates])

    earned = []
    # caculate the achievements which have be got
    if practice_count >= 1:
        earned.append("First Practice")
    if practice_count >= 5:
        earned.append("5 Practices")
    if total_minutes >= 120:
        earned.append("120 Minutes")
    if type_count >= 3:
        earned.append("3 Training Types")
    if streak >= 3:
        earned.append("3-Day Streak")
    if total_xp >= 500:
        earned.append("500 XP")
    if streak >= 7:
        earned.append("7-Day Streak")

    new_achievements = []
    for name in earned:
        # already unlocked? INSERT OR IGNORE leaves it as it is
        cursor = connection.execute(
            "INSERT OR IGNORE INTO achievements "
            "(user_id, achievement_name, unlocked_date) VALUES (?, ?, ?)",
            (user_id, name, unlocked_date),
        )
        if cursor.rowcount == 1:
            new_achievements.append(name)
    return new_achievements
