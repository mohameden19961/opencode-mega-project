from codeguard.utils.hash import HashUtils

class TestHashUtils:
    def test_init(self):
        obj = HashUtils()
        assert obj is not None
