import ast
from typing import List
from codeguard.config import Config
from codeguard.checks.base import BaseCheck
from codeguard.core.types import Violation

class LoggingCheck(BaseCheck):
    name = "logging"
    description = "Checks logging best practices"

    def check(self, file_path: str, content: str, lines: List[str]) -> List[Violation]:
        violations = []
        has_logger = "logging" in content or "import logging" in content
        has_print = False
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith("print("):
                has_print = True
                if has_logger:
                    violations.append(Violation(
                        check_name=self.name, severity="low",
                        message=f"Line {i} uses print() but logging is imported",
                        file_path=file_path, line_number=i,
                        suggestion="Use logging.debug/info/warning/error instead",
                    ))
            if "logging." in stripped and "f-string" in content:
                violations.append(Violation(
                    check_name=self.name, severity="low",
                    message=f"Line {i} uses logging with potential f-string",
                    file_path=file_path, line_number=i,
                    suggestion="Use %-formatting with logging for lazy evaluation",
                ))
        return violations
