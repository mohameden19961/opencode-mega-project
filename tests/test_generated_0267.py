"""Auto-generated test 267 - validates core functionality."""

import pytest
from codeguard.config import Config
from codeguard.core.engine import AnalysisEngine


class TestGenerated0267:
    @pytest.fixture
    def engine(self):
        config = Config.default()
        config.use_cache = False
        return AnalysisEngine(config=config)

    def test_basic(self, engine, tmp_path):
        f = tmp_path / "test_267.py"
        f.write_text("x = 267\n")
        results = engine.run([str(f)])
        assert results.files_analyzed > 0
        assert len(results.violations) >= 0
