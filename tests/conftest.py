import pytest
from codeguard.config import Config


@pytest.fixture
def default_config():
    return Config.default()


@pytest.fixture
def sample_python_file(tmp_path):
    content = """
def hello(name):
    print(f"Hello, {name}!")
    return True


class MyClass:
    def method_one(self):
        pass
"""
    path = tmp_path / "sample.py"
    path.write_text(content)
    return str(path)


@pytest.fixture
def complex_python_file(tmp_path):
    content = """
import os
import sys


def complex_function(a, b, c, d, e, f, g):
    if a > 0:
        if b > 0:
            if c > 0:
                if d > 0:
                    print("deep nesting")
                    return True
    return False


class TestClass:
    def method_a(self):
        pass

    def method_b(self):
        pass
"""
    path = tmp_path / "complex.py"
    path.write_text(content)
    return str(path)


@pytest.fixture
def unsafe_python_file(tmp_path):
    content = """
import os

def run_command(cmd):
    os.system(cmd)


def load_data(data):
    result = eval(data)
    return result


def query_db(conn, sql):
    return conn.execute(f"SELECT * FROM users WHERE id = {sql}")
"""
    path = tmp_path / "unsafe.py"
    path.write_text(content)
    return str(path)
