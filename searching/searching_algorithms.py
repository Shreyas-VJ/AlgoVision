"""Searching algorithms converted into animation steps."""

from __future__ import annotations


Step = dict[str, object]


ALGORITHM_DETAILS = {
    "Linear Search": {
        "time": "O(n)",
        "space": "O(1)",
        "best": "O(1) when the target is the first element.",
        "average": "O(n) because about half the array is checked on average.",
        "worst": "O(n) when the target is last or absent.",
        "explanation": "Linear Search checks every element from left to right until it finds the target.",
    },
    "Binary Search": {
        "time": "O(log n)",
        "space": "O(1)",
        "best": "O(1) when the target is exactly at the middle.",
        "average": "O(log n) because the search range is halved every step.",
        "worst": "O(log n) when repeated halving continues until one element remains.",
        "explanation": "Binary Search works only on a sorted array. It checks the middle value and eliminates half of the remaining range.",
    },
}


class SearchingAlgorithms:
    """Pure searching logic that returns UI-friendly animation steps."""

    @staticmethod
    def linear_search(values: list[int], target: int) -> tuple[list[Step], int, int]:
        """Search one by one from left to right."""

        steps: list[Step] = []
        comparisons = 0
        found_index = -1

        for index, value in enumerate(values):
            comparisons += 1
            steps.append(
                _step(
                    action="check",
                    active=[index],
                    eliminated=list(range(index)),
                    found=[],
                    message=f"Checking index {index}: {value}",
                )
            )
            if value == target:
                found_index = index
                steps.append(
                    _step(
                        action="found",
                        active=[index],
                        eliminated=list(range(index)),
                        found=[index],
                        message=f"Target {target} found at index {index}.",
                    )
                )
                break

        if found_index == -1:
            steps.append(
                _step(
                    action="missing",
                    active=[],
                    eliminated=list(range(len(values))),
                    found=[],
                    message=f"Target {target} was not found.",
                )
            )

        return steps, found_index, comparisons

    @staticmethod
    def binary_search(values: list[int], target: int) -> tuple[list[Step], int, int]:
        """Search a sorted array by repeatedly halving the active range."""

        steps: list[Step] = []
        comparisons = 0
        found_index = -1
        left = 0
        right = len(values) - 1
        eliminated: set[int] = set()

        while left <= right:
            active_range = list(range(left, right + 1))
            steps.append(
                _step(
                    action="range",
                    active=active_range,
                    eliminated=sorted(eliminated),
                    found=[],
                    message=f"Active search range: index {left} to {right}.",
                )
            )

            mid = (left + right) // 2
            comparisons += 1
            steps.append(
                _step(
                    action="check",
                    active=[mid],
                    eliminated=sorted(eliminated),
                    found=[],
                    message=f"Checking middle index {mid}: {values[mid]}.",
                )
            )

            if values[mid] == target:
                found_index = mid
                steps.append(
                    _step(
                        action="found",
                        active=[mid],
                        eliminated=sorted(eliminated),
                        found=[mid],
                        message=f"Target {target} found at index {mid}.",
                    )
                )
                break

            if values[mid] < target:
                eliminated.update(range(left, mid + 1))
                steps.append(
                    _step(
                        action="eliminate",
                        active=[],
                        eliminated=sorted(eliminated),
                        found=[],
                        message=f"{values[mid]} is smaller than {target}. Eliminating left half.",
                    )
                )
                left = mid + 1
            else:
                eliminated.update(range(mid, right + 1))
                steps.append(
                    _step(
                        action="eliminate",
                        active=[],
                        eliminated=sorted(eliminated),
                        found=[],
                        message=f"{values[mid]} is greater than {target}. Eliminating right half.",
                    )
                )
                right = mid - 1

        if found_index == -1:
            steps.append(
                _step(
                    action="missing",
                    active=[],
                    eliminated=list(range(len(values))),
                    found=[],
                    message=f"Target {target} was not found.",
                )
            )

        return steps, found_index, comparisons


def _step(action: str, active: list[int], eliminated: list[int], found: list[int], message: str) -> Step:
    """Create one animation step."""

    return {
        "action": action,
        "active": active[:],
        "eliminated": eliminated[:],
        "found": found[:],
        "message": message,
    }
