"""Edge case tests for config parsing."""
import pytest
from codeguard.config import load_config

class TestConfigEdgeCases:
    def test_empty_file(self, tmp_path):
        f = tmp_path / ".codeguard.yml"
        f.write_text("")
        config = load_config(str(f))
        assert config is not None

    def test_empty_sections(self, tmp_path):
        f = tmp_path / ".codeguard.yml"
        f.write_text("complexity:\nstyle:\n")
        config = load_config(str(f))
        assert config is not None
        assert config.complexity.max_cyclomatic == 10

    def test_invalid_yaml(self, tmp_path):
        f = tmp_path / ".codeguard.yml"
        f.write_text(": invalid :")
        config = load_config(str(f))
        assert config is not None

    def test_nonexistent_file(self):
        config = load_config("/nonexistent/.codeguard.yml")
        assert config is not None
