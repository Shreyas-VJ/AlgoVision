"""Centralized colors, fonts, and ttk styling."""

from __future__ import annotations

from tkinter import ttk

COLORS = {
    "bg": "#f6f8fb",
    "panel": "#ffffff",
    "panel_2": "#eef4f8",
    "card": "#ffffff",
    "cyan": "#3b82f6",
    "cyan_dark": "#2563eb",
    "green": "#2fa67a",
    "yellow": "#f2c94c",
    "red": "#eb5757",
    "magenta": "#9b6ad6",
    "orange": "#f2994a",
    "text": "#223044",
    "muted": "#6b778c",
    "grid": "#d8e2ec",
    "wall": "#334155",
    "white": "#ffffff",
}

FONT = "Segoe UI"


def configure_styles(root) -> None:
    """Apply a clean light theme to ttk widgets."""

    style = ttk.Style(root)
    style.theme_use("clam")
    root.option_add("*TCombobox*Listbox.background", COLORS["white"])
    root.option_add("*TCombobox*Listbox.foreground", COLORS["text"])
    root.option_add("*TCombobox*Listbox.selectBackground", COLORS["cyan"])
    root.option_add("*TCombobox*Listbox.selectForeground", COLORS["white"])
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
        background=[("active", COLORS["cyan"]), ("disabled", COLORS["grid"])],
        foreground=[("active", COLORS["white"]), ("disabled", COLORS["muted"])],
    )
    style.configure(
        "Accent.TButton",
        background=COLORS["magenta"],
        foreground=COLORS["white"],
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
        background=COLORS["panel"],
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
        background=COLORS["white"],
        fieldbackground=COLORS["white"],
        foreground=COLORS["text"],
        bordercolor=COLORS["grid"],
        rowheight=26,
        font=(FONT, 9),
    )
    style.configure(
        "Treeview.Heading",
        background=COLORS["cyan_dark"],
        foreground=COLORS["white"],
        font=(FONT, 9, "bold"),
    )
    style.map("Treeview", background=[("selected", COLORS["cyan_dark"])])
