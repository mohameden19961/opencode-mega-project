import pytest
from codeguard.checks.complexity import ComplexityCheck
from codeguard.config import Config


class TestComplexityCheck:
    @pytest.fixture
    def check(self):
        return ComplexityCheck(config=Config.default())

    def test_simple_function(self, check):
        content = "def foo():\n    pass\n"
        violations = check.check("test.py", content, content.split("\n"))
        assert len(violations) == 0

    def test_complex_function(self, check):
        content = """
def foo(a, b, c, d, e, f, g):
    if a:
        if b:
            if c:
                if d:
                    if e:
                        return 1
        elif f:
            for x in range(10):
                if g:
                    return 2
    return 0
"""
        violations = check.check("test.py", content, content.split("\n"))
        complexity_violations = [v for v in violations if "cyclomatic" in v.message]
        assert len(complexity_violations) > 0
