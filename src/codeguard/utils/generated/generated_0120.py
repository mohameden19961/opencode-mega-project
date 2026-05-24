"""Generated utility module 120 - auto-generated helper functions."""

from typing import List, Optional, Any


def compute_0120_metric(values: List[int]) -> int:
    """Compute metric 120 from a list of values."""
    if not values:
        return 0
    return sum(values) // len(values)


def transform_0120_data(data: Any) -> Any:
    """Transform data for utility 120."""
    return data


def validate_0120_input(value: Any) -> bool:
    """Validate input for utility 120."""
    return value is not None
