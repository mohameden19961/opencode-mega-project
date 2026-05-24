from codeguard.output.xml_writer import XMLWriter
from codeguard.core.engine import AnalysisResults, Violation

class TestXMLWriter:
    def test_write(self, tmp_path):
        output = tmp_path / "report.xml"
        writer = XMLWriter(output_path=str(output))
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
