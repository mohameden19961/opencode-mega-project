import pytest
from codeguard.core.collector import FileCollector
from codeguard.config import Config


class TestFileCollector:
    @pytest.fixture
    def collector(self):
        return FileCollector(config=Config.default())

    def test_collect_single_file(self, collector, sample_python_file):
        files = collector.collect([sample_python_file])
        assert len(files) == 1
        assert files[0].endswith("sample.py")

    def test_collect_directory(self, collector, tmp_path):
        (tmp_path / "a.py").write_text("x = 1")
        (tmp_path / "b.py").write_text("y = 2")
        (tmp_path / "c.txt").write_text("text")
        files = collector.collect([str(tmp_path)])
        assert len(files) == 2
        assert all(f.endswith(".py") for f in files)

    def test_collect_nonexistent_path(self, collector):
        files = collector.collect(["/nonexistent/path"])
        assert len(files) == 0
