import re
import ast
from typing import List
from codeguard.config import Config
from codeguard.checks.base import BaseCheck
from codeguard.core.types import Violation


class SecurityCheck(BaseCheck):
    name = "security"
    description = "Checks for security vulnerabilities"

    SQL_INJECTION_PATTERNS = [
        r"execute\([\"'].*?%.*?[\"']\s*%",
        r"execute\([\"'].*?\{.*?\}[\"']\.format",
        r"execute\(f[\"']",
    ]

    def __init__(self, config: Config):
        super().__init__(config)
        self.dangerous_functions = config.security.dangerous_functions
        self.check_sql = config.security.check_sql_injection
        self.check_path = config.security.check_path_traversal
        self.check_cmd = config.security.check_command_injection

    def check(self, file_path: str, content: str, lines: List[str]) -> List[Violation]:
        violations = []
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return violations

        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func_name = self._get_func_name(node)
                if func_name in self.dangerous_functions:
                    violations.append(Violation(
                        check_name=self.name,
                        severity="high",
                        message=f"Use of potentially dangerous function '{func_name}'",
                        file_path=file_path,
                        line_number=node.lineno,
                        suggestion=f"Consider safer alternatives to '{func_name}'",
                    ))

        if self.check_sql:
            for i, line in enumerate(lines, 1):
                for pattern in self.SQL_INJECTION_PATTERNS:
                    if re.search(pattern, line):
                        violations.append(Violation(
                            check_name=self.name,
                            severity="critical",
                            message="Potential SQL injection vulnerability detected",
                            file_path=file_path,
                            line_number=i,
                            suggestion="Use parameterized queries with placeholders",
                        ))

        if self.check_path:
            for i, line in enumerate(lines, 1):
                if "open(" in line and "../" in line:
                    violations.append(Violation(
                        check_name=self.name,
                        severity="high",
                        message="Potential path traversal detected",
                        file_path=file_path,
                        line_number=i,
                        suggestion="Sanitize file paths and use allowlists",
                    ))

        if self.check_cmd:
            for i, line in enumerate(lines, 1):
                if re.search(r"(os\.system|subprocess\.(call|Popen|run))\(", line):
                    if "%" in line or "f'" in line or 'f"' in line:
                        violations.append(Violation(
                            check_name=self.name,
                            severity="critical",
                            message="Potential command injection vulnerability",
                            file_path=file_path,
                            line_number=i,
                            suggestion="Use subprocess with list arguments instead of shell=True",
                        ))

        return violations

    def _get_func_name(self, node: ast.Call) -> str:
        if isinstance(node.func, ast.Attribute):
            return f"{self._get_attr_base(node.func)}.{node.func.attr}"
        elif isinstance(node.func, ast.Name):
            return node.func.id
        return ""

    def _get_attr_base(self, node: ast.Attribute) -> str:
        if isinstance(node.value, ast.Name):
            return node.value.id
        elif isinstance(node.value, ast.Attribute):
            return f"{self._get_attr_base(node.value)}.{node.value.attr}"
        return ""
