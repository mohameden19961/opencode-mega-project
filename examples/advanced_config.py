
from codeguard import analyze
from codeguard.config import Config

config = Config.default()
config.checks_enabled = ["security", "complexity", "duplication"]
config.severity_threshold = "high"
config.complexity.max_cyclomatic = 8
config.use_cache = False
config.max_workers = 2

results = analyze(["/path/to/project"], config=config)
print(f"Found {len(results.violations)} violations")
for v in results.get_violations("high"):
    print(f"  [{v.severity}] {v.check_name}: {v.message}")
