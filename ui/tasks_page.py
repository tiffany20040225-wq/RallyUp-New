"""three target about tennis"""

import customtkinter as ctk

from database import get_practices
from tasks import get_multiTasks


def build_tasks_page(parent):
    """
    display all three goals 
    """
    goals = get_multiTasks(get_practices())
    frame = ctk.CTkFrame(parent)
    ctk.CTkLabel(
        frame, text="Training Tasks", font=ctk.CTkFont(size=28, weight="bold")
    ).pack(pady=(12, 3))
    ctk.CTkLabel(frame, text="Small goals help build a steady tennis routine.").pack(
        pady=(0, 8)
    )

    for task in goals:
        card = ctk.CTkFrame(frame)
        card.pack(fill="x", padx=16, pady=4)
        ctk.CTkLabel(
            card, text=task["name"], font=ctk.CTkFont(size=19, weight="bold"),
            anchor="w",
        ).pack(fill="x", padx=14, pady=(6, 1))
        ctk.CTkLabel(card, text=task["description"], anchor="w").pack(
            fill="x", padx=14
        )
        status = "  •  Complete!" if task["progress"] >= task["target"] else ""
        ctk.CTkLabel(
            card, text=f"{task['progress']} / {task['target']} {task['unit']}{status}",
            anchor="w",
        ).pack(fill="x", padx=14, pady=(2, 3))
        progress = ctk.CTkProgressBar(card)
        progress.pack(fill="x", padx=14, pady=(0, 3))
        progress.set(min(task["progress"] / task["target"], 1))

    ctk.CTkLabel(
        frame, text="Daily tasks reset tomorrow. Weekly tasks start again on Monday."
    ).pack(pady=(5, 8))
    return frame
