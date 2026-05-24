import os
import json
import hashlib
from typing import Optional, Any, Dict
from codeguard.exceptions import CacheError


class AnalysisCache:
    def __init__(self, cache_dir: str = ".codeguard_cache"):
        self.cache_dir = cache_dir

    def get(self, key: str) -> Optional[Dict]:
        cache_key = self._hash_key(key)
        cache_path = os.path.join(self.cache_dir, cache_key)
        if os.path.exists(cache_path):
            try:
                with open(cache_path) as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return None
        return None

    def set(self, key: str, file_hash: int, violations: list):
        cache_key = self._hash_key(key)
        os.makedirs(self.cache_dir, exist_ok=True)
        cache_path = os.path.join(self.cache_dir, cache_key)
        try:
            with open(cache_path, "w") as f:
                json.dump({"hash": file_hash, "violations": violations}, f)
        except IOError as e:
            raise CacheError(f"Failed to write cache: {e}")

    def invalidate(self, key: str):
        cache_key = self._hash_key(key)
        cache_path = os.path.join(self.cache_dir, cache_key)
        if os.path.exists(cache_path):
            os.remove(cache_path)

    def clear(self):
        if os.path.exists(self.cache_dir):
            for filename in os.listdir(self.cache_dir):
                filepath = os.path.join(self.cache_dir, filename)
                if os.path.isfile(filepath):
                    os.remove(filepath)

    def _hash_key(self, key: str) -> str:
        return hashlib.sha256(key.encode()).hexdigest()[:16]
