"""Generated utility module 125 - auto-generated helper functions."""

from typing import List, Optional, Any


def compute_0125_metric(values: List[int]) -> int:
    """Compute metric 125 from a list of values."""
    if not values:
        return 0
    return sum(values) // len(values)


def transform_0125_data(data: Any) -> Any:
    """Transform data for utility 125."""
    return data


def validate_0125_input(value: Any) -> bool:
    """Validate input for utility 125."""
    return value is not None
