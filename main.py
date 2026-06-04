"""CodeVerse: Algorithm Learning Platform.

Run this file to start the Tkinter desktop application.
"""

from __future__ import annotations

import sys
import tkinter as tk
from tkinter import ttk, messagebox

from sorting.sorting_visualizer import SortingVisualizer
from searching.searching_visualizer import SearchingVisualizer
from utils.theme import COLORS, FONT, configure_styles
from utils.widgets import DashboardCard, SectionFrame


class SplashScreen(tk.Toplevel):
    """Small splash screen shown before the main dashboard."""

    def __init__(self, parent: tk.Tk) -> None:
        super().__init__(parent)
        self.overrideredirect(True)
        self.configure(bg=COLORS["bg"])
        self.geometry("620x340+360+190")

        box = tk.Frame(
            self, bg=COLORS["panel"], highlightbackground=COLORS["cyan"], highlightthickness=2)
        box.pack(expand=True, fill="both", padx=18, pady=18)

        tk.Label(
            box,
            text="CodeVerse",
            bg=COLORS["panel"],
            fg=COLORS["cyan"],
            font=(FONT, 30, "bold"),
        ).pack(pady=(58, 8))
        tk.Label(
            box,
            text="Algorithm Learning Platform",
            bg=COLORS["panel"],
            fg=COLORS["muted"],
            font=(FONT, 13),
        ).pack()

        bar = ttk.Progressbar(box, mode="indeterminate", length=330)
        bar.pack(pady=42)
        bar.start(12)


class AlgoVisionApp(tk.Tk):
    """Main application window and navigation controller."""

    def __init__(self) -> None:
        super().__init__()
        self.title("CodeVerse: Algorithm Learning Platform")
        self.geometry("1280x760")
        self.minsize(1120, 680)
        self.configure(bg=COLORS["bg"])
        configure_styles(self)

        self.current_frame: tk.Frame | None = None
        self.frames: dict[str, tk.Frame] = {}
        self._build_menu()
        self._bind_shortcuts()

        splash = SplashScreen(self)
        self.withdraw()
        self.after(1200, lambda: self._show_after_splash(splash))

    def _show_after_splash(self, splash: SplashScreen) -> None:
        splash.destroy()
        self.deiconify()
        self.show_dashboard()

    def _build_menu(self) -> None:
        menubar = tk.Menu(
            self,
            bg=COLORS["panel"],
            fg=COLORS["text"],
            activebackground=COLORS["panel_2"],
            activeforeground=COLORS["cyan"],
        )
        module_menu = tk.Menu(menubar, tearoff=0,
                              bg=COLORS["panel"], fg=COLORS["text"], activebackground=COLORS["panel_2"])
        module_menu.add_command(
            label="Home", accelerator="Ctrl+H", command=self.show_dashboard)
        module_menu.add_command(
            label="Sorting", accelerator="Ctrl+1", command=lambda: self.show_module("sorting"))
        module_menu.add_command(label="Searching", accelerator="Ctrl+2",
                                command=lambda: self.show_module("searching"))
        module_menu.add_command(label="Pathfinding", accelerator="Ctrl+3",
                                command=lambda: self.show_module("pathfinding"))
        module_menu.add_separator()
        module_menu.add_command(label="Exit", command=self.destroy)
        menubar.add_cascade(label="Navigate", menu=module_menu)

        help_menu = tk.Menu(menubar, tearoff=0,
                            bg=COLORS["panel"], fg=COLORS["text"], activebackground=COLORS["panel_2"])
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="Keyboard Shortcuts",
                              command=self.show_shortcuts)
        menubar.add_cascade(label="Help", menu=help_menu)
        self.config(menu=menubar)

    def _bind_shortcuts(self) -> None:
        self.bind("<Control-h>", lambda _event: self.show_dashboard())
        self.bind("<Control-Key-1>", lambda _event: self.show_module("sorting"))
        self.bind("<Control-Key-2>",
                  lambda _event: self.show_module("searching"))
        self.bind("<Control-Key-3>",
                  lambda _event: self.show_module("pathfinding"))
        self.bind("<Escape>", lambda _event: self.show_dashboard())

    def _set_frame(self, frame: tk.Frame) -> None:
        if self.current_frame is not None:
            self.current_frame.pack_forget()
        self.current_frame = frame
        self.current_frame.pack(fill="both", expand=True)

    def show_dashboard(self) -> None:
        if "dashboard" not in self.frames:
            self.frames["dashboard"] = Dashboard(self)
        self._set_frame(self.frames["dashboard"])

    def show_module(self, module_name: str) -> None:
        if module_name not in self.frames:
            if module_name == "sorting":
                self.frames[module_name] = SortingVisualizer(self)
            elif module_name == "searching":
                self.frames[module_name] = SearchingVisualizer(self)
            elif module_name == "pathfinding":
                self.frames[module_name] = PathfindingVisualizer(self)
        self._set_frame(self.frames[module_name])

    def show_about(self) -> None:
        messagebox.showinfo(
            "About CodeVerse",
            "CodeVerse: Algorithm Learning Platform\n\n"
            "A 4th semester DAA mini project built with Python, Tkinter, Canvas, "
            "OOP, and matplotlib.\n\n"
            "Modules: Sorting, Searching, Dijkstra.",
        )

    def show_shortcuts(self) -> None:
        messagebox.showinfo(
            "Keyboard Shortcuts",
            "Ctrl+H: Home\nCtrl+1: Sorting\nCtrl+2: Searching\nCtrl+3: Pathfinding\nEsc: Home",
        )


