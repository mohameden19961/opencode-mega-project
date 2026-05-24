import pytest
from codeguard.config import Config
from codeguard.fixers.whitespace import TrailingWhitespaceFixer
from codeguard.fixers.lines import LineEndingFixer

class TestTrailingWhitespaceFixer:
    def test_removes_spaces(self, tmp_path):
        f = tmp_path / "t.py"; f.write_text("x = 1   \ny = 2\n")
        r = TrailingWhitespaceFixer(Config.default()).fix(str(f), f.read_text(), f.read_text().split("\n"))
        assert r.fixed; assert "   \n" not in f.read_text()

class TestLineEndingFixer:
    def test_fix_crlf(self, tmp_path):
        f = tmp_path / "t.py"; f.write_text("x = 1\r\ny = 2\r\n")
        r = LineEndingFixer(Config.default()).fix(str(f), f.read_text(), f.read_text().split("\n"))
        assert r.fixed; assert "\r\n" not in f.read_text()
