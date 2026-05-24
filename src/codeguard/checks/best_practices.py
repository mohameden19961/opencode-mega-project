import ast
from typing import List
from codeguard.config import Config
from codeguard.checks.base import BaseCheck
from codeguard.core.engine import Violation

class BestPracticesCheck(BaseCheck):
    name = "best_practices"
    description = "Checks general best practices"

    def check(self, file_path: str, content: str, lines: List[str]) -> List[Violation]:
        violations = []
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return violations
        for node in ast.walk(tree):
            if isinstance(node, ast.Global):
                violations.append(Violation(
                    check_name=self.name, severity="low",
                    message="Use of global variables",
                    file_path=file_path, line_number=node.lineno,
                    suggestion="Avoid global variables, use function parameters or classes",
                ))
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    if node.func.attr == "sort" and isinstance(node.func.value, ast.List):
                        violations.append(Violation(
                            check_name=self.name, severity="low",
                            message="list.sort() modifies in-place",
                            file_path=file_path, line_number=node.lineno,
                            suggestion="Use sorted() for immutable behavior",
                        ))
        if len(lines) > 1000:
            violations.append(Violation(
                check_name=self.name, severity="low",
                message=f"File has {len(lines)} lines",
                file_path=file_path, line_number=1,
                suggestion="Consider splitting into smaller modules",
            ))
        return violations
