
import hashlib
from typing import Optional
from codeguard.config import Config

class HashUtils:
    @staticmethod
    def hash_file(path: str, algorithm: str = "sha256") -> Optional[str]:
        try:
            h = hashlib.new(algorithm)
            with open(path, "rb") as f:
                for chunk in iter(lambda: f.read(65536), b""):
                    h.update(chunk)
            return h.hexdigest()
        except Exception:
            return None

    @staticmethod
    def hash_content(content: str, algorithm: str = "sha256") -> str:
        h = hashlib.new(algorithm)
        h.update(content.encode())
        return h.hexdigest()
