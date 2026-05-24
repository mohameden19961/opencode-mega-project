import pytest
from codeguard.config import Config
from codeguard.core.engine import AnalysisEngine

class TestIntegration20:
    @pytest.fixture
    def engine(self):
        config = Config.default()
        config.use_cache = False
        return AnalysisEngine(config=config)

    def test_integration(self, engine, tmp_path):
        f = tmp_path / "test_20.py"
        f.write_text("x = 20\n")
        results = engine.run([str(f)])
        assert results.files_analyzed > 0
