import os
import json
import hashlib
from typing import Optional, Any, Dict
from codeguard.exceptions import CacheError


import time
from collections import OrderedDict

class AnalysisCache:
    def __init__(self, cache_dir: str = ".codeguard_cache", max_size: int = 1000):
        self.cache_dir = cache_dir
        self.max_size = max_size
        self._memory_cache = OrderedDict()
        self._access_times = {}

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

    def _evict_if_needed(self):
        if len(self._memory_cache) >= self.max_size:
            oldest = next(iter(self._memory_cache))
            del self._memory_cache[oldest]

    def set(self, key: str, file_hash: int, violations: list):
        cache_key = self._hash_key(key)
        self._evict_if_needed()
        self._memory_cache[cache_key] = {"hash": file_hash, "violations": violations}
        self._access_times[cache_key] = time.time()
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

    def clear_memory(self):
        self._memory_cache.clear()
        self._access_times.clear()

    def get_stats(self) -> dict:
        return {"memory_entries": len(self._memory_cache), "max_size": self.max_size,
            "disk_entries": len(os.listdir(self.cache_dir)) if os.path.exists(self.cache_dir) else 0}

    def clear(self):
        if os.path.exists(self.cache_dir):
            for filename in os.listdir(self.cache_dir):
                filepath = os.path.join(self.cache_dir, filename)
                if os.path.isfile(filepath):
                    os.remove(filepath)

    def _hash_key(self, key: str) -> str:
        return hashlib.sha256(key.encode()).hexdigest()[:16]
