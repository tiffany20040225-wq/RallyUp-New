"""home page, firstly show"""

import customtkinter as ctk

from achievements import calculate_streak, get_current_title
from database import get_practices, get_achievements_unlocked, get_user
from tasks import get_multiTasks
from xp_system import caculate_level


def build_home_page(parent, show_pages):
    """
    read the saved progress and build the level, title, streak and task
    """
    player = get_user()
    sessions = get_practices()
    achievements = get_achievements_unlocked()
    level, level_xp, needed_xp = caculate_level(player["total_xp"])
    streak = calculate_streak([session["date"] for session in sessions])
    tasks = get_multiTasks(sessions)

    # design the frame of home page
    frame = ctk.CTkFrame(parent)
    ctk.CTkLabel(
        frame, text="RallyUp — Tennis XP", font=ctk.CTkFont(size=29, weight="bold")
    ).pack(pady=(12, 2))
    ctk.CTkLabel(frame, text="Every minute on court moves you forward.").pack(
        pady=(0, 9)
    )
    ctk.CTkLabel(
        frame, text=f"Welcome, {player['name']}!", font=ctk.CTkFont(size=22, weight="bold")
    ).pack()
    ctk.CTkLabel(frame, text=f"Title: {get_current_title(achievements)}").pack(
        pady=(2, 8)
    )

    ctk.CTkLabel(frame, text=f"Level {level}", font=ctk.CTkFont(size=26)).pack()
    ctk.CTkLabel(frame, text=f"{player['total_xp']} total XP").pack(pady=(1, 4))
    progress = ctk.CTkProgressBar(frame, width=320)
    progress.pack()
    progress.set(level_xp / needed_xp)
    ctk.CTkLabel(frame, text=f"{level_xp} / {needed_xp} XP to next level").pack(
        pady=(3, 8)
    )

    if streak == 0:
        streak_text = "Your next practice can start a new streak."
    elif streak == 1:
        streak_text = "1-day practice streak — a great start!"
    else:
        streak_text = f"{streak}-day practice streak — keep your rhythm!"
    ctk.CTkLabel(frame, text=streak_text, font=ctk.CTkFont(size=16)).pack(
        pady=(0, 6)
    )

    for task in tasks[:2]:
        task_frame = ctk.CTkFrame(frame)
        task_frame.pack(fill="x", padx=20, pady=3)
        ctk.CTkLabel(
            task_frame,
            text=f"{task['name']}: {task['progress']} / {task['target']} {task['unit']}",
            anchor="w",
        ).pack(fill="x", padx=12, pady=(5, 3))
        task_progress = ctk.CTkProgressBar(task_frame)
        task_progress.pack(fill="x", padx=12, pady=(0, 6))
        task_progress.set(min(task["progress"] / task["target"], 1))

    ctk.CTkButton(
        frame, text="Log Practice", height=42, command=lambda: show_pages("log")
    ).pack(pady=(8, 4))
    ctk.CTkButton(
        frame, text="See All Tasks", fg_color="transparent", border_width=1,
        command=lambda: show_pages("tasks"),
    ).pack(pady=(0, 8))
    return frame
