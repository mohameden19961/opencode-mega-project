import pytest
from codeguard.checks.style import StyleCheck
from codeguard.config import Config

class TestStyleEdgeCase17:
    @pytest.fixture
    def check(self):
        return StyleCheck(config=Config.default())

    def test_edge_case(self, check):
        content = ""
        violations = check.check("test.py", content, content.split("\n"))
        assert isinstance(violations, list)
