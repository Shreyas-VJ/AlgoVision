"""Sorting algorithms converted into animation steps.

Each method returns:
    steps, comparisons, swaps

The visualizer reads the step list using Tkinter's after() method, so the UI
stays responsive while the bars animate.
"""

from __future__ import annotations


Step = dict[str, object]


ALGORITHM_DETAILS = {
    "Bubble Sort": {
        "time": "O(n^2)",
        "space": "O(1)",
        "explanation": "Compares adjacent elements and repeatedly bubbles the largest value to the end.",
    },
    "Selection Sort": {
        "time": "O(n^2)",
        "space": "O(1)",
        "explanation": "Selects the smallest element from the unsorted part and places it at the front.",
    },
    "Insertion Sort": {
        "time": "O(n^2)",
        "space": "O(1)",
        "explanation": "Builds the sorted part one item at a time by inserting each value into its correct position.",
    },
    "Merge Sort": {
        "time": "O(n log n)",
        "space": "O(n)",
        "explanation": "Divides the array into smaller parts, sorts them, and merges the sorted parts.",
    },
    "Quick Sort": {
        "time": "O(n log n) average, O(n^2) worst",
        "space": "O(log n)",
        "explanation": "Chooses a pivot, partitions smaller and larger values, then sorts both sides recursively.",
    },
    "Heap Sort": {
        "time": "O(n log n)",
        "space": "O(1)",
        "explanation": "Builds a max heap and repeatedly moves the largest value into its final sorted position.",
    },
}


