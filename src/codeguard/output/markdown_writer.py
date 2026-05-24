from typing import Optional
from codeguard.config import Config
from codeguard.core.engine import AnalysisResults


class MarkdownWriter:
    def __init__(self, output_path: Optional[str] = None, config: Optional[Config] = None):
        self.output_path = output_path
        self.config = config or Config.default()

    def write(self, results: AnalysisResults):
        lines = []
        lines.append("# CodeGuard Analysis Report")
        lines.append("")
        lines.append("## Summary")
        lines.append("")
        lines.append(f"- **Files analyzed**: {results.files_analyzed}")
        lines.append(f"- **Total lines**: {results.total_lines}")
        lines.append(f"- **Duration**: {results.duration:.2f}s")
        lines.append(f"- **Total violations**: {len(results.violations)}")
        lines.append("")
        severity_counts = results.count_by_severity()
        if any(severity_counts.values()):
            lines.append("## Severity Breakdown")
            lines.append("")
            for severity, count in severity_counts.items():
                if count > 0:
                    lines.append(f"- **{severity.capitalize()}**: {count}")
            lines.append("")
        if results.violations:
            lines.append("## Violations")
            lines.append("")
            lines.append("| Severity | Check | Message | Location | Suggestion |")
            lines.append("|----------|-------|---------|----------|------------|")
            for v in results.violations:
                location = f"{v.file_path}:{v.line_number}"
                suggestion = v.suggestion or ""
                lines.append(f"| {v.severity.upper()} | {v.check_name} | {v.message} | {location} | {suggestion} |")
        output = "\n".join(lines)
        if self.output_path:
            with open(self.output_path, "w") as f:
                f.write(output)
        else:
            print(output)
