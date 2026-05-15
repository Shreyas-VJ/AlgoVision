"""Tkinter page for animated searching algorithm visualization."""

from __future__ import annotations

import random
import time
import tkinter as tk
from tkinter import messagebox, ttk

from searching.searching_algorithms import ALGORITHM_DETAILS, SearchingAlgorithms
from utils.performance_store import record_result
from utils.theme import COLORS, FONT
from utils.widgets import SectionFrame, StatGrid, make_labeled_scale


class SearchingVisualizer(tk.Frame):
    """Professional searching visualizer page for AlgoVision."""

    def __init__(self, parent: tk.Widget) -> None:
        super().__init__(parent, bg=COLORS["bg"])
        self.values: list[int] = []
        self.steps: list[dict[str, object]] = []
        self.step_index = 0
        self.running = False
        self.after_id: str | None = None
        self.found_index = -1
        self.final_comparisons = 0
        self.final_time_ms = 0.0

        self.algorithms = {
            "Linear Search": SearchingAlgorithms.linear_search,
            "Binary Search": SearchingAlgorithms.binary_search,
        }

        self._build_ui()
        self.generate_array()

    def _build_ui(self) -> None:
        """Build the searching visualizer screen."""

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        header = tk.Frame(self, bg=COLORS["bg"])
        header.grid(row=0, column=0, sticky="ew", padx=26, pady=(20, 10))
        header.grid_columnconfigure(0, weight=1)
        tk.Label(
            header,
            text="Searching Visualizer",
            bg=COLORS["bg"],
            fg=COLORS["green"],
            font=(FONT, 26, "bold"),
        ).grid(row=0, column=0, sticky="w")
        tk.Label(
            header,
            text="Visualize target lookup with checked elements, found states, and binary-search elimination.",
            bg=COLORS["bg"],
            fg=COLORS["muted"],
            font=(FONT, 11),
        ).grid(row=1, column=0, sticky="w", pady=(6, 0))

        main = tk.Frame(self, bg=COLORS["bg"])
        main.grid(row=1, column=0, sticky="nsew", padx=26, pady=(6, 22))
        main.grid_columnconfigure(0, weight=0)
        main.grid_columnconfigure(1, weight=1)
        main.grid_columnconfigure(2, weight=0)
        main.grid_rowconfigure(0, weight=1)

        self._build_controls(main)
        self._build_canvas(main)
        self._build_info_panel(main)

    def _build_controls(self, parent: tk.Frame) -> None:
        controls = SectionFrame(parent, "Controls")
        controls.grid(row=0, column=0, sticky="ns", padx=(0, 12))

        tk.Label(controls.body, text="Algorithm", bg=COLORS["panel"], fg=COLORS["muted"], font=(FONT, 10)).pack(anchor="w")
        self.algorithm_var = tk.StringVar(value="Linear Search")
        dropdown = ttk.Combobox(
            controls.body,
            textvariable=self.algorithm_var,
            values=list(self.algorithms.keys()),
            state="readonly",
            width=22,
        )
        dropdown.pack(fill="x", pady=(5, 12))
        dropdown.bind("<<ComboboxSelected>>", self._on_algorithm_changed)

        self.size_scale, _ = make_labeled_scale(controls.body, "Array Size", 8, 80, 32)
        self.size_scale.master.pack(fill="x", pady=8)
        self.speed_scale, _ = make_labeled_scale(controls.body, "Search Speed", 1, 100, 52)
        self.speed_scale.master.pack(fill="x", pady=8)

        tk.Label(controls.body, text="Target Value", bg=COLORS["panel"], fg=COLORS["muted"], font=(FONT, 10)).pack(anchor="w", pady=(12, 4))
        self.target_var = tk.StringVar()
        tk.Entry(
            controls.body,
            textvariable=self.target_var,
            bg=COLORS["panel_2"],
            fg=COLORS["text"],
            insertbackground=COLORS["cyan"],
            relief="flat",
            font=(FONT, 11),
        ).pack(fill="x", ipady=7)

        button_area = tk.Frame(controls.body, bg=COLORS["panel"])
        button_area.pack(fill="x", pady=(14, 8))
        ttk.Button(button_area, text="Random Array", command=self.generate_array).pack(fill="x", pady=5)
        ttk.Button(button_area, text="Sorted Array", command=self.generate_sorted_array).pack(fill="x", pady=5)
        ttk.Button(button_area, text="Start Search", command=self.start_search).pack(fill="x", pady=5)
        ttk.Button(button_area, text="Stop", command=self.stop_search).pack(fill="x", pady=5)
        ttk.Button(button_area, text="Reset", command=self.reset_visualizer).pack(fill="x", pady=5)

        legend = tk.Frame(controls.body, bg=COLORS["panel"])
        legend.pack(fill="x", pady=(14, 0))
        for label, color in [
            ("Active range", COLORS["cyan_dark"]),
            ("Current check", COLORS["yellow"]),
            ("Eliminated", COLORS["magenta"]),
            ("Found", COLORS["green"]),
        ]:
            row = tk.Frame(legend, bg=COLORS["panel"])
            row.pack(fill="x", pady=3)
            tk.Label(row, bg=color, width=3).pack(side="left")
            tk.Label(row, text=label, bg=COLORS["panel"], fg=COLORS["text"], font=(FONT, 9)).pack(side="left", padx=8)

    def _build_canvas(self, parent: tk.Frame) -> None:
        visual = SectionFrame(parent, "Animated Array")
        visual.grid(row=0, column=1, sticky="nsew", padx=12)
        visual.body.grid_rowconfigure(0, weight=1)
        visual.body.grid_columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(visual.body, bg=COLORS["panel_2"], highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.canvas.bind("<Configure>", lambda _event: self.draw_array())

        self.status_var = tk.StringVar(value="Generate an array, enter a target, and start searching.")
        tk.Label(
            visual.body,
            textvariable=self.status_var,
            bg=COLORS["panel"],
            fg=COLORS["text"],
            font=(FONT, 10),
        ).grid(row=1, column=0, sticky="ew", pady=(10, 0))

    def _build_info_panel(self, parent: tk.Frame) -> None:
        side = tk.Frame(parent, bg=COLORS["bg"], width=300)
        side.grid(row=0, column=2, sticky="ns", padx=(12, 0))
        side.grid_propagate(False)

        metrics = SectionFrame(side, "Live Metrics")
        metrics.pack(fill="x", pady=(0, 12))
        self.stats = StatGrid(metrics.body, ["Comparisons", "Result", "Time"])
        self.stats.pack(fill="x")

        complexity = SectionFrame(side, "Complexity")
        complexity.pack(fill="x", pady=(0, 12))
        self.complexity_var = tk.StringVar()
        tk.Label(
            complexity.body,
            textvariable=self.complexity_var,
            bg=COLORS["panel"],
            fg=COLORS["text"],
            font=(FONT, 10, "bold"),
            justify="left",
            wraplength=250,
        ).pack(anchor="w")

        explanation = SectionFrame(side, "Algorithm Explanation")
        explanation.pack(fill="both", expand=True)
        self.explanation_var = tk.StringVar()
        tk.Label(
            explanation.body,
            textvariable=self.explanation_var,
            bg=COLORS["panel"],
            fg=COLORS["muted"],
            font=(FONT, 10),
            justify="left",
            wraplength=250,
        ).pack(anchor="nw", fill="both")

        self.update_algorithm_info()

    def _on_algorithm_changed(self, _event=None) -> None:
        """Refresh array style and text when algorithm changes."""

        self.stop_search()
        if self.algorithm_var.get() == "Binary Search":
            self.generate_sorted_array()
        else:
            self.generate_array()
        self.update_algorithm_info()

    def generate_array(self) -> None:
        """Generate a random array for Linear Search."""

        self.stop_search()
        size = int(self.size_scale.get())
        self.values = random.sample(range(1, 200), size)
        self.target_var.set(str(random.choice(self.values)))
        self._reset_state("Random array generated.")

    def generate_sorted_array(self) -> None:
        """Generate a sorted array, required for Binary Search."""

        self.stop_search()
        size = int(self.size_scale.get())
        self.values = sorted(random.sample(range(1, 200), size))
        self.target_var.set(str(random.choice(self.values)))
        self._reset_state("Sorted array generated for binary search.")

    def reset_visualizer(self) -> None:
        """Reset using the best array type for the selected algorithm."""

        if self.algorithm_var.get() == "Binary Search":
            self.generate_sorted_array()
        else:
            self.generate_array()

    def _reset_state(self, message: str) -> None:
        self.steps = []
        self.step_index = 0
        self.found_index = -1
        self.final_comparisons = 0
        self.final_time_ms = 0.0
        self.stats.set("Comparisons", 0)
        self.stats.set("Result", "-")
        self.stats.set("Time", "0 ms")
        self.status_var.set(message)
        self.draw_array()

    def start_search(self) -> None:
        """Build search steps and animate them with after()."""

        if self.running:
            return
        try:
            target = int(self.target_var.get())
        except ValueError:
            messagebox.showerror("Invalid Target", "Please enter a numeric target value.")
            return

        if self.algorithm_var.get() == "Binary Search" and self.values != sorted(self.values):
            self.values.sort()
            self.status_var.set("Array sorted automatically for Binary Search.")
            self.draw_array()

        start_time = time.perf_counter()
        self.steps, self.found_index, self.final_comparisons = self.algorithms[self.algorithm_var.get()](self.values, target)
        self.final_time_ms = (time.perf_counter() - start_time) * 1000
        self.step_index = 0
        self.running = True
        self._animate_next_step()

    def stop_search(self) -> None:
        """Pause animation without freezing or closing the UI."""

        self.running = False
        if self.after_id is not None:
            self.after_cancel(self.after_id)
            self.after_id = None

    def _animate_next_step(self) -> None:
        """Draw one step and schedule the next one."""

        if not self.running:
            return

        if self.step_index >= len(self.steps):
            self.running = False
            self.after_id = None
            self.stats.set("Comparisons", self.final_comparisons)
            self.stats.set("Result", "Found" if self.found_index != -1 else "Not found")
            self.stats.set("Time", f"{self.final_time_ms:.2f} ms")
            record_result(
                "searching",
                self.algorithm_var.get(),
                {
                    "time_ms": self.final_time_ms,
                    "comparisons": self.final_comparisons,
                    "result": "Found" if self.found_index != -1 else "Not found",
                },
            )
            return

        step = self.steps[self.step_index]
        self.status_var.set(str(step["message"]))
        self.draw_array(
            active_indices=list(step["active"]),
            eliminated_indices=list(step["eliminated"]),
            found_indices=list(step["found"]),
            action=str(step["action"]),
        )

        self.step_index += 1
        progress = self.step_index / max(1, len(self.steps))
        self.stats.set("Comparisons", int(self.final_comparisons * progress))
        self.stats.set("Result", "Searching")
        self.stats.set("Time", f"{self.final_time_ms * progress:.2f} ms")

        delay = max(10, 135 - int(self.speed_scale.get()))
        self.after_id = self.after(delay, self._animate_next_step)

    def draw_array(
        self,
        active_indices: list[int] | None = None,
        eliminated_indices: list[int] | None = None,
        found_indices: list[int] | None = None,
        action: str = "",
    ) -> None:
        """Draw array values as responsive animated boxes."""

        active_indices = active_indices or []
        eliminated_indices = eliminated_indices or []
        found_indices = found_indices or []
        self.canvas.delete("all")

        if not self.values:
            return

        width = max(self.canvas.winfo_width(), 620)
        height = max(self.canvas.winfo_height(), 360)
        padding = 24
        columns = min(len(self.values), max(1, int((width - padding * 2) // 54)))
        box_width = (width - padding * 2) / columns
        box_height = 48
        gap_y = 14

        for index, value in enumerate(self.values):
            row = index // columns
            col = index % columns
            x1 = padding + col * box_width + 4
            y1 = 54 + row * (box_height + gap_y)
            x2 = padding + (col + 1) * box_width - 4
            y2 = y1 + box_height

            color = COLORS["grid"]
            text_color = COLORS["text"]
            if index in active_indices and action == "range":
                color = COLORS["cyan_dark"]
                text_color = COLORS["white"]
            if index in eliminated_indices:
                color = COLORS["magenta"]
                text_color = COLORS["white"]
            if index in active_indices and action == "check":
                color = COLORS["yellow"]
                text_color = COLORS["text"]
            if index in found_indices or (index in active_indices and action == "found"):
                color = COLORS["green"]
                text_color = COLORS["white"]

            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=COLORS["panel"])
            self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=str(value), fill=text_color, font=(FONT, 9, "bold"))
            if box_width > 46:
                self.canvas.create_text((x1 + x2) / 2, y2 + 10, text=str(index), fill=COLORS["muted"], font=(FONT, 7))

        self.canvas.create_text(
            padding,
            18,
            anchor="w",
            text="Cyan = active range   Yellow = current check   Purple = eliminated   Green = found",
            fill=COLORS["muted"],
            font=(FONT, 9),
        )

    def update_algorithm_info(self) -> None:
        """Refresh complexity and explanation panels."""

        details = ALGORITHM_DETAILS[self.algorithm_var.get()]
        self.complexity_var.set(
            f"Time Complexity: {details['time']}\n"
            f"Space Complexity: {details['space']}\n\n"
            f"Best Case: {details['best']}\n"
            f"Average Case: {details['average']}\n"
            f"Worst Case: {details['worst']}"
        )
        self.explanation_var.set(str(details["explanation"]))
