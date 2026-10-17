"""RallyUp entrance and menu"""

import customtkinter as ctk

from database import init_db
from ui.achievements_page import build_achievements_page
from ui.history_page import build_history_page
from ui.home_page import build_home_page
from ui.log_practice_page import build_log_practice_page
from ui.profile_page import build_profile_page
from ui.tasks_page import build_tasks_page


ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class RallyUpApp(ctk.CTk):
    def __init__(self):
        """
        Create the window and sidebar, then open Home.
        """
        super().__init__()
        self.title("RallyUp — Tennis XP")
        self.geometry("1000x700")
        self.minsize(760, 560)

        sidebar = ctk.CTkFrame(self, width=180)
        sidebar.pack(side="left", fill="y", padx=(16, 8), pady=16)
        sidebar.pack_propagate(False)
        ctk.CTkLabel(
            sidebar, text="RallyUp", font=ctk.CTkFont(size=25, weight="bold")
        ).pack(pady=(22, 2))
        ctk.CTkLabel(sidebar, text="Tennis XP").pack(pady=(0, 22))

        pages = [
            ("Home", "home"),
            ("Log Practice", "log"),
            ("Tasks", "tasks"),
            ("History", "history"),
            ("Achievements", "achievements"),
            ("Dashboard", "dashboard"),
            ("Profile", "profile"),
        ]
        for label, p_name in pages:
            ctk.CTkButton(
                sidebar,
                text=label,
                command=lambda name=p_name: self.show_multiPages(name),
            ).pack(fill="x", padx=14, pady=5)

        self.content = ctk.CTkFrame(self, fg_color="transparent")
        self.content.pack(side="left", fill="both", expand=True, padx=(8, 16), pady=16)
        self.current_page = None
        self.current_stage = None
        self.current_page_name = None
        self.show_multiPages("home")

    def show_multiPages(self, p_name):
        """
        Build the requested page and remove old pages
        """
        if p_name == self.current_page_name:
            return
        # add the new page, because the old page could flash
        stage = ctk.CTkFrame(self.content, fg_color="transparent", corner_radius=0)

        try:
            if p_name == "home":
                page = build_home_page(stage, self.show_multiPages)
            elif p_name == "log":
                page = build_log_practice_page(stage, self.show_multiPages)
            elif p_name == "tasks":
                page = build_tasks_page(stage)
            elif p_name == "history":
                page = build_history_page(stage)
            elif p_name == "achievements":
                page = build_achievements_page(stage)
            elif p_name == "dashboard":
                from ui.dashboard_page import build_dashboard_page

                page = build_dashboard_page(stage)
            elif p_name == "profile":
                page = build_profile_page(stage)
            else:
                raise ValueError(f"Unknown page: {p_name}")
            page.pack(fill="both", expand=True)
        except Exception:
            stage.destroy()
            raise

        old_stage = self.current_stage
        stage.place(relx=0, rely=0, relwidth=1, relheight=1)
        stage.lift()
        self.current_stage = stage
        self.current_page = page
        self.current_page_name = p_name
        if old_stage is not None:
            old_stage.destroy()


if __name__ == "__main__":
    init_db()
    app = RallyUpApp()
    app.mainloop()
