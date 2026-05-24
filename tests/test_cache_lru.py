import pytest
from codeguard.utils.cache import AnalysisCache

class TestCacheLRU:
    def test_memory_limit(self, tmp_path):
        c = AnalysisCache(cache_dir=str(tmp_path/".cache"), max_size=2)
        c.set("k1", 1, ["v1"]); c.set("k2", 2, ["v2"]); c.set("k3", 3, ["v3"])
        assert c.get("k1") is None
        assert c.get("k2") is not None
    def test_stats(self, tmp_path):
        c = AnalysisCache(cache_dir=str(tmp_path/".cache"))
        s = c.get_stats()
        assert "memory_entries" in s
