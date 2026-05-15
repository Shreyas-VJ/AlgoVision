"""Complexity Analysis and Performance Comparison page."""

from __future__ import annotations

import csv
import random
import time
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

try:
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure
except ImportError:
    Figure = None
    FigureCanvasTkAgg = None

from pathfinding.pathfinding_algorithms import ALGORITHM_DETAILS as PATH_DETAILS
from pathfinding.pathfinding_algorithms import PathfindingAlgorithms
from searching.searching_algorithms import ALGORITHM_DETAILS as SEARCH_DETAILS
from searching.searching_algorithms import SearchingAlgorithms
from sorting.sorting_algorithms import ALGORITHM_DETAILS as SORT_DETAILS
from sorting.sorting_algorithms import SortingAlgorithms
from utils.performance_store import get_results
from utils.theme import COLORS, FONT
from utils.widgets import SectionFrame


SORT_FUNCS = {
    "Bubble Sort": SortingAlgorithms.bubble_sort,
    "Selection Sort": SortingAlgorithms.selection_sort,
    "Insertion Sort": SortingAlgorithms.insertion_sort,
    "Merge Sort": SortingAlgorithms.merge_sort,
    "Quick Sort": SortingAlgorithms.quick_sort,
    "Heap Sort": SortingAlgorithms.heap_sort,
}

SEARCH_FUNCS = {
    "Linear Search": SearchingAlgorithms.linear_search,
    "Binary Search": SearchingAlgorithms.binary_search,
}

PATH_FUNCS = {
    "Dijkstra": PathfindingAlgorithms.dijkstra,
    "A*": PathfindingAlgorithms.astar,
}

COMPLEXITY_ROWS = [
    ("Bubble Sort", "O(n)", "O(n^2)", "O(n^2)", "O(1)"),
    ("Selection Sort", "O(n^2)", "O(n^2)", "O(n^2)", "O(1)"),
    ("Insertion Sort", "O(n)", "O(n^2)", "O(n^2)", "O(1)"),
    ("Merge Sort", "O(n log n)", "O(n log n)", "O(n log n)", "O(n)"),
    ("Quick Sort", "O(n log n)", "O(n log n)", "O(n^2)", "O(log n)"),
    ("Heap Sort", "O(n log n)", "O(n log n)", "O(n log n)", "O(1)"),
    ("Linear Search", "O(1)", "O(n)", "O(n)", "O(1)"),
    ("Binary Search", "O(1)", "O(log n)", "O(log n)", "O(1)"),
    ("Dijkstra", "O((V + E) log V)", "O((V + E) log V)", "O((V + E) log V)", "O(V)"),
    ("A*", "O(E) typical", "O(E) typical", "O((V + E) log V)", "O(V)"),
]


