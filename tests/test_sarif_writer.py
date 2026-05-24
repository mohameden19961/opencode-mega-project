import json
from codeguard.output.sarif_writer import SARIFWriter
from codeguard.core.engine import AnalysisResults, Violation

class TestSARIFWriter:
    def test_write(self, tmp_path):
        out = tmp_path / "results.sarif"
        SARIFWriter(output_path=str(out)).write(AnalysisResults(
            files_analyzed=1, total_lines=5, duration=0.1,
            violations=[Violation(check_name="test", severity="high",
                message="msg", file_path="a.py", line_number=3)]))
        assert out.exists()
        data = json.loads(out.read_text())
        assert data["version"] == "2.1.0"
        assert len(data["runs"][0]["results"]) == 1
