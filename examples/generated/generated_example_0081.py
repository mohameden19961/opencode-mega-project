"""Generated example 81 - demonstrates CodeGuard features."""

from codeguard import analyze
from codeguard.config import Config


def example_0081():
    """Run analysis with specific configuration."""
    config = Config.default()
    config.severity_threshold = "medium"
    config.max_workers = 2
    results = analyze(["src/"], config=config)
    print(f"Example 81: {len(results.violations)} violations found")
    return results


if __name__ == "__main__":
    result = example_0081()
    print(f"Files analyzed: {result.files_analyzed}")
