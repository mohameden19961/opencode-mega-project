import ast
import re
from typing import List
from codeguard.config import Config
from codeguard.checks.base import BaseCheck
from codeguard.core.types import Violation


class NamingCheck(BaseCheck):
    name = "naming"
    description = "Checks naming conventions"

    PATTERNS = {
        "module": re.compile(r"^[a-z][a-z0-9_]*$"),
        "class": re.compile(r"^[A-Z][a-zA-Z0-9]*$"),
        "function": re.compile(r"^[a-z][a-z0-9_]*$"),
        "variable": re.compile(r"^[a-z][a-z0-9_]*$"),
        "constant": re.compile(r"^[A-Z][A-Z0-9_]*$"),
        "parameter": re.compile(r"^[a-z][a-z0-9_]*$"),
    }

    RESERVED = {"i", "j", "k", "l", "x", "y", "z", "foo", "bar", "baz", "tmp", "temp", "data", "result"}

    def check(self, file_path: str, content: str, lines: List[str]) -> List[Violation]:
        violations = []
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return violations

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                if not self.PATTERNS["class"].match(node.name):
                    violations.append(Violation(
                        check_name=self.name,
                        severity="medium",
                        message=f"Class '{node.name}' should use PascalCase",
                        file_path=file_path,
                        line_number=node.lineno,
                        suggestion=f"Rename '{node.name}' to match PascalCase convention",
                    ))

            elif isinstance(node, ast.FunctionDef):
                if not self.PATTERNS["function"].match(node.name):
                    violations.append(Violation(
                        check_name=self.name,
                        severity="medium",
                        message=f"Function '{node.name}' should use snake_case",
                        file_path=file_path,
                        line_number=node.lineno,
                        suggestion=f"Rename '{node.name}' to match snake_case convention",
                    ))

            elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
                if node.id.isupper() and len(node.id) > 2:
                    continue
                if not self.PATTERNS["variable"].match(node.id) and not node.id.startswith("_"):
                    violations.append(Violation(
                        check_name=self.name,
                        severity="low",
                        message=f"Variable '{node.id}' should use snake_case",
                        file_path=file_path,
                        line_number=node.lineno,
                        suggestion=f"Rename '{node.id}' to snake_case",
                    ))

        return violations
