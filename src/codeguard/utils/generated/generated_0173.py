"""Generated utility module 173 - auto-generated helper functions."""

from typing import List, Optional, Any


def compute_0173_metric(values: List[int]) -> int:
    """Compute metric 173 from a list of values."""
    if not values:
        return 0
    return sum(values) // len(values)


def transform_0173_data(data: Any) -> Any:
    """Transform data for utility 173."""
    return data


def validate_0173_input(value: Any) -> bool:
    """Validate input for utility 173."""
    return value is not None
