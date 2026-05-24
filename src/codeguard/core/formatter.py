from typing import List
from codeguard.core.engine import Violation, AnalysisResults


class ResultsFormatter:
    @staticmethod
    def format_violations(violations: List[Violation]) -> List[str]:
        formatted = []
        for v in violations:
            location = f"{v.file_path}:{v.line_number}"
            if v.column:
                location += f":{v.column}"
            msg = f"[{v.severity.upper()}] {v.check_name}: {v.message}"
            formatted.append(f"{location} - {msg}")
            if v.suggestion:
                formatted.append(f"  Suggestion: {v.suggestion}")
        return formatted

    @staticmethod
    def summary(results: AnalysisResults) -> str:
        parts = [f"Files analyzed: {results.files_analyzed}"]
        parts.append(f"Total lines: {results.total_lines}")
        parts.append(f"Duration: {results.duration:.2f}s")
        parts.append(f"Total violations: {len(results.violations)}")
        severity_counts = results.count_by_severity()
        for severity, count in severity_counts.items():
            if count > 0:
                parts.append(f"  {severity}: {count}")
        if results.errors:
            parts.append(f"Errors: {len(results.errors)}")
        return "\n".join(parts)
