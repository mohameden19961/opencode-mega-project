from codeguard.checks.api_design import APIDesignCheck
from codeguard.config import Config

class TestAPIDesignCheck:
    def test_getter_without_property(self):
        check = APIDesignCheck(config=Config.default())
        content = "class A:\n    def get_value(self):\n        return 1\n"
        violations = check.check("test.py", content, content.split("\n"))
        assert len(violations) > 0
