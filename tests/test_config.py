import pytest
import yaml
from codeguard.config import Config, load_config


class TestConfig:
    def test_default_config(self):
        config = Config.default()
        assert config.verbose is False
        assert config.use_cache is True
        assert config.severity_threshold == "low"
        assert len(config.checks_enabled) == 9
        assert config.max_workers == 4

    def test_from_dict(self):
        data = {
            "verbose": True,
            "use_cache": False,
            "severity_threshold": "high",
            "max_workers": 8,
            "complexity": {"max_cyclomatic": 15},
            "style": {"max_line_length": 120},
        }
        config = Config.from_dict(data)
        assert config.verbose is True
        assert config.use_cache is False
        assert config.severity_threshold == "high"
        assert config.max_workers == 8
        assert config.complexity.max_cyclomatic == 15
        assert config.style.max_line_length == 120

    def test_save_and_load(self, tmp_path):
        config_path = tmp_path / ".codeguard.yml"
        config = Config.default()
        config.severity_threshold = "critical"
        config.save(str(config_path))
        assert config_path.exists()
        loaded = load_config(str(config_path))
        assert loaded.severity_threshold == "critical"
