"""use Pandas Matplotlib, chart show"""

import customtkinter as ctk
from matplotlib import rcParams
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from database import get_practices
from practice_stats import summarize_practices


# the training type 
rcParams["font.sans-serif"] = ["PingFang SC", "Microsoft YaHei", "Noto Sans CJK SC", "DejaVu Sans"]


# summary designed
def add_summary_card(parent, label, value):
    """
    Add one label and value card to the dashboard.
    """
    card = ctk.CTkFrame(parent)
    card.pack(side="left", fill="x", expand=True, padx=4)
    ctk.CTkLabel(card, text=str(value), font=ctk.CTkFont(size=23, weight="bold")).pack(
        pady=(7, 2)
    )
    ctk.CTkLabel(card, text=label).pack(pady=(0, 7))

# summary chart show
def add_chart(parent, figure):
    canvas = FigureCanvasTkAgg(figure, master=parent)
    canvas.draw()
    return canvas.get_tk_widget()


def build_dashboard_page(parent):
    """
    design the dashboard page , and recaculate the data if come back
    """
    stats = summarize_practices(get_practices())
    frame = ctk.CTkFrame(parent)
    ctk.CTkLabel(
        frame, text="Practice Dashboard", font=ctk.CTkFont(size=28, weight="bold")
    ).pack(pady=(12, 3))
    ctk.CTkLabel(frame, text="See your tennis practice add up.").pack(pady=(0, 8))

    if stats["practice_count"] == 0:
        ctk.CTkLabel(
            frame, text="No practice data yet. Log a practice to see your charts."
        ).pack(pady=35)
        return frame

    cards = ctk.CTkFrame(frame, fg_color="transparent")
    cards.pack(fill="x", padx=10, pady=(0, 6))
    add_summary_card(cards, "Practices", stats["practice_count"])
    add_summary_card(cards, "Total minutes", stats["total_minutes"])
    add_summary_card(cards, "Last 7 days", stats["last_7_minutes"])
    add_summary_card(cards, "Average minutes", stats["average_minutes"])

    day_word = "day" if stats["streak_days"] == 1 else "days"
    ctk.CTkLabel(
        frame, text=f"Current practice streak: {stats['streak_days']} {day_word}",
        font=ctk.CTkFont(size=16, weight="bold"),
    ).pack(pady=(0, 4))

    chart_frame = ctk.CTkFrame(frame)
    chart_frame.pack(fill="both", expand=True, padx=10, pady=(0, 8))
    chart_content = ctk.CTkFrame(chart_frame, fg_color="transparent")
    chart_content.pack(fill="both", expand=True, padx=4, pady=4)

    dark = ctk.get_appearance_mode() == "Dark"
    background = "#26303b" if dark else "#ffffff"
    text_color = "#f0f3f7" if dark else "#26303b"
    grid_color = "#53606e" if dark else "#dce3ea"

    # chart distribution
    daily_figure = Figure(figsize=(4.4, 2.4), dpi=100, facecolor=background)
    daily_axis = daily_figure.add_subplot(111)
    daily_axis.set_facecolor(background)
    # the bar chart
    daily_axis.bar(stats["day_labels"], stats["day_minutes"], color="#4b9cd3")

    daily_axis.set_title("Practice minutes by day (last 7 days)", color=text_color)
    daily_axis.set_ylabel("Minutes", color=text_color)
    daily_axis.tick_params(colors=text_color, labelsize=9)
    daily_axis.spines[["top", "right"]].set_visible(False)
    daily_axis.spines[["left", "bottom"]].set_color(grid_color)
    daily_axis.grid(axis="y", color=grid_color, alpha=0.5)

    daily_axis.set_axisbelow(True)
    daily_figure.tight_layout()
    daily_chart = add_chart(chart_content, daily_figure)

    type_figure = Figure(figsize=(4.4, 2.4), dpi=100, facecolor=background)
    type_axis = type_figure.add_subplot(111)
    names = list(reversed(stats["training_types"]))
    minutes = list(reversed(stats["type_minutes"]))
    type_axis.set_facecolor(background)
    type_axis.barh(names, minutes, color="#62b596")
    type_axis.set_title("Minutes by training type (top 5)", color=text_color)
    type_axis.set_xlabel("Minutes", color=text_color)
    type_axis.tick_params(colors=text_color, labelsize=9)
    type_axis.spines[["top", "right"]].set_visible(False)
    type_axis.spines[["left", "bottom"]].set_color(grid_color)
    type_axis.grid(axis="x", color=grid_color, alpha=0.5)
    type_axis.set_axisbelow(True)
    type_figure.tight_layout()
    type_chart = add_chart(chart_content, type_figure)

    def show_chart(selection):
        """
        switch the visible chart so the page still fits in the window
        """
        daily_chart.pack_forget()
        type_chart.pack_forget()
        chart = daily_chart if selection == "Last 7 days" else type_chart
        chart.pack(fill="both", expand=True)

    selector = ctk.CTkSegmentedButton(
        frame, values=["Last 7 days", "Training types"], command=show_chart
    )
    selector.pack(pady=(0, 8))
    selector.set("Last 7 days")
    show_chart("Last 7 days")
    return frame
