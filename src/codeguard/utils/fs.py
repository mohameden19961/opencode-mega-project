import os
import hashlib
from typing import List


class FileSystemUtils:
    @staticmethod
    def read_file(path: str) -> str:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    @staticmethod
    def write_file(path: str, content: str):
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

    @staticmethod
    def file_hash(path: str) -> str:
        hasher = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                hasher.update(chunk)
        return hasher.hexdigest()

    @staticmethod
    def get_file_size(path: str) -> int:
        return os.path.getsize(path)

    @staticmethod
    def list_files(directory: str, pattern: str = "*.py") -> List[str]:
        import glob
        return sorted(glob.glob(os.path.join(directory, "**", pattern), recursive=True))

    @staticmethod
    def ensure_directory(path: str):
        os.makedirs(path, exist_ok=True)
