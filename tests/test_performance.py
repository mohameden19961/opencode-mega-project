from codeguard.checks.performance import PerformanceCheck
from codeguard.config import Config


class TestPerformanceCheck:
    def test_nested_loop_detection(self):
        check = PerformanceCheck(config=Config.default())
        content = """
def process():
    for i in range(10):
        for j in range(10):
            print(i, j)
"""
        violations = check.check("test.py", content, content.split("\n"))
        nested = [v for v in violations if "Nested loop" in v.message]
        assert len(nested) > 0

    def test_slow_import_detection(self):
        check = PerformanceCheck(config=Config.default())
        content = """
import pandas as pd
import numpy as np

def process():
    pass
"""
        violations = check.check("test.py", content, content.split("\n"))
        slow_imports = [v for v in violations if "Slow import" in v.message]
        assert len(slow_imports) > 0
