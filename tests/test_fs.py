import pytest
from codeguard.utils.fs import FileSystemUtils


class TestFileSystemUtils:
    def test_read_write_file(self, tmp_path):
        filepath = tmp_path / "test.txt"
        FileSystemUtils.write_file(str(filepath), "hello world")
        content = FileSystemUtils.read_file(str(filepath))
        assert content == "hello world"

    def test_file_hash(self, tmp_path):
        filepath = tmp_path / "test.txt"
        FileSystemUtils.write_file(str(filepath), "content")
        h = FileSystemUtils.file_hash(str(filepath))
        assert len(h) == 64
