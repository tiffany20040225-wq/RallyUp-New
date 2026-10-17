"""achievements page"""

import customtkinter as ctk

from achievements import ACHIEVEMENTS, get_current_title
from database import get_achievements_unlocked


def build_achievements_page(parent):
    """
    show unlocked and locked achievements
    """
    unlocked = get_achievements_unlocked()
    frame = ctk.CTkFrame(parent)
    ctk.CTkLabel(
        frame, text="Achievements", font=ctk.CTkFont(size=28, weight="bold")
    ).pack(pady=(14, 4))
    ctk.CTkLabel(frame, text=f"{len(unlocked)} of {len(ACHIEVEMENTS)} unlocked").pack()
    ctk.CTkLabel(frame, text=f"Current title: {get_current_title(unlocked)}").pack(
        pady=(2, 8)
    )

    page_size = 3
    page_index = 0
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
    def show_achievements():
        """
        show achievements and update the navigation buttons
        """
        for child in list_frame.winfo_children():
            child.destroy()
        for achievement in ACHIEVEMENTS[page_index * page_size:(page_index + 1) * page_size]:
            row = ctk.CTkFrame(list_frame)
            row.pack(fill="x", pady=3)
            details = ctk.CTkFrame(row, fg_color="transparent")
            details.pack(side="left", fill="x", expand=True, padx=12, pady=6)
            ctk.CTkLabel(
                details, text=achievement["name"],
                font=ctk.CTkFont(size=16, weight="bold"), anchor="w",
            ).pack(fill="x")
            ctk.CTkLabel(details, text=achievement["goal"], anchor="w").pack(fill="x")
            ctk.CTkLabel(
                details, text=f"Title: {achievement['title']}", anchor="w"
            ).pack(fill="x")
            name = achievement["name"]
            status = f"Unlocked  {unlocked[name]}" if name in unlocked else "Locked"
            ctk.CTkLabel(row, text=status).pack(side="right", padx=12, pady=8)
        pages = (len(ACHIEVEMENTS) + page_size - 1) // page_size
        page_label.configure(text=f"{page_index + 1} / {pages}")
        previous_button.configure(state="normal" if page_index else "disabled")
        next_button.configure(state="normal" if page_index < pages - 1 else "disabled")

    # dump the pages
    def change_page(step):
        nonlocal page_index
        page_index += step
        show_achievements()

    previous_button.configure(command=lambda: change_page(-1))
    next_button.configure(command=lambda: change_page(1))
    show_achievements()
    return frame