class ComplexityAnalysisPage(tk.Frame):
    """Dashboard page for charts, tables, exports, and educational comparisons."""

    def __init__(self, parent: tk.Widget) -> None:
        super().__init__(parent, bg=COLORS["bg"])
        self.figure = None
        self.figure_canvas = None
        self.current_chart = tk.StringVar(value="Sorting")
        self.data = self._build_demo_data()
        self._build_ui()
        self.refresh_data()

    def _build_ui(self) -> None:
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        header = tk.Frame(self, bg=COLORS["bg"])
        header.grid(row=0, column=0, sticky="ew", padx=26, pady=(20, 10))
        header.grid_columnconfigure(0, weight=1)
        tk.Label(header, text="Complexity Analysis", bg=COLORS["bg"], fg=COLORS["magenta"], font=(FONT, 26, "bold")).grid(row=0, column=0, sticky="w")
        tk.Label(
            header,
            text="Compare theoretical complexity with measured performance from AlgoVision visualizers.",
            bg=COLORS["bg"],
            fg=COLORS["muted"],
            font=(FONT, 11),
        ).grid(row=1, column=0, sticky="w", pady=(6, 0))

        actions = tk.Frame(header, bg=COLORS["bg"])
        actions.grid(row=0, column=1, rowspan=2, sticky="e")
        ttk.Button(actions, text="Refresh Results", command=self.refresh_data).pack(side="left", padx=4)
        ttk.Button(actions, text="Save Graph", command=self.save_graph).pack(side="left", padx=4)
        ttk.Button(actions, text="Export Report", command=self.export_report).pack(side="left", padx=4)

        body = tk.Frame(self, bg=COLORS["bg"])
        body.grid(row=1, column=0, sticky="nsew", padx=26, pady=(6, 22))
        body.grid_columnconfigure(0, weight=1)
        body.grid_columnconfigure(1, weight=0)
        body.grid_rowconfigure(0, weight=1)

        left = tk.Frame(body, bg=COLORS["bg"])
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        left.grid_rowconfigure(1, weight=1)
        left.grid_columnconfigure(0, weight=1)

        chart_tabs = tk.Frame(left, bg=COLORS["bg"])
        chart_tabs.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        for name in ["Sorting", "Searching", "Pathfinding", "Growth"]:
            ttk.Radiobutton(
                chart_tabs,
                text=name,
                variable=self.current_chart,
                value=name,
                command=self.draw_chart,
            ).pack(side="left", padx=(0, 8))

        chart_panel = SectionFrame(left, "Performance Charts")
        chart_panel.grid(row=1, column=0, sticky="nsew")
        chart_panel.body.grid_rowconfigure(0, weight=1)
        chart_panel.body.grid_columnconfigure(0, weight=1)
        self.chart_container = chart_panel.body

        right = tk.Frame(body, bg=COLORS["bg"], width=360)
        right.grid(row=0, column=1, sticky="ns")
        right.grid_propagate(False)

        self._build_table(right)
        self._build_explanations(right)

    def _build_table(self, parent: tk.Frame) -> None:
        table_panel = SectionFrame(parent, "Theoretical Complexity Table")
        table_panel.pack(fill="both", expand=True, pady=(0, 12))

        columns = ("Algorithm", "Best", "Average", "Worst", "Space")
        self.table = ttk.Treeview(table_panel.body, columns=columns, show="headings", height=10)
        for column in columns:
            self.table.heading(column, text=column)
            self.table.column(column, width=70 if column != "Algorithm" else 112, anchor="w")
        for row in COMPLEXITY_ROWS:
            self.table.insert("", "end", values=row)
        self.table.pack(fill="both", expand=True)

    def _build_explanations(self, parent: tk.Frame) -> None:
        explain = SectionFrame(parent, "Educational Notes")
        explain.pack(fill="both", expand=True)
        text = (
            "Execution time is measured in milliseconds. Comparisons and swaps come from the algorithm step builders.\n\n"
            "Sorting charts compare time, comparisons, and swaps. Searching charts compare time and comparisons. "
            "Pathfinding charts compare visited nodes, path length, and time.\n\n"
            "Dynamic mode: run any visualizer first, then press Refresh Results here. If no run data exists, "
            "AlgoVision displays small built-in benchmark samples for demonstration."
        )
        tk.Label(explain.body, text=text, bg=COLORS["panel"], fg=COLORS["muted"], font=(FONT, 9), justify="left", wraplength=300).pack(anchor="nw")

    def refresh_data(self) -> None:
        """Refresh measured data from visualizer runs, then redraw charts."""

        results = get_results()
        demo = self._build_demo_data()
        self.data = demo
        for category, algorithms in results.items():
            for algorithm, metrics in algorithms.items():
                if category in self.data:
                    self.data[category][algorithm] = dict(metrics)
        self.draw_chart()

    def draw_chart(self) -> None:
        """Draw the selected chart."""

        for child in self.chart_container.winfo_children():
            child.destroy()

        if Figure is None or FigureCanvasTkAgg is None:
            tk.Label(
                self.chart_container,
                text="Matplotlib is required for charts. Install it with: pip install matplotlib",
                bg=COLORS["panel"],
                fg=COLORS["muted"],
                font=(FONT, 11),
            ).grid(row=0, column=0, sticky="nsew")
            return

        self.figure = Figure(figsize=(8, 5), dpi=100, facecolor=COLORS["panel"])
        chart = self.current_chart.get()
        if chart == "Sorting":
            self._draw_sorting_chart()
        elif chart == "Searching":
            self._draw_searching_chart()
        elif chart == "Pathfinding":
            self._draw_pathfinding_chart()
        else:
            self._draw_growth_chart()

        self.figure.tight_layout()
        self.figure_canvas = FigureCanvasTkAgg(self.figure, master=self.chart_container)
        self.figure_canvas.draw()
        self.figure_canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

    def _draw_sorting_chart(self) -> None:
        axis1 = self.figure.add_subplot(131)
        axis2 = self.figure.add_subplot(132)
        axis3 = self.figure.add_subplot(133)
        names = list(SORT_FUNCS)
        short = ["Bubble", "Select", "Insert", "Merge", "Quick", "Heap"]
        sorting = self.data["sorting"]
        self._bar(axis1, short, [sorting[name]["time_ms"] for name in names], "Execution Time", COLORS["cyan"])
        self._bar(axis2, short, [sorting[name]["comparisons"] for name in names], "Comparisons", COLORS["yellow"])
        self._bar(axis3, short, [sorting[name]["swaps"] for name in names], "Swaps", COLORS["magenta"])

    def _draw_searching_chart(self) -> None:
        axis1 = self.figure.add_subplot(121)
        axis2 = self.figure.add_subplot(122)
        names = list(SEARCH_FUNCS)
        searching = self.data["searching"]
        self._bar(axis1, names, [searching[name]["time_ms"] for name in names], "Execution Time", COLORS["green"])
        self._bar(axis2, names, [searching[name]["comparisons"] for name in names], "Comparisons", COLORS["yellow"])

    def _draw_pathfinding_chart(self) -> None:
        axis1 = self.figure.add_subplot(131)
        axis2 = self.figure.add_subplot(132)
        axis3 = self.figure.add_subplot(133)
        names = list(PATH_FUNCS)
        path = self.data["pathfinding"]
        self._bar(axis1, names, [path[name]["visited"] for name in names], "Nodes Visited", COLORS["cyan"])
        self._bar(axis2, names, [path[name]["time_ms"] for name in names], "Execution Time", COLORS["green"])
        self._bar(axis3, names, [path[name]["path_length"] for name in names], "Path Length", COLORS["magenta"])

    def _draw_growth_chart(self) -> None:
        axis = self.figure.add_subplot(111)
        sizes = [10, 20, 40, 80, 160]
        axis.plot(sizes, sizes, color=COLORS["green"], marker="o", label="O(n)")
        axis.plot(sizes, [n.bit_length() for n in sizes], color=COLORS["cyan"], marker="o", label="O(log n)")
        axis.plot(sizes, [n * n for n in sizes], color=COLORS["red"], marker="o", label="O(n^2)")
        axis.plot(sizes, [n * n.bit_length() for n in sizes], color=COLORS["magenta"], marker="o", label="O(n log n)")
        self._style_axis(axis, "Complexity Growth Comparison")
        axis.legend(facecolor=COLORS["panel"], labelcolor=COLORS["text"])

    def _bar(self, axis, labels: list[str], values: list[float], title: str, color: str) -> None:
        axis.bar(labels, values, color=color)
        self._style_axis(axis, title)
        axis.tick_params(axis="x", rotation=35)

    def _style_axis(self, axis, title: str) -> None:
        axis.set_title(title, color=COLORS["text"], fontsize=10)
        axis.set_facecolor(COLORS["panel"])
        axis.tick_params(colors=COLORS["muted"], labelsize=8)
        axis.grid(True, color=COLORS["grid"], alpha=0.35)
        for spine in axis.spines.values():
            spine.set_color(COLORS["grid"])

    def save_graph(self) -> None:
        """Save the current graph as a PNG image."""

        if self.figure is None:
            messagebox.showwarning("No Graph", "No graph is available to save.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png")],
            initialfile=f"algovision_{self.current_chart.get().lower()}_chart.png",
        )
        if not path:
            return
        self.figure.savefig(path, facecolor=COLORS["panel"])
        messagebox.showinfo("Graph Saved", f"Graph saved to:\n{path}")

    def export_report(self) -> None:
        """Export measured analysis data and complexity rows as a CSV report."""

        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Report", "*.csv")],
            initialfile="algovision_analysis_report.csv",
        )
        if not path:
            return

        with Path(path).open("w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["AlgoVision Complexity Analysis Report"])
            writer.writerow([])
            writer.writerow(["Category", "Algorithm", "Metric", "Value"])
            for category, algorithms in self.data.items():
                for algorithm, metrics in algorithms.items():
                    for metric, value in metrics.items():
                        writer.writerow([category, algorithm, metric, value])
            writer.writerow([])
            writer.writerow(["Algorithm", "Best Case", "Average Case", "Worst Case", "Space Complexity"])
            writer.writerows(COMPLEXITY_ROWS)

        messagebox.showinfo("Report Exported", f"Report exported to:\n{path}")

    def _build_demo_data(self) -> dict[str, dict[str, dict[str, float | int]]]:
        """Generate small benchmark data so charts are useful before visualizer runs."""

        values = random.sample(range(1, 200), 32)
        sorted_values = sorted(values)
        sorting_data = {}
        for name, func in SORT_FUNCS.items():
            start = time.perf_counter()
            _steps, comparisons, swaps = func(values)
            sorting_data[name] = {
                "time_ms": (time.perf_counter() - start) * 1000,
                "comparisons": comparisons,
                "swaps": swaps,
            }

        target = sorted_values[-1]
        searching_data = {}
        for name, func in SEARCH_FUNCS.items():
            input_values = sorted_values if name == "Binary Search" else values
            start = time.perf_counter()
            _steps, _found, comparisons = func(input_values, target)
            searching_data[name] = {
                "time_ms": (time.perf_counter() - start) * 1000,
                "comparisons": comparisons,
            }

        walls = {(6, col) for col in range(4, 18)}
        pathfinding_data = {}
        for name, func in PATH_FUNCS.items():
            start = time.perf_counter()
            visited, path = func(20, 34, (5, 5), (14, 27), walls)
            pathfinding_data[name] = {
                "visited": len(visited),
                "time_ms": (time.perf_counter() - start) * 1000,
                "path_length": len(path),
            }

        return {
            "sorting": sorting_data,
            "searching": searching_data,
            "pathfinding": pathfinding_data,
        }
