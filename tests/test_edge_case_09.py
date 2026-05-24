import pytest
from codeguard.checks.documentation import DocumentationCheck
from codeguard.config import Config

class TestDocumentationEdgeCase09:
    @pytest.fixture
    def check(self):
        return DocumentationCheck(config=Config.default())

    def test_edge_case(self, check):
        content = ""
        violations = check.check("test.py", content, content.split("\n"))
        assert isinstance(violations, list)
