from codeguard.checks.logging import LoggingCheck
from codeguard.config import Config

class TestLoggingCheck:
    def test_print_with_logging(self):
        check = LoggingCheck(config=Config.default())
        content = "import logging\nprint('hello')\n"
        violations = check.check("test.py", content, content.split("\n"))
        assert len(violations) > 0
