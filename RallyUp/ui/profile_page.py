"""player information page"""
import customtkinter as ctk

from achievements import get_current_title
from database import get_practices, get_achievements_unlocked, get_user, update_uname


def build_profile_page(parent):
    # design the profile page 
    """
    display the saved profile and a form for changing the player name
    """
    user = get_user()
    practices = get_practices()
    title = get_current_title(get_achievements_unlocked())

    frame = ctk.CTkFrame(parent)
    ctk.CTkLabel(
        frame, text="Player Profile", font=ctk.CTkFont(size=28, weight="bold")
    ).pack(pady=(16, 16))
    ctk.CTkLabel(frame, text=f"Title: {title}", font=ctk.CTkFont(size=18)).pack(
        pady=(0, 12)
    )
    ctk.CTkLabel(frame, text=f"Level {user['level']}  •  {user['total_xp']} XP").pack()
    ctk.CTkLabel(frame, text=f"{len(practices)} practices recorded").pack(
        pady=(5, 28)
    )

    form = ctk.CTkFrame(frame, fg_color="transparent")
    form.pack(fill="x", padx=40)
    ctk.CTkLabel(form, text="Player name", anchor="w").pack(fill="x")
    name_entry = ctk.CTkEntry(form)
    name_entry.insert(0, user["name"])
    name_entry.pack(fill="x", pady=(4, 16))
    message = ctk.CTkLabel(form, text="")
    message.pack(pady=(7, 0))

    def save_name():
        # shorten the name, too long can not show
        name = name_entry.get().strip()
        if not name:
            message.configure(text="Please enter a player name.", text_color="#c23a3a")
            return
        if len(name) > 30:
            message.configure(text="Use 30 characters or fewer.", text_color="#c23a3a")
            return
        update_uname(name)
        message.configure(text="Profile saved!", text_color="#23875b")

    ctk.CTkButton(form, text="Save Name", height=40, command=save_name).pack()
    return frame
