from codeguard.checks.dependencies import DependencyCheck
from codeguard.config import Config

class TestDependencyCheck:
    def test_deprecated_module(self):
        check = DependencyCheck(config=Config.default())
        content = "import distutils\n"
        violations = check.check("test.py", content, content.split("\n"))
        assert len(violations) > 0

    def test_ok_module(self):
        check = DependencyCheck(config=Config.default())
        content = "import os\n"
        violations = check.check("test.py", content, content.split("\n"))
        assert len(violations) == 0
