
import os
import sys
from codeguard import analyze
from codeguard.config import Config

def main():
    config = Config.default()
    config.severity_threshold = os.environ.get("CODEGUARD_SEVERITY", "high")
    paths = os.environ.get("CODEGUARD_PATHS", "src/").split(",")
    config.checks_enabled = os.environ.get("CODEGUARD_CHECKS", "").split(",") if os.environ.get("CODEGUARD_CHECKS") else config.checks_enabled
    results = analyze(paths, config=config)
    violations = results.get_violations(config.severity_threshold)
    if violations:
        print(f"::warning::Found {len(violations)} violations")
        for v in violations:
            print(f"::warning file={v.file_path},line={v.line_number}::{v.message}")
        sys.exit(1)
    print(f"::notice::No violations found in {results.files_analyzed} files")

if __name__ == "__main__":
    main()
