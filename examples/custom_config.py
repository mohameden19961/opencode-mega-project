from codeguard.config import Config
from codeguard import analyze

config = Config.default()
config.checks_enabled = ["security", "complexity"]
config.severity_threshold = "high"
config.complexity.max_cyclomatic = 8
config.use_cache = False

results = analyze(["my_project/"], config=config)

for violation in results.get_violations("high"):
    print(f"{violation.file_path}:{violation.line_number}")
    print(f"  [{violation.severity}] {violation.check_name}: {violation.message}")
    if violation.suggestion:
        print(f"  Suggestion: {violation.suggestion}")
    print()
