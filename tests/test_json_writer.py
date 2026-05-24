import json
from codeguard.output.json_writer import JSONWriter
from codeguard.core.engine import AnalysisResults, Violation


class TestJSONWriter:
    def test_write(self, tmp_path):
        output = tmp_path / "report.json"
        writer = JSONWriter(output_path=str(output))
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
        data = json.loads(output.read_text())
        assert data["summary"]["files_analyzed"] == 1
        assert len(data["violations"]) == 1
