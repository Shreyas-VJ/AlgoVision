"""Reusable Tkinter widgets used across the visualizers."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from utils.theme import COLORS, FONT


class SectionFrame(tk.Frame):
    """A titled panel with a body frame."""

    def __init__(self, parent, title: str) -> None:
        super().__init__(parent, bg=COLORS["panel"], highlightbackground=COLORS["grid"], highlightthickness=1)
        tk.Label(self, text=title, bg=COLORS["panel"], fg=COLORS["text"], font=(FONT, 13, "bold")).pack(anchor="w", padx=18, pady=(14, 4))
        self.body = tk.Frame(self, bg=COLORS["panel"])
        self.body.pack(fill="both", expand=True, padx=18, pady=(4, 16))


class DashboardCard(tk.Frame):
    """Clickable card used on the home dashboard."""

    def __init__(self, parent, title: str, subtitle: str, accent: str, command) -> None:
        super().__init__(parent, bg=COLORS["card"], highlightbackground=COLORS["grid"], highlightthickness=1, cursor="hand2")
        self.command = command
        self.accent = accent
        self.bind("<Button-1>", lambda _event: command())

        tk.Frame(self, bg=accent, height=4).pack(fill="x")
        tk.Label(self, text=title, bg=COLORS["card"], fg=COLORS["text"], font=(FONT, 18, "bold")).pack(anchor="w", padx=20, pady=(22, 8))
        tk.Label(
            self,
            text=subtitle,
            bg=COLORS["card"],
            fg=COLORS["muted"],
            font=(FONT, 11),
            wraplength=300,
            justify="left",
        ).pack(anchor="w", padx=20, pady=(0, 18))
        ttk.Button(self, text="Open Module", command=command).pack(anchor="w", padx=20, pady=(0, 24))
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _on_enter(self, _event) -> None:
        self.configure(highlightbackground=self.accent, highlightthickness=2)

    def _on_leave(self, _event) -> None:
        self.configure(highlightbackground=COLORS["grid"], highlightthickness=1)


class HoverButton(tk.Label):
    """A label-based button with simple hover styling."""

    def __init__(
        self,
        parent,
        text: str,
        command,
        bg: str = COLORS["panel"],
        hover_bg: str = COLORS["panel_2"],
        fg: str = COLORS["text"],
        accent: str = COLORS["cyan"],
        anchor: str = "w",
        font_size: int = 11,
    ) -> None:
        super().__init__(
            parent,
            text=text,
            bg=bg,
            fg=fg,
            anchor=anchor,
            padx=16,
            pady=10,
            cursor="hand2",
            font=(FONT, font_size, "bold"),
        )
        self.command = command
        self.normal_bg = bg
        self.hover_bg = hover_bg
        self.normal_fg = fg
        self.hover_fg = accent
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", lambda _event: self.command())

    def _on_enter(self, _event) -> None:
        self.configure(bg=self.hover_bg, fg=self.hover_fg)

    def _on_leave(self, _event) -> None:
        self.configure(bg=self.normal_bg, fg=self.normal_fg)


class ModernModuleCard(tk.Frame):
    """Large clickable dashboard card with hover effect."""

    def __init__(self, parent, title: str, subtitle: str, accent: str, command) -> None:
        super().__init__(
            parent,
            bg=COLORS["card"],
            highlightbackground=COLORS["grid"],
            highlightthickness=1,
            cursor="hand2",
        )
        self.command = command
        self.accent = accent
        self._bind_clicks(self)

        top_line = tk.Frame(self, bg=accent, height=3)
        top_line.pack(fill="x")
        content = tk.Frame(self, bg=COLORS["card"])
        content.pack(fill="both", expand=True, padx=22, pady=22)
        self._bind_clicks(content)

        badge = tk.Label(content, text="OPEN", bg=COLORS["panel_2"], fg=accent, font=(FONT, 9, "bold"), padx=10, pady=4)
        badge.pack(anchor="w")
        title_label = tk.Label(content, text=title, bg=COLORS["card"], fg=COLORS["text"], font=(FONT, 18, "bold"), anchor="w")
        title_label.pack(anchor="w", pady=(18, 8))
        subtitle_label = tk.Label(
            content,
            text=subtitle,
            bg=COLORS["card"],
            fg=COLORS["muted"],
            font=(FONT, 10),
            wraplength=280,
            justify="left",
        )
        subtitle_label.pack(anchor="w", fill="x")
        action = tk.Label(content, text="Launch module ->", bg=COLORS["card"], fg=accent, font=(FONT, 10, "bold"), cursor="hand2")
        action.pack(anchor="w", pady=(22, 0))

        for widget in (badge, title_label, subtitle_label, action):
            self._bind_clicks(widget)

        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        content.bind("<Enter>", self._on_enter)
        content.bind("<Leave>", self._on_leave)

    def _bind_clicks(self, widget) -> None:
        widget.bind("<Button-1>", lambda _event: self.command())

    def _on_enter(self, _event) -> None:
        self.configure(highlightbackground=self.accent, highlightthickness=2)

    def _on_leave(self, _event) -> None:
        self.configure(highlightbackground=COLORS["grid"], highlightthickness=1)


class StatGrid(tk.Frame):
    """Small labeled statistics grid."""

    def __init__(self, parent, labels: list[str]) -> None:
        super().__init__(parent, bg=COLORS["panel"])
        self.values: dict[str, tk.StringVar] = {}
        for index, label in enumerate(labels):
            tk.Label(self, text=label, bg=COLORS["panel"], fg=COLORS["muted"], font=(FONT, 9)).grid(row=0, column=index, sticky="w", padx=8)
            var = tk.StringVar(value="0")
            self.values[label] = var
            tk.Label(self, textvariable=var, bg=COLORS["panel"], fg=COLORS["text"], font=(FONT, 12, "bold")).grid(row=1, column=index, sticky="w", padx=8, pady=(2, 0))

    def set(self, label: str, value) -> None:
        """Update a single statistic."""

        self.values[label].set(str(value))


def make_labeled_scale(parent, text: str, from_: int, to: int, value: int) -> tuple[tk.Scale, tk.StringVar]:
    """Create a horizontal scale with a live value label."""

    wrap = tk.Frame(parent, bg=COLORS["panel"])
    var = tk.StringVar(value=str(value))
    tk.Label(wrap, text=text, bg=COLORS["panel"], fg=COLORS["muted"], font=(FONT, 10)).pack(anchor="w")
    scale = tk.Scale(
        wrap,
        from_=from_,
        to=to,
        orient="horizontal",
        bg=COLORS["panel"],
        fg=COLORS["text"],
        troughcolor=COLORS["grid"],
        highlightthickness=0,
        activebackground=COLORS["cyan"],
        sliderrelief="flat",
        command=lambda val: var.set(str(int(float(val)))),
    )
    scale.set(value)
    scale.pack(fill="x")
    tk.Label(wrap, textvariable=var, bg=COLORS["panel"], fg=COLORS["cyan"], font=(FONT, 9, "bold")).pack(anchor="e")
    return scale, var
