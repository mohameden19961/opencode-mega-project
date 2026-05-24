
import csv
import io
from typing import Optional
from codeguard.config import Config
from codeguard.core.engine import AnalysisResults

class CSVWriter:
    def __init__(self, output_path: Optional[str] = None, config: Optional[Config] = None):
        self.output_path = output_path
        self.config = config or Config.default()

    def write(self, results: AnalysisResults):
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["severity", "check", "message", "file", "line", "suggestion"])
        for v in results.violations:
            writer.writerow([v.severity, v.check_name, v.message, v.file_path, v.line_number, v.suggestion or ""])
        result = output.getvalue()
        if self.output_path:
            with open(self.output_path, "w") as f:
                f.write(result)
        else:
            print(result)
