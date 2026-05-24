"""Interactive HTML dashboard with charts."""
from typing import Optional
from codeguard.config import Config
from codeguard.core.engine import AnalysisResults

class DashboardWriter:
    def __init__(self, output_path=None, config=None):
        self.output_path = output_path
        self.config = config or Config.default()

    def write(self, results):
        sev = results.count_by_severity()
        checks = results.count_by_check()
        violations_rows = "".join(
            f"<tr><td>{v.severity}</td><td>{v.check_name}</td><td>{v.message}</td>"
            f"<td>{v.file_path}:{v.line_number}</td></tr>"
            for v in results.violations[:20]
        )
        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"><title>CodeGuard Dashboard</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
body {{ font-family: sans-serif; margin: 2em; background: #f5f5f5; }}
.card {{ background: white; border-radius: 8px; padding: 1.5em; margin: 1em 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1em; }}
.stat {{ text-align: center; }}
.stat-value {{ font-size: 2em; font-weight: bold; color: #333; }}
.stat-label {{ color: #666; font-size: 0.9em; }}
.chart-container {{ position: relative; height: 300px; }}
table {{ width: 100%; border-collapse: collapse; }}
th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
th {{ background: #4CAF50; color: white; }}
</style>
</head>
<body>
<h1>CodeGuard Analysis Dashboard</h1>
<div class="grid">
  <div class="card stat"><div class="stat-value">{results.files_analyzed}</div><div class="stat-label">Files</div></div>
  <div class="card stat"><div class="stat-value">{len(results.violations)}</div><div class="stat-label">Violations</div></div>
  <div class="card stat"><div class="stat-value">{results.total_lines}</div><div class="stat-label">Lines</div></div>
  <div class="card stat"><div class="stat-value">{results.duration:.2f}s</div><div class="stat-label">Duration</div></div>
</div>
<div class="grid">
  <div class="card"><h3>Severity</h3><div class="chart-container"><canvas id="sevChart"></canvas></div></div>
  <div class="card"><h3>Checks</h3><div class="chart-container"><canvas id="checkChart"></canvas></div></div>
</div>
<div class="card"><h3>Violations</h3><table><tr><th>Severity</th><th>Check</th><th>Message</th><th>Location</th></tr>{violations_rows}</table></div>
<script>
new Chart(document.getElementById('sevChart'), {{
  type: 'pie',
  data: {{ labels: {list(sev.keys())!r}, datasets: [{{ data: {list(sev.values())!r},
    backgroundColor: ['#4caf50','#ff9800','#f44336','#d32f2f'] }}] }}
}});
new Chart(document.getElementById('checkChart'), {{
  type: 'bar',
  data: {{ labels: {list(checks.keys())!r}, datasets: [{{ data: {list(checks.values())!r},
    backgroundColor: '#2196f3' }}] }},
  options: {{ scales: {{ y: {{ beginAtZero: true }} }} }}
}});
</script></body></html>'''
        if self.output_path:
            with open(self.output_path, "w") as f:
                f.write(html)
