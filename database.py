"""RallyUp sql saved locally"""

import sqlite3
from datetime import datetime
from pathlib import Path

from achievements import check_achievements
from xp_system import calculate_level, calculate_xp


DATABASE_PATH = Path(__file__).resolve().parent / "data" / "rallyup.db"
DEFAULT_USER_ID = 1


def connect():
    """
    the function about opening the SQLite 
    """
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_db():
    """
    initialize the data of database
    """
    connection = connect()
    try:
        with connection:
            connection.execute(
                "CREATE TABLE IF NOT EXISTS users ("
                "id INTEGER PRIMARY KEY, name TEXT NOT NULL, "
                "total_xp INTEGER NOT NULL DEFAULT 0, level INTEGER NOT NULL DEFAULT 1)"
            )
            connection.execute(
                "CREATE TABLE IF NOT EXISTS practices ("
                "id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL, date TEXT NOT NULL, "
                "duration INTEGER NOT NULL, training_type TEXT NOT NULL, "
                "xp_earned INTEGER NOT NULL, "
                "FOREIGN KEY (user_id) REFERENCES users(id))"
            )
            connection.execute(
                "CREATE TABLE IF NOT EXISTS achievements ("
                "id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL, "
                "achievement_name TEXT NOT NULL, unlocked_date TEXT NOT NULL, "
                "UNIQUE (user_id, achievement_name), "
                "FOREIGN KEY (user_id) REFERENCES users(id))"
            )
            connection.execute(
                "INSERT OR IGNORE INTO users (id, name, total_xp, level) "
                "VALUES (?, ?, 0, 1)",
                (DEFAULT_USER_ID, "Player"),
            )
    finally:
        connection.close()


def get_user():
    """
    read name, XP and level, show to dict
    """
    connection = connect()
    try:
        row = connection.execute(
            "SELECT id, name, total_xp, level FROM users WHERE id = ?",
            (DEFAULT_USER_ID,),
        ).fetchone()
        return dict(row)
    finally:
        connection.close()


def update_uname(name):
    """
    update player's name
    """
    connection = connect()
    try:
        with connection:
            connection.execute(
                "UPDATE users SET name = ? WHERE id = ?", (name, DEFAULT_USER_ID)
            )
    finally:
        connection.close()


def save_practice(duration, training_type):
    """
    save one practice and return its XP, new level and newly unlocked achievements
    """
    earned_xp = calculate_xp(duration)
    saved_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    connection = connect()
    try:
        # commit on success. If an exception leaves this block
        # roll back its pending writes.
        with connection:
            user = connection.execute(
                "SELECT total_xp FROM users WHERE id = ?", (DEFAULT_USER_ID,)
            ).fetchone()
            total_xp = user["total_xp"] + earned_xp
            level = calculate_level(total_xp)
            # With our default SQLite settings, this first INSERT
            # starts the transaction.
            connection.execute(
                "INSERT INTO practices "
                "(user_id, date, duration, training_type, xp_earned) "
                "VALUES (?, ?, ?, ?, ?)",
                (DEFAULT_USER_ID, saved_date, duration, training_type, earned_xp),
            )
            # Use the practice record's connection for the XP update
            # keeping both writes in the same transaction
            connection.execute(
                "UPDATE users SET total_xp = ?, level = ? WHERE id = ?",
                (total_xp, level, DEFAULT_USER_ID),
            )
            # pass this connection to the achievement INSERTs too
            # do not commit them 
            new_achievements = check_achievements(
                connection, DEFAULT_USER_ID, saved_date
            )
        # The with block has committed all pending writes
        # before this saved result is returned.
        return earned_xp, level, new_achievements
    finally:
        # Close the connection 
        connection.close()


def get_practices():
    # get practices
    """
    return the practices
    """
    connection = connect()
    try:
        rows = connection.execute(
            "SELECT date, duration, training_type, xp_earned "
            "FROM practices WHERE user_id = ? ORDER BY id DESC",
            (DEFAULT_USER_ID,),
        ).fetchall()
        results = []
        for r in rows:
            results.append(dict(r))
        return results
    finally:
        connection.close()


def get_achievements_unlocked():
    """
    get the unlocked achievement name which was earned
    """
    connection = connect()
    try:
        rows = connection.execute(
            "SELECT achievement_name, unlocked_date FROM achievements "
            "WHERE user_id = ?",
            (DEFAULT_USER_ID,),
        ).fetchall()
        results = {}
        for r in rows:
            results[r["achievement_name"]] = r["unlocked_date"]
        return results
    finally:
        connection.close()
