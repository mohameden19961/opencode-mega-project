from codeguard.checks.duplication import DuplicationCheck
from codeguard.config import Config


class TestDuplicationCheck:
    def test_no_duplication(self):
        check = DuplicationCheck(config=Config.default())
        content = """
def foo():
    return 1

def bar():
    return 2
"""
        violations = check.check("test.py", content, content.split("\n"))
        dup_violations = [v for v in violations if "similar" in v.message]
        assert len(dup_violations) == 0
