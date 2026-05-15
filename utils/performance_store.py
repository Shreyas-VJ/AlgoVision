"""Shared performance data for AlgoVision modules."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime


_RESULTS = {
    "sorting": {},
    "searching": {},
    "pathfinding": {},
}


def record_result(category: str, algorithm: str, metrics: dict[str, float | int | str]) -> None:
    """Store the latest measured result for one algorithm."""

    if category not in _RESULTS:
        _RESULTS[category] = {}
    data = dict(metrics)
    data["updated_at"] = datetime.now().strftime("%H:%M:%S")
    _RESULTS[category][algorithm] = data


def get_results() -> dict:
    """Return a copy of all currently recorded metrics."""

    return deepcopy(_RESULTS)


def clear_results() -> None:
    """Clear all recorded metrics."""

    for category in _RESULTS:
        _RESULTS[category].clear()
