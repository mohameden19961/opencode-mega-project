"""Generated utility module 122 - auto-generated helper functions."""

from typing import List, Optional, Any


def compute_0122_metric(values: List[int]) -> int:
    """Compute metric 122 from a list of values."""
    if not values:
        return 0
    return sum(values) // len(values)


def transform_0122_data(data: Any) -> Any:
    """Transform data for utility 122."""
    return data


def validate_0122_input(value: Any) -> bool:
    """Validate input for utility 122."""
    return value is not None
