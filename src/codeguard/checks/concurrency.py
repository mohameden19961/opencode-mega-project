import ast
from typing import List
from codeguard.config import Config
from codeguard.checks.base import BaseCheck
from codeguard.core.engine import Violation

class ConcurrencyCheck(BaseCheck):
    name = "concurrency"
    description = "Checks concurrency patterns"

    def check(self, file_path: str, content: str, lines: List[str]) -> List[Violation]:
        violations = []
        if "threading" in content or "multiprocessing" in content or "asyncio" in content:
            violations.append(Violation(
                check_name=self.name, severity="low",
                message="Concurrency usage detected",
                file_path=file_path, line_number=1,
                suggestion="Ensure proper synchronization and avoid shared state",
            ))
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return violations
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    if node.func.attr == "sleep" and "thread" in content.lower():
                        violations.append(Violation(
                            check_name=self.name, severity="medium",
                            message="time.sleep() in threaded context",
                            file_path=file_path, line_number=node.lineno,
                            suggestion="Use threading.Event() instead of sleep",
                        ))
        return violations
