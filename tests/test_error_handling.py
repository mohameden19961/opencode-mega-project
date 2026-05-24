from codeguard.checks.error_handling import ErrorHandlingCheck
from codeguard.config import Config

class TestErrorHandlingCheck:
    def test_bare_except(self):
        check = ErrorHandlingCheck(config=Config.default())
        content = "try:\n    x = 1\nexcept:\n    pass\n"
        violations = check.check("test.py", content, content.split("\n"))
        bare = [v for v in violations if "Bare except" in v.message]
        assert len(bare) > 0

    def test_good_except(self):
        check = ErrorHandlingCheck(config=Config.default())
        content = "try:\n    x = 1\nexcept ValueError:\n    pass\n"
        violations = check.check("test.py", content, content.split("\n"))
        assert len(violations) == 0
