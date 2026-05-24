import ast
from typing import List
from codeguard.config import Config
from codeguard.checks.base import BaseCheck
from codeguard.core.engine import Violation

class DependencyCheck(BaseCheck):
    name = "dependencies"
    description = "Checks dependency patterns"

    DEPRECATED_MODULES = {
        "distutils", "imp", "formatter", "optparse",
        "audiodev", "sgmllib", "timeline",
    }

    def check(self, file_path: str, content: str, lines: List[str]) -> List[Violation]:
        violations = []
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return violations
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.split(".")[0] in self.DEPRECATED_MODULES:
                        violations.append(Violation(
                            check_name=self.name, severity="medium",
                            message=f"Import of deprecated module '{alias.name}'",
                            file_path=file_path, line_number=node.lineno,
                            suggestion=f"Replace '{alias.name}' with its modern alternative",
                        ))
            elif isinstance(node, ast.ImportFrom):
                if node.module and node.module.split(".")[0] in self.DEPRECATED_MODULES:
                    violations.append(Violation(
                        check_name=self.name, severity="medium",
                        message=f"Import from deprecated module '{node.module}'",
                        file_path=file_path, line_number=node.lineno,
                        suggestion=f"Replace '{node.module}' with its modern alternative",
                    ))
        return violations
