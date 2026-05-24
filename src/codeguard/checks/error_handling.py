import ast
from typing import List
from codeguard.config import Config
from codeguard.checks.base import BaseCheck
from codeguard.core.types import Violation

class ErrorHandlingCheck(BaseCheck):
    name = "error_handling"
    description = "Checks error handling patterns"

    BARE_EXCEPT_MSG = "Bare except clause detected"
    PASS_IN_EXCEPT_MSG = "Empty except clause with pass"

    def check(self, file_path: str, content: str, lines: List[str]) -> List[Violation]:
        violations = []
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return violations
        for node in ast.walk(tree):
            if isinstance(node, ast.Try):
                for handler in node.handlers:
                    if handler.type is None:
                        violations.append(Violation(
                            check_name=self.name, severity="medium",
                            message=self.BARE_EXCEPT_MSG,
                            file_path=file_path, line_number=handler.lineno,
                            suggestion="Specify exception type(s) to catch",
                        ))
                    if (isinstance(handler.body, list) and len(handler.body) == 1
                            and isinstance(handler.body[0], ast.Pass)):
                        violations.append(Violation(
                            check_name=self.name, severity="medium",
                            message=self.PASS_IN_EXCEPT_MSG,
                            file_path=file_path, line_number=handler.lineno,
                            suggestion="Handle or log the exception properly",
                        ))
        return violations
