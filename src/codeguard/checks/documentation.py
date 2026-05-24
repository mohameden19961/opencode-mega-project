import ast
from typing import List
from codeguard.config import Config
from codeguard.checks.base import BaseCheck
from codeguard.core.engine import Violation


class DocumentationCheck(BaseCheck):
    name = "documentation"
    description = "Checks documentation coverage"

    def __init__(self, config: Config):
        super().__init__(config)
        self.require_docstrings = config.documentation.require_docstrings
        self.min_length = config.documentation.min_docstring_length
        self.check_public = config.documentation.check_public_api

    def check(self, file_path: str, content: str, lines: List[str]) -> List[Violation]:
        violations = []
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return violations

        if isinstance(tree, ast.Module):
            if self.require_docstrings and not ast.get_docstring(tree):
                violations.append(Violation(
                    check_name=self.name,
                    severity="medium",
                    message="Module missing docstring",
                    file_path=file_path,
                    line_number=1,
                    suggestion="Add a module-level docstring describing the module's purpose",
                ))

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                if self.require_docstrings and not ast.get_docstring(node):
                    if self.check_public and node.name.startswith("_"):
                        continue
                    violations.append(Violation(
                        check_name=self.name,
                        severity="low" if node.name.startswith("_") else "medium",
                        message=f"{type(node).__name__[:-3]} '{node.name}' missing docstring",
                        file_path=file_path,
                        line_number=node.lineno,
                        suggestion=f"Add a docstring to {type(node).__name__[:-3].lower()} '{node.name}'",
                    ))
                else:
                    docstring = ast.get_docstring(node) or ""
                    if len(docstring.strip()) < self.min_length:
                        violations.append(Violation(
                            check_name=self.name,
                            severity="low",
                            message=f"Docstring for '{node.name}' is too short ({len(docstring.strip())} chars, min: {self.min_length})",
                            file_path=file_path,
                            line_number=node.lineno,
                            suggestion="Expand the docstring to include more details",
                        ))

        return violations
