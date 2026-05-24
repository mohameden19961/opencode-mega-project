from codeguard.checks.maintainability import MaintainabilityCheck
from codeguard.config import Config

class TestMaintainabilityCheck:
    def test_low_documentation(self):
        check = MaintainabilityCheck(config=Config.default())
        content = "x = 1\n" * 200
        violations = check.check("test.py", content, content.split("\n"))
        doc_v = [v for v in violations if "documentation" in v.message]
        assert len(doc_v) > 0
