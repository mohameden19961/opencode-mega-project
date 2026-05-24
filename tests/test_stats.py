from codeguard.utils.stats import StatsUtils

class TestStatsUtils:
    def test_init(self):
        obj = StatsUtils()
        assert obj is not None
