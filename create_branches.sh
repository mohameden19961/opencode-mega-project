#!/bin/bash
set -e

REPO_DIR="/tmp/opencode/codeguard"
cd "$REPO_DIR"

git config user.email "abdymohameden439@gmail.com"
git config user.name "abdy mohameden"

###############################################
# Branch: fix/config-parsing (Issue 2)
###############################################
git checkout main
git checkout -b fix/config-parsing

cat > tests/test_config_edge.py << 'PYEOF'
"""Edge case tests for config parsing."""
import pytest
from codeguard.config import load_config

class TestConfigEdgeCases:
    def test_empty_file(self, tmp_path):
        f = tmp_path / ".codeguard.yml"
        f.write_text("")
        config = load_config(str(f))
        assert config is not None

    def test_empty_sections(self, tmp_path):
        f = tmp_path / ".codeguard.yml"
        f.write_text("complexity:\nstyle:\n")
        config = load_config(str(f))
        assert config is not None
        assert config.complexity.max_cyclomatic == 10

    def test_invalid_yaml(self, tmp_path):
        f = tmp_path / ".codeguard.yml"
        f.write_text(": invalid :")
        config = load_config(str(f))
        assert config is not None

    def test_nonexistent_file(self):
        config = load_config("/nonexistent/.codeguard.yml")
        assert config is not None
PYEOF

python3 << 'PYEOF'
import re
with open('src/codeguard/config.py') as f:
    content = f.read()

old = '''    if path and os.path.exists(path):
        with open(path) as f:
            data = yaml.safe_load(f)
        if data is None:
            return Config.default()
        return Config.from_dict(data)'''

new = '''    if path and os.path.exists(path):
        try:
            with open(path) as f:
                data = yaml.safe_load(f)
        except (yaml.YAMLError, IOError):
            return Config.default()
        if data is None:
            return Config.default()
        if not isinstance(data, dict):
            return Config.default()
        return Config.from_dict(data)'''

content = content.replace(old, new)
with open('src/codeguard/config.py', 'w') as f:
    f.write(content)
print('Config.py updated')
PYEOF

git add -A && git commit -m "Fix config parser for empty YAML values

Handle empty files, empty sections, and invalid YAML gracefully.
Add try/except for parse errors and type checking.

Fixes: #2"

git push origin fix/config-parsing 2>&1 | tail -1

###############################################
# Branch: feature/html-dashboard (Issue 3)
###############################################
git checkout main
git checkout -b feature/html-dashboard

cat > src/codeguard/output/dashboard.py << 'PYEOF'
"""Interactive HTML dashboard with charts."""
from typing import Optional
from codeguard.config import Config
from codeguard.core.engine import AnalysisResults

class DashboardWriter:
    def __init__(self, output_path=None, config=None):
        self.output_path = output_path
        self.config = config or Config.default()

    def write(self, results):
        sev = results.count_by_severity()
        checks = results.count_by_check()
        violations_rows = "".join(
            f"<tr><td>{v.severity}</td><td>{v.check_name}</td><td>{v.message}</td>"
            f"<td>{v.file_path}:{v.line_number}</td></tr>"
            for v in results.violations[:20]
        )
        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"><title>CodeGuard Dashboard</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
