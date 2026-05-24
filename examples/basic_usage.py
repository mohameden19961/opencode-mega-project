from codeguard import analyze
from codeguard.config import Config

config = Config.default()
config.style.max_line_length = 120
config.severity_threshold = "medium"

results = analyze(["src/"], config=config)

print(f"Files analyzed: {results.files_analyzed}")
print(f"Violations found: {len(results.violations)}")
print(f"Duration: {results.duration:.2f}s")

severity_counts = results.count_by_severity()
for severity, count in severity_counts.items():
    if count:
        print(f"  {severity}: {count}")
