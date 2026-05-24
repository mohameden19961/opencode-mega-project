import pytest
from codeguard.checks.naming import NamingCheck
from codeguard.config import Config

class TestNamingEdgeCase18:
    @pytest.fixture
    def check(self):
        return NamingCheck(config=Config.default())

    def test_edge_case(self, check):
        content = ""
        violations = check.check("test.py", content, content.split("\n"))
        assert isinstance(violations, list)
