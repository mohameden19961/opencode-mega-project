import ast
from typing import List
from codeguard.config import Config
from codeguard.checks.base import BaseCheck
from codeguard.core.engine import Violation


class PerformanceCheck(BaseCheck):
    name = "performance"
    description = "Checks for performance issues"

    def __init__(self, config: Config):
        super().__init__(config)
        self.max_complexity = config.performance.max_complexity
        self.check_nested = config.performance.check_nested_loops
        self.check_alloc = config.performance.check_large_allocations
        self.check_imports = config.performance.check_slow_imports

    def check(self, file_path: str, content: str, lines: List[str]) -> List[Violation]:
        violations = []
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return violations

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if self.check_nested:
                    violations.extend(self._check_nested_loops(node, file_path))
                if self.check_alloc:
                    violations.extend(self._check_large_allocations(node, file_path))

        if self.check_imports:
            violations.extend(self._check_import_performance(tree, file_path))

        return violations

    def _check_nested_loops(self, node: ast.FunctionDef, file_path: str) -> List[Violation]:
        violations = []
        for child in ast.walk(node):
            if isinstance(child, (ast.For, ast.While)):
                for nested in ast.walk(child):
                    if nested is not child and isinstance(nested, (ast.For, ast.While)):
                        violations.append(Violation(
                            check_name=self.name,
                            severity="medium",
                            message=f"Nested loop detected in '{node.name}'",
                            file_path=file_path,
                            line_number=nested.lineno,
                            suggestion="Consider flattening the loop or using itertools.product",
                        ))
                        break
        return violations

    def _check_large_allocations(self, node: ast.FunctionDef, file_path: str) -> List[Violation]:
        violations = []
        for child in ast.walk(node):
            if isinstance(child, ast.ListComp):
                if isinstance(child.elt, (ast.List, ast.Dict, ast.Set)):
                    violations.append(Violation(
                        check_name=self.name,
                        severity="low",
                        message=f"Large list comprehension in '{node.name}' may cause memory issues",
                        file_path=file_path,
                        line_number=child.lineno,
                        suggestion="Consider using a generator expression instead",
                    ))
        return violations

    def _check_import_performance(self, tree: ast.AST, file_path: str) -> List[Violation]:
        violations = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                if node.module and node.module.startswith(("matplotlib", "pandas", "numpy", "tensorflow", "torch", "sklearn")):
                    violations.append(Violation(
                        check_name=self.name,
                        severity="low",
                        message=f"Slow import '{node.module}' detected at module level",
                        file_path=file_path,
                        line_number=node.lineno,
                        suggestion="Consider lazy imports inside functions",
                    ))
        return violations
