from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Violation:
    check_name: str
    severity: str
    message: str
    file_path: str
    line_number: int = 0
    column: int = 0
    suggestion: Optional[str] = None
