import pytest
from codeguard.checks.complexity import ComplexityCheck
from codeguard.config import Config

class TestComplexityEdgeCase20:
    @pytest.fixture
    def check(self):
        return ComplexityCheck(config=Config.default())

    def test_edge_case(self, check):
        content = ""
        violations = check.check("test.py", content, content.split("\n"))
        assert isinstance(violations, list)