class Dashboard(tk.Frame):
    """Professional landing dashboard with navigation cards."""

    def __init__(self, app: AlgoVisionApp) -> None:
        super().__init__(app, bg=COLORS["bg"])
        self.app = app
        self._build()

    def _build(self) -> None:
        hero = tk.Frame(self, bg=COLORS["bg"])
        hero.pack(fill="x", padx=36, pady=(28, 16))

        tk.Label(
            hero,
            text="DAA Visualizzer Pro",
            bg=COLORS["bg"],
            fg=COLORS["cyan"],
            font=(FONT, 34, "bold"),
        ).pack(anchor="w")
        tk.Label(
            hero,
            text="Interactive Algorithm Learning Platform for sorting, searching, and pathfinding.",
            bg=COLORS["bg"],
            fg=COLORS["muted"],
            font=(FONT, 13),
        ).pack(anchor="w", pady=(5, 0))

        quick_nav = tk.Frame(hero, bg=COLORS["bg"])
        quick_nav.pack(anchor="w", pady=18)
        ttk.Button(quick_nav, text="Sorting", command=lambda: self.app.show_module(
            "sorting")).pack(side="left", padx=(0, 10))
        ttk.Button(quick_nav, text="Searching", command=lambda: self.app.show_module(
            "searching")).pack(side="left", padx=10)
        ttk.Button(quick_nav, text="Pathfinding", command=lambda: self.app.show_module(
            "pathfinding")).pack(side="left", padx=10)

        cards = tk.Frame(self, bg=COLORS["bg"])
        cards.pack(fill="both", expand=True, padx=36, pady=12)
        cards.columnconfigure((0, 1, 2), weight=1, uniform="cards")

        DashboardCard(
            cards,
            title="Sorting Visualizer",
            subtitle="Bubble, Selection, Insertion, Merge, Quick, and Heap Sort.",
            accent=COLORS["cyan"],
            command=lambda: self.app.show_module("sorting"),
        ).grid(row=0, column=0, sticky="nsew", padx=(0, 12), pady=12)
        DashboardCard(
            cards,
            title="Searching Visualizer",
            subtitle="Linear and Binary Search with animated target discovery.",
            accent=COLORS["green"],
            command=lambda: self.app.show_module("searching"),
        ).grid(row=0, column=1, sticky="nsew", padx=12, pady=12)
        DashboardCard(
            cards,
            title="Pathfinding Visualizer",
            subtitle="Draw walls and compare Dijkstra with A* Search.",
            accent=COLORS["magenta"],
            command=lambda: self.app.show_module("pathfinding"),
        ).grid(row=0, column=2, sticky="nsew", padx=(12, 0), pady=12)

        info = SectionFrame(self, "Mini Project Highlights")
        info.pack(fill="x", padx=36, pady=(0, 18))
        text = (
            "Built for Design and Analysis of Algorithms demonstrations: animated Canvas visualizations, "
            "comparison counters, complexity panels, explanation sections, keyboard shortcuts, and charts."
        )
        tk.Label(info.body, text=text, bg=COLORS["panel"], fg=COLORS["text"], font=(
            FONT, 11), wraplength=1100, justify="left").pack(anchor="w")

        footer = tk.Frame(self, bg=COLORS["bg"])
        footer.pack(fill="x", side="bottom", padx=36, pady=(4, 18))
        tk.Label(
            footer,
            text="© 2026 CodeVerse: Algorithm Learning Platform | Python + Tkinter + Matplotlib",
            bg=COLORS["bg"],
            fg=COLORS["muted"],
            font=(FONT, 10),
        ).pack(side="left")


def main() -> int:
    """Start CodeVerse and print a clear fix if Tkinter is unavailable."""

    try:
        app = AlgoVisionApp()
        app.mainloop()
    except tk.TclError as error:
        print("\n CodeVerse could not start because Tkinter/Tcl is not working.")
        print("This is a Python installation issue, not an CodeVerse code error.\n")
        print(f"Details: {error}\n")
        print("Fix:")
        print("1. Repair or reinstall Python from python.org.")
        print("2. In the installer, enable 'tcl/tk and IDLE' and 'pip'.")
        print("3. Test with:")
        print('   python -c "import tkinter as tk; root=tk.Tk(); root.destroy(); print(\'Tkinter OK\')"')
        print("4. Then run:")
        print(
            '   cd "C:\\Users\\Shreyas\\OneDrive\\Desktop\\DAA Visualizer Pro\\AlgoVision"')
        print("   python main.py\n")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
