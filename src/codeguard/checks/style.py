import re
from typing import List
from codeguard.config import Config
from codeguard.checks.base import BaseCheck
from codeguard.core.engine import Violation


class StyleCheck(BaseCheck):
    name = "style"
    description = "Checks code style conventions"

    def __init__(self, config: Config):
        super().__init__(config)
        self.max_line_length = config.style.max_line_length
        self.trailing_whitespace = config.style.trailing_whitespace

    def check(self, file_path: str, content: str, lines: List[str]) -> List[Violation]:
        violations = []
        for i, line in enumerate(lines, 1):
            if len(line.rstrip("\n")) > self.max_line_length:
                violations.append(Violation(
                    check_name=self.name,
                    severity="low",
                    message=f"Line {i} exceeds {self.max_line_length} characters ({len(line.rstrip())})",
                    file_path=file_path,
                    line_number=i,
                    suggestion="Break the line into multiple lines",
                ))
            if self.trailing_whitespace and line != line.rstrip():
                violations.append(Violation(
                    check_name=self.name,
                    severity="low",
                    message=f"Line {i} has trailing whitespace",
                    file_path=file_path,
                    line_number=i,
                    suggestion="Remove trailing whitespace",
                ))
            if line.strip().startswith("print("):
                violations.append(Violation(
                    check_name=self.name,
                    severity="low",
                    message=f"Line {i} uses print statement (consider logging)",
                    file_path=file_path,
                    line_number=i,
                    suggestion="Replace print with logging module",
                ))
        return violations
