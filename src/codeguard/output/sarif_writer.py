"""SARIF 2.1.0 output writer for GitHub Code Scanning."""
import json
from typing import Optional
from codeguard.config import Config
from codeguard.core.engine import AnalysisResults

class SARIFWriter:
    def __init__(self, output_path=None, config=None):
        self.output_path = output_path
        self.config = config or Config.default()

    def write(self, results):
        rules = {}
        items = []
        for v in results.violations:
            rid = v.check_name
            if rid not in rules:
                rules[rid] = {"id": rid, "name": rid,
                    "shortDescription": {"text": v.message},
                    "properties": {"severity": v.severity}}
            items.append({
                "ruleId": rid,
                "level": "error" if v.severity == "critical" else "warning",
                "message": {"text": v.message},
                "locations": [{"physicalLocation": {
                    "artifactLocation": {"uri": v.file_path},
                    "region": {"startLine": v.line_number}}}]})
        sarif = {"$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
            "version": "2.1.0",
            "runs": [{"tool": {"driver": {"name": "CodeGuard", "version": "0.1.0",
                "rules": list(rules.values())}}, "results": items}]}
        out = json.dumps(sarif, indent=2)
        if self.output_path:
            with open(self.output_path, "w") as f:
                f.write(out)
