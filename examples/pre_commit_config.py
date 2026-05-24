
from codeguard import analyze
from codeguard.config import Config

def run_pre_commit():
    import subprocess
    result = subprocess.run(["git", "diff", "--cached", "--name-only"],
                          capture_output=True, text=True)
    files = [f for f in result.stdout.strip().split("\n") if f.endswith(".py")]
    if files:
        config = Config.default()
        config.severity_threshold = "medium"
        results = analyze(files, config=config)
        violations = results.get_violations("medium")
        if violations:
            for v in violations:
                print(f"{v.file_path}:{v.line_number} - {v.message}")
            exit(1)

if __name__ == "__main__":
    run_pre_commit()
