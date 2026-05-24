import ast
from typing import List
from codeguard.config import Config
from codeguard.checks.base import BaseCheck
from codeguard.core.types import Violation


class TypingCheck(BaseCheck):
    name = "typing"
    description = "Checks type annotation usage"

    def check(self, file_path: str, content: str, lines: List[str]) -> List[Violation]:
        violations = []
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return violations

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if node.name.startswith("__") and node.name not in ("__init__", "__call__"):
                    continue
                has_return_annotation = node.returns is not None
                if not has_return_annotation:
                    violations.append(Violation(
                        check_name=self.name,
                        severity="low",
                        message=f"Function '{node.name}' missing return type annotation",
                        file_path=file_path,
                        line_number=node.lineno,
                        suggestion=f"Add return type annotation to '{node.name}'",
                    ))
                for arg in node.args.args:
                    if arg.arg == "self":
                        continue
                    if arg.annotation is None:
                        violations.append(Violation(
                            check_name=self.name,
                            severity="low",
                            message=f"Parameter '{arg.arg}' in '{node.name}' missing type annotation",
                            file_path=file_path,
                            line_number=node.lineno,
                            suggestion=f"Add type annotation for parameter '{arg.arg}'",
                        ))

        return violations
