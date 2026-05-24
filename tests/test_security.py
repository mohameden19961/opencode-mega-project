from codeguard.checks.security import SecurityCheck
from codeguard.config import Config


class TestSecurityCheck:
    def test_dangerous_function_detection(self):
        check = SecurityCheck(config=Config.default())
        content = """
import os
os.system("ls -la")
result = eval("1 + 1")
exec("print('hello')")
"""
        violations = check.check("test.py", content, content.split("\n"))
        dangerous = [v for v in violations if "dangerous function" in v.message]
        assert len(dangerous) >= 1

    def test_sql_injection_detection(self):
        check = SecurityCheck(config=Config.default())
        content = """
def query(conn, user):
    sql = f"SELECT * FROM users WHERE id = {user}"
    conn.execute(sql)
"""
        violations = check.check("test.py", content, content.split("\n"))
        sql_violations = [v for v in violations if "SQL injection" in v.message]
        assert len(sql_violations) > 0

    def test_clean_code(self):
        check = SecurityCheck(config=Config.default())
        content = """
def greet(name):
    return f"Hello, {name}!"

def add(a, b):
    return a + b
"""
        violations = check.check("test.py", content, content.split("\n"))
        assert len(violations) == 0
