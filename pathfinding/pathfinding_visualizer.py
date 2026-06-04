"""Tkinter page for interactive pathfinding visualization."""

from __future__ import annotations

import time
import tkinter as tk
from tkinter import ttk

from pathfinding.pathfinding_algorithms import ALGORITHM_DETAILS, COMPARISON_TEXT, PathfindingAlgorithms
from utils.performance_store import record_result
from utils.theme import COLORS, FONT
from utils.widgets import SectionFrame, StatGrid, make_labeled_scale


Node = tuple[int, int]


class PathfindingVisualizer(tk.Frame):
    """Professional grid visualizer for Dijkstra and A* Search."""

    def __init__(self, parent: tk.Widget) -> None:
        super().__init__(parent, bg=COLORS["bg"])
        self.rows = 20
        self.cols = 34
        self.start_node: Node = (5, 5)
        self.end_node: Node = (14, 27)
        self.walls: set[Node] = set()
        self.visited_order: list[Node] = []
        self.path: list[Node] = []
        self.visited_index = 0
        self.path_index = 0
        self.running = False
        self.after_id: str | None = None
        self.elapsed_ms = 0.0

        self.algorithms = {
            "Dijkstra Algorithm": PathfindingAlgorithms.dijkstra,
            "A* Search Algorithm": PathfindingAlgorithms.astar,
        }
        self.mode_var = tk.StringVar(value="Wall")
        self.algorithm_var = tk.StringVar(value="Dijkstra Algorithm")

        self._build_ui()
        self.after(100, self.draw_grid)

    def _build_ui(self) -> None:
        """Build the full pathfinding page."""

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        header = tk.Frame(self, bg=COLORS["bg"])
        header.grid(row=0, column=0, sticky="ew", padx=26, pady=(20, 10))
        header.grid_columnconfigure(0, weight=1)
        tk.Label(
            header,
            text="Pathfinding Visualizer",
            bg=COLORS["bg"],
            fg=COLORS["magenta"],
            font=(FONT, 26, "bold"),
        ).grid(row=0, column=0, sticky="w")
        tk.Label(
            header,
            text="Draw walls, choose start/end nodes, and watch shortest-path algorithms explore the grid.",
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
        self._build_grid_canvas(main)
        self._build_info_panel(main)

    def _build_controls(self, parent: tk.Frame) -> None:
        controls = SectionFrame(parent, "Controls")
        controls.grid(row=0, column=0, sticky="ns", padx=(0, 12))

        tk.Label(controls.body, text="Algorithm", bg=COLORS["panel"], fg=COLORS["muted"], font=(FONT, 10)).pack(anchor="w")
        dropdown = ttk.Combobox(
            controls.body,
            textvariable=self.algorithm_var,
            values=list(self.algorithms.keys()),
            state="readonly",
            width=24,
        )
        dropdown.pack(fill="x", pady=(5, 12))
        dropdown.bind("<<ComboboxSelected>>", lambda _event: self.update_algorithm_info())

        tk.Label(controls.body, text="Edit Mode", bg=COLORS["panel"], fg=COLORS["muted"], font=(FONT, 10)).pack(anchor="w", pady=(4, 6))
        for option in ["Wall", "Erase", "Start", "End"]:
            tk.Radiobutton(
                controls.body,
                text=option,
                variable=self.mode_var,
                value=option,
                bg=COLORS["panel"],
                fg=COLORS["text"],
                selectcolor=COLORS["panel_2"],
                activebackground=COLORS["panel"],
                activeforeground=COLORS["cyan"],
                font=(FONT, 10),
            ).pack(anchor="w", pady=1)

        self.speed_scale, _ = make_labeled_scale(controls.body, "Animation Speed", 1, 100, 58)
        self.speed_scale.master.pack(fill="x", pady=(14, 10))

        button_area = tk.Frame(controls.body, bg=COLORS["panel"])
        button_area.pack(fill="x", pady=(10, 8))
        ttk.Button(button_area, text="Start Visualization", command=self.start_visualization).pack(fill="x", pady=5)
        ttk.Button(button_area, text="Stop", command=self.stop_visualization).pack(fill="x", pady=5)
        ttk.Button(button_area, text="Clear Grid", command=self.clear_grid).pack(fill="x", pady=5)
        ttk.Button(button_area, text="Reset", command=self.reset_grid).pack(fill="x", pady=5)

        hint = tk.Label(
            controls.body,
            text="Tip: choose Wall mode and drag on the grid to create obstacles.",
            bg=COLORS["panel"],
            fg=COLORS["muted"],
            font=(FONT, 9),
            wraplength=220,
            justify="left",
        )
        hint.pack(anchor="w", pady=(12, 0))

    def _build_grid_canvas(self, parent: tk.Frame) -> None:
        visual = SectionFrame(parent, "Interactive Grid")
        visual.grid(row=0, column=1, sticky="nsew", padx=12)
        visual.body.grid_rowconfigure(0, weight=1)
        visual.body.grid_columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(visual.body, bg=COLORS["panel_2"], highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.canvas.bind("<Configure>", lambda _event: self.draw_grid())
        self.canvas.bind("<Button-1>", self.handle_grid_click)
        self.canvas.bind("<B1-Motion>", self.handle_grid_click)

        self.status_var = tk.StringVar(value="Select a mode, edit the grid, then start visualization.")
        tk.Label(
            visual.body,
            textvariable=self.status_var,
            bg=COLORS["panel"],
            fg=COLORS["text"],
            font=(FONT, 10),
        ).grid(row=1, column=0, sticky="ew", pady=(10, 0))

    def _build_info_panel(self, parent: tk.Frame) -> None:
        side = tk.Frame(parent, bg=COLORS["bg"], width=310)
        side.grid(row=0, column=2, sticky="ns", padx=(12, 0))
        side.grid_propagate(False)

        metrics = SectionFrame(side, "Live Metrics")
        metrics.pack(fill="x", pady=(0, 12))
        self.stats = StatGrid(metrics.body, ["Visited", "Path", "Time"])
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
            wraplength=260,
        ).pack(anchor="w")

        explanation = SectionFrame(side, "Explanation")
        explanation.pack(fill="both", expand=True, pady=(0, 12))
        self.explanation_var = tk.StringVar()
        tk.Label(
            explanation.body,
            textvariable=self.explanation_var,
            bg=COLORS["panel"],
            fg=COLORS["muted"],
            font=(FONT, 9),
            justify="left",
            wraplength=260,
        ).pack(anchor="nw", fill="both")

        legend = SectionFrame(side, "Legend")
        legend.pack(fill="x")
        for label, color in [
            ("Start node", COLORS["green"]),
            ("End node", COLORS["red"]),
            ("Wall", COLORS["wall"]),
            ("Visited", COLORS["cyan_dark"]),
            ("Shortest path", COLORS["yellow"]),
        ]:
            row = tk.Frame(legend.body, bg=COLORS["panel"])
            row.pack(fill="x", pady=2)
            tk.Label(row, bg=color, width=3).pack(side="left")
            tk.Label(row, text=label, bg=COLORS["panel"], fg=COLORS["text"], font=(FONT, 9)).pack(side="left", padx=8)

        self.update_algorithm_info()

    def handle_grid_click(self, event) -> None:
        """Edit a grid cell according to the current edit mode."""

        if self.running:
            return

        cell = self.event_to_cell(event)
        if cell is None:
            return

        mode = self.mode_var.get()
        if mode == "Wall" and cell not in {self.start_node, self.end_node}:
            self.walls.add(cell)
        elif mode == "Erase":
            self.walls.discard(cell)
        elif mode == "Start" and cell != self.end_node:
            self.walls.discard(cell)
            self.start_node = cell
        elif mode == "End" and cell != self.start_node:
            self.walls.discard(cell)
            self.end_node = cell

        self.clear_path_marks()

    def event_to_cell(self, event) -> Node | None:
        """Convert mouse coordinates into a row/column pair."""

        cell_size, x_offset, y_offset = self._grid_geometry()
        col = int((event.x - x_offset) / cell_size)
        row = int((event.y - y_offset) / cell_size)
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return row, col
        return None

    def start_visualization(self) -> None:
        """Run the selected algorithm and animate visited nodes and path."""

        if self.running:
            return

        self.clear_path_marks(redraw=False)
        algorithm_name = self.algorithm_var.get()
        algorithm = self.algorithms[algorithm_name]
        start = time.perf_counter()
        self.visited_order, self.path = algorithm(self.rows, self.cols, self.start_node, self.end_node, self.walls)
        self.elapsed_ms = (time.perf_counter() - start) * 1000

        self.visited_index = 0
        self.path_index = 0
        self.running = True
        self.status_var.set(f"Animating {algorithm_name}...")
        self._animate_visited()

    def start(self) -> None:
        """Shortcut-friendly alias for starting the pathfinding visualizer."""

        self.start_visualization()

    def stop_visualization(self) -> None:
        """Stop the current animation safely."""

        self.running = False
        if self.after_id is not None:
            self.after_cancel(self.after_id)
            self.after_id = None
        self.status_var.set("Visualization stopped.")

    def clear_grid(self) -> None:
        """Remove walls and animation marks while keeping start/end positions."""

        self.stop_visualization()
        self.walls.clear()
        self.clear_path_marks()
        self.status_var.set("Grid cleared.")

    def reset_grid(self) -> None:
        """Restore the default grid layout."""

        self.stop_visualization()
        self.walls.clear()
        self.start_node = (5, 5)
        self.end_node = (14, 27)
        self.clear_path_marks()
        self.status_var.set("Grid reset to default start and end nodes.")

    def reset_visualizer(self) -> None:
        """Shortcut-friendly alias for resetting the pathfinding visualizer."""

        self.reset_grid()

    def clear_path_marks(self, redraw: bool = True) -> None:
        """Clear visited/path overlays but keep walls."""

        self.visited_order = []
        self.path = []
        self.visited_index = 0
        self.path_index = 0
        self.elapsed_ms = 0.0
        self.stats.set("Visited", 0)
        self.stats.set("Path", 0)
        self.stats.set("Time", "0 ms")
        if redraw:
            self.draw_grid()

    def _animate_visited(self) -> None:
        """Animate visited nodes one by one."""

        if not self.running:
            return

        if self.visited_index < len(self.visited_order):
            self.visited_index += 1
            self.draw_grid(visited_count=self.visited_index, path_count=0)
            self.stats.set("Visited", self.visited_index)
            delay = max(5, 105 - int(self.speed_scale.get()))
            self.after_id = self.after(delay, self._animate_visited)
            return

        self._animate_path()

    def _animate_path(self) -> None:
        """Animate shortest path after visited animation finishes."""

        if not self.running:
            return

        if self.path_index <= len(self.path):
            self.draw_grid(visited_count=len(self.visited_order), path_count=self.path_index)
            self.stats.set("Path", self.path_index)
            self.path_index += 1
            delay = max(8, 115 - int(self.speed_scale.get()))
            self.after_id = self.after(delay, self._animate_path)
            return

        self.running = False
        self.after_id = None
        self.stats.set("Visited", len(self.visited_order))
        self.stats.set("Path", len(self.path))
        self.stats.set("Time", f"{self.elapsed_ms:.2f} ms")
        record_result(
            "pathfinding",
            "A*" if self.algorithm_var.get() == "A* Search Algorithm" else "Dijkstra",
            {
                "visited": len(self.visited_order),
                "time_ms": self.elapsed_ms,
                "path_length": len(self.path),
            },
        )
        if self.path:
            self.status_var.set(f"Shortest path found with length {len(self.path)}.")
        else:
            self.status_var.set("No path found. Try removing some walls.")

    def draw_grid(self, visited_count: int = 0, path_count: int = 0) -> None:
        """Draw the grid, nodes, walls, visited nodes, and shortest path."""

        self.canvas.delete("all")
        cell_size, x_offset, y_offset = self._grid_geometry()
        visited = set(self.visited_order[:visited_count])
        path = set(self.path[:path_count])

        for row in range(self.rows):
            for col in range(self.cols):
                node = (row, col)
                x1 = x_offset + col * cell_size
                y1 = y_offset + row * cell_size
                x2 = x1 + cell_size - 1
                y2 = y1 + cell_size - 1
                fill = COLORS["panel_2"]

                if node in self.walls:
                    fill = COLORS["wall"]
                if node in visited:
                    fill = COLORS["cyan_dark"]
                if node in path:
                    fill = COLORS["yellow"]
                if node == self.start_node:
                    fill = COLORS["green"]
                if node == self.end_node:
                    fill = COLORS["red"]

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline=COLORS["grid"])

        self.canvas.create_text(
            16,
            16,
            anchor="w",
            text=f"Mode: {self.mode_var.get()}   |   Drag to edit grid",
            fill=COLORS["muted"],
            font=(FONT, 9),
        )

    def _grid_geometry(self) -> tuple[float, float, float]:
        """Calculate responsive grid cell size and centered offsets."""

        width = max(self.canvas.winfo_width(), 620)
        height = max(self.canvas.winfo_height(), 360)
        top_padding = 34
        cell_size = min((width - 20) / self.cols, (height - top_padding - 10) / self.rows)
        x_offset = (width - self.cols * cell_size) / 2
        y_offset = top_padding + max(0, (height - top_padding - self.rows * cell_size) / 2)
        return cell_size, x_offset, y_offset

    def update_algorithm_info(self) -> None:
        """Refresh complexity and explanation panels."""

        details = ALGORITHM_DETAILS[self.algorithm_var.get()]
        self.complexity_var.set(
            f"Time Complexity: {details['time']}\n"
            f"Space Complexity: {details['space']}"
        )
        self.explanation_var.set(
            f"{details['explanation']}\n\n"
            f"Difference:\n{COMPARISON_TEXT}\n\n"
            "Heuristic in A*:\nManhattan distance estimates how many grid moves remain "
            "from a node to the end node."
        )
