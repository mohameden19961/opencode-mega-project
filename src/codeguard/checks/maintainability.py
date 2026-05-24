import ast
from typing import List
from codeguard.config import Config
from codeguard.checks.base import BaseCheck
from codeguard.core.types import Violation

class MaintainabilityCheck(BaseCheck):
    name = "maintainability"
    description = "Checks maintainability index"

    def check(self, file_path: str, content: str, lines: List[str]) -> List[Violation]:
        violations = []
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return violations
        func_count = 0
        class_count = 0
        total_lines = len(lines)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_count += 1
            elif isinstance(node, ast.ClassDef):
                class_count += 1
        comment_lines = sum(1 for l in lines if l.strip().startswith("#"))
        docstring_lines = 0
        for node in ast.walk(tree):
            doc = ast.get_docstring(node)
            if doc:
                docstring_lines += len(doc.split("\n"))
        if total_lines > 0:
            comment_ratio = (comment_lines + docstring_lines) / total_lines
            if comment_ratio < 0.05 and total_lines > 100:
                violations.append(Violation(
                    check_name=self.name, severity="medium",
                    message=f"Low documentation ratio ({comment_ratio:.1%})",
                    file_path=file_path, line_number=1,
                    suggestion="Add more comments and docstrings",
                ))
        return violations
