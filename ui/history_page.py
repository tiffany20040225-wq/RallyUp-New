"""history page"""

import customtkinter as ctk

from database import get_practices


def build_history_page(parent):
    """
    design the history page frame
    """
    practices = get_practices()
    frame = ctk.CTkFrame(parent)
    ctk.CTkLabel(
        frame, text="Practice History", font=ctk.CTkFont(size=28, weight="bold")
    ).pack(pady=(14, 4))
    ctk.CTkLabel(frame, text=f"{len(practices)} practices recorded").pack(
        pady=(0, 8)
    )

    if not practices:
        ctk.CTkLabel(
            frame, text="No practices yet. Log your first time on court!"
        ).pack(pady=30)
        return frame

    per = 4
    start_at = 0
    list_frame = ctk.CTkFrame(frame, fg_color="transparent")
    list_frame.pack(fill="both", expand=True, padx=16)
    navigation = ctk.CTkFrame(frame, fg_color="transparent")
    navigation.pack(pady=(3, 10))
    previous_button = ctk.CTkButton(navigation, text="Previous", width=100)
    previous_button.pack(side="left", padx=5)
    page_label = ctk.CTkLabel(navigation, text="", width=92)
    page_label.pack(side="left", padx=5)
    next_button = ctk.CTkButton(navigation, text="Next", width=100)
    next_button.pack(side="left", padx=5)

    # design the function to hanle conveniently
    def show_records():
        """
        Replace visible rows and refresh the page number 
        """
        for child in list_frame.winfo_children():
            child.destroy()
        for practice in practices[start_at:start_at + per]:
            row = ctk.CTkFrame(list_frame)
            row.pack(fill="x", pady=3)
            ctk.CTkLabel(
                row, text=practice["training_type"],
                font=ctk.CTkFont(size=16, weight="bold"), anchor="w",
            ).pack(fill="x", padx=12, pady=(5, 1))
            details = (
                f"{practice['date']}   •   {practice['duration']} minutes"
                f"   •   +{practice['xp_earned']} XP"
            )
            ctk.CTkLabel(row, text=details, anchor="w").pack(
                fill="x", padx=12, pady=(0, 5)
            )
        pages = (len(practices) + per - 1) // per
        page_label.configure(text=f"{start_at // per + 1} / {pages}")
        previous_button.configure(state="normal" if start_at > 0 else "disabled")
        next_button.configure(
            state="normal" if start_at + per < len(practices) else "disabled"
        )

    def move(step):
        """
        move the starting record 
        """
        nonlocal start_at
        start_at += step * per
        show_records()

    previous_button.configure(command=lambda: move(-1))
    next_button.configure(command=lambda: move(1))
    show_records()
    return frame
