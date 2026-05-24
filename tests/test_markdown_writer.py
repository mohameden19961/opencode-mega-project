from codeguard.output.markdown_writer import MarkdownWriter
from codeguard.core.engine import AnalysisResults, Violation


class TestMarkdownWriter:
    def test_write(self, tmp_path):
        output = tmp_path / "report.md"
        writer = MarkdownWriter(output_path=str(output))
        results = AnalysisResults(
            files_analyzed=1,
            total_lines=20,
            duration=0.3,
            violations=[
                Violation(check_name="test", severity="critical",
                          message="critical issue", file_path="a.py",
                          line_number=1),
            ],
        )
        writer.write(results)
        assert output.exists()
        content = output.read_text()
        assert "CodeGuard Analysis Report" in content
        assert "critical issue" in content
