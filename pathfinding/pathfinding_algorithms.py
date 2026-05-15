"""Pathfinding algorithms used by the AlgoVision visualizer."""

from __future__ import annotations

import heapq


Node = tuple[int, int]


ALGORITHM_DETAILS = {
    "Dijkstra Algorithm": {
        "time": "O((V + E) log V)",
        "space": "O(V)",
        "explanation": (
            "Dijkstra expands the unvisited node with the smallest known distance. "
            "Because every grid edge has equal cost here, it finds the shortest path "
            "by spreading outward from the start node."
        ),
    },
    "A* Search Algorithm": {
        "time": "O(E) typical, O((V + E) log V) worst",
        "space": "O(V)",
        "explanation": (
            "A* combines the distance already travelled with a heuristic estimate to "
            "the goal. This visualizer uses Manhattan distance, which works well for "
            "four-direction grid movement."
        ),
    },
}


COMPARISON_TEXT = (
    "Dijkstra is uninformed: it guarantees the shortest path by exploring cheapest "
    "known distances in all directions. A* is informed: it also uses a heuristic, "
    "so it usually visits fewer nodes when the heuristic points toward the goal."
)


class PathfindingAlgorithms:
    """Pure pathfinding routines for Dijkstra and A* Search."""

    @staticmethod
    def dijkstra(rows: int, cols: int, start: Node, end: Node, walls: set[Node]) -> tuple[list[Node], list[Node]]:
        """Find a shortest path using Dijkstra's algorithm."""

        queue: list[tuple[int, Node]] = [(0, start)]
        distances = {start: 0}
        came_from: dict[Node, Node] = {}
        visited_order: list[Node] = []
        visited: set[Node] = set()

        while queue:
            current_distance, current = heapq.heappop(queue)
            if current in visited:
                continue
            visited.add(current)
            visited_order.append(current)

            if current == end:
                break

            for neighbor in _neighbors(current, rows, cols):
                if neighbor in walls:
                    continue
                new_distance = current_distance + 1
                if new_distance < distances.get(neighbor, float("inf")):
                    distances[neighbor] = new_distance
                    came_from[neighbor] = current
                    heapq.heappush(queue, (new_distance, neighbor))

        return visited_order, _reconstruct_path(came_from, start, end)

    @staticmethod
    def astar(rows: int, cols: int, start: Node, end: Node, walls: set[Node]) -> tuple[list[Node], list[Node]]:
        """Find a shortest path using A* Search with Manhattan distance."""

        queue: list[tuple[int, int, Node]] = [(_manhattan(start, end), 0, start)]
        costs = {start: 0}
        came_from: dict[Node, Node] = {}
        visited_order: list[Node] = []
        visited: set[Node] = set()

        while queue:
            _priority, current_cost, current = heapq.heappop(queue)
            if current in visited:
                continue
            visited.add(current)
            visited_order.append(current)

            if current == end:
                break

            for neighbor in _neighbors(current, rows, cols):
                if neighbor in walls:
                    continue
                new_cost = current_cost + 1
                if new_cost < costs.get(neighbor, float("inf")):
                    costs[neighbor] = new_cost
                    came_from[neighbor] = current
                    priority = new_cost + _manhattan(neighbor, end)
                    heapq.heappush(queue, (priority, new_cost, neighbor))

        return visited_order, _reconstruct_path(came_from, start, end)


def _neighbors(node: Node, rows: int, cols: int) -> list[Node]:
    """Return valid four-direction grid neighbors."""

    row, col = node
    candidates = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
    return [(r, c) for r, c in candidates if 0 <= r < rows and 0 <= c < cols]


def _manhattan(a: Node, b: Node) -> int:
    """Estimate grid distance without diagonal movement."""

    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def _reconstruct_path(came_from: dict[Node, Node], start: Node, end: Node) -> list[Node]:
    """Rebuild the path from end to start."""

    if end == start:
        return [start]
    if end not in came_from:
        return []

    path = [end]
    current = end
    while current != start:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path
