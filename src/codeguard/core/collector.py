import os
import fnmatch
from typing import List
from codeguard.config import Config


class FileCollector:
    SUPPORTED_EXTENSIONS = {".py", ".pyx", ".pyw", ".pyi"}
    SUPPORTED_FILENAMES = {
        "sshd_config", "ssh_config", "authorized_keys", "known_hosts",
        "id_rsa", "id_ed25519", "id_ecdsa", "id_dsa",
    }
    BINARY_SIGNATURES = [
        bytes([0x7f, 0x45, 0x4c, 0x46]),
        bytes([0x89, 0x50, 0x4e, 0x47]),
        bytes([0xff, 0xd8, 0xff]),
        bytes([0x25, 0x50, 0x44, 0x46]),
        bytes([0x1f, 0x8b]),
        bytes([0x50, 0x4b]),
    ]

    @staticmethod
    def is_binary(filepath):
        try:
            with open(filepath, "rb") as f:
                header = f.read(4)
                if not header:
                    return False
                for sig in FileCollector.BINARY_SIGNATURES:
                    if header.startswith(sig):
                        return True
                return b"\x00" in f.read(8192)
        except IOError:
            return False

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
                if self._is_supported(filepath) and not self._is_excluded(filepath) and not self.is_binary(filepath):
                    files.append(filepath)
        return files

    def _is_supported(self, filepath: str) -> bool:
        ext = os.path.splitext(filepath)[1]
        if ext in self.SUPPORTED_EXTENSIONS:
            return True
        basename = os.path.basename(filepath)
        return basename in self.SUPPORTED_FILENAMES

    def _is_excluded(self, filepath: str) -> bool:
        for pattern in self.config.exclude_patterns:
            if fnmatch.fnmatch(filepath, pattern):
                return True
            if fnmatch.fnmatch(os.path.basename(filepath), pattern):
                return True
        return False
