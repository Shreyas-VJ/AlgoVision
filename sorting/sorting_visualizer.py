"""Tkinter page for animated sorting algorithm visualization."""

from __future__ import annotations

import random
import time
import tkinter as tk
from tkinter import ttk

from sorting.sorting_algorithms import ALGORITHM_DETAILS, SortingAlgorithms
from utils.performance_store import record_result
from utils.theme import COLORS, FONT
from utils.widgets import SectionFrame, StatGrid, make_labeled_scale


class SortingVisualizer(tk.Frame):
    """Professional sorting visualizer page for AlgoVision."""

    def __init__(self, parent: tk.Widget) -> None:
        super().__init__(parent, bg=COLORS["bg"])
        self.values: list[int] = []
        self.steps: list[dict[str, object]] = []
        self.step_index = 0
        self.running = False
        self.after_id: str | None = None
        self.final_comparisons = 0
        self.final_swaps = 0
        self.final_time_ms = 0.0

        self.algorithms = {
            "Bubble Sort": SortingAlgorithms.bubble_sort,
            "Selection Sort": SortingAlgorithms.selection_sort,
            "Insertion Sort": SortingAlgorithms.insertion_sort,
            "Merge Sort": SortingAlgorithms.merge_sort,
            "Quick Sort": SortingAlgorithms.quick_sort,
            "Heap Sort": SortingAlgorithms.heap_sort,
        }

        self._build_ui()
        self.generate_array()

    def _build_ui(self) -> None:
        """Build the complete visualizer layout."""

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        header = tk.Frame(self, bg=COLORS["bg"])
        header.grid(row=0, column=0, sticky="ew", padx=26, pady=(20, 10))
        header.grid_columnconfigure(0, weight=1)

        tk.Label(
            header,
            text="Sorting Visualizer",
            bg=COLORS["bg"],
            fg=COLORS["cyan"],
            font=(FONT, 26, "bold"),
        ).grid(row=0, column=0, sticky="w")
        tk.Label(
            header,
            text="Animate comparisons, swaps, and sorted elements for six classic DAA sorting algorithms.",
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
        self.algorithm_var = tk.StringVar(value="Bubble Sort")
        dropdown = ttk.Combobox(
            controls.body,
            textvariable=self.algorithm_var,
            values=list(self.algorithms.keys()),
            state="readonly",
            width=22,
        )
        dropdown.pack(fill="x", pady=(5, 12))
        dropdown.bind("<<ComboboxSelected>>", lambda _event: self.update_algorithm_info())

        self.size_scale, _ = make_labeled_scale(controls.body, "Array Size", 8, 90, 36)
        self.size_scale.master.pack(fill="x", pady=8)
        self.speed_scale, _ = make_labeled_scale(controls.body, "Sorting Speed", 1, 100, 48)
        self.speed_scale.master.pack(fill="x", pady=8)

        button_area = tk.Frame(controls.body, bg=COLORS["panel"])
        button_area.pack(fill="x", pady=(14, 8))
        ttk.Button(button_area, text="Random Array", command=self.generate_array).pack(fill="x", pady=5)
        ttk.Button(button_area, text="Start", command=self.start_sorting).pack(fill="x", pady=5)
        ttk.Button(button_area, text="Stop", command=self.stop_sorting).pack(fill="x", pady=5)
        ttk.Button(button_area, text="Reset", command=self.reset_visualizer).pack(fill="x", pady=5)

        legend = tk.Frame(controls.body, bg=COLORS["panel"])
        legend.pack(fill="x", pady=(14, 0))
        for label, color in [
            ("Comparison", COLORS["yellow"]),
            ("Swap / Write", COLORS["red"]),
            ("Sorted", COLORS["green"]),
            ("Default", COLORS["cyan"]),
        ]:
            row = tk.Frame(legend, bg=COLORS["panel"])
            row.pack(fill="x", pady=3)
            tk.Label(row, bg=color, width=3).pack(side="left")
            tk.Label(row, text=label, bg=COLORS["panel"], fg=COLORS["text"], font=(FONT, 9)).pack(side="left", padx=8)

    def _build_canvas(self, parent: tk.Frame) -> None:
        visual = SectionFrame(parent, "Animated Bars")
        visual.grid(row=0, column=1, sticky="nsew", padx=12)
        visual.body.grid_rowconfigure(0, weight=1)
        visual.body.grid_columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(visual.body, bg=COLORS["panel_2"], highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.canvas.bind("<Configure>", lambda _event: self.draw_bars())

        self.status_var = tk.StringVar(value="Generate an array, choose an algorithm, and press Start.")
        tk.Label(
            visual.body,
            textvariable=self.status_var,
            bg=COLORS["panel"],
            fg=COLORS["text"],
            font=(FONT, 10),
        ).grid(row=1, column=0, sticky="ew", pady=(10, 0))

    def _build_info_panel(self, parent: tk.Frame) -> None:
        side = tk.Frame(parent, bg=COLORS["bg"], width=280)
        side.grid(row=0, column=2, sticky="ns", padx=(12, 0))
        side.grid_propagate(False)

        stats_panel = SectionFrame(side, "Live Metrics")
        stats_panel.pack(fill="x", pady=(0, 12))
        self.stats = StatGrid(stats_panel.body, ["Comparisons", "Swaps", "Time"])
        self.stats.pack(fill="x")

        complexity_panel = SectionFrame(side, "Complexity")
        complexity_panel.pack(fill="x", pady=(0, 12))
        self.complexity_var = tk.StringVar()
        tk.Label(
            complexity_panel.body,
            textvariable=self.complexity_var,
            bg=COLORS["panel"],
            fg=COLORS["text"],
            font=(FONT, 11, "bold"),
            justify="left",
        ).pack(anchor="w")

        explanation_panel = SectionFrame(side, "Algorithm Explanation")
        explanation_panel.pack(fill="both", expand=True)
        self.explanation_var = tk.StringVar()
        tk.Label(
            explanation_panel.body,
            textvariable=self.explanation_var,
            bg=COLORS["panel"],
            fg=COLORS["muted"],
            font=(FONT, 10),
            justify="left",
            wraplength=230,
        ).pack(anchor="nw", fill="both")

        self.update_algorithm_info()

    def generate_array(self) -> None:
        """Create a fresh random array."""

        self.stop_sorting()
        size = int(self.size_scale.get())
        self.values = [random.randint(8, 100) for _ in range(size)]
        self.steps = []
        self.step_index = 0
        self.final_comparisons = 0
        self.final_swaps = 0
        self.final_time_ms = 0.0
        self.stats.set("Comparisons", 0)
        self.stats.set("Swaps", 0)
        self.stats.set("Time", "0 ms")
        self.status_var.set("Random array generated.")
        self.draw_bars()

    def reset_visualizer(self) -> None:
        """Reset the visualizer to a new unsorted state."""

        self.generate_array()

    def start_sorting(self) -> None:
        """Prepare sorting steps and start non-blocking animation."""

        if self.running:
            return

        algorithm_name = self.algorithm_var.get()
        algorithm = self.algorithms[algorithm_name]
        start_time = time.perf_counter()
        self.steps, self.final_comparisons, self.final_swaps = algorithm(self.values)
        self.final_time_ms = (time.perf_counter() - start_time) * 1000
        self.step_index = 0
        self.running = True
        self.status_var.set(f"Animating {algorithm_name}...")
        self._animate_next_step()

    def stop_sorting(self) -> None:
        """Pause animation without closing the app."""

        self.running = False
        if self.after_id is not None:
            self.after_cancel(self.after_id)
            self.after_id = None
        self.status_var.set("Animation stopped.")

    def _animate_next_step(self) -> None:
        """Draw one animation step and schedule the next one."""

        if not self.running:
            return

        if self.step_index >= len(self.steps):
            self.running = False
            self.after_id = None
            self.stats.set("Comparisons", self.final_comparisons)
            self.stats.set("Swaps", self.final_swaps)
            self.stats.set("Time", f"{self.final_time_ms:.2f} ms")
            record_result(
                "sorting",
                self.algorithm_var.get(),
                {
                    "time_ms": self.final_time_ms,
                    "comparisons": self.final_comparisons,
                    "swaps": self.final_swaps,
                },
            )
            self.status_var.set("Sorting complete.")
            return

        step = self.steps[self.step_index]
        self.values = list(step["array"])
        self.draw_bars(
            active_indices=list(step["active"]),
            sorted_indices=list(step["sorted"]),
            action=str(step["action"]),
        )

        self.step_index += 1
        self._update_live_metrics()
        delay = max(4, 105 - int(self.speed_scale.get()))
        self.after_id = self.after(delay, self._animate_next_step)

    def _update_live_metrics(self) -> None:
        """Show approximate progress metrics during animation."""

        if not self.steps:
            return
        progress = self.step_index / len(self.steps)
        self.stats.set("Comparisons", int(self.final_comparisons * progress))
        self.stats.set("Swaps", int(self.final_swaps * progress))
        self.stats.set("Time", f"{self.final_time_ms * progress:.2f} ms")

    def draw_bars(
        self,
        active_indices: list[int] | None = None,
        sorted_indices: list[int] | None = None,
        action: str = "",
    ) -> None:
        """Draw bars with color-coded comparison, swap, and sorted states."""

        active_indices = active_indices or []
        sorted_indices = sorted_indices or []
        self.canvas.delete("all")

        if not self.values:
            return

        width = max(self.canvas.winfo_width(), 620)
        height = max(self.canvas.winfo_height(), 360)
        padding = 22
        available_width = width - padding * 2
        available_height = height - padding * 2 - 18
        bar_width = available_width / len(self.values)
        max_value = max(self.values)

        for index, value in enumerate(self.values):
            x1 = padding + index * bar_width + 2
            x2 = padding + (index + 1) * bar_width - 2
            y2 = height - padding
            y1 = y2 - (value / max_value) * available_height

            color = COLORS["cyan"]
            if index in sorted_indices:
                color = COLORS["green"]
            if index in active_indices and action == "compare":
                color = COLORS["yellow"]
            if index in active_indices and action in {"swap", "write"}:
                color = COLORS["red"]
            if action == "done":
                color = COLORS["green"]

            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")
            if bar_width > 24:
                self.canvas.create_text(
                    (x1 + x2) / 2,
                    y1 - 8,
                    text=str(value),
                    fill=COLORS["muted"],
                    font=(FONT, 7),
                )

        self.canvas.create_text(
            padding,
            14,
            anchor="w",
            text="Yellow = comparison   Red = swap/write   Green = sorted",
            fill=COLORS["muted"],
            font=(FONT, 9),
        )

    def update_algorithm_info(self) -> None:
        """Refresh explanation and complexity labels."""

        details = ALGORITHM_DETAILS[self.algorithm_var.get()]
        self.complexity_var.set(
            f"Time Complexity\n{details['time']}\n\nSpace Complexity\n{details['space']}"
        )
        self.explanation_var.set(str(details["explanation"]))
