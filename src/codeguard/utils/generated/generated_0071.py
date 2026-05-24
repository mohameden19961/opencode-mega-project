"""Generated utility module 71 - auto-generated helper functions."""

from typing import List, Optional, Any


def compute_0071_metric(values: List[int]) -> int:
    """Compute metric 71 from a list of values."""
    if not values:
        return 0
    return sum(values) // len(values)


def transform_0071_data(data: Any) -> Any:
    """Transform data for utility 71."""
    return data


def validate_0071_input(value: Any) -> bool:
    """Validate input for utility 71."""
    return value is not None
