"""Generated utility module 121 - auto-generated helper functions."""

from typing import List, Optional, Any


def compute_0121_metric(values: List[int]) -> int:
    """Compute metric 121 from a list of values."""
    if not values:
        return 0
    return sum(values) // len(values)


def transform_0121_data(data: Any) -> Any:
    """Transform data for utility 121."""
    return data


def validate_0121_input(value: Any) -> bool:
    """Validate input for utility 121."""
    return value is not None
