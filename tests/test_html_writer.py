from codeguard.output.html_writer import HTMLWriter
from codeguard.core.engine import AnalysisResults, Violation


class TestHTMLWriter:
    def test_write(self, tmp_path):
        output = tmp_path / "report.html"
        writer = HTMLWriter(output_path=str(output))
        results = AnalysisResults(
            files_analyzed=2,
            total_lines=50,
            duration=1.0,
            violations=[
                Violation(check_name="test", severity="low",
                          message="test msg", file_path="a.py",
                          line_number=3, suggestion="fix it"),
            ],
        )
        writer.write(results)
        assert output.exists()
        content = output.read_text()
        assert "<h1>CodeGuard Analysis Report</h1>" in content
        assert "test msg" in content
