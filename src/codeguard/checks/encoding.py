import os
from typing import List
from codeguard.config import Config
from codeguard.checks.base import BaseCheck
from codeguard.core.engine import Violation

class EncodingCheck(BaseCheck):
    name = "encoding"
    description = "Checks file encoding and character usage"

    def __init__(self, config: Config):
        super().__init__(config)

    def check(self, file_path: str, content: str, lines: List[str]) -> List[Violation]:
        violations = []
        try:
            content.encode("ascii")
        except UnicodeEncodeError:
            violations.append(Violation(
                check_name=self.name, severity="low",
                message="File contains non-ASCII characters",
                file_path=file_path, line_number=1,
                suggestion="Consider using ASCII-compatible encoding",
            ))
        for i, line in enumerate(lines, 1):
            if len(line) > 0 and line[-1] == "\r":
                violations.append(Violation(
                    check_name=self.name, severity="low",
                    message=f"Line {i} uses CRLF line endings",
                    file_path=file_path, line_number=i,
                    suggestion="Use LF line endings instead",
                ))
            if "\t" in line:
                violations.append(Violation(
                    check_name=self.name, severity="low",
                    message=f"Line {i} contains tab characters",
                    file_path=file_path, line_number=i,
                    suggestion="Use spaces instead of tabs",
                ))
        return violations
