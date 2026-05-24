from typing import List
from codeguard.config import Config
from codeguard.fixers.base import BaseFixer, FixResult

class TrailingWhitespaceFixer(BaseFixer):
    name = "trailing_whitespace"
    def fix(self, file_path, content, lines):
        fixed = []; changes = 0
        for line in lines:
            s = line.rstrip()
            if line != s:
                fixed.append(s + "\n"); changes += 1
            else:
                fixed.append(line)
        if changes > 0:
            with open(file_path, "w") as f:
                f.writelines(fixed)
        return FixResult(file_path, changes > 0, changes, f"Removed {changes} trailing whitespace")
