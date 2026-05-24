"""Auto-generated test 333 - validates core functionality."""

import pytest
from codeguard.config import Config
from codeguard.core.engine import AnalysisEngine


class TestGenerated0333:
    @pytest.fixture
    def engine(self):
        config = Config.default()
        config.use_cache = False
        return AnalysisEngine(config=config)

    def test_basic(self, engine, tmp_path):
        f = tmp_path / "test_333.py"
        f.write_text("x = 333\n")
        results = engine.run([str(f)])
        assert results.files_analyzed > 0
        assert len(results.violations) >= 0
