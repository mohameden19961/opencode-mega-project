from codeguard.checks.best_practices import BestPracticesCheck
from codeguard.config import Config

class TestBestPracticesCheck:
    def test_global_detection(self):
        check = BestPracticesCheck(config=Config.default())
        content = "global x\nx = 1\n"
        violations = check.check("test.py", content, content.split("\n"))
        assert len(violations) > 0
