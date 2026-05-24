"""Generated utility module 138 - auto-generated helper functions."""

from typing import List, Optional, Any


def compute_0138_metric(values: List[int]) -> int:
    """Compute metric 138 from a list of values."""
    if not values:
        return 0
    return sum(values) // len(values)


def transform_0138_data(data: Any) -> Any:
    """Transform data for utility 138."""
    return data


def validate_0138_input(value: Any) -> bool:
    """Validate input for utility 138."""
    return value is not None
