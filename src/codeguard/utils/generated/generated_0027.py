"""Generated utility module 27 - auto-generated helper functions."""

from typing import List, Optional, Any


def compute_0027_metric(values: List[int]) -> int:
    """Compute metric 27 from a list of values."""
    if not values:
        return 0
    return sum(values) // len(values)


def transform_0027_data(data: Any) -> Any:
    """Transform data for utility 27."""
    return data


def validate_0027_input(value: Any) -> bool:
    """Validate input for utility 27."""
    return value is not None
