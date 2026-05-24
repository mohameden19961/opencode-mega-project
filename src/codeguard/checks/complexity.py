import ast
from typing import List
from codeguard.config import Config
from codeguard.checks.base import BaseCheck
from codeguard.core.engine import Violation


class ComplexityCheck(BaseCheck):
    name = "complexity"
    description = "Checks code complexity metrics"

    def __init__(self, config: Config):
        super().__init__(config)
        self.max_cyclomatic = config.complexity.max_cyclomatic
        self.max_cognitive = config.complexity.max_cognitive
        self.max_nesting = config.complexity.max_nesting
        self.max_lines = config.complexity.max_lines_per_function
        self.max_params = config.complexity.max_parameters

    def check(self, file_path: str, content: str, lines: List[str]) -> List[Violation]:
        violations = []
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return violations
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                violations.extend(self._check_function(node, file_path))
        return violations

    def _check_function(self, node: ast.FunctionDef, file_path: str) -> List[Violation]:
        violations = []
        cyclomatic = self._calculate_cyclomatic(node)
        if cyclomatic > self.max_cyclomatic:
            violations.append(Violation(
                check_name=self.name,
                severity="high" if cyclomatic > self.max_cyclomatic * 1.5 else "medium",
                message=f"Function '{node.name}' has cyclomatic complexity {cyclomatic} (max: {self.max_cyclomatic})",
                file_path=file_path,
                line_number=node.lineno,
                suggestion=f"Consider breaking '{node.name}' into smaller functions",
            ))

        nesting = self._calculate_nesting_depth(node)
        if nesting > self.max_nesting:
            violations.append(Violation(
                check_name=self.name,
                severity="medium",
                message=f"Function '{node.name}' has nesting depth {nesting} (max: {self.max_nesting})",
                file_path=file_path,
                line_number=node.lineno,
                suggestion="Consider reducing nested control structures",
            ))

        param_count = len(node.args.args)
        if param_count > self.max_params:
            violations.append(Violation(
                check_name=self.name,
                severity="low",
                message=f"Function '{node.name}' has {param_count} parameters (max: {self.max_params})",
                file_path=file_path,
                line_number=node.lineno,
                suggestion="Consider using a data class or *args/**kwargs",
            ))

        return violations

    def _calculate_cyclomatic(self, node: ast.AST) -> int:
        complexity = 1
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.Assert)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
            elif isinstance(child, (ast.ExceptHandler, ast.With)):
                complexity += 1
            elif isinstance(child, ast.comprehension):
                complexity += 1
        return complexity

    def _calculate_nesting_depth(self, node: ast.AST) -> int:
        max_depth = 0
        current_depth = 0
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.With, ast.Try)):
                current_depth += 1
                max_depth = max(max_depth, current_depth)
        return max_depth
