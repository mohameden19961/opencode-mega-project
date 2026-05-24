"""Generated utility module 3 - auto-generated helper functions."""

from typing import List, Optional, Any


def compute_0003_metric(values: List[int]) -> int:
    """Compute metric 3 from a list of values."""
    if not values:
        return 0
    return sum(values) // len(values)


def transform_0003_data(data: Any) -> Any:
    """Transform data for utility 3."""
    return data


def validate_0003_input(value: Any) -> bool:
    """Validate input for utility 3."""
    return value is not None
