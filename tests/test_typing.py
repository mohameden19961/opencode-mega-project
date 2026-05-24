from codeguard.checks.typing import TypingCheck
from codeguard.config import Config


class TestTypingCheck:
    def test_missing_return_annotation(self):
        check = TypingCheck(config=Config.default())
        content = "def foo():\n    return 1\n"
        violations = check.check("test.py", content, content.split("\n"))
        return_violations = [v for v in violations if "return type" in v.message]
        assert len(return_violations) > 0

    def test_missing_param_annotation(self):
        check = TypingCheck(config=Config.default())
        content = "def foo(x):\n    return x\n"
        violations = check.check("test.py", content, content.split("\n"))
        param_violations = [v for v in violations if "Parameter" in v.message]
        assert len(param_violations) > 0

    def good_annotations(self):
        check = TypingCheck(config=Config.default())
        content = "def foo(x: int) -> int:\n    return x\n"
        violations = check.check("test.py", content, content.split("\n"))
        assert len(violations) == 0