class SortingAlgorithms:
    """Pure sorting algorithms that produce beginner-friendly animation steps."""

    @staticmethod
    def bubble_sort(values: list[int]) -> tuple[list[Step], int, int]:
        arr = values[:]
        steps: list[Step] = []
        comparisons = swaps = 0
        n = len(arr)

        for i in range(n):
            for j in range(0, n - i - 1):
                comparisons += 1
                steps.append(_step(arr, "compare", [j, j + 1], list(range(n - i, n))))
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    swaps += 1
                    steps.append(_step(arr, "swap", [j, j + 1], list(range(n - i, n))))
            steps.append(_step(arr, "sorted", [n - i - 1], list(range(n - i - 1, n))))

        steps.append(_step(arr, "done", [], list(range(n))))
        return steps, comparisons, swaps

    @staticmethod
    def selection_sort(values: list[int]) -> tuple[list[Step], int, int]:
        arr = values[:]
        steps: list[Step] = []
        comparisons = swaps = 0
        n = len(arr)

        for i in range(n):
            min_index = i
            for j in range(i + 1, n):
                comparisons += 1
                steps.append(_step(arr, "compare", [min_index, j], list(range(i))))
                if arr[j] < arr[min_index]:
                    min_index = j
            if min_index != i:
                arr[i], arr[min_index] = arr[min_index], arr[i]
                swaps += 1
                steps.append(_step(arr, "swap", [i, min_index], list(range(i))))
            steps.append(_step(arr, "sorted", [i], list(range(i + 1))))

        steps.append(_step(arr, "done", [], list(range(n))))
        return steps, comparisons, swaps

    @staticmethod
    def insertion_sort(values: list[int]) -> tuple[list[Step], int, int]:
        arr = values[:]
        steps: list[Step] = []
        comparisons = swaps = 0

        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            while j >= 0:
                comparisons += 1
                steps.append(_step(arr, "compare", [j, j + 1], list(range(i))))
                if arr[j] <= key:
                    break
                arr[j + 1] = arr[j]
                swaps += 1
                steps.append(_step(arr, "swap", [j, j + 1], list(range(i))))
                j -= 1
            arr[j + 1] = key
            steps.append(_step(arr, "write", [j + 1], list(range(i + 1))))

        steps.append(_step(arr, "done", [], list(range(len(arr)))))
        return steps, comparisons, swaps

    @staticmethod
    def merge_sort(values: list[int]) -> tuple[list[Step], int, int]:
        arr = values[:]
        steps: list[Step] = []
        counters = {"comparisons": 0, "swaps": 0}

        def merge(left: int, mid: int, right: int) -> None:
            left_part = arr[left : mid + 1]
            right_part = arr[mid + 1 : right + 1]
            i = j = 0
            k = left

            while i < len(left_part) and j < len(right_part):
                counters["comparisons"] += 1
                steps.append(_step(arr, "compare", [left + i, mid + 1 + j], []))
                if left_part[i] <= right_part[j]:
                    arr[k] = left_part[i]
                    i += 1
                else:
                    arr[k] = right_part[j]
                    j += 1
                counters["swaps"] += 1
                steps.append(_step(arr, "write", [k], list(range(left, k + 1))))
                k += 1

            while i < len(left_part):
                arr[k] = left_part[i]
                counters["swaps"] += 1
                steps.append(_step(arr, "write", [k], list(range(left, k + 1))))
                i += 1
                k += 1

            while j < len(right_part):
                arr[k] = right_part[j]
                counters["swaps"] += 1
                steps.append(_step(arr, "write", [k], list(range(left, k + 1))))
                j += 1
                k += 1

        def divide(left: int, right: int) -> None:
            if left >= right:
                return
            mid = (left + right) // 2
            divide(left, mid)
            divide(mid + 1, right)
            merge(left, mid, right)

        divide(0, len(arr) - 1)
        steps.append(_step(arr, "done", [], list(range(len(arr)))))
        return steps, counters["comparisons"], counters["swaps"]

    @staticmethod
    def quick_sort(values: list[int]) -> tuple[list[Step], int, int]:
        arr = values[:]
        steps: list[Step] = []
        counters = {"comparisons": 0, "swaps": 0}

        def partition(low: int, high: int) -> int:
            pivot = arr[high]
            i = low - 1
            for j in range(low, high):
                counters["comparisons"] += 1
                steps.append(_step(arr, "compare", [j, high], []))
                if arr[j] <= pivot:
                    i += 1
                    if i != j:
                        arr[i], arr[j] = arr[j], arr[i]
                        counters["swaps"] += 1
                        steps.append(_step(arr, "swap", [i, j], []))
            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            counters["swaps"] += 1
            steps.append(_step(arr, "swap", [i + 1, high], [i + 1]))
            return i + 1

        def sort(low: int, high: int) -> None:
            if low < high:
                pivot_index = partition(low, high)
                sort(low, pivot_index - 1)
                sort(pivot_index + 1, high)

        sort(0, len(arr) - 1)
        steps.append(_step(arr, "done", [], list(range(len(arr)))))
        return steps, counters["comparisons"], counters["swaps"]

    @staticmethod
    def heap_sort(values: list[int]) -> tuple[list[Step], int, int]:
        arr = values[:]
        steps: list[Step] = []
        counters = {"comparisons": 0, "swaps": 0}

        def heapify(size: int, root: int) -> None:
            largest = root
            left = 2 * root + 1
            right = 2 * root + 2

            if left < size:
                counters["comparisons"] += 1
                steps.append(_step(arr, "compare", [largest, left], list(range(size, len(arr)))))
                if arr[left] > arr[largest]:
                    largest = left

            if right < size:
                counters["comparisons"] += 1
                steps.append(_step(arr, "compare", [largest, right], list(range(size, len(arr)))))
                if arr[right] > arr[largest]:
                    largest = right

            if largest != root:
                arr[root], arr[largest] = arr[largest], arr[root]
                counters["swaps"] += 1
                steps.append(_step(arr, "swap", [root, largest], list(range(size, len(arr)))))
                heapify(size, largest)

        n = len(arr)
        for index in range(n // 2 - 1, -1, -1):
            heapify(n, index)

        for index in range(n - 1, 0, -1):
            arr[index], arr[0] = arr[0], arr[index]
            counters["swaps"] += 1
            steps.append(_step(arr, "swap", [0, index], list(range(index, n))))
            heapify(index, 0)

        steps.append(_step(arr, "done", [], list(range(n))))
        return steps, counters["comparisons"], counters["swaps"]


def _step(array: list[int], action: str, active: list[int], sorted_indices: list[int]) -> Step:
    """Create one animation step with a copy of the current array."""

    return {
        "array": array[:],
        "action": action,
        "active": active[:],
        "sorted": sorted_indices[:],
    }
