import os
import subprocess
from typing import List, Optional


class GitUtils:
    @staticmethod
    def get_repo_root(path: str = ".") -> Optional[str]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--show-toplevel"],
                capture_output=True, text=True, cwd=path, timeout=10,
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        return None

    @staticmethod
    def get_tracked_files(path: str = ".") -> List[str]:
        try:
            result = subprocess.run(
                ["git", "ls-files"],
                capture_output=True, text=True, cwd=path, timeout=10,
            )
            if result.returncode == 0:
                return result.stdout.strip().split("\n") if result.stdout.strip() else []
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        return []

    @staticmethod
    def get_modified_files(path: str = ".") -> List[str]:
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only"],
                capture_output=True, text=True, cwd=path, timeout=10,
            )
            if result.returncode == 0:
                return result.stdout.strip().split("\n") if result.stdout.strip() else []
        except Exception:
            pass
        return []

    @staticmethod
    def get_untracked_files(path: str = ".") -> List[str]:
        try:
            result = subprocess.run(
                ["git", "ls-files", "--others", "--exclude-standard"],
                capture_output=True, text=True, cwd=path, timeout=10,
            )
            if result.returncode == 0:
                return result.stdout.strip().split("\n") if result.stdout.strip() else []
        except Exception:
            pass
        return []
