from codeguard.checks.documentation import DocumentationCheck
from codeguard.config import Config


class TestDocumentationCheck:
    def test_missing_module_docstring(self):
        check = DocumentationCheck(config=Config.default())
        content = "x = 1\n"
        violations = check.check("test.py", content, content.split("\n"))
        module_violations = [v for v in violations if "Module missing" in v.message]
        assert len(module_violations) > 0

    def test_missing_function_docstring(self):
        check = DocumentationCheck(config=Config.default())
        content = "def foo():\n    pass\n"
        violations = check.check("test.py", content, content.split("\n"))
        func_violations = [v for v in violations if "missing docstring" in v.message]
        assert len(func_violations) > 0

    def test_good_documentation(self):
        check = DocumentationCheck(config=Config.default())
        content = '"""Module docstring."""\n\ndef foo():\n    """Function docstring."""\n    pass\n'
        violations = check.check("test.py", content, content.split("\n"))
        assert len(violations) == 0
