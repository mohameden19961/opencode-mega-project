"""Example plugin demonstrating the CodeGuard plugin system."""
from typing import List
from codeguard.checks.base import BaseCheck
from codeguard.core.engine import Violation
from codeguard.config import Config

class TodoCheck(BaseCheck):
    name = "todo_check"
    description = "Warns about TODO/FIXME comments"

    def check(self, file_path: str, content: str, lines: List[str]) -> List[Violation]:
        violations = []
        for i, line in enumerate(lines, 1):
            if "TODO" in line:
                violations.append(Violation(
                    check_name=self.name, severity="low",
                    message=f"Line {i} contains TODO comment",
                    file_path=file_path, line_number=i,
                    suggestion="Address TODO before committing",
                ))
            if "FIXME" in line:
                violations.append(Violation(
                    check_name=self.name, severity="medium",
                    message=f"Line {i} contains FIXME comment",
                    file_path=file_path, line_number=i,
                    suggestion="Fix the issue before committing",
                ))
        return violations
