import ast
from typing import List
from codeguard.config import Config
from codeguard.checks.base import BaseCheck
from codeguard.core.types import Violation

class APIDesignCheck(BaseCheck):
    name = "api_design"
    description = "Checks API design patterns"

    def check(self, file_path: str, content: str, lines: List[str]) -> List[Violation]:
        violations = []
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return violations
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if node.name.startswith("get_") or node.name.startswith("set_"):
                    for decorator in node.decorator_list:
                        if isinstance(decorator, ast.Name) and decorator.id == "property":
                            break
                    else:
                        if len(node.args.args) > 1:
                            violations.append(Violation(
                                check_name=self.name, severity="low",
                                message=f"Function '{node.name}' looks like a getter/setter",
                                file_path=file_path, line_number=node.lineno,
                                suggestion="Consider using @property decorator",
                            ))
        return violations
