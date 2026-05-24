import pytest
from codeguard.core.reporter import ReportGenerator
from codeguard.config import Config


class TestReportGenerator:
    @pytest.fixture
    def generator(self):
        return ReportGenerator(config=Config.default())

    def test_generate_html(self, generator, tmp_path):
        writer = generator.generate("html", str(tmp_path))
        assert writer is not None
        assert (tmp_path / "report.html").exists()
