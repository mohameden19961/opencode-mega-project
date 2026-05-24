from codeguard.utils.network import NetworkUtils

class TestNetworkUtils:
    def test_init(self):
        obj = NetworkUtils()
        assert obj is not None
