
import subprocess
import sys
from codeguard import analyze
from codeguard.config import Config

def main():
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
        capture_output=True, text=True
    )
    files = [f for f in result.stdout.strip().split("\n") if f.endswith(".py")]
    if not files:
        sys.exit(0)
    config = Config.default()
    config.severity_threshold = "medium"
    results = analyze(files, config=config)
    violations = results.get_violations("medium")
    if violations:
        for v in violations:
            print(f"{v.file_path}:{v.line_number}: {v.message}")
        sys.exit(1)
    sys.exit(0)

if __name__ == "__main__":
    main()
