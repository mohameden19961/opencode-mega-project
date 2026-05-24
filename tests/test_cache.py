import pytest
from codeguard.utils.cache import AnalysisCache


class TestAnalysisCache:
    @pytest.fixture
    def cache(self, tmp_path):
        return AnalysisCache(cache_dir=str(tmp_path / ".cache"))

    def test_set_and_get(self, cache):
        cache.set("test_key", 12345, [{"msg": "test"}])
        result = cache.get("test_key")
        assert result is not None
        assert result["hash"] == 12345
        assert result["violations"] == [{"msg": "test"}]

    def test_get_nonexistent(self, cache):
        result = cache.get("nonexistent")
        assert result is None

    def test_clear(self, cache):
        cache.set("key1", 1, [])
        cache.set("key2", 2, [])
        cache.clear()
        assert cache.get("key1") is None
        assert cache.get("key2") is None
