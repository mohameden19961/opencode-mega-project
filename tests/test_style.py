from codeguard.checks.style import StyleCheck
from codeguard.config import Config


class TestStyleCheck:
    def test_line_length(self):
        config = Config.default()
        config.style.max_line_length = 20
        check = StyleCheck(config=config)
        content = "x" * 30 + "\n"
        violations = check.check("test.py", content, content.split("\n"))
        line_violations = [v for v in violations if "exceeds" in v.message]
        assert len(line_violations) > 0

    def test_trailing_whitespace(self):
        config = Config.default()
        config.style.trailing_whitespace = True
        check = StyleCheck(config=config)
        content = "line_with_space   \n"
        violations = check.check("test.py", content, content.split("\n"))
        trailing = [v for v in violations if "trailing" in v.message]
        assert len(trailing) > 0

    def test_clean_code(self):
        check = StyleCheck(config=Config.default())
        content = "def foo():\n    pass\n"
        violations = check.check("test.py", content, content.split("\n"))
        assert len(violations) == 0
