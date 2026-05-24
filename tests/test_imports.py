from codeguard.checks.imports import ImportCheck
from codeguard.config import Config


class TestImportCheck:
    def test_empty_file(self):
        check = ImportCheck(config=Config.default())
        violations = check.check("test.py", "", [""])
        assert len(violations) == 0
