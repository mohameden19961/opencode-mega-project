import json
from typing import Optional
from codeguard.config import Config
from codeguard.core.engine import AnalysisResults


class JSONWriter:
    def __init__(self, output_path: Optional[str] = None, config: Optional[Config] = None):
        self.output_path = output_path
        self.config = config or Config.default()

    def write(self, results: AnalysisResults):
        data = {
            "summary": {
                "files_analyzed": results.files_analyzed,
                "total_lines": results.total_lines,
                "duration_seconds": results.duration,
                "total_violations": len(results.violations),
                "errors": len(results.errors),
            },
            "severity_counts": results.count_by_severity(),
            "check_counts": results.count_by_check(),
            "violations": [
                {
                    "check": v.check_name,
                    "severity": v.severity,
                    "message": v.message,
                    "file": v.file_path,
                    "line": v.line_number,
                    "column": v.column,
                    "suggestion": v.suggestion,
                }
                for v in results.violations
            ],
            "errors": results.errors,
        }
        output = json.dumps(data, indent=2, ensure_ascii=False)
        if self.output_path:
            with open(self.output_path, "w") as f:
                f.write(output)
        else:
            print(output)
