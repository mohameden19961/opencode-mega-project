from typing import Optional, List
from codeguard.config import Config
from codeguard.core.engine import AnalysisResults, Violation
from codeguard.core.formatter import ResultsFormatter


class TerminalWriter:
    def __init__(self, output_path: Optional[str] = None, config: Optional[Config] = None):
        self.output_path = output_path
        self.config = config or Config.default()

    def write(self, results: AnalysisResults):
        lines = []
        lines.append("=" * 60)
        lines.append("CodeGuard Analysis Report")
        lines.append("=" * 60)
        lines.append("")
        lines.append(ResultsFormatter.summary(results))
        lines.append("")
        if results.violations:
            lines.append("-" * 60)
            lines.append("Violations:")
            lines.append("-" * 60)
            for v in results.violations:
                severity_tag = self._severity_color(v.severity)
                location = f"{v.file_path}:{v.line_number}"
                lines.append(f"  [{severity_tag}] {v.check_name}: {v.message}")
                lines.append(f"    at {location}")
                if v.suggestion:
                    lines.append(f"    -> {v.suggestion}")
                lines.append("")
        output = "\n".join(lines)
        if self.output_path:
            with open(self.output_path, "w") as f:
                f.write(output)
        else:
            print(output)

    def write_violations(self, violations: List[Violation]):
        for v in violations:
            severity_tag = self._severity_color(v.severity)
            print(f"[{severity_tag}] {v.file_path}:{v.line_number} - {v.message}")

    def _severity_color(self, severity: str) -> str:
        colors = {
            "critical": "CRIT",
            "high": "HIGH",
            "medium": "MED",
            "low": "LOW",
        }
        return colors.get(severity, severity.upper())
