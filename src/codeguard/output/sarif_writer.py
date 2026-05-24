
import json
from typing import Optional
from codeguard.config import Config
from codeguard.core.engine import AnalysisResults

class SARIFWriter:
    def __init__(self, output_path: Optional[str] = None, config: Optional[Config] = None):
        self.output_path = output_path
        self.config = config or Config.default()

    def write(self, results: AnalysisResults):
        sarif = {
            "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
            "version": "2.1.0",
            "runs": [{
                "tool": {"driver": {"name": "CodeGuard", "version": "1.0.0"}},
                "results": [{
                    "ruleId": v.check_name,
                    "level": v.severity,
                    "message": {"text": v.message},
                    "locations": [{
                        "physicalLocation": {
                            "artifactLocation": {"uri": v.file_path},
                            "region": {"startLine": v.line_number}
                        }
                    }]
                } for v in results.violations]
            }]
        }
        output = json.dumps(sarif, indent=2)
        if self.output_path:
            with open(self.output_path, "w") as f:
                f.write(output)
        else:
            print(output)
