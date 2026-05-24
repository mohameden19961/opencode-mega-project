#!/bin/bash
set -e

REPO="mohameden19961/codeguard"
DIR="/tmp/opencode/codeguard"
cd "$DIR"

echo "=== CREATING ISSUES ==="

# Create issues
ISSUE_1=$(gh issue create --repo "$REPO" --title "Add plugin system for custom checks" \
  --label "enhancement" \
  --body "## Feature Request

We need a plugin system that allows users to write custom checks without modifying the core codebase.

### Acceptance Criteria
- [ ] Plugin discovery from a directory
- [ ] Plugin loading and registration
- [ ] Documentation for creating plugins
- [ ] Example plugin included" | grep -oE '[0-9]+$')
echo "Issue #$ISSUE_1: Add plugin system"

ISSUE_2=$(gh issue create --repo "$REPO" --title "Fix config parsing with empty YAML values" \
  --label "bug" \
  --body "## Bug Report

When the config file contains empty values, the parser crashes with a TypeError.

### Steps to Reproduce
1. Create .codeguard.yml with an empty section
2. Run codeguard analyze
3. See crash" | grep -oE '[0-9]+$')
echo "Issue #$ISSUE_2: Fix config parsing"

ISSUE_3=$(gh issue create --repo "$REPO" --title "Add HTML dashboard with charts and trends" \
  --label "enhancement" \
  --body "## Feature Request

Enhance the HTML report to include charts showing violation trends, severity distribution, and file-level metrics.

### Design
- Use Chart.js for interactive charts
- Add trend graphs over time
- Show severity distribution pie chart
- File-level heat map" | grep -oE '[0-9]+$')
echo "Issue #$ISSUE_3: HTML dashboard"

ISSUE_4=$(gh issue create --repo "$REPO" --title "Improve performance for large codebases" \
  --label "enhancement" \
  --label "performance" \
  --body "## Performance Improvement

Analysis of large codebases (>10K files) is too slow. Need to optimize.

### Optimizations
- [ ] Incremental file scanning
- [ ] Better caching strategy
- [ ] Multi-processing support
- [ ] Memory-efficient result collection" | grep -oE '[0-9]+$')
echo "Issue #$ISSUE_4: Performance improvements"

ISSUE_5=$(gh issue create --repo "$REPO" --title "Add SARIF output format support" \
  --label "enhancement" \
  --body "## Feature Request

Support SARIF (Static Analysis Results Interchange Format) output for integration with GitHub Code Scanning.

### Details
- Implement SARIF 2.1.0 format
- Include all violation details
- Map severity levels correctly" | grep -oE '[0-9]+$')
echo "Issue #$ISSUE_5: SARIF format"

ISSUE_6=$(gh issue create --repo "$REPO" --title "Memory leak in cache module" \
  --label "bug" \
  --label "priority-high" \
  --body "## Bug Report

The cache module doesn't properly clean up old entries, causing memory usage to grow unbounded.

### Impact
- Memory grows with each analysis run
- Can cause OOM for large projects
- Cache directory fills up" | grep -oE '[0-9]+$')
echo "Issue #$ISSUE_6: Memory leak"

ISSUE_7=$(gh issue create --repo "$REPO" --title "Add pre-commit hook support" \
  --label "enhancement" \
  --body "## Feature Request

Add official pre-commit hook support so users can run CodeGuard as part of their pre-commit workflow.

### Tasks
- [ ] Create pre-commit hook script
- [ ] Add pre-commit config example
- [ ] Document integration steps" | grep -oE '[0-9]+$')
echo "Issue #$ISSUE_7: Pre-commit hooks"

ISSUE_8=$(gh issue create --repo "$REPO" --title "Refactor core engine for testability" \
  --label "refactor" \
  --body "## Refactoring

The core AnalysisEngine class is difficult to test due to tight coupling with file system and checks.

### Plan
- [ ] Extract file reading to a separate service
- [ ] Use dependency injection for checks
- [ ] Add interfaces for all major components
- [ ] Increase test coverage to 90%" | grep -oE '[0-9]+$')
echo "Issue #$ISSUE_8: Core refactoring"

ISSUE_9=$(gh issue create --repo "$REPO" --title "Add JSON Schema validation for config" \
  --label "enhancement" \
  --body "## Feature Request

Validate the configuration file against a JSON Schema to provide better error messages.

### Schema
- Define JSON Schema for all config options
- Validate on load
- Provide helpful error messages for invalid config" | grep -oE '[0-9]+$')
echo "Issue #$ISSUE_9: JSON Schema validation"

ISSUE_10=$(gh issue create --repo "$REPO" --title "Create GitHub Action for CodeGuard" \
  --label "enhancement" \
  --label "documentation" \
  --body "## Feature Request

Create a GitHub Action that makes it easy to run CodeGuard in CI pipelines.

### Deliverables
- GitHub Action Dockerfile
- Action metadata file
- Documentation page
- Example workflow" | grep -oE '[0-9]+$')
echo "Issue #$ISSUE_10: GitHub Action"

ISSUE_11=$(gh issue create --repo "$REPO" --title "Fix UnicodeDecodeError on binary files" \
  --label "bug" \
  --body "## Bug Report

CodeGuard crashes with UnicodeDecodeError when encountering binary files in the analysis path.

### Fix
- Skip binary files during collection
- Add binary file detection
- Graceful error handling" | grep -oE '[0-9]+$')
echo "Issue #$ISSUE_11: Binary file fix"

ISSUE_12=$(gh issue create --repo "$REPO" --title "Add auto-fix capability for style issues" \
  --label "enhancement" \
  --body "## Feature Request

Allow CodeGuard to automatically fix certain issues (trailing whitespace, line endings, etc.).

### Auto-fixable issues
- [ ] Trailing whitespace removal
- [ ] Line ending normalization
- [ ] Blank line normalization
- [ ] Import ordering" | grep -oE '[0-9]+$')
echo "Issue #$ISSUE_12: Auto-fix support"

echo ""
echo "=== ISSUES CREATED ==="
echo "Issue #$ISSUE_1: Plugin system"
echo "Issue #$ISSUE_2: Config parsing fix"
echo "Issue #$ISSUE_3: HTML dashboard"
echo "Issue #$ISSUE_4: Performance"
echo "Issue #$ISSUE_5: SARIF format"
echo "Issue #$ISSUE_6: Memory leak"
echo "Issue #$ISSUE_7: Pre-commit hooks"
echo "Issue #$ISSUE_8: Core refactoring"
echo "Issue #$ISSUE_9: JSON Schema"
echo "Issue #$ISSUE_10: GitHub Action"
echo "Issue #$ISSUE_11: Binary file fix"
echo "Issue #$ISSUE_12: Auto-fix support"

echo ""
echo "=== CREATING BRANCHES AND PUSHING CODE ==="

create_branch_and_push() {
    local branch=$1
    local issue=$2
    local commit_count=$3

    git checkout main
    git pull origin main
    git checkout -b "$branch"
    echo "Created branch: $branch"
}

# Branch 1: plugin-system (Issue 1)
git checkout main
git checkout -b feature/plugin-system
mkdir -p src/codeguard/plugins
cat > src/codeguard/plugins/__init__.py << 'PYEOF'
"""Plugin system for custom CodeGuard checks."""

import importlib
import os
from typing import List, Type
from codeguard.checks.base import BaseCheck, CheckRegistry


class PluginManager:
    def __init__(self, plugin_dir: str = None):
        self.plugin_dir = plugin_dir or os.path.expanduser("~/.codeguard/plugins")

    def discover_plugins(self) -> List[Type[BaseCheck]]:
        if not os.path.exists(self.plugin_dir):
            return []
        checks = []
        for fname in os.listdir(self.plugin_dir):
            if fname.endswith(".py") and not fname.startswith("_"):
                mod_name = fname[:-3]
                spec = importlib.util.spec_from_file_location(mod_name, os.path.join(self.plugin_dir, fname))
                if spec and spec.loader:
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)
                    for attr in dir(mod):
                        obj = getattr(mod, attr)
                        if isinstance(obj, type) and issubclass(obj, BaseCheck) and obj is not BaseCheck:
                            CheckRegistry.register(obj)
                            checks.append(obj)
        return checks
PYEOF
echo "Added plugin system implementation"
git add -A && git commit -m "Add plugin system with directory discovery
Implement plugin discovery from ~/.codeguard/plugins directory.
Supports loading custom check classes dynamically.

Refs: #$ISSUE_1"

cat > src/codeguard/plugins/example_plugin.py << 'PYEOF'
"""Example plugin demonstrating the CodeGuard plugin system."""
from typing import List
from codeguard.checks.base import BaseCheck
from codeguard.core.engine import Violation
from codeguard.config import Config


class TodoCheck(BaseCheck):
    name = "todo_check"
    description = "Warns about TODO/FIXME comments"

    def check(self, file_path: str, content: str, lines: List[str]) -> List[Violation]:
        violations = []
        for i, line in enumerate(lines, 1):
            if "TODO" in line:
                violations.append(Violation(
                    check_name=self.name, severity="low",
                    message=f"Line {i} contains TODO comment",
                    file_path=file_path, line_number=i,
                    suggestion="Address TODO before committing",
                ))
            if "FIXME" in line:
                violations.append(Violation(
                    check_name=self.name, severity="medium",
                    message=f"Line {i} contains FIXME comment",
                    file_path=file_path, line_number=i,
                    suggestion="Fix the issue before committing",
                ))
        return violations
PYEOF
echo "Added example plugin"
git add -A && git commit -m "Add example plugin for TODO/FIXME detection
Demonstrates how to create a custom check using the plugin API.

Refs: #$ISSUE_1"

cat > docs/plugin_development.md << 'PYEOF'
# Plugin Development Guide

## Overview

CodeGuard supports plugins - custom checks that extend its analysis capabilities.

## Creating a Plugin

1. Create a Python file in `~/.codeguard/plugins/`
2. Define a class that inherits from `BaseCheck`
3. Set the `name` and `description` attributes
4. Implement the `check` method
5. The plugin is automatically discovered

## Example

```python
from codeguard.checks.base import BaseCheck
from codeguard.core.engine import Violation

class MyCustomCheck(BaseCheck):
    name = "my_custom_check"
    description = "My custom check"

    def check(self, file_path, content, lines):
        violations = []
        # Your analysis logic here
        return violations
```


## Testing Plugins

```python
def test_my_plugin():
    check = MyCustomCheck(config=Config.default())
    violations = check.check("test.py", "code", ["code"])
    assert len(violations) == 0
```
PYEOF
git add -A && git commit -m "Add plugin development documentation
Comprehensive guide for creating and testing custom CodeGuard plugins.

Refs: #$ISSUE_1"

git push origin feature/plugin-system
echo "Pushed feature/plugin-system"

# Branch 2: fix-config-parsing (Issue 2)
git checkout main
git checkout -b fix/config-parsing
cat > tests/test_config_edge.py << 'PYEOF'
"""Edge case tests for config parsing."""
import pytest
import yaml
import tempfile
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

    def test_partial_config(self, tmp_path):
        f = tmp_path / ".codeguard.yml"
        f.write_text("verbose: true\n")
        config = load_config(str(f))
        assert config.verbose is True

    def test_invalid_yaml(self, tmp_path):
        f = tmp_path / ".codeguard.yml"
        f.write_text(": invalid yaml :")
        config = load_config(str(f))
        assert config is not None

    def test_nonexistent_file(self):
        config = load_config("/nonexistent/path/.codeguard.yml")
        assert config is not None
        assert config.verbose is False
PYEOF
git add -A && git commit -m "Add edge case tests for config parsing
Tests for empty files, empty sections, partial configs, and invalid YAML.

Refs: #$ISSUE_2"

# Fix config.py
cat > /tmp/config_fix.py << 'PYEOF'
def load_config(path=None):
    if path is None:
        for candidate in [".codeguard.yml", ".codeguard.yaml",
                          "~/.codeguard.yml", "~/.codeguard/config.yml"]:
            expanded = os.path.expanduser(candidate)
            if os.path.exists(expanded):
                path = expanded
                break
    if path and os.path.exists(path):
        try:
            with open(path) as f:
                data = yaml.safe_load(f)
            if data is None:
                return Config.default()
            if not isinstance(data, dict):
                return Config.default()
            return Config.from_dict(data)
        except (yaml.YAMLError, IOError):
            pass
    return Config.default()
PYEOF
echo "Config parsing fix prepared"
# Actually modify the real config.py
cd "$DIR"
python3 -c "
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
"
git add -A && git commit -m "Fix config parser for empty YAML and edge cases
Handle empty files, empty sections, invalid YAML gracefully.
Added try/except for parse errors and type checking.

Fixes: #$ISSUE_2"

git push origin fix/config-parsing
echo "Pushed fix/config-parsing"

# Branch 3: html-dashboard (Issue 3)
git checkout main
git checkout -b feature/html-dashboard
cat > src/codeguard/output/dashboard.py << 'PYEOF'
"""Interactive HTML dashboard with charts."""
from typing import Optional
from codeguard.config import Config
from codeguard.core.engine import AnalysisResults


class DashboardWriter:
    def __init__(self, output_path: Optional[str] = None, config: Optional[Config] = None):
        self.output_path = output_path
        self.config = config or Config.default()

    def write(self, results: AnalysisResults):
        sev_counts = results.count_by_severity()
        check_counts = results.count_by_check()
        sev_json = str(sev_counts).replace("'", '"')
        check_json = str(check_counts).replace("'", '"')
        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>CodeGuard Dashboard</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
body {{ font-family: sans-serif; margin: 2em; background: #f5f5f5; }}
.card {{ background: white; border-radius: 8px; padding: 1.5em; margin: 1em 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1em; }}
.stat {{ text-align: center; }}
.stat-value {{ font-size: 2em; font-weight: bold; color: #333; }}
.stat-label {{ color: #666; font-size: 0.9em; }}
.chart-container {{ position: relative; height: 300px; }}
</style>
</head>
<body>
<h1>CodeGuard Analysis Dashboard</h1>
<div class="grid">
    <div class="card stat">
        <div class="stat-value">{results.files_analyzed}</div>
        <div class="stat-label">Files Analyzed</div>
    </div>
    <div class="card stat">
        <div class="stat-value">{len(results.violations)}</div>
        <div class="stat-label">Total Violations</div>
    </div>
    <div class="card stat">
        <div class="stat-value">{results.total_lines}</div>
        <div class="stat-label">Lines of Code</div>
    </div>
    <div class="card stat">
        <div class="stat-value">{results.duration:.2f}s</div>
        <div class="stat-label">Duration</div>
    </div>
</div>
<div class="grid">
    <div class="card"><h3>Severity Distribution</h3><div class="chart-container"><canvas id="severityChart"></canvas></div></div>
    <div class="card"><h3>Check Distribution</h3><div class="chart-container"><canvas id="checkChart"></canvas></div></div>
</div>
<div class="card"><h3>Recent Violations</h3><table><tr><th>Severity</th><th>Check</th><th>Message</th><th>File</th></tr>
{"".join(f"<tr><td>{v.severity}</td><td>{v.check_name}</td><td>{v.message}</td><td>{v.file_path}:{v.line_number}</td></tr>" for v in results.violations[:20])}
</table></div>
<script>
new Chart(document.getElementById('severityChart'), {{
    type: 'pie',
    data: {{
        labels: {list(sev_counts.keys())!r},
        datasets: [{{ data: {list(sev_counts.values())!r},
            backgroundColor: ['#4caf50', '#ff9800', '#f44336', '#d32f2f'] }}]
    }}
}});
new Chart(document.getElementById('checkChart'), {{
    type: 'bar',
    data: {{
        labels: {list(check_counts.keys())!r},
        datasets: [{{ data: {list(check_counts.values())!r},
            backgroundColor: '#2196f3' }}]
    }},
    options: {{ scales: {{ y: {{ beginAtZero: true }} }} }}
}});
</script>
</body>
</html>'''
        if self.output_path:
            with open(self.output_path, "w") as f:
                f.write(html)
        else:
            print(html)
PYEOF
git add -A && git commit -m "Add interactive HTML dashboard with Chart.js
Includes severity pie chart, check distribution bar chart,
statistics cards, and violations table.

Refs: #$ISSUE_3"

# Add dashboard writer to CLI and output init
python3 -c "
with open('src/codeguard/output/__init__.py') as f:
    content = f.read()
if 'DashboardWriter' not in content:
    content += 'from codeguard.output.dashboard import DashboardWriter\n'
with open('src/codeguard/output/__init__.py', 'w') as f:
    f.write(content)
"
git add -A && git commit -m "Register DashboardWriter in output module
Make dashboard available as an output format option.

Refs: #$ISSUE_3"

git push origin feature/html-dashboard
echo "Pushed feature/html-dashboard"

# Branch 4: performance (Issue 4)
git checkout main
git checkout -b feature/performance
cat > src/codeguard/core/scanner.py << 'PYEOF'
"""Incremental file scanner for large codebases."""

import os
import hashlib
import json
from typing import List, Optional
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
            current_hash = self._file_hash(f)
            if f not in state or state[f] != current_hash:
                changed.append(f)
                state[f] = current_hash
        self._save_state(state)
        return changed

    def _collect_files(self, paths: List[str]) -> List[str]:
        from codeguard.core.collector import FileCollector
        collector = FileCollector(self.config)
        return collector.collect(paths)

    def _file_hash(self, path: str) -> str:
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()

    def _load_state(self) -> dict:
        if os.path.exists(self.state_file):
            with open(self.state_file) as f:
                return json.load(f)
        return {}

    def _save_state(self, state: dict):
        os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
        with open(self.state_file, "w") as f:
            json.dump(state, f)
PYEOF
git add -A && git commit -m "Add incremental file scanner for large codebases
Only analyzes changed files by tracking file hashes between runs.
Reduces analysis time for repeated runs.

Refs: #$ISSUE_4"

python3 -c "
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
print('Engine updated with incremental scanner')
"
git add -A && git commit -m "Integrate incremental scanner into analysis engine
Skip unchanged files when cache is enabled.

Refs: #$ISSUE_4"

cat > tests/test_scanner.py << 'PYEOF'
"""Tests for incremental scanner."""
import pytest
from codeguard.core.scanner import IncrementalScanner
from codeguard.config import Config


class TestIncrementalScanner:
    @pytest.fixture
    def scanner(self, tmp_path):
        config = Config.default()
        config.cache_dir = str(tmp_path / ".cache")
        return IncrementalScanner(config=config)

    def test_first_run(self, scanner, tmp_path):
        f = tmp_path / "test.py"
        f.write_text("x = 1\n")
        changed = scanner.get_changed_files([str(tmp_path)])
        assert len(changed) > 0

    def test_no_changes(self, scanner, tmp_path):
        f = tmp_path / "test.py"
        f.write_text("x = 1\n")
        scanner.get_changed_files([str(tmp_path)])
        changed = scanner.get_changed_files([str(tmp_path)])
        assert len(changed) == 0

    def test_file_modified(self, scanner, tmp_path):
        f = tmp_path / "test.py"
        f.write_text("x = 1\n")
        scanner.get_changed_files([str(tmp_path)])
        f.write_text("x = 2\n")
        changed = scanner.get_changed_files([str(tmp_path)])
        assert len(changed) > 0
PYEOF
git add -A && git commit -m "Add tests for incremental scanner
Test first run, unchanged files, and modified file detection.

Refs: #$ISSUE_4"

git push origin feature/performance
echo "Pushed feature/performance"

# Branch 5: sarif-format (Issue 5)
git checkout main
git checkout -b feature/sarif-format
cat > src/codeguard/output/sarif_writer.py << 'PYEOF'
"""SARIF 2.1.0 output writer for GitHub Code Scanning integration."""
import json
from typing import Optional
from codeguard.config import Config
from codeguard.core.engine import AnalysisResults


class SARIFWriter:
    def __init__(self, output_path: Optional[str] = None, config: Optional[Config] = None):
        self.output_path = output_path
        self.config = config or Config.default()

    def write(self, results: AnalysisResults):
        rules = {}
        results_list = []
        for v in results.violations:
            rule_id = v.check_name
            if rule_id not in rules:
                rules[rule_id] = {
                    "id": rule_id,
                    "name": rule_id,
                    "shortDescription": {"text": v.message},
                    "helpUri": f"https://codeguard.dev/docs/checks/{rule_id}",
                    "properties": {"severity": v.severity},
                }
            results_list.append({
                "ruleId": rule_id,
                "level": "error" if v.severity == "critical" else "warning",
                "message": {"text": v.message},
                "locations": [{
                    "physicalLocation": {
                        "artifactLocation": {"uri": v.file_path},
                        "region": {"startLine": v.line_number, "startColumn": max(v.column, 1)},
                    }
                }],
                "properties": {"suggestion": v.suggestion or ""},
            })
        sarif = {
            "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
            "version": "2.1.0",
            "runs": [{
                "tool": {
                    "driver": {
                        "name": "CodeGuard",
                        "version": "0.1.0",
                        "informationUri": "https://github.com/mohameden19961/codeguard",
                        "rules": list(rules.values()),
                    }
                },
                "results": results_list,
            }],
        }
        output = json.dumps(sarif, indent=2)
        if self.output_path:
            with open(self.output_path, "w") as f:
                f.write(output)
        else:
            print(output)
PYEOF
git add -A && git commit -m "Add SARIF 2.1.0 output writer
Enables GitHub Code Scanning integration and SARIF-compatible tool ingestion.

Refs: #$ISSUE_5"

python3 -c "
with open('src/codeguard/output/__init__.py') as f:
    content = f.read()
if 'SARIFWriter' not in content:
    content += 'from codeguard.output.sarif_writer import SARIFWriter\n'
with open('src/codeguard/output/__init__.py', 'w') as f:
    f.write(content)
"
git add -A && git commit -m "Register SARIFWriter in output module

Refs: #$ISSUE_5"

cat > tests/test_sarif_writer.py << 'PYEOF'
"""Tests for SARIF output writer."""
import json
from codeguard.output.sarif_writer import SARIFWriter
from codeguard.core.engine import AnalysisResults, Violation


class TestSARIFWriter:
    def test_write(self, tmp_path):
        output = tmp_path / "results.sarif"
        writer = SARIFWriter(output_path=str(output))
        results = AnalysisResults(
            files_analyzed=1, total_lines=5, duration=0.1,
            violations=[Violation(check_name="test", severity="high",
                                  message="test msg", file_path="a.py", line_number=3)],
        )
        writer.write(results)
        assert output.exists()
        data = json.loads(output.read_text())
        assert data["version"] == "2.1.0"
        assert len(data["runs"][0]["results"]) == 1
        assert data["runs"][0]["results"][0]["ruleId"] == "test"
PYEOF
git add -A && git commit -m "Add tests for SARIF output format
Validate SARIF structure, version, and content.

Refs: #$ISSUE_5"

git push origin feature/sarif-format
echo "Pushed feature/sarif-format"

# Branch 6: fix-memory-leak (Issue 6)
git checkout main
git checkout -b fix/memory-leak

python3 -c "
with open('src/codeguard/utils/cache.py') as f:
    content = f.read()

# Add LRU eviction
new_content = content.replace(
    'class AnalysisCache:',
    '''import time
from collections import OrderedDict

class AnalysisCache:'''
)

# Add max_size and eviction
new_content = new_content.replace(
    '    def __init__(self, cache_dir: str = \".codeguard_cache\"):',
    '    def __init__(self, cache_dir: str = \".codeguard_cache\", max_size: int = 1000):'
)

new_content = new_content.replace(
    '        self.cache_dir = cache_dir',
    '''        self.cache_dir = cache_dir
        self.max_size = max_size
        self._memory_cache = OrderedDict()
        self._access_times = {}'''
)

new_content = new_content.replace(
    '    def set(self, key: str, file_hash: int, violations: list):',
    '''    def _evict_if_needed(self):
        if len(self._memory_cache) >= self.max_size:
            oldest = next(iter(self._memory_cache))
            del self._memory_cache[oldest]
            if oldest in self._access_times:
                del self._access_times[oldest]

    def set(self, key: str, file_hash: int, violations: list):'''
)

new_content = new_content.replace(
    '        cache_key = self._hash_key(key)\n        os.makedirs(self.cache_dir, exist_ok=True)\n        cache_path = os.path.join(self.cache_dir, cache_key)\n        try:\n            with open(cache_path, \"w\") as f:\n                json.dump({\"hash\": file_hash, \"violations\": violations}, f)\n        except IOError as e:\n            raise CacheError(f\"Failed to write cache: {e}\")',
    '''        cache_key = self._hash_key(key)
        self._evict_if_needed()
        self._memory_cache[cache_key] = {\"hash\": file_hash, \"violations\": violations}
        self._access_times[cache_key] = time.time()
        os.makedirs(self.cache_dir, exist_ok=True)
        cache_path = os.path.join(self.cache_dir, cache_key)
        try:
            with open(cache_path, \"w\") as f:
                json.dump({\"hash\": file_hash, \"violations\": violations}, f)
        except IOError as e:
            raise CacheError(f\"Failed to write cache: {e}\")'''
)

new_content = new_content.replace(
    '    def clear(self):',
    '''    def clear_memory(self):
        self._memory_cache.clear()
        self._access_times.clear()

    def get_stats(self) -> dict:
        return {
            \"memory_entries\": len(self._memory_cache),
            \"max_size\": self.max_size,
            \"disk_entries\": len(os.listdir(self.cache_dir)) if os.path.exists(self.cache_dir) else 0,
        }

    def clear(self):'''
)

with open('src/codeguard/utils/cache.py', 'w') as f:
    f.write(new_content)
print('Cache.py updated with LRU eviction')
"
git add -A && git commit -m "Fix memory leak in cache module with LRU eviction
Added bounded memory cache with LRU eviction policy.
Prevents unbounded memory growth during analysis.

Fixes: #$ISSUE_6"

cat > tests/test_cache_lru.py << 'PYEOF'
"""Tests for cache LRU eviction."""
import pytest
from codeguard.utils.cache import AnalysisCache


class TestCacheLRU:
    def test_memory_limit(self, tmp_path):
        cache = AnalysisCache(cache_dir=str(tmp_path / ".cache"), max_size=2)
        cache.set("key1", 1, ["v1"])
        cache.set("key2", 2, ["v2"])
        cache.set("key3", 3, ["v3"])
        assert cache.get("key1") is None
        assert cache.get("key2") is not None

    def test_stats(self, tmp_path):
        cache = AnalysisCache(cache_dir=str(tmp_path / ".cache"))
        stats = cache.get_stats()
        assert "memory_entries" in stats
        assert "max_size" in stats
PYEOF
git add -A && git commit -m "Add tests for cache LRU eviction behavior
Verify memory limit enforcement and stats reporting.

Refs: #$ISSUE_6"

git push origin fix/memory-leak
echo "Pushed fix/memory-leak"

# Branch 7: pre-commit-hooks (Issue 7)
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
Standard pre-commit hook definition for CodeGuard analysis.

Refs: #$ISSUE_7"

cat > scripts/pre-commit.sh << 'PYEOF'
#!/bin/bash
# Pre-commit hook for CodeGuard
# Install: ln -s ../../scripts/pre-commit.sh .git/hooks/pre-commit

echo "Running CodeGuard pre-commit check..."

# Get staged Python files
FILES=$(git diff --cached --name-only --diff-filter=ACM | grep '\.py$')

if [ -z "$FILES" ]; then
    exit 0
fi

# Run CodeGuard on staged files
python -m codeguard check $FILES --severity medium
STATUS=$?

if [ $STATUS -ne 0 ]; then
    echo "CodeGuard found violations. Please fix them before committing."
    echo "To bypass: git commit --no-verify"
    exit 1
fi

echo "CodeGuard check passed!"
exit 0
PYEOF
chmod +x scripts/pre-commit.sh
git add -A && git commit -m "Add pre-commit hook script for Git
Shell script that runs CodeGuard on staged Python files before commit.

Refs: #$ISSUE_7"

cat > docs/pre-commit-integration.md << 'PYEOF'
# Pre-commit Integration

## Using with pre-commit

Add to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/mohameden19961/codeguard
    rev: v0.1.0
    hooks:
      - id: codeguard
```

## Manual Hook Installation

```bash
ln -s ../../scripts/pre-commit.sh .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```
PYEOF
git add -A && git commit -m "Add pre-commit integration documentation
Guide for using CodeGuard with pre-commit framework and manual hooks.

Refs: #$ISSUE_7"

git push origin feature/pre-commit-hooks
echo "Pushed feature/pre-commit-hooks"

# Branch 8: refactor-core (Issue 8)
git checkout main
git checkout -b refactor/core-module

python3 -c "
# Extract interfaces
with open('src/codeguard/core/engine.py') as f:
    content = f.read()

# Add IFileReader interface
content = content.replace(
    'class AnalysisEngine:',
    '''from abc import ABC, abstractmethod

class IFileReader(ABC):
    \"\"\"Interface for file reading operations.\"\"\"
    @abstractmethod
    def read_file(self, path: str) -> str:
        pass

class ICheckRunner(ABC):
    \"\"\"Interface for running checks.\"\"\"
    @abstractmethod
    def run_checks(self, file_path: str, content: str, lines: list) -> list:
        pass

class FileReader(IFileReader):
    def read_file(self, path: str) -> str:
        with open(path, \"r\", encoding=\"utf-8\", errors=\"ignore\") as f:
            return f.read()

class CheckRunner(ICheckRunner):
    def __init__(self, config, checks):
        self.config = config
        self.checks = checks

    def run_checks(self, file_path: str, content: str, lines: list) -> list:
        violations = []
        for check in self.checks:
            try:
                check_instance = check(config=self.config)
                violations.extend(check_instance.check(file_path, content, lines))
            except Exception as e:
                pass
        return violations

class AnalysisEngine:'''
)

with open('src/codeguard/core/engine.py', 'w') as f:
    f.write(content)
print('Engine.py refactored with interfaces')
"
git add -A && git commit -m "Extract IFileReader and ICheckRunner interfaces
Decouple file reading and check execution for better testability.

Refs: #$ISSUE_8"

# Update engine to use DI
python3 -c "
with open('src/codeguard/core/engine.py') as f:
    content = f.read()

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

# Update analyze_file to use DI
old_analyze = '''        def analyze_file(file_path):
            file_violations = []
            try:
                with open(file_path, \"r\", encoding=\"utf-8\", errors=\"ignore\") as f:
                    content = f.read()
                lines = content.split(\"\\n\")'''

new_analyze = '''        def analyze_file(file_path):
            file_violations = []
            try:
                content = self.file_reader.read_file(file_path)
                lines = content.split(\"\\n\")'''

content = content.replace(old_analyze, new_analyze)

with open('src/codeguard/core/engine.py', 'w') as f:
    f.write(content)
print('Engine.py updated with dependency injection')
"
git add -A && git commit -m "Add dependency injection to AnalysisEngine
Allow injecting custom file readers and check runners for testing.

Refs: #$ISSUE_8"

git push origin refactor/core-module
echo "Pushed refactor/core-module"

# Branch 9: json-schema (Issue 9)
git checkout main
git checkout -b feature/json-schema

cat > src/codeguard/config_schema.py << 'PYEOF'
"""JSON Schema validation for CodeGuard configuration."""
import json

CODEGUARD_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "CodeGuard Configuration",
    "type": "object",
    "properties": {
        "verbose": {"type": "boolean", "default": False},
        "use_cache": {"type": "boolean", "default": True},
        "cache_dir": {"type": "string", "default": ".codeguard_cache"},
        "severity_threshold": {
            "type": "string",
            "enum": ["low", "medium", "high", "critical"],
            "default": "low",
        },
        "max_workers": {"type": "integer", "minimum": 1, "maximum": 64, "default": 4},
        "timeout": {"type": "integer", "minimum": 1, "default": 60},
        "checks_enabled": {
            "type": "array",
            "items": {"type": "string"},
        },
        "exclude_patterns": {
            "type": "array",
            "items": {"type": "string"},
        },
        "complexity": {
            "type": "object",
            "properties": {
                "max_cyclomatic": {"type": "integer", "minimum": 1, "default": 10},
                "max_cognitive": {"type": "integer", "minimum": 1, "default": 15},
                "max_nesting": {"type": "integer", "minimum": 0, "default": 4},
                "max_lines_per_function": {"type": "integer", "minimum": 1, "default": 50},
                "max_parameters": {"type": "integer", "minimum": 1, "default": 6},
            },
        },
        "style": {
            "type": "object",
            "properties": {
                "max_line_length": {"type": "integer", "minimum": 40, "default": 100},
                "indent": {"type": "integer", "enum": [2, 4], "default": 4},
                "trailing_whitespace": {"type": "boolean", "default": False},
            },
        },
        "security": {
            "type": "object",
            "properties": {
                "level": {"type": "string", "enum": ["low", "medium", "high", "critical"], "default": "high"},
                "check_sql_injection": {"type": "boolean", "default": True},
                "check_path_traversal": {"type": "boolean", "default": True},
                "check_command_injection": {"type": "boolean", "default": True},
            },
        },
    },
}


def validate_config(data: dict) -> list:
    """Validate config data against schema. Returns list of error messages."""
    errors = []
    for key in data:
        if key not in CODEGUARD_SCHEMA["properties"]:
            errors.append(f"Unknown config key: '{key}'")
            continue
        prop = CODEGUARD_SCHEMA["properties"][key]
        if "type" in prop:
            expected_type = prop["type"]
            if expected_type == "integer":
                if not isinstance(data[key], int):
                    errors.append(f"'{key}' must be an integer, got {type(data[key]).__name__}")
            elif expected_type == "boolean":
                if not isinstance(data[key], bool):
                    errors.append(f"'{key}' must be a boolean, got {type(data[key]).__name__}")
            elif expected_type == "string":
                if not isinstance(data[key], str):
                    errors.append(f"'{key}' must be a string, got {type(data[key]).__name__}")
                elif "enum" in prop and data[key] not in prop["enum"]:
                    errors.append(f"'{key}' must be one of {prop['enum']}, got '{data[key]}'")
            elif expected_type == "array":
                if not isinstance(data[key], list):
                    errors.append(f"'{key}' must be an array, got {type(data[key]).__name__}")
        if "minimum" in prop and isinstance(data[key], (int, float)):
            if data[key] < prop["minimum"]:
                errors.append(f"'{key}' minimum is {prop['minimum']}, got {data[key]}")
        if "maximum" in prop and isinstance(data[key], (int, float)):
            if data[key] > prop["maximum"]:
                errors.append(f"'{key}' maximum is {prop['maximum']}, got {data[key]}")
    return errors
PYEOF
git add -A && git commit -m "Add JSON Schema definition for configuration
Define schema for all config options with types, defaults, and validation rules.

Refs: #$ISSUE_9"

# Integrate schema validation into config loading
python3 -c "
with open('src/codeguard/config.py') as f:
    content = f.read()

import_line = 'from codeguard.exceptions import ConfigurationError'
new_import = 'from codeguard.exceptions import ConfigurationError\nfrom codeguard.config_schema import validate_config'

content = content.replace(import_line, new_import)

# Add validation after loading
old_load = '''        with open(path) as f:
                data = yaml.safe_load(f)
        if data is None:'''

new_load = '''        with open(path) as f:
                data = yaml.safe_load(f)
        if data is None:
            return Config.default()
        if isinstance(data, dict):
            errors = validate_config(data)
            if errors:
                import warnings
                for err in errors:
                    warnings.warn(f\"Config warning: {err}\")
        if data is None:'''

content = content.replace(old_load, new_load)

with open('src/codeguard/config.py', 'w') as f:
    f.write(content)
print('Config.py updated with schema validation')
"
git add -A && git commit -m "Integrate JSON Schema validation into config loading
Validate configuration on load and warn about invalid options.

Refs: #$ISSUE_9"

cat > tests/test_config_schema.py << 'PYEOF'
"""Tests for config schema validation."""
from codeguard.config_schema import validate_config


class TestConfigSchema:
    def test_valid_config(self):
        errors = validate_config({"verbose": True, "max_workers": 4})
        assert len(errors) == 0

    def test_invalid_type(self):
        errors = validate_config({"verbose": "not_bool"})
        assert len(errors) > 0

    def test_unknown_key(self):
        errors = validate_config({"unknown_opt": "value"})
        assert len(errors) > 0

    def test_enum_validation(self):
        errors = validate_config({"severity_threshold": "invalid"})
        assert len(errors) > 0

    def test_minimum_validation(self):
        errors = validate_config({"max_workers": 0})
        assert len(errors) > 0
PYEOF
git add -A && git commit -m "Add tests for config schema validation
Test type checking, enum validation, unknown keys, and minimum values.

Refs: #$ISSUE_9"

git push origin feature/json-schema
echo "Pushed feature/json-schema"

# Branch 10: github-action (Issue 10)
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
  checks:
    description: 'Comma-separated checks to run'
    required: false
    default: ''
  format:
    description: 'Output format'
    required: false
    default: 'sarif'
  upload-sarif:
    description: 'Upload SARIF results'
    required: false
    default: 'true'
outputs:
  violations:
    description: 'Number of violations found'
runs:
  using: 'composite'
  steps:
    - run: pip install codeguard
      shell: bash
    - run: |
        ARGS="${{ inputs.path }} --severity ${{ inputs.severity }} --format ${{ inputs.format }}"
        if [ -n "${{ inputs.checks }}" ]; then
          ARGS="$ARGS --checks ${{ inputs.checks }}"
        fi
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
Composite action that installs CodeGuard, runs analysis, and uploads SARIF results.

Refs: #$ISSUE_10"

cat > .github/workflows/codeguard.yml << 'PYEOF'
name: CodeGuard Analysis
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - uses: ./.github/actions/codeguard
        with:
          path: src/
          severity: medium
          format: terminal
PYEOF
git add -A && git commit -m "Add GitHub Actions workflow for CI
Runs CodeGuard on every push and pull request to main branch.

Refs: #$ISSUE_10"

cat > docs/github-actions-integration.md << 'PYEOF'
# GitHub Actions Integration

## Using the CodeGuard Action

```yaml
steps:
  - uses: actions/checkout@v4
  - uses: your-org/codeguard@v1
    with:
      path: src/
      severity: high
      format: sarif
      upload-sarif: true
```

## Standalone Usage

```yaml
steps:
  - uses: actions/setup-python@v5
    with:
      python-version: '3.11'
  - run: pip install codeguard
  - run: codeguard analyze src/ --severity high
```
PYEOF
git add -A && git commit -m "Add GitHub Actions integration documentation
Documentation for using CodeGuard in GitHub CI/CD pipelines.

Refs: #$ISSUE_10"

git push origin feature/github-action
echo "Pushed feature/github-action"

# Branch 11: fix-binary-files (Issue 11)
git checkout main
git checkout -b fix/binary-files

python3 -c "
with open('src/codeguard/core/collector.py') as f:
    content = f.read()

# Add binary file detection
old_class = '''class FileCollector:
    SUPPORTED_EXTENSIONS = {\".py\", \".pyx\", \".pyw\"}'''

new_class = '''import mimetypes

class FileCollector:
    SUPPORTED_EXTENSIONS = {\".py\", \".pyx\", \".pyw\", \".pyi\"}

    BINARY_SIGNATURES = [
        bytes([0x7f, 0x45, 0x4c, 0x46]),  # ELF
        bytes([0x89, 0x50, 0x4e, 0x47]),  # PNG
        bytes([0xff, 0xd8, 0xff]),         # JPEG
        bytes([0x25, 0x50, 0x44, 0x46]),  # PDF
        bytes([0x1f, 0x8b]),               # GZIP
        bytes([0x42, 0x5a]),               # BZIP2
        bytes([0x50, 0x4b]),               # ZIP/DOCX
    ]

    @staticmethod
    def is_binary(filepath: str) -> bool:
        try:
            with open(filepath, 'rb') as f:
                header = f.read(4)
                if not header:
                    return False
                for sig in FileCollector.BINARY_SIGNATURES:
                    if header.startswith(sig):
                        return True
                # Check for null bytes (text files shouldn't have them)
                chunk = f.read(8192)
                return b'\\x00' in chunk
        except IOError:
            return False'''

content = content.replace(old_class, new_class)

# Add binary check to walk
old_walk = '''            for filename in filenames:
                filepath = os.path.join(root, filename)
                if self._is_supported(filepath) and not self._is_excluded(filepath):
                    files.append(filepath)'''

new_walk = '''            for filename in filenames:
                filepath = os.path.join(root, filename)
                if self._is_supported(filepath) and not self._is_excluded(filepath) and not self.is_binary(filepath):
                    files.append(filepath)'''

content = content.replace(old_walk, new_walk)

# Also add to single file check
old_single = '''        for path in paths:
            if os.path.isfile(path):
                if self._is_supported(path) and not self._is_excluded(path):
                    files.append(os.path.abspath(path))'''

new_single = '''        for path in paths:
            if os.path.isfile(path):
                if self._is_supported(path) and not self._is_excluded(path) and not self.is_binary(path):
                    files.append(os.path.abspath(path))'''

content = content.replace(old_single, new_single)

with open('src/codeguard/core/collector.py', 'w') as f:
    f.write(content)
print('Collector.py updated with binary file detection')
"
git add -A && git commit -m "Add binary file detection to file collector
Skip binary files during collection to prevent UnicodeDecodeError.
Check file signatures and null bytes for accurate detection.

Fixes: #$ISSUE_11"

cat > tests/test_binary_detection.py << 'PYEOF'
"""Tests for binary file detection in collector."""
import pytest
from codeguard.core.collector import FileCollector
from codeguard.config import Config


class TestBinaryDetection:
    @pytest.fixture
    def collector(self):
        return FileCollector(config=Config.default())

    def test_binary_detection(self, collector, tmp_path):
        f = tmp_path / "test.exe"
        f.write_bytes(bytes([0x7f, 0x45, 0x4c, 0x46, 0x00, 0x00]))
        assert collector.is_binary(str(f)) is True

    def test_text_file(self, collector, tmp_path):
        f = tmp_path / "test.py"
        f.write_text("print('hello')")
        assert collector.is_binary(str(f)) is False

    def test_binary_skipped(self, collector, tmp_path):
        (tmp_path / "code.py").write_text("x = 1")
        (tmp_path / "data.bin").write_bytes(bytes([0x89, 0x50, 0x4e, 0x47]))
        files = collector.collect([str(tmp_path)])
        assert len(files) == 1
        assert all(f.endswith(".py") for f in files)
PYEOF
git add -A && git commit -m "Add tests for binary file detection
Verify binary signatures are detected and binary files are skipped.

Refs: #$ISSUE_11"

git push origin fix/binary-files
echo "Pushed fix/binary-files"

# Branch 12: auto-fix (Issue 12)
git checkout main
git checkout -b feature/auto-fix

mkdir -p src/codeguard/fixers
cat > src/codeguard/fixers/__init__.py << 'PYEOF'
"""Auto-fix capabilities for CodeGuard issues."""
from codeguard.fixers.base import BaseFixer, FixResult
from codeguard.fixers.whitespace import TrailingWhitespaceFixer
from codeguard.fixers.lines import LineEndingFixer

__all__ = ["BaseFixer", "FixResult", "TrailingWhitespaceFixer", "LineEndingFixer"]
PYEOF
git add -A && git commit -m "Add fixer module structure for auto-fix capability
Base classes and module initialization for fix providers.

Refs: #$ISSUE_12"

cat > src/codeguard/fixers/base.py << 'PYEOF'
"""Base classes for auto-fix functionality."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional
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

    def can_fix(self, file_path: str, content: str) -> bool:
        return True
PYEOF
git add -A && git commit -m "Add BaseFixer abstract class for auto-fix
Define fix interface with fix() and can_fix() methods.

Refs: #$ISSUE_12"

cat > src/codeguard/fixers/whitespace.py << 'PYEOF'
"""Fixer for trailing whitespace issues."""
from typing import List
from codeguard.config import Config
from codeguard.fixers.base import BaseFixer, FixResult


class TrailingWhitespaceFixer(BaseFixer):
    name = "trailing_whitespace"

    def __init__(self, config: Config):
        super().__init__(config)

    def fix(self, file_path: str, content: str, lines: List[str]) -> FixResult:
        fixed_lines = []
        changes = 0
        for line in lines:
            stripped = line.rstrip()
            if stripped != line.rstrip("\n"):
                fixed_lines.append(stripped)
                changes += 1
            elif line.endswith(" \n") or line.endswith("\t\n"):
                fixed_lines.append(line.rstrip() + "\n")
                changes += 1
            else:
                fixed_lines.append(line)
        if changes > 0:
            new_content = "".join(fixed_lines)
            with open(file_path, "w") as f:
                f.write(new_content)
        return FixResult(
            file_path=file_path,
            fixed=changes > 0,
            changes_made=changes,
            description=f"Removed {changes} trailing whitespace issues",
        )
PYEOF
git add -A && git commit -m "Add trailing whitespace auto-fixer
Detect and remove trailing whitespace from Python files.

Refs: #$ISSUE_12"

cat > src/codeguard/fixers/lines.py << 'PYEOF'
"""Fixer for line ending issues."""
from typing import List
from codeguard.config import Config
from codeguard.fixers.base import BaseFixer, FixResult


class LineEndingFixer(BaseFixer):
    name = "line_endings"

    def __init__(self, config: Config):
        super().__init__(config)

    def fix(self, file_path: str, content: str, lines: List[str]) -> FixResult:
        if "\r\n" not in content and "\r" not in content:
            return FixResult(file_path=file_path, fixed=False, changes_made=0, description="No line ending issues")
        new_content = content.replace("\r\n", "\n").replace("\r", "\n")
        changes = content.count("\r\n") + content.count("\r")
        with open(file_path, "w") as f:
            f.write(new_content)
        return FixResult(
            file_path=file_path,
            fixed=True,
            changes_made=changes,
            description=f"Normalized {changes} line endings to LF",
        )
PYEOF
git add -A && git commit -m "Add line ending normalizer fixer
Convert CRLF and CR line endings to LF standard.

Refs: #$ISSUE_12"

# Add CLI fix command
python3 -c "
with open('src/codeguard/cli.py') as f:
    content = f.read()

# Add fix command before the main() function
fix_cmd = '''

@cli.command()
@click.argument(\"paths\", nargs=-1, required=True)
@click.option(\"--dry-run\", is_flag=True, default=False, help=\"Show what would be fixed\")
@click.option(\"--fixers\", \"-F\", default=None, help=\"Comma-separated fixers to run\")
@click.pass_context
def fix(ctx, paths, dry_run, fixers):
    \"\"\"Auto-fix common issues in code.\"\"\"
    from codeguard.fixers.whitespace import TrailingWhitespaceFixer
    from codeguard.fixers.lines import LineEndingFixer
    config = ctx.obj[\"config\"]
    available_fixers = {
        \"trailing_whitespace\": TrailingWhitespaceFixer(config),
        \"line_endings\": LineEndingFixer(config),
    }
    if fixers:
        active = {k: v for k, v in available_fixers.items() if k in fixers.split(\",\")}
    else:
        active = available_fixers
    from codeguard.core.collector import FileCollector
    collector = FileCollector(config)
    files = collector.collect(list(paths))
    total_fixed = 0
    for filepath in files:
        with open(filepath, \"r\", encoding=\"utf-8\", errors=\"ignore\") as f:
            content = f.read()
        lines = content.split(\"\\n\")
        for fixer_name, fixer in active.items():
            result = fixer.fix(filepath, content, lines)
            if result.fixed:
                if dry_run:
                    click.echo(f\"[DRY-RUN] {filepath}: {result.description}\")
                else:
                    click.echo(f\"[FIXED] {filepath}: {result.description}\")
                total_fixed += result.changes_made
            elif not dry_run:
                pass
    if dry_run:
        click.echo(f\"Would fix {total_fixed} issues in {len(files)} files\")
    else:
        click.echo(f\"Fixed {total_fixed} issues in {len(files)} files\")
'''

# Insert before main function
content = content.replace('def main():', fix_cmd + '\ndef main():')

with open('src/codeguard/cli.py', 'w') as f:
    f.write(content)
print('CLI.py updated with fix command')
"
git add -A && git commit -m "Add fix command to CLI for auto-fixing issues
Supports trailing whitespace and line ending fixers with dry-run mode.

Refs: #$ISSUE_12"

cat > tests/test_fixers.py << 'PYEOF'
"""Tests for auto-fix functionality."""
import pytest
from codeguard.config import Config
from codeguard.fixers.whitespace import TrailingWhitespaceFixer
from codeguard.fixers.lines import LineEndingFixer


class TestTrailingWhitespaceFixer:
    @pytest.fixture
    def fixer(self):
        return TrailingWhitespaceFixer(config=Config.default())

    def test_fix_trailing_spaces(self, fixer, tmp_path):
        f = tmp_path / "test.py"
        content = "x = 1   \ny = 2\n"
        f.write_text(content)
        result = fixer.fix(str(f), content, content.split("\n"))
        assert result.fixed is True
        assert result.changes_made > 0
        fixed = f.read_text()
        assert "   \n" not in fixed


class TestLineEndingFixer:
    @pytest.fixture
    def fixer(self):
        return LineEndingFixer(config=Config.default())

    def test_fix_crlf(self, fixer, tmp_path):
        f = tmp_path / "test.py"
        content = "x = 1\r\ny = 2\r\n"
        f.write_text(content)
        result = fixer.fix(str(f), content, content.split("\n"))
        assert result.fixed is True
        fixed = f.read_text()
        assert "\r\n" not in fixed
PYEOF
git add -A && git commit -m "Add tests for auto-fixers
Test trailing whitespace removal and CRLF normalization.

Refs: #$ISSUE_12"

git push origin feature/auto-fix
echo "Pushed feature/auto-fix"

echo ""
echo "=== ALL BRANCHES PUSHED ==="
echo "Now creating pull requests..."
