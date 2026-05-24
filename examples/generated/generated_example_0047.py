"""Generated example 47 - demonstrates CodeGuard features."""

from codeguard import analyze
from codeguard.config import Config


def example_0047():
    """Run analysis with specific configuration."""
    config = Config.default()
    config.severity_threshold = "medium"
    config.max_workers = 8
    results = analyze(["src/"], config=config)
    print(f"Example 47: {len(results.violations)} violations found")
    return results


if __name__ == "__main__":
    result = example_0047()
    print(f"Files analyzed: {result.files_analyzed}")
