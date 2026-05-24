"""Generated example 84 - demonstrates CodeGuard features."""

from codeguard import analyze
from codeguard.config import Config


def example_0084():
    """Run analysis with specific configuration."""
    config = Config.default()
    config.severity_threshold = "medium"
    config.max_workers = 5
    results = analyze(["src/"], config=config)
    print(f"Example 84: {len(results.violations)} violations found")
    return results


if __name__ == "__main__":
    result = example_0084()
    print(f"Files analyzed: {result.files_analyzed}")
