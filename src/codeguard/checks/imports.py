import ast
from typing import List
from codeguard.config import Config
from codeguard.checks.base import BaseCheck
from codeguard.core.engine import Violation


class ImportCheck(BaseCheck):
    name = "imports"
    description = "Checks import organization"

    STD_LIBS = {
        "os", "sys", "re", "json", "math", "time", "datetime",
        "collections", "itertools", "functools", "pathlib",
        "typing", "abc", "copy", "random", "hashlib",
        "subprocess", "tempfile", "shutil", "glob", "fnmatch",
        "argparse", "logging", "warnings", "dataclasses",
        "enum", "io", "textwrap", "string", "decimal",
        "fractions", "statistics", "uuid", "pprint",
        "configparser", "fileinput", "linecache", "pickle",
        "shelve", "marshal", "dbm", "sqlite3",
    }

    THIRD_PARTY_PREFIXES = {"flask", "django", "numpy", "pandas",
                            "requests", "click", "yaml", "rich",
                            "jinja2", "pytest", "mypy", "black",
                            "ruff", "pre_commit"}

    def check(self, file_path: str, content: str, lines: List[str]) -> List[Violation]:
        violations = []
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return violations

        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append((node.lineno, "import", alias.name))
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for alias in node.names:
                    imports.append((node.lineno, "from", module, alias.name))

        std_imports = []
        third_imports = []
        local_imports = []

        for imp in imports:
            if imp[1] == "import":
                name = imp[2]
                top_level = name.split(".")[0]
                if top_level in self.STD_LIBS:
                    std_imports.append(imp)
                elif any(name.startswith(p) for p in self.THIRD_PARTY_PREFIXES):
                    third_imports.append(imp)
                else:
                    local_imports.append(imp)
            elif imp[1] == "from":
                module = imp[2]
                top_level = module.split(".")[0] if module else ""
                if top_level in self.STD_LIBS:
                    std_imports.append(imp)
                elif any(module.startswith(p) for p in self.THIRD_PARTY_PREFIXES):
                    third_imports.append(imp)
                else:
                    local_imports.append(imp)

        return violations
