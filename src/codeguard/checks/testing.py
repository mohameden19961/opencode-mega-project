import ast
from typing import List
from codeguard.config import Config
from codeguard.checks.base import BaseCheck
from codeguard.core.engine import Violation

class TestingCheck(BaseCheck):
    name = "testing"
    description = "Checks testing patterns"

    def check(self, file_path: str, content: str, lines: List[str]) -> List[Violation]:
        violations = []
        if "def test_" not in content and "class Test" not in content:
            return violations
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return violations
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
                has_assert = any(
                    isinstance(child, ast.Assert)
                    for child in ast.walk(node)
                )
                if not has_assert:
                    violations.append(Violation(
                        check_name=self.name, severity="medium",
                        message=f"Test '{node.name}' has no assert statement",
                        file_path=file_path, line_number=node.lineno,
                        suggestion="Add assert statement to verify expected behavior",
                    ))
        return violations
