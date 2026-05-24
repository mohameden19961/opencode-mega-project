"""Example 00 - demonstrates CodeGuard usage pattern 0."""

from codeguard import analyze
from codeguard.config import Config


def run_analysis():
    config = Config.default()
    config.severity_threshold = "medium" if 0 % 2 == 0 else "high"
    results = analyze(["src/"], config=config)
    print(f"Found {len(results.violations)} violations")
    return results


if __name__ == "__main__":
    run_analysis()
