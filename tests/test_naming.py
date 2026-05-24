from codeguard.checks.naming import NamingCheck
from codeguard.config import Config


class TestNamingCheck:
    def test_bad_class_name(self):
        check = NamingCheck(config=Config.default())
        content = "class bad_class_name:\n    pass\n"
        violations = check.check("test.py", content, content.split("\n"))
        class_violations = [v for v in violations if "Class" in v.message]
        assert len(class_violations) > 0

    def test_bad_function_name(self):
        check = NamingCheck(config=Config.default())
        content = "def BadFunctionName():\n    pass\n"
        violations = check.check("test.py", content, content.split("\n"))
        func_violations = [v for v in violations if "Function" in v.message]
        assert len(func_violations) > 0

    def test_good_names(self):
        check = NamingCheck(config=Config.default())
        content = """
class MyClass:
    def my_method(self):
        pass

def my_function():
    pass
"""
        violations = check.check("test.py", content, content.split("\n"))
        assert len(violations) == 0
