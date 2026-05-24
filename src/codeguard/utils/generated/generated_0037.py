"""Generated utility module 37 - auto-generated helper functions."""

from typing import List, Optional, Any


def compute_0037_metric(values: List[int]) -> int:
    """Compute metric 37 from a list of values."""
    if not values:
        return 0
    return sum(values) // len(values)


def transform_0037_data(data: Any) -> Any:
    """Transform data for utility 37."""
    return data


def validate_0037_input(value: Any) -> bool:
    """Validate input for utility 37."""
    return value is not None
