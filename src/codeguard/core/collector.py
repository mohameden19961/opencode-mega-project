import os
import fnmatch
from typing import List
from codeguard.config import Config


class FileCollector:
    SUPPORTED_EXTENSIONS = {".py", ".pyx", ".pyw"}

    def __init__(self, config: Config):
        self.config = config

    def collect(self, paths: List[str]) -> List[str]:
        files = []
        for path in paths:
            if os.path.isfile(path):
                if self._is_supported(path) and not self._is_excluded(path):
                    files.append(os.path.abspath(path))
            elif os.path.isdir(path):
                files.extend(self._walk_directory(path))
            else:
                continue
        return sorted(set(files))

    def _walk_directory(self, directory: str) -> List[str]:
        files = []
        for root, dirs, filenames in os.walk(directory):
            dirs[:] = [d for d in dirs if not self._is_excluded(os.path.join(root, d))]
            for filename in filenames:
                filepath = os.path.join(root, filename)
                if self._is_supported(filepath) and not self._is_excluded(filepath):
                    files.append(filepath)
        return files

    def _is_supported(self, filepath: str) -> bool:
        ext = os.path.splitext(filepath)[1]
        return ext in self.SUPPORTED_EXTENSIONS

    def _is_excluded(self, filepath: str) -> bool:
        for pattern in self.config.exclude_patterns:
            if fnmatch.fnmatch(filepath, pattern):
                return True
            if fnmatch.fnmatch(os.path.basename(filepath), pattern):
                return True
        return False
