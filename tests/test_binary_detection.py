import pytest
from codeguard.core.collector import FileCollector
from codeguard.config import Config

class TestBinaryDetection:
    @pytest.fixture
    def collector(self):
        return FileCollector(config=Config.default())

    def test_binary_detected(self, collector, tmp_path):
        f = tmp_path / "test.exe"
        f.write_bytes(bytes([0x7f, 0x45, 0x4c, 0x46, 0x00, 0x00]))
        assert collector.is_binary(str(f)) is True

    def test_text_not_binary(self, collector, tmp_path):
        f = tmp_path / "test.py"
        f.write_text("print('hello')")
        assert collector.is_binary(str(f)) is False

    def test_binary_skipped(self, collector, tmp_path):
        (tmp_path / "code.py").write_text("x=1")
        (tmp_path / "data.bin").write_bytes(bytes([0x89, 0x50, 0x4e, 0x47]))
        files = collector.collect([str(tmp_path)])
        assert len(files) == 1
