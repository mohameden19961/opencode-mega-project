import ast
from typing import List, Dict, Tuple
from codeguard.config import Config
from codeguard.checks.base import BaseCheck
from codeguard.core.types import Violation


class DuplicationCheck(BaseCheck):
    name = "duplication"
    description = "Detects code duplication"

    MIN_SIMILARITY_LINES = 5

    def check(self, file_path: str, content: str, lines: List[str]) -> List[Violation]:
        violations = []
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return violations

        functions = []
        classes = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                body_lines = self._get_body_lines(node)
                functions.append((node.name, body_lines, node.lineno))
            elif isinstance(node, ast.ClassDef):
                classes.append((node.name, node.lineno))

        for i, (name1, body1, lineno1) in enumerate(functions):
            for j, (name2, body2, lineno2) in enumerate(functions):
                if i >= j:
                    continue
                similarity = self._calculate_similarity(body1, body2)
                if similarity >= 0.8 and len(body1) >= self.MIN_SIMILARITY_LINES:
                    violations.append(Violation(
                        check_name=self.name,
                        severity="medium",
                        message=f"Function '{name1}' is {similarity:.0%} similar to '{name2}'",
                        file_path=file_path,
                        line_number=lineno1,
                        suggestion=f"Consider merging '{name1}' and '{name2}' into a shared function",
                    ))

        return violations

    def _get_body_lines(self, node: ast.FunctionDef) -> List[str]:
        lines = []
        for child in ast.walk(node):
            if isinstance(child, (ast.Expr, ast.Assign, ast.Return,
                                  ast.If, ast.For, ast.While, ast.Call)):
                lines.append(type(child).__name__)
        return lines

    def _calculate_similarity(self, lines1: List[str], lines2: List[str]) -> float:
        if not lines1 or not lines2:
            return 0.0
        shorter = set(lines1) if len(lines1) < len(lines2) else set(lines2)
        longer = set(lines2) if len(lines1) < len(lines2) else set(lines1)
        if not longer:
            return 0.0
        intersection = shorter.intersection(longer)
        return len(intersection) / len(longer)
