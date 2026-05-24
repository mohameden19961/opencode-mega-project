import pytest
from codeguard.checks.security import SecurityCheck
from codeguard.config import Config

class TestSecurityEdgeCase16:
    @pytest.fixture
    def check(self):
        return SecurityCheck(config=Config.default())

    def test_edge_case(self, check):
        content = ""
        violations = check.check("test.py", content, content.split("\n"))
        assert isinstance(violations, list)
