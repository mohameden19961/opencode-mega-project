import pytest
from codeguard.core.engine import AnalysisEngine, Violation, AnalysisResults
from codeguard.config import Config


class TestAnalysisEngine:
    @pytest.fixture
    def engine(self):
        config = Config.default()
        config.use_cache = False
        return AnalysisEngine(config=config)

    def test_run_empty(self, engine):
        results = engine.run([])
        assert results.files_analyzed == 0
        assert len(results.violations) == 0

    def test_run_single_file(self, engine, sample_python_file):
        results = engine.run([sample_python_file])
        assert results.files_analyzed > 0
        assert results.total_lines > 0

    def test_run_directory(self, engine, tmp_path):
        (tmp_path / "test_file.py").write_text("x = 1\n")
        results = engine.run([str(tmp_path)])
        assert results.files_analyzed > 0


class TestAnalysisResults:
    def test_get_violations_by_severity(self):
        results = AnalysisResults()
        results.violations = [
            Violation(check_name="test", severity="low", message="low", file_path="a.py"),
            Violation(check_name="test", severity="high", message="high", file_path="a.py"),
            Violation(check_name="test", severity="critical", message="critical", file_path="a.py"),
        ]
        high_violations = results.get_violations("high")
        assert len(high_violations) == 2

    def test_count_by_severity(self):
        results = AnalysisResults()
        results.violations = [
            Violation(check_name="a", severity="low", message="", file_path="a.py"),
            Violation(check_name="b", severity="low", message="", file_path="a.py"),
            Violation(check_name="c", severity="high", message="", file_path="a.py"),
        ]
        counts = results.count_by_severity()
        assert counts["low"] == 2
        assert counts["high"] == 1
