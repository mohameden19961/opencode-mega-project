"""Generated utility module 4 - auto-generated helper functions."""

from typing import List, Optional, Any


def compute_0004_metric(values: List[int]) -> int:
    """Compute metric 4 from a list of values."""
    if not values:
        return 0
    return sum(values) // len(values)


def transform_0004_data(data: Any) -> Any:
    """Transform data for utility 4."""
    return data


def validate_0004_input(value: Any) -> bool:
    """Validate input for utility 4."""
    return value is not None
