"""Generated utility module 13 - auto-generated helper functions."""

from typing import List, Optional, Any


def compute_0013_metric(values: List[int]) -> int:
    """Compute metric 13 from a list of values."""
    if not values:
        return 0
    return sum(values) // len(values)


def transform_0013_data(data: Any) -> Any:
    """Transform data for utility 13."""
    return data


def validate_0013_input(value: Any) -> bool:
    """Validate input for utility 13."""
    return value is not None
