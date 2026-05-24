from codeguard.checks.testing import TestingCheck
from codeguard.config import Config

class TestTestingCheck:
    def test_test_without_assert(self):
        check = TestingCheck(config=Config.default())
        content = "def test_something():\n    pass\n"
        violations = check.check("test.py", content, content.split("\n"))
        assert len(violations) > 0

    def test_test_with_assert(self):
        check = TestingCheck(config=Config.default())
        content = "def test_something():\n    assert True\n"
        violations = check.check("test.py", content, content.split("\n"))
        assert len(violations) == 0
