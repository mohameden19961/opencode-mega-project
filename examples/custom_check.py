
from typing import List
from codeguard.checks.base import BaseCheck, CheckRegistry
from codeguard.core.engine import Violation
from codeguard.config import Config

class CustomNamingCheck(BaseCheck):
    name = "custom_naming"
    description = "Custom naming convention check"

    def check(self, file_path: str, content: str, lines: List[str]) -> List[Violation]:
        violations = []
        for i, line in enumerate(lines, 1):
            if "TODO" in line:
                violations.append(Violation(
                    check_name=self.name, severity="low",
                    message=f"Line {i} contains TODO",
                    file_path=file_path, line_number=i,
                    suggestion="Address TODO before committing",
                ))
        return violations

CheckRegistry.register(CustomNamingCheck)
