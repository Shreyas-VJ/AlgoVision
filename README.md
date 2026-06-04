<<<<<<< HEAD
# AlgoVision

**AlgoVision - Interactive DAA Algorithm Visualizer** is a professional Python Tkinter desktop application built for Design and Analysis of Algorithms mini project demonstrations, GitHub portfolio presentation, and viva explanation.

The application visualizes sorting, searching, pathfinding, and complexity analysis through a modern dark dashboard with neon cyan and purple accents.

## Features

- Animated splash screen with loading indicator
- Professional dashboard with top menu bar, sidebar navigation, status bar, and modern cards
- Sorting Visualizer with Bubble, Selection, Insertion, Merge, Quick, and Heap Sort
- Searching Visualizer with Linear Search and Binary Search
- Pathfinding Visualizer with Dijkstra Algorithm and A* Search Algorithm
- Complexity Analysis dashboard with matplotlib charts
- Export graph as image and export analysis report as CSV
- Real-time metrics for comparisons, swaps, execution time, visited nodes, and path length
- Algorithm explanation panels and theoretical complexity tables
- Keyboard shortcuts for faster demonstration
- Modular object-oriented code structure
- Tkinter Canvas based animations using `after()` to avoid UI freezing

## Installation

1. Open a terminal in the project folder:

```powershell
cd "C:\Users\Shreyas\OneDrive\Desktop\DAA Visualizer Pro\AlgoVision"
```

2. Create a virtual environment:

```powershell
python -m venv .venv
```

3. Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

4. Install dependencies:

```powershell
pip install -r requirements.txt
```

## How To Run

From the main project folder:

```powershell
cd "C:\Users\Shreyas\OneDrive\Desktop\DAA Visualizer Pro"
python .\AlgoVision\main.py
```

Or from inside the `AlgoVision` folder:

```powershell
cd "C:\Users\Shreyas\OneDrive\Desktop\DAA Visualizer Pro\AlgoVision"
python main.py
```

## Troubleshooting Tkinter

If the app fails with an error like:

```text
_tkinter.TclError: Can't find a usable init.tcl
```

then Python's Tcl/Tk installation is broken or incomplete. AlgoVision cannot open until Tkinter itself works.

Test Tkinter with:

```powershell
python -c "import tkinter as tk; root=tk.Tk(); root.destroy(); print('Tkinter OK')"
```

If that command fails, repair or reinstall Python from python.org and make sure the installer includes:

- `tcl/tk and IDLE`
- `pip`
- `Add python.exe to PATH`

After reinstalling, run:

```powershell
python -m pip install -r requirements.txt
python main.py
```

## Algorithms Used

### Sorting

- Bubble Sort
- Selection Sort
- Insertion Sort
- Merge Sort
- Quick Sort
- Heap Sort

### Searching

- Linear Search
- Binary Search

### Pathfinding

- Dijkstra Algorithm
- A* Search Algorithm with Manhattan distance heuristic

## Keyboard Shortcuts

- `Ctrl + H`: Home dashboard
- `Ctrl + S`: Start current visualizer
- `Ctrl + R`: Reset current page
- `Ctrl + Q`: Quit application

## Project Structure

```text
AlgoVision/
|-- main.py
|-- complexity_analysis.py
|-- requirements.txt
|-- README.md
|-- assets/
|-- sorting/
|   |-- sorting_algorithms.py
|   |-- sorting_visualizer.py
|-- searching/
|   |-- searching_algorithms.py
|   |-- searching_visualizer.py
|-- pathfinding/
|   |-- pathfinding_algorithms.py
|   |-- pathfinding_visualizer.py
|-- utils/
|   |-- performance_store.py
|   |-- theme.py
|   |-- widgets.py
```

## Screenshots

Add screenshots here after running the application:

- Dashboard
- Sorting Visualizer
- Searching Visualizer
- Pathfinding Visualizer
- Complexity Analysis

## Viva Explanation Points

- The app follows object-oriented programming with separate classes for the main app, dashboard pages, visualizers, algorithms, and reusable widgets.
- Algorithm logic is separated from GUI code, making the implementation easier to explain.
- Animations use Tkinter's `after()` method instead of blocking loops, so the UI remains responsive.
- Sorting metrics include comparisons, swaps, and execution time.
- Searching metrics include comparisons, result, and execution time.
- Pathfinding metrics include visited nodes, path length, and execution time.
- A* uses Manhattan distance as a heuristic to guide the search toward the goal.
- The Complexity Analysis page combines theoretical complexity with measured runtime data from visualizer runs.

## Future Enhancements

- Add maze generation for pathfinding
- Add graph traversal algorithms such as BFS and DFS
- Add recursion tree visualizations
- Add step-by-step pseudocode highlighting
- Add screenshot capture from inside the app
- Package the app as a Windows executable

## Academic Use

This project is intended for academic learning, classroom demonstration, mini project evaluation, and viva presentation for Design and Analysis of Algorithms.
=======
# AlgoVision
>>>>>>> aaed2a32b3d059b3330eaacc076e4e8f110380a8
