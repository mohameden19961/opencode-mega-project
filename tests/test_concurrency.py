from codeguard.checks.concurrency import ConcurrencyCheck
from codeguard.config import Config

class TestConcurrencyCheck:
    def test_concurrency_detection(self):
        check = ConcurrencyCheck(config=Config.default())
        content = "import threading\nx = 1\n"
        violations = check.check("test.py", content, content.split("\n"))
        assert len(violations) > 0
