import pytest
from codeguard.core.scanner import IncrementalScanner
from codeguard.config import Config

class TestIncrementalScanner:
    @pytest.fixture
    def scanner(self, tmp_path):
        cfg = Config.default()
        cfg.cache_dir = str(tmp_path / ".cache")
        return IncrementalScanner(config=cfg)

    def test_first_run(self, scanner, tmp_path):
        (tmp_path / "t.py").write_text("x=1\n")
        changed = scanner.get_changed_files([str(tmp_path)])
        assert len(changed) > 0

    def test_no_changes(self, scanner, tmp_path):
        (tmp_path / "t.py").write_text("x=1\n")
        scanner.get_changed_files([str(tmp_path)])
        changed = scanner.get_changed_files([str(tmp_path)])
        assert len(changed) == 0

    def test_modified(self, scanner, tmp_path):
        f = tmp_path / "t.py"
        f.write_text("x=1\n")
        scanner.get_changed_files([str(tmp_path)])
        f.write_text("x=2\n")
        changed = scanner.get_changed_files([str(tmp_path)])
        assert len(changed) > 0
