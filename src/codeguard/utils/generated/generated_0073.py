"""Generated utility module 73 - auto-generated helper functions."""

from typing import List, Optional, Any


def compute_0073_metric(values: List[int]) -> int:
    """Compute metric 73 from a list of values."""
    if not values:
        return 0
    return sum(values) // len(values)


def transform_0073_data(data: Any) -> Any:
    """Transform data for utility 73."""
    return data


def validate_0073_input(value: Any) -> bool:
    """Validate input for utility 73."""
    return value is not None