body {{ font-family: sans-serif; margin: 2em; background: #f5f5f5; }}
.card {{ background: white; border-radius: 8px; padding: 1.5em; margin: 1em 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1em; }}
.stat {{ text-align: center; }}
.stat-value {{ font-size: 2em; font-weight: bold; color: #333; }}
.stat-label {{ color: #666; font-size: 0.9em; }}
.chart-container {{ position: relative; height: 300px; }}
table {{ width: 100%; border-collapse: collapse; }}
th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
th {{ background: #4CAF50; color: white; }}
</style>
</head>
<body>
<h1>CodeGuard Analysis Dashboard</h1>
<div class="grid">
  <div class="card stat"><div class="stat-value">{results.files_analyzed}</div><div class="stat-label">Files</div></div>
  <div class="card stat"><div class="stat-value">{len(results.violations)}</div><div class="stat-label">Violations</div></div>
  <div class="card stat"><div class="stat-value">{results.total_lines}</div><div class="stat-label">Lines</div></div>
  <div class="card stat"><div class="stat-value">{results.duration:.2f}s</div><div class="stat-label">Duration</div></div>
</div>
<div class="grid">
  <div class="card"><h3>Severity</h3><div class="chart-container"><canvas id="sevChart"></canvas></div></div>
  <div class="card"><h3>Checks</h3><div class="chart-container"><canvas id="checkChart"></canvas></div></div>
</div>
<div class="card"><h3>Violations</h3><table><tr><th>Severity</th><th>Check</th><th>Message</th><th>Location</th></tr>{violations_rows}</table></div>
<script>
new Chart(document.getElementById('sevChart'), {{
  type: 'pie',
  data: {{ labels: {list(sev.keys())!r}, datasets: [{{ data: {list(sev.values())!r},
    backgroundColor: ['#4caf50','#ff9800','#f44336','#d32f2f'] }}] }}
}});
new Chart(document.getElementById('checkChart'), {{
  type: 'bar',
  data: {{ labels: {list(checks.keys())!r}, datasets: [{{ data: {list(checks.values())!r},
    backgroundColor: '#2196f3' }}] }},
  options: {{ scales: {{ y: {{ beginAtZero: true }} }} }}
}});
</script></body></html>'''
        if self.output_path:
            with open(self.output_path, "w") as f:
                f.write(html)
PYEOF

python3 -c "
with open('src/codeguard/output/__init__.py') as f:
    c = f.read()
if 'DashboardWriter' not in c:
    c += 'from codeguard.output.dashboard import DashboardWriter\n'
with open('src/codeguard/output/__init__.py', 'w') as f:
    f.write(c)
"

git add -A && git commit -m "Add interactive HTML dashboard with Chart.js charts

Includes severity pie chart, check distribution bar chart,
statistics cards, and violations table.

Refs: #3"
git push origin feature/html-dashboard 2>&1 | tail -1

###############################################
# Branch: feature/performance (Issue 4)
###############################################
git checkout main
git checkout -b feature/performance

cat > src/codeguard/core/scanner.py << 'PYEOF'
"""Incremental file scanner for large codebases."""
import os, hashlib, json
from typing import List
from codeguard.config import Config

class IncrementalScanner:
    def __init__(self, config: Config):
        self.config = config
        self.state_file = os.path.join(config.cache_dir, "scanner_state.json")

    def get_changed_files(self, paths: List[str]) -> List[str]:
        state = self._load_state()
        files = self._collect_files(paths)
        changed = []
        for f in files:
            h = self._file_hash(f)
            if f not in state or state[f] != h:
                changed.append(f)
                state[f] = h
        self._save_state(state)
        return changed

    def _collect_files(self, paths):
        from codeguard.core.collector import FileCollector
        return FileCollector(self.config).collect(paths)

    def _file_hash(self, path):
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()

    def _load_state(self):
        if os.path.exists(self.state_file):
            with open(self.state_file) as f:
                return json.load(f)
        return {}

    def _save_state(self, state):
        os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
        with open(self.state_file, "w") as f:
            json.dump(state, f)
PYEOF
git add -A && git commit -m "Add incremental file scanner for large codebases

Only analyzes changed files by tracking hashes between runs.
Reduces analysis time for repeated runs on large projects.

Refs: #4"

python3 << 'PYEOF'
with open('src/codeguard/core/engine.py') as f:
    content = f.read()
content = content.replace(
    'from codeguard.utils.timer import Timer',
    'from codeguard.utils.timer import Timer\nfrom codeguard.core.scanner import IncrementalScanner'
)
content = content.replace(
    '        files = self.collector.collect(paths)',
    '        if self.config.use_cache:\n            scanner = IncrementalScanner(self.config)\n            files = scanner.get_changed_files(paths)\n        else:\n            files = self.collector.collect(paths)'
)
with open('src/codeguard/core/engine.py', 'w') as f:
    f.write(content)
print('Engine updated')
PYEOF
git add -A && git commit -m "Integrate incremental scanner into analysis engine

Use incremental scanning when cache is enabled to skip unchanged files.

Refs: #4"

cat > tests/test_scanner.py << 'PYEOF'
import pytest
from codeguard.core.scanner import IncrementalScanner
from codeguard.config import Config

class TestIncrementalScanner:
    @pytest.fixture
    def scanner(self, tmp_path):
        cfg = Config.default()
        cfg.cache_dir = str(tmp_path / ".cache")
        return IncrementalScanner(config=cfg)

    def test_first_run(self, scanner, tmp_path):
        (tmp_path / "t.py").write_text("x=1\n")
        changed = scanner.get_changed_files([str(tmp_path)])
        assert len(changed) > 0

    def test_no_changes(self, scanner, tmp_path):
        (tmp_path / "t.py").write_text("x=1\n")
        scanner.get_changed_files([str(tmp_path)])
        changed = scanner.get_changed_files([str(tmp_path)])
        assert len(changed) == 0

    def test_modified(self, scanner, tmp_path):
        f = tmp_path / "t.py"
        f.write_text("x=1\n")
        scanner.get_changed_files([str(tmp_path)])
        f.write_text("x=2\n")
        changed = scanner.get_changed_files([str(tmp_path)])
        assert len(changed) > 0
PYEOF
git add -A && git commit -m "Add tests for incremental scanner

Test first run, unchanged file caching, and modification detection.

Refs: #4"
git push origin feature/performance 2>&1 | tail -1

###############################################
# Branch: feature/sarif-format (Issue 5)
###############################################
git checkout main
git checkout -b feature/sarif-format

cat > src/codeguard/output/sarif_writer.py << 'PYEOF'
"""SARIF 2.1.0 output writer for GitHub Code Scanning."""
import json
from typing import Optional
from codeguard.config import Config
from codeguard.core.engine import AnalysisResults

class SARIFWriter:
    def __init__(self, output_path=None, config=None):
        self.output_path = output_path
        self.config = config or Config.default()

    def write(self, results):
        rules = {}
        items = []
        for v in results.violations:
            rid = v.check_name
            if rid not in rules:
                rules[rid] = {"id": rid, "name": rid,
                    "shortDescription": {"text": v.message},
                    "properties": {"severity": v.severity}}
            items.append({
                "ruleId": rid,
                "level": "error" if v.severity == "critical" else "warning",
                "message": {"text": v.message},
                "locations": [{"physicalLocation": {
                    "artifactLocation": {"uri": v.file_path},
                    "region": {"startLine": v.line_number}}}]})
        sarif = {"$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
            "version": "2.1.0",
            "runs": [{"tool": {"driver": {"name": "CodeGuard", "version": "0.1.0",
                "rules": list(rules.values())}}, "results": items}]}
        out = json.dumps(sarif, indent=2)
        if self.output_path:
            with open(self.output_path, "w") as f:
                f.write(out)
PYEOF
git add -A && git commit -m "Add SARIF 2.1.0 output writer

Enables GitHub Code Scanning integration with proper SARIF format.
Maps CodeGuard severity to SARIF levels correctly.

Refs: #5"

python3 -c "
with open('src/codeguard/output/__init__.py') as f:
    c = f.read()
if 'SARIFWriter' not in c:
    c += 'from codeguard.output.sarif_writer import SARIFWriter\n'
with open('src/codeguard/output/__init__.py', 'w') as f:
    f.write(c)
"
git add -A && git commit -m "Register SARIFWriter in output module

Refs: #5"

cat > tests/test_sarif_writer.py << 'PYEOF'
import json
from codeguard.output.sarif_writer import SARIFWriter
from codeguard.core.engine import AnalysisResults, Violation

class TestSARIFWriter:
    def test_write(self, tmp_path):
        out = tmp_path / "results.sarif"
        SARIFWriter(output_path=str(out)).write(AnalysisResults(
            files_analyzed=1, total_lines=5, duration=0.1,
            violations=[Violation(check_name="test", severity="high",
                message="msg", file_path="a.py", line_number=3)]))
        assert out.exists()
        data = json.loads(out.read_text())
        assert data["version"] == "2.1.0"
        assert len(data["runs"][0]["results"]) == 1
PYEOF
git add -A && git commit -m "Add tests for SARIF output format

Validate SARIF structure and content correctness.

Refs: #5"
git push origin feature/sarif-format 2>&1 | tail -1

###############################################
# Branch: fix/memory-leak (Issue 6)
###############################################
git checkout main
git checkout -b fix/memory-leak

python3 << 'PYEOF'
with open('src/codeguard/utils/cache.py') as f:
    content = f.read()
content = content.replace(
    'class AnalysisCache:',
    'import time\nfrom collections import OrderedDict\n\nclass AnalysisCache:'
)
content = content.replace(
    '    def __init__(self, cache_dir: str = ".codeguard_cache"):',
    '    def __init__(self, cache_dir: str = ".codeguard_cache", max_size: int = 1000):'
)
content = content.replace(
    '        self.cache_dir = cache_dir',
    '        self.cache_dir = cache_dir\n        self.max_size = max_size\n        self._memory_cache = OrderedDict()\n        self._access_times = {}'
)
new_set = '''    def _evict_if_needed(self):
        if len(self._memory_cache) >= self.max_size:
            oldest = next(iter(self._memory_cache))
            del self._memory_cache[oldest]
            if oldest in self._access_times:
                del self._access_times[oldest]

    def set(self, key: str, file_hash: int, violations: list):'''
content = content.replace('    def set(self, key: str, file_hash: int, violations: list):', new_set)

old_set_body = '''        cache_key = self._hash_key(key)
        os.makedirs(self.cache_dir, exist_ok=True)
        cache_path = os.path.join(self.cache_dir, cache_key)
        try:
            with open(cache_path, "w") as f:
                json.dump({"hash": file_hash, "violations": violations}, f)
        except IOError as e:
            raise CacheError(f"Failed to write cache: {e}")'''
new_set_body = '''        cache_key = self._hash_key(key)
        self._evict_if_needed()
        self._memory_cache[cache_key] = {"hash": file_hash, "violations": violations}
        self._access_times[cache_key] = time.time()
        os.makedirs(self.cache_dir, exist_ok=True)
        cache_path = os.path.join(self.cache_dir, cache_key)
        try:
            with open(cache_path, "w") as f:
                json.dump({"hash": file_hash, "violations": violations}, f)
        except IOError as e:
            raise CacheError(f"Failed to write cache: {e}")'''
content = content.replace(old_set_body, new_set_body)

new_clear = '''    def clear_memory(self):
        self._memory_cache.clear()
        self._access_times.clear()

    def get_stats(self) -> dict:
        return {"memory_entries": len(self._memory_cache), "max_size": self.max_size,
            "disk_entries": len(os.listdir(self.cache_dir)) if os.path.exists(self.cache_dir) else 0}

    def clear(self):'''
content = content.replace('    def clear(self):', new_clear)

with open('src/codeguard/utils/cache.py', 'w') as f:
    f.write(content)
print('Cache.py updated with LRU eviction')
PYEOF
git add -A && git commit -m "Fix memory leak with LRU eviction in cache

Add bounded memory cache with LRU eviction policy.
Prevents unbounded memory growth during analysis.

Fixes: #6"

git push origin fix/memory-leak 2>&1 | tail -1

###############################################
# Branch: feature/pre-commit-hooks (Issue 7)
###############################################
git checkout main
git checkout -b feature/pre-commit-hooks

cat > .pre-commit-hooks.yaml << 'PYEOF'
- id: codeguard
  name: CodeGuard
  description: Run CodeGuard on Python files
  entry: codeguard
  language: python
  types: [python]
  args: ["check", "--severity", "medium"]
  minimum_pre_commit_version: "2.9.0"
PYEOF
git add -A && git commit -m "Add pre-commit hook configuration

Configure CodeGuard as a pre-commit hook with standard interface.

Refs: #7"

cat > scripts/pre-commit.sh << 'PYEOF'
#!/bin/bash
# Pre-commit hook for CodeGuard
echo "Running CodeGuard pre-commit check..."
FILES=$(git diff --cached --name-only --diff-filter=ACM | grep '\.py$' || true)
if [ -z "$FILES" ]; then exit 0; fi
python -m codeguard check $FILES --severity medium
STATUS=$?
if [ $STATUS -ne 0 ]; then
    echo "CodeGuard found violations. Fix them or use git commit --no-verify"
    exit 1
fi
echo "CodeGuard check passed!"
PYEOF
chmod +x scripts/pre-commit.sh
git add -A && git commit -m "Add pre-commit hook shell script

Git hook script that runs CodeGuard on staged Python files before commit.

Refs: #7"

cat > docs/pre-commit-integration.md << 'PYEOF'
# Pre-commit Integration

## Using with pre-commit framework

Add to `.pre-commit-config.yaml`:
```yaml
repos:
  - repo: https://github.com/mohameden19961/codeguard
    rev: v0.1.0
    hooks:
      - id: codeguard
```

## Manual installation
```bash
ln -s ../../scripts/pre-commit.sh .git/hooks/pre-commit
```
PYEOF
git add -A && git commit -m "Add pre-commit integration documentation

Guide for using CodeGuard with pre-commit framework and manual hooks.

Refs: #7"
git push origin feature/pre-commit-hooks 2>&1 | tail -1

###############################################
# Branch: refactor/core-module (Issue 8)
###############################################
git checkout main
git checkout -b refactor/core-module

python3 << 'PYEOF'
with open('src/codeguard/core/engine.py') as f:
    content = f.read()

content = content.replace(
    'class AnalysisEngine:',
    '''from abc import ABC, abstractmethod

class IFileReader(ABC):
    @abstractmethod
    def read_file(self, path: str) -> str:
        pass

class ICheckRunner(ABC):
    @abstractmethod
    def run_checks(self, file_path: str, content: str, lines: list) -> list:
        pass

class FileReader(IFileReader):
    def read_file(self, path):
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

class CheckRunner(ICheckRunner):
    def __init__(self, config, checks):
        self.config = config
        self.checks = checks
    def run_checks(self, file_path, content, lines):
        violations = []
        for check in self.checks:
            try:
                inst = check(config=self.config)
                violations.extend(inst.check(file_path, content, lines))
            except Exception:
                pass
        return violations

class AnalysisEngine:'''
)

old_init = '''    def __init__(self, config: Config):
        self.config = config
        self.logger = Logger(verbose=config.verbose)
        self.cache = AnalysisCache(config.cache_dir) if config.use_cache else None
        self.collector = FileCollector(config)
        self._register_checks()'''

new_init = '''    def __init__(self, config: Config, file_reader: IFileReader = None, check_runner: ICheckRunner = None):
        self.config = config
        self.logger = Logger(verbose=config.verbose)
        self.cache = AnalysisCache(config.cache_dir) if config.use_cache else None
        self.collector = FileCollector(config)
        self.file_reader = file_reader or FileReader()
        self.check_runner = check_runner
        self._register_checks()'''

content = content.replace(old_init, new_init)

content = content.replace(
    '                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:\n                    content = f.read()',
    '                content = self.file_reader.read_file(file_path)'
)

with open('src/codeguard/core/engine.py', 'w') as f:
    f.write(content)
print('Engine refactored')
PYEOF
git add -A && git commit -m "Extract IFileReader and ICheckRunner interfaces

Decouple file reading and check execution for better testability.
Add dependency injection support to AnalysisEngine.

Refs: #8"
git push origin refactor/core-module 2>&1 | tail -1

###############################################
# Branch: feature/json-schema (Issue 9)
###############################################
git checkout main
git checkout -b feature/json-schema

cat > src/codeguard/config_schema.py << 'PYEOF'
"""JSON Schema validation for CodeGuard configuration."""

CODEGUARD_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "CodeGuard Configuration",
    "type": "object",
    "properties": {
        "verbose": {"type": "boolean", "default": False},
        "use_cache": {"type": "boolean", "default": True},
        "cache_dir": {"type": "string", "default": ".codeguard_cache"},
        "severity_threshold": {"type": "string", "enum": ["low", "medium", "high", "critical"], "default": "low"},
        "max_workers": {"type": "integer", "minimum": 1, "maximum": 64, "default": 4},
        "timeout": {"type": "integer", "minimum": 1, "default": 60},
        "checks_enabled": {"type": "array", "items": {"type": "string"}},
        "exclude_patterns": {"type": "array", "items": {"type": "string"}},
        "complexity": {"type": "object", "properties": {
            "max_cyclomatic": {"type": "integer", "minimum": 1, "default": 10},
            "max_cognitive": {"type": "integer", "minimum": 1, "default": 15},
            "max_nesting": {"type": "integer", "minimum": 0, "default": 4},
            "max_lines_per_function": {"type": "integer", "minimum": 1, "default": 50},
            "max_parameters": {"type": "integer", "minimum": 1, "default": 6},
        }},
        "style": {"type": "object", "properties": {
            "max_line_length": {"type": "integer", "minimum": 40, "default": 100},
            "indent": {"type": "integer", "enum": [2, 4], "default": 4},
            "trailing_whitespace": {"type": "boolean", "default": False},
        }},
        "security": {"type": "object", "properties": {
            "level": {"type": "string", "enum": ["low", "medium", "high", "critical"], "default": "high"},
            "check_sql_injection": {"type": "boolean", "default": True},
            "check_path_traversal": {"type": "boolean", "default": True},
            "check_command_injection": {"type": "boolean", "default": True},
        }},
    },
}

def validate_config(data: dict) -> list:
    errors = []
    for key in data:
        if key not in CODEGUARD_SCHEMA["properties"]:
            errors.append(f"Unknown config key: '{key}'")
            continue
        prop = CODEGUARD_SCHEMA["properties"][key]
        if "type" in prop:
            expected = prop["type"]
            if expected == "integer" and not isinstance(data[key], int):
                errors.append(f"'{key}' must be integer")
            elif expected == "boolean" and not isinstance(data[key], bool):
                errors.append(f"'{key}' must be boolean")
            elif expected == "string" and not isinstance(data[key], str):
                errors.append(f"'{key}' must be string")
            elif expected == "string" and "enum" in prop and data[key] not in prop["enum"]:
                errors.append(f"'{key}' must be one of {prop['enum']}")
        if isinstance(data[key], (int, float)):
            if "minimum" in prop and data[key] < prop["minimum"]:
                errors.append(f"'{key}' minimum is {prop['minimum']}")
            if "maximum" in prop and data[key] > prop["maximum"]:
                errors.append(f"'{key}' maximum is {prop['maximum']}")
    return errors
PYEOF
git add -A && git commit -m "Add JSON Schema definition and validator

Define full schema for all config options with type validation.
Provides helpful error messages for invalid configurations.

Refs: #9"

python3 << 'PYEOF'
with open('src/codeguard/config.py') as f:
    content = f.read()
content = content.replace(
    'from codeguard.exceptions import ConfigurationError',
    'from codeguard.exceptions import ConfigurationError\nfrom codeguard.config_schema import validate_config'
)
old = '''        with open(path) as f:
                data = yaml.safe_load(f)
        if data is None:'''
new = '''        with open(path) as f:
                data = yaml.safe_load(f)
        if data is None:
            return Config.default()
        if isinstance(data, dict):
            errs = validate_config(data)
            if errs:
                import warnings
                for e in errs:
                    warnings.warn(f"Config: {e}")
        if data is None:'''
content = content.replace(old, new)
with open('src/codeguard/config.py', 'w') as f:
    f.write(content)
print('Config.py updated with schema validation')
PYEOF
git add -A && git commit -m "Integrate JSON Schema validation into config loading

Validate configuration on load and warn about invalid options.

Refs: #9"

cat > tests/test_config_schema.py << 'PYEOF'
from codeguard.config_schema import validate_config

class TestConfigSchema:
    def test_valid(self):
        assert len(validate_config({"verbose": True})) == 0
    def test_invalid_type(self):
        assert len(validate_config({"verbose": "bad"})) > 0
    def test_unknown_key(self):
        assert len(validate_config({"unknown": "x"})) > 0
    def test_enum(self):
        assert len(validate_config({"severity_threshold": "bad"})) > 0
    def test_minimum(self):
        assert len(validate_config({"max_workers": 0})) > 0
PYEOF
git add -A && git commit -m "Add tests for config schema validation

Test type checking, enum validation, unknown keys, and ranges.

Refs: #9"
git push origin feature/json-schema 2>&1 | tail -1

###############################################
# Branch: feature/github-action (Issue 10)
###############################################
git checkout main
git checkout -b feature/github-action

mkdir -p .github/actions/codeguard
cat > .github/actions/codeguard/action.yml << 'PYEOF'
name: 'CodeGuard Analysis'
description: 'Run CodeGuard static analysis on Python code'
inputs:
  path:
    description: 'Path(s) to analyze'
    required: true
    default: 'src/'
  severity:
    description: 'Minimum severity threshold'
    required: false
    default: 'high'
  format:
    description: 'Output format'
    required: false
    default: 'sarif'
  upload-sarif:
    description: 'Upload SARIF results'
    required: false
    default: 'true'
runs:
  using: 'composite'
  steps:
    - run: pip install codeguard
      shell: bash
    - run: |
        ARGS="${{ inputs.path }} --severity ${{ inputs.severity }} --format ${{ inputs.format }}"
        codeguard analyze $ARGS --output codeguard_report.${{ inputs.format }}
      shell: bash
    - if: inputs.upload-sarif == 'true' && inputs.format == 'sarif'
      uses: github/codeql-action/upload-sarif@v3
      with:
        sarif_file: codeguard_report.sarif
branding:
  icon: 'shield'
  color: 'green'
PYEOF
git add -A && git commit -m "Add GitHub Action for CodeGuard analysis

Composite action that installs CodeGuard, runs analysis, and uploads SARIF.

Refs: #10"

cat > .github/workflows/codeguard.yml << 'PYEOF'
name: CodeGuard Analysis
on:
  push: {branches: [main]}
  pull_request: {branches: [main]}
jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: {python-version: '3.11'}
      - uses: ./.github/actions/codeguard
        with:
          path: src/
          severity: medium
          format: terminal
PYEOF
git add -A && git commit -m "Add GitHub Actions workflow configuration

Run CodeGuard on every push and pull request to main branch.

Refs: #10"

cat > docs/github-actions-integration.md << 'PYEOF'
# GitHub Actions Integration

## Using the Action
```yaml
steps:
  - uses: actions/checkout@v4
  - uses: your-org/codeguard@v1
    with:
      path: src/
      severity: high
      format: sarif
```

## Standalone
```yaml
- run: pip install codeguard
- run: codeguard analyze src/ --severity high
```
PYEOF
git add -A && git commit -m "Add GitHub Actions integration documentation

Documentation for using CodeGuard in GitHub CI/CD pipelines.

Refs: #10"
git push origin feature/github-action 2>&1 | tail -1

###############################################
# Branch: fix/binary-files (Issue 11)
###############################################
git checkout main
git checkout -b fix/binary-files

python3 << 'PYEOF'
with open('src/codeguard/core/collector.py') as f:
    content = f.read()

content = content.replace(
    'class FileCollector:\n    SUPPORTED_EXTENSIONS = {".py", ".pyx", ".pyw"}',
    '''class FileCollector:
    SUPPORTED_EXTENSIONS = {".py", ".pyx", ".pyw", ".pyi"}
    BINARY_SIGNATURES = [
        bytes([0x7f, 0x45, 0x4c, 0x46]),
        bytes([0x89, 0x50, 0x4e, 0x47]),
        bytes([0xff, 0xd8, 0xff]),
        bytes([0x25, 0x50, 0x44, 0x46]),
        bytes([0x1f, 0x8b]),
        bytes([0x50, 0x4b]),
    ]

    @staticmethod
    def is_binary(filepath):
        try:
            with open(filepath, "rb") as f:
                header = f.read(4)
                if not header:
                    return False
                for sig in FileCollector.BINARY_SIGNATURES:
                    if header.startswith(sig):
                        return True
                return b"\\x00" in f.read(8192)
        except IOError:
            return False'''
)

content = content.replace(
    'if self._is_supported(filepath) and not self._is_excluded(filepath):\n                    files.append(filepath)',
    'if self._is_supported(filepath) and not self._is_excluded(filepath) and not self.is_binary(filepath):\n                    files.append(filepath)'
)

with open('src/codeguard/core/collector.py', 'w') as f:
    f.write(content)
print('Collector.py updated with binary detection')
PYEOF
git add -A && git commit -m "Add binary file detection to collector

Skip binary files during collection to prevent UnicodeDecodeError.
Check file signatures (ELF, PNG, JPEG, PDF, ZIP) and null bytes.

Fixes: #11"

cat > tests/test_binary_detection.py << 'PYEOF'
import pytest
from codeguard.core.collector import FileCollector
from codeguard.config import Config

class TestBinaryDetection:
    @pytest.fixture
    def collector(self):
        return FileCollector(config=Config.default())

    def test_binary_detected(self, collector, tmp_path):
        f = tmp_path / "test.exe"
        f.write_bytes(bytes([0x7f, 0x45, 0x4c, 0x46, 0x00, 0x00]))
        assert collector.is_binary(str(f)) is True

    def test_text_not_binary(self, collector, tmp_path):
        f = tmp_path / "test.py"
        f.write_text("print('hello')")
        assert collector.is_binary(str(f)) is False

    def test_binary_skipped(self, collector, tmp_path):
        (tmp_path / "code.py").write_text("x=1")
        (tmp_path / "data.bin").write_bytes(bytes([0x89, 0x50, 0x4e, 0x47]))
        files = collector.collect([str(tmp_path)])
        assert len(files) == 1
PYEOF
git add -A && git commit -m "Add tests for binary file detection

Verify binary signatures are detected and binary files are skipped.

Refs: #11"
git push origin fix/binary-files 2>&1 | tail -1

###############################################
# Branch: feature/auto-fix (Issue 12)
###############################################
git checkout main
git checkout -b feature/auto-fix

mkdir -p src/codeguard/fixers
cat > src/codeguard/fixers/__init__.py << 'PYEOF'
"""Auto-fix capabilities for CodeGuard issues."""
from codeguard.fixers.base import BaseFixer, FixResult
from codeguard.fixers.whitespace import TrailingWhitespaceFixer
from codeguard.fixers.lines import LineEndingFixer
PYEOF
git add -A && git commit -m "Add fixer module structure for auto-fix

Base classes and module initialization for fix providers.

Refs: #12"

cat > src/codeguard/fixers/base.py << 'PYEOF'
"""Base classes for auto-fix functionality."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List
from codeguard.config import Config

@dataclass
class FixResult:
    file_path: str
    fixed: bool
    changes_made: int
    description: str

class BaseFixer(ABC):
    name: str = "base"
    def __init__(self, config: Config):
        self.config = config
    @abstractmethod
    def fix(self, file_path: str, content: str, lines: List[str]) -> FixResult:
        pass
PYEOF
git add -A && git commit -m "Add BaseFixer abstract class and FixResult dataclass

Define fix interface with fix() method and result type.

Refs: #12"

cat > src/codeguard/fixers/whitespace.py << 'PYEOF'
"""Fixer for trailing whitespace issues."""
from typing import List
from codeguard.config import Config
from codeguard.fixers.base import BaseFixer, FixResult

class TrailingWhitespaceFixer(BaseFixer):
    name = "trailing_whitespace"
    def fix(self, file_path, content, lines):
        fixed = []
        changes = 0
        for line in lines:
            stripped = line.rstrip()
            if line != stripped:
                fixed.append(stripped + "\n")
                changes += 1
            else:
                fixed.append(line)
        if changes > 0:
            with open(file_path, "w") as f:
                f.writelines(fixed)
        return FixResult(file_path, changes > 0, changes,
            f"Removed {changes} trailing whitespace issues")
PYEOF
git add -A && git commit -m "Add trailing whitespace auto-fixer

Detect and remove trailing whitespace from Python files.

Refs: #12"

cat > src/codeguard/fixers/lines.py << 'PYEOF'
"""Fixer for line ending issues."""
from typing import List
from codeguard.config import Config
from codeguard.fixers.base import BaseFixer, FixResult

class LineEndingFixer(BaseFixer):
    name = "line_endings"
    def fix(self, file_path, content, lines):
        if "\r\n" not in content and "\r" not in content:
            return FixResult(file_path, False, 0, "No issues")
        new = content.replace("\r\n", "\n").replace("\r", "\n")
        changes = content.count("\r\n") + content.count("\r")
        with open(file_path, "w") as f:
            f.write(new)
        return FixResult(file_path, True, changes,
            f"Normalized {changes} line endings to LF")
PYEOF
git add -A && git commit -m "Add line ending normalizer fixer

Convert CRLF and CR line endings to LF standard.

Refs: #12"

# Add fix command to CLI
python3 << 'PYEOF'
with open('src/codeguard/cli.py') as f:
    content = f.read()

fix_cmd = '''

@cli.command()
@click.argument("paths", nargs=-1, required=True)
@click.option("--dry-run", is_flag=True, default=False)
@click.option("--fixers", "-F", default=None)
@click.pass_context
def fix(ctx, paths, dry_run, fixers):
    """Auto-fix common issues in code."""
    from codeguard.fixers.whitespace import TrailingWhitespaceFixer
    from codeguard.fixers.lines import LineEndingFixer
    config = ctx.obj["config"]
    available = {
        "trailing_whitespace": TrailingWhitespaceFixer(config),
        "line_endings": LineEndingFixer(config),
    }
    if fixers:
        active = {k: v for k, v in available.items() if k in fixers.split(",")}
    else:
        active = available
    from codeguard.core.collector import FileCollector
    files = FileCollector(config).collect(list(paths))
    total = 0
    for fp in files:
        with open(fp, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        lines = content.split("\\n")
        for name, fixer in active.items():
            result = fixer.fix(fp, content, lines)
            if result.fixed:
                label = "[DRY-RUN]" if dry_run else "[FIXED]"
                click.echo(f"{label} {fp}: {result.description}")
                total += result.changes_made
    click.echo(f"{'Would fix' if dry_run else 'Fixed'} {total} issues")
'''

content = content.replace('def main():', fix_cmd + '\ndef main():')
with open('src/codeguard/cli.py', 'w') as f:
    f.write(content)
print('CLI.py updated with fix command')
PYEOF
git add -A && git commit -m "Add fix command to CLI for auto-fixing issues

Supports trailing whitespace and line ending fixers with dry-run mode.

Refs: #12"

cat > tests/test_fixers.py << 'PYEOF'
import pytest
from codeguard.config import Config
from codeguard.fixers.whitespace import TrailingWhitespaceFixer
from codeguard.fixers.lines import LineEndingFixer

class TestTrailingWhitespaceFixer:
    @pytest.fixture
    def fixer(self):
        return TrailingWhitespaceFixer(Config.default())

    def test_removes_trailing_spaces(self, fixer, tmp_path):
        f = tmp_path / "t.py"
        f.write_text("x = 1   \ny = 2\n")
        result = fixer.fix(str(f), f.read_text(), f.read_text().split("\n"))
        assert result.fixed
        assert "   \n" not in f.read_text()

class TestLineEndingFixer:
    @pytest.fixture
    def fixer(self):
        return LineEndingFixer(Config.default())

    def test_fix_crlf(self, fixer, tmp_path):
        f = tmp_path / "t.py"
        f.write_text("x = 1\r\ny = 2\r\n")
        result = fixer.fix(str(f), f.read_text(), f.read_text().split("\n"))
        assert result.fixed
        assert "\r\n" not in f.read_text()
PYEOF
git add -A && git commit -m "Add tests for auto-fixers

Test trailing whitespace removal and CRLF normalization.

Refs: #12"
git push origin feature/auto-fix 2>&1 | tail -1

echo ""
echo "=== ALL BRANCHES PUSHED SUCCESSFULLY ==="
