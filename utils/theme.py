"""Centralized dark neon theme for AlgoVision."""

from __future__ import annotations

from tkinter import ttk


COLORS = {
    "bg": "#08111f",
    "panel": "#101b2d",
    "panel_2": "#15243a",
    "card": "#122036",
    "cyan": "#19d3ff",
    "cyan_dark": "#0b7fa3",
    "green": "#39ff9f",
    "yellow": "#ffd166",
    "red": "#ff5c7c",
    "magenta": "#b56cff",
    "orange": "#ff9f1c",
    "text": "#edf6ff",
    "muted": "#9fb4c9",
    "grid": "#20334e",
    "white": "#ffffff",
}

FONT = "Segoe UI"


def configure_styles(root) -> None:
    """Apply a consistent dark theme to Tk and ttk widgets."""

    root.option_add("*Background", COLORS["bg"])
    root.option_add("*Foreground", COLORS["text"])
    root.option_add("*activeBackground", COLORS["panel_2"])
    root.option_add("*activeForeground", COLORS["cyan"])
    root.option_add("*insertBackground", COLORS["cyan"])
    root.option_add("*selectBackground", COLORS["cyan_dark"])
    root.option_add("*selectForeground", COLORS["white"])
    root.option_add("*Menu.background", COLORS["panel"])
    root.option_add("*Menu.foreground", COLORS["text"])
    root.option_add("*Menu.activeBackground", COLORS["cyan_dark"])
    root.option_add("*Menu.activeForeground", COLORS["white"])
    root.option_add("*Menu.borderWidth", 0)

    style = ttk.Style(root)
    style.theme_use("clam")

    style.configure("TFrame", background=COLORS["bg"])
    style.configure("Card.TFrame", background=COLORS["panel"])
    style.configure("TLabel", background=COLORS["bg"], foreground=COLORS["text"], font=(FONT, 10))

    style.configure(
        "TButton",
        background=COLORS["cyan_dark"],
        foreground=COLORS["white"],
        borderwidth=0,
        focusthickness=0,
        padding=(16, 9),
        font=(FONT, 10, "bold"),
    )
    style.map(
        "TButton",
        background=[("active", COLORS["cyan"]), ("pressed", COLORS["magenta"]), ("disabled", COLORS["grid"])],
        foreground=[("active", COLORS["bg"]), ("pressed", COLORS["white"]), ("disabled", COLORS["muted"])],
    )

    style.configure("Accent.TButton", background=COLORS["magenta"], foreground=COLORS["white"])
    style.map(
        "Accent.TButton",
        background=[("active", COLORS["cyan"]), ("pressed", COLORS["magenta"]), ("disabled", COLORS["grid"])],
        foreground=[("active", COLORS["bg"]), ("pressed", COLORS["white"]), ("disabled", COLORS["muted"])],
    )

    style.configure(
        "TCombobox",
        fieldbackground=COLORS["panel_2"],
        background=COLORS["panel_2"],
        foreground=COLORS["text"],
        arrowcolor=COLORS["cyan"],
        bordercolor=COLORS["grid"],
        lightcolor=COLORS["grid"],
        darkcolor=COLORS["grid"],
        padding=5,
    )
    style.map(
        "TCombobox",
        fieldbackground=[("readonly", COLORS["panel_2"])],
        selectbackground=[("readonly", COLORS["cyan_dark"])],
        selectforeground=[("readonly", COLORS["white"])],
        foreground=[("readonly", COLORS["text"])],
    )

    style.configure(
        "TEntry",
        fieldbackground=COLORS["panel_2"],
        foreground=COLORS["text"],
        insertcolor=COLORS["cyan"],
        bordercolor=COLORS["grid"],
        lightcolor=COLORS["grid"],
        darkcolor=COLORS["grid"],
        padding=6,
    )

    style.configure(
        "Horizontal.TScale",
        background=COLORS["panel"],
        troughcolor=COLORS["grid"],
        sliderthickness=16,
    )

    style.configure(
        "TProgressbar",
        background=COLORS["cyan"],
        troughcolor=COLORS["grid"],
        bordercolor=COLORS["panel"],
        lightcolor=COLORS["cyan"],
        darkcolor=COLORS["cyan"],
    )

    style.configure(
        "TRadiobutton",
        background=COLORS["bg"],
        foreground=COLORS["text"],
        font=(FONT, 10, "bold"),
        padding=(10, 6),
    )
    style.map(
        "TRadiobutton",
        background=[("active", COLORS["panel_2"])],
        foreground=[("active", COLORS["cyan"]), ("selected", COLORS["cyan"])],
    )

    style.configure(
        "Treeview",
        background=COLORS["panel_2"],
        fieldbackground=COLORS["panel_2"],
        foreground=COLORS["text"],
        bordercolor=COLORS["grid"],
        rowheight=26,
        font=(FONT, 9),
    )
    style.configure(
        "Treeview.Heading",
        background=COLORS["cyan_dark"],
        foreground=COLORS["white"],
        borderwidth=0,
        font=(FONT, 9, "bold"),
    )
    style.map("Treeview", background=[("selected", COLORS["cyan_dark"])], foreground=[("selected", COLORS["white"])])

    style.configure("TNotebook", background=COLORS["bg"], borderwidth=0)
    style.configure(
        "TNotebook.Tab",
        background=COLORS["panel"],
        foreground=COLORS["muted"],
        padding=(14, 8),
        font=(FONT, 10, "bold"),
    )
    style.map(
        "TNotebook.Tab",
        background=[("selected", COLORS["panel_2"]), ("active", COLORS["card"])],
        foreground=[("selected", COLORS["cyan"]), ("active", COLORS["text"])],
    )
