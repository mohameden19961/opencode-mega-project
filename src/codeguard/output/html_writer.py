from typing import Optional
from codeguard.config import Config
from codeguard.core.engine import AnalysisResults


class HTMLWriter:
    def __init__(self, output_path: Optional[str] = None, config: Optional[Config] = None):
        self.output_path = output_path
        self.config = config or Config.default()

    def write(self, results: AnalysisResults):
        rows = ""
        for v in results.violations:
            rows += f"""
            <tr>
                <td><span class="severity-{v.severity}">{v.severity.upper()}</span></td>
                <td>{v.check_name}</td>
                <td>{v.message}</td>
                <td>{v.file_path}:{v.line_number}</td>
                <td>{v.suggestion or ''}</td>
            </tr>"""
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>CodeGuard Report</title>
    <style>
        body {{ font-family: sans-serif; margin: 2em; }}
        h1 {{ color: #333; }}
        .summary {{ background: #f5f5f5; padding: 1em; border-radius: 4px; }}
        table {{ border-collapse: collapse; width: 100%; margin-top: 1em; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background: #4CAF50; color: white; }}
        .severity-critical {{ color: #d32f2f; font-weight: bold; }}
        .severity-high {{ color: #f44336; }}
        .severity-medium {{ color: #ff9800; }}
        .severity-low {{ color: #4caf50; }}
    </style>
</head>
<body>
    <h1>CodeGuard Analysis Report</h1>
    <div class="summary">
        <p>Files analyzed: {results.files_analyzed}</p>
        <p>Total lines: {results.total_lines}</p>
        <p>Duration: {results.duration:.2f}s</p>
        <p>Total violations: {len(results.violations)}</p>
    </div>
    <table>
        <thead>
            <tr>
                <th>Severity</th>
                <th>Check</th>
                <th>Message</th>
                <th>Location</th>
                <th>Suggestion</th>
            </tr>
        </thead>
        <tbody>{rows}
        </tbody>
    </table>
</body>
</html>"""
        if self.output_path:
            with open(self.output_path, "w") as f:
                f.write(html)
        else:
            print(html)
