import sys
from codeguard import analyze
from codeguard.config import Config

config = Config.default()
config.severity_threshold = "high"

results = analyze(["src/", "tests/"], config=config)

violations = results.get_violations("high")
if violations:
    print(f"Found {len(violations)} high-severity violations!")
    for v in violations:
        print(f"  {v.file_path}:{v.line_number} - {v.message}")
    sys.exit(1)
else:
    print(f"All clear! {results.files_analyzed} files analyzed.")
    sys.exit(0)
