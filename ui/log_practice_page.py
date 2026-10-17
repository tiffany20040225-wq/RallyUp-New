"""record practice"""

import customtkinter as ctk

from achievements import title_4Achievement
from database import get_practices, get_user, save_practice
from tasks import get_multiTasks


TRAINING_TYPES = [
    "Serve", "Forehand", "Backhand", "Footwork", "Volley", "Match Play", "Other"
]


def validate_practice(duration_text, training_type_text):
    """
    Return cleaned inputs or an error message before any database save,caculate the text,warning the wrong
    """
    duration_text = duration_text.strip()
    training_type = training_type_text.strip()
    if not duration_text:
        return None, None, "Please enter the practice duration."
    try:
        duration = int(duration_text)
    except ValueError:
        return None, None, "Duration must be a whole number of minutes."
    if duration <= 0:
        return None, None, "Duration must be greater than zero."
    if not training_type:
        return None, None, "Please choose or enter a training type."
    if len(training_type) > 50:
        return None, None, "Training type must be 50 characters or fewer."
    return duration, training_type, ""


def build_log_practice_page(parent, show_page):
    """
    build the practice form and connect its save and Home buttons,design the page frame
    """
    frame = ctk.CTkFrame(parent)
    ctk.CTkLabel(
        frame, text="Log Practice", font=ctk.CTkFont(size=28, weight="bold")
    ).pack(pady=(14, 4))
    ctk.CTkLabel(frame, text="One minute on court earns one XP.").pack(pady=(0, 12))

    form = ctk.CTkFrame(frame, fg_color="transparent")
    form.pack(fill="x", padx=24)
    ctk.CTkLabel(form, text="Duration (minutes)", anchor="w").pack(fill="x")
    duration_entry = ctk.CTkEntry(form, placeholder_text="e.g. 30")
    duration_entry.pack(fill="x", pady=(4, 10))
    ctk.CTkLabel(form, text="Training type", anchor="w").pack(fill="x")
    type_entry = ctk.CTkComboBox(form, values=TRAINING_TYPES)
    type_entry.set("Serve")
    type_entry.pack(fill="x", pady=(4, 10))
    ctk.CTkLabel(
        form, text="Choose a type or type your own.", anchor="w"
    ).pack(fill="x", pady=(0, 8))

    message = ctk.CTkTextbox(form, height=95, wrap="word")
    message.pack(fill="x", pady=(8, 4))
    message.configure(state="disabled")

    # show the message 
    def show_message(value):
        """
        replace the feedback text and make it read-only again
        """
        message.configure(state="normal")
        message.delete("1.0", "end")
        message.insert("1.0", value)
        message.configure(state="disabled")

    # save the input of user and show this to user
    def on_save():
        """
        save the input of user and show this to user
        """
        duration, training_type, error = validate_practice(
            duration_entry.get(), type_entry.get()
        )
        if error:
            show_message(error)
            return

        previous_level = get_user()["level"]
        # compare tasks before and after, so "complete" only appears once
        before_tasks = get_multiTasks(get_practices())
        earned_xp, level, unlocked = save_practice(duration, training_type)
        after_tasks = get_multiTasks(get_practices())

        result = f"Practice saved! +{earned_xp} XP. You are Level {level}."
        if level > previous_level:
            result += "\nLevel up! Your court time is adding up."
        for before, after in zip(before_tasks, after_tasks):
            if before["progress"] < before["target"] <= after["progress"]:
                result += f"\nTask complete: {after['name']}!"
        for name in unlocked:
            result += f"\nAchievement: {name} — title: {title_4Achievement(name)}!"

        show_message(result)
        duration_entry.delete(0, "end")
        home_button.pack(pady=(8, 0))

    ctk.CTkButton(form, text="Save Practice", height=42, command=on_save).pack()
    home_button = ctk.CTkButton(
        form, text="View Updated Home", command=lambda: show_page("home")
    )
    return frame
