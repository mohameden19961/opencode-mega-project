from codeguard.checks.encoding import EncodingCheck
from codeguard.config import Config

class TestEncodingCheck:
    def test_ascii_file(self):
        check = EncodingCheck(config=Config.default())
        content = "print('hello')\n"
        violations = check.check("test.py", content, content.split("\n"))
        ascii_v = [v for v in violations if "non-ASCII" in v.message]
        assert len(ascii_v) == 0

    def test_non_ascii(self):
        check = EncodingCheck(config=Config.default())
        content = "print('héllo')\n"
        violations = check.check("test.py", content, content.split("\n"))
        ascii_v = [v for v in violations if "non-ASCII" in v.message]
        assert len(ascii_v) > 0
