from typing import List
from codeguard.config import Config
from codeguard.fixers.base import BaseFixer, FixResult

class LineEndingFixer(BaseFixer):
    name = "line_endings"
    def fix(self, file_path, content, lines):
        if "\r\n" not in content and "\r" not in content:
            return FixResult(file_path, False, 0, "No issues")
        new = content.replace("\r\n", "\n").replace("\r", "\n")
        changes = content.count("\r\n") + content.count("\r")
        with open(file_path, "w") as f:
            f.write(new)
        return FixResult(file_path, True, changes, f"Normalized {changes} line endings")
