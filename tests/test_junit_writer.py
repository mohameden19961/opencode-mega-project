from codeguard.output.junit_writer import JUNITWriter
from codeguard.core.engine import AnalysisResults, Violation

class TestJUNITWriter:
    def test_write(self, tmp_path):
        output = tmp_path / "report.junit"
        writer = JUNITWriter(output_path=str(output))
        results = AnalysisResults(
            files_analyzed=1,
            total_lines=10,
            duration=0.5,
            violations=[
                Violation(check_name="test", severity="high",
                          message="test violation", file_path="a.py",
                          line_number=5),
            ],
        )
        writer.write(results)
        assert output.exists()
        content = output.read_text()
        assert "test" in content.lower() or "violation" in content
