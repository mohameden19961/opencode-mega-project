<div align="center">

# 🛡️ CodeGuard

**Python Code Quality & Security Analysis Tool**

[![License: MIT](https://img.shields.io/badge/License-MIT-6E40C9?style=flat-square)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Commits](https://img.shields.io/badge/1,500_commits-22d3ee?style=flat-square)](https://github.com/mohameden19961/codeguard)
[![PRs](https://img.shields.io/badge/12_PR_merged-10b981?style=flat-square)](https://github.com/mohameden19961/codeguard/pulls)
[![Release](https://img.shields.io/badge/v0.2.0-6E40C9?style=flat-square)](https://github.com/mohameden19961/codeguard/releases)

---

<p align="center">
  <b>Analyze</b> •
  <b>Detect</b> •
  <b>Fix</b> •
  <b>Report</b>
</p>

**CodeGuard** is a comprehensive static analysis tool that scans your Python codebase for complexity issues, security vulnerabilities, style violations, performance bottlenecks, and more — with multiple output formats, auto-fix capabilities, and CI/CD integration.

```text
$ codeguard analyze src/

[21:10:52] [INFO] Running 9 checks on 279 files
[21:10:52] [INFO] Analysis complete: 556 violations in 279 files (0.58s)

==========================================================
  Severity Breakdown:
    high      :    5  #####
    low       :  176  ########################################
    medium    :  375  ########################################
==========================================================
```

[![GitHub Pages](https://img.shields.io/badge/GitHub_Pages-live-22d3ee?style=flat-square)](https://mohameden19961.github.io/codeguard/)
[![PyPI](https://img.shields.io/badge/PyPI-coming_soon-3776AB?style=flat-square&logo=pypi&logoColor=white)](https://pypi.org/project/codeguard/)

</div>

---

## ✨ Features

| Category | Capabilities |
|----------|-------------|
| 🔍 **Code Analysis** | Cyclomatic complexity, nesting depth, function length, parameter count |
| 🛡️ **Security** | SQL injection, command injection, path traversal, dangerous functions |
| 🎨 **Style** | Line length, trailing whitespace, naming conventions, import order |
| ⚡ **Performance** | Nested loops, memory allocation, slow imports |
| 📚 **Documentation** | Module/function/class docstrings, coverage analysis |
| 🔄 **Duplication** | Code clone detection, similarity analysis |
| 🏷️ **Typing** | Type annotation coverage, return types, parameter types |

### 🚀 Advanced Features

- **Plugin System** — Custom checks via `~/.codeguard/plugins/`
- **Auto-Fix** — Trailing whitespace & line ending normalization
- **Interactive Dashboard** — HTML reports with Chart.js charts
- **SARIF Format** — GitHub Code Scanning integration
- **Pre-commit Hooks** — Built-in `.pre-commit-hooks.yaml`
- **GitHub Action** — Composite action with SARIF upload
- **JSON Schema** — Config validation with helpful warnings
- **Incremental Scanning** — Skip unchanged files via hash tracking
- **LRU Cache** — Bounded memory cache for repeated runs

---

## 📦 Installation

```bash
# From source
git clone https://github.com/mohameden19961/codeguard.git
cd codeguard
pip install -e .

# Quick install
pip install -e .  # after cloning
```

---

## 🚀 Quick Start

```bash
# Analyze a file or directory
codeguard analyze src/

# Check with severity threshold
codeguard check src/ --severity high

# Generate HTML dashboard
codeguard analyze src/ --format html --output report.html

# Auto-fix issues
codeguard fix src/ --fixers trailing_whitespace,line_endings

# Generate SARIF for GitHub Code Scanning
codeguard analyze src/ --format sarif --output results.sarif

# Init default config
codeguard init
```

---

## 📋 Commands

| Command | Description |
|---------|-------------|
| `analyze` | Run full analysis on paths |
| `check` | Run checks, exit 1 if violations found (CI mode) |
| `report` | Generate detailed report |
| `fix` | Auto-fix common issues (trailing whitespace, line endings) |
| `init` | Create default `.codeguard.yml` |

---

## ⚙️ Configuration

```yaml
# .codeguard.yml
verbose: false
use_cache: true
severity_threshold: medium
max_workers: 4
checks_enabled:
  - complexity
  - style
  - security
  - performance
  - documentation
  - naming
  - imports
  - duplication
  - typing
exclude_patterns:
  - "*.pyc"
  - __pycache__
  - .git
  - venv
  - build
  - dist
complexity:
  max_cyclomatic: 10
  max_nesting: 4
  max_lines_per_function: 50
  max_parameters: 6
style:
  max_line_length: 100
  indent: 4
security:
  level: high
  check_sql_injection: true
  check_path_traversal: true
  check_command_injection: true
```

---

## 📊 Output Formats

| Format | File | Use Case |
|--------|------|----------|
| **Terminal** | stdout | Local development |
| **JSON** | `.json` | Machine-readable / CI |
| **HTML** | `.html` | Detailed reports |
| **Markdown** | `.md` | Documentation |
| **Dashboard** | `.html` | Interactive charts (Chart.js) |
| **SARIF** | `.sarif` | GitHub Code Scanning |

---

## 🧩 Plugin System

```python
# ~/.codeguard/plugins/my_check.py
from codeguard.checks.base import BaseCheck
from codeguard.core.engine import Violation

class MyCheck(BaseCheck):
    name = "my_check"
    description = "My custom check"
    
    def check(self, file_path, content, lines):
        violations = []
        # Your logic here
        return violations
```

---

## 🔄 CI/CD Integration

### GitHub Actions

```yaml
steps:
  - uses: actions/checkout@v4
  - uses: actions/setup-python@v5
    with: {python-version: "3.11"}
  - run: pip install codeguard
  - run: codeguard check src/ --severity high
```

### Pre-commit

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/mohameden19961/codeguard
    rev: v0.2.0
    hooks:
      - id: codeguard
```

---

## 📁 Project Structure

```
codeguard/
├── src/codeguard/
│   ├── cli.py              # CLI entry point
│   ├── config.py            # Configuration module
│   ├── config_schema.py     # JSON Schema validation
│   ├── core/
│   │   ├── engine.py        # Analysis engine
│   │   ├── collector.py     # File discovery
│   │   ├── scanner.py       # Incremental scanner
│   │   ├── reporter.py      # Report generation
│   │   └── formatter.py     # Results formatting
│   ├── checks/
│   │   ├── base.py          # Base check + registry
│   │   ├── complexity.py    # Complexity analysis
│   │   ├── style.py         # Style checks
│   │   ├── security.py      # Security audits
│   │   ├── performance.py   # Performance checks
│   │   ├── documentation.py # Docstring checks
│   │   ├── naming.py        # Naming conventions
│   │   ├── imports.py       # Import organization
│   │   ├── duplication.py   # Clone detection
│   │   └── typing.py        # Type annotation checks
│   ├── output/
│   │   ├── terminal_writer.py
│   │   ├── json_writer.py
│   │   ├── html_writer.py
│   │   ├── markdown_writer.py
│   │   ├── dashboard.py     # Chart.js dashboard
│   │   └── sarif_writer.py  # SARIF 2.1.0
│   ├── fixers/
│   │   ├── base.py          # Fixer interface
│   │   ├── whitespace.py    # Trailing whitespace
│   │   └── lines.py         # Line endings
│   ├── plugins/
│   │   ├── __init__.py      # Plugin manager
│   │   └── example_plugin.py
│   └── utils/
│       ├── cache.py         # LRU cache
│       ├── parallel.py      # Thread pool
│       ├── timer.py         # Performance timer
│       ├── log.py           # Logger
│       ├── fs.py            # File system helpers
│       └── ast_utils.py     # AST parsing
├── tests/
│   ├── test_engine.py
│   ├── test_*.py            # 60+ test files
│   └── fixtures/
├── docs/
│   ├── getting-started.md
│   ├── usage.md
│   ├── configuration.md
│   ├── checks.md
│   ├── plugin_development.md
│   └── pre-commit-integration.md
├── examples/
├── config/
└── .github/actions/codeguard/
```

---

## 🧪 Running Tests

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run all tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=src/codeguard --cov-report=term-missing
```

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📜 Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

---

## 🔒 Security

See [SECURITY.md](SECURITY.md) for policy.

---

## 📄 License

MIT — see [LICENSE](LICENSE).

---

<div align="center">

**Built with 1,500 commits • 12 PRs • 32 files**  
[![GitHub](https://img.shields.io/badge/GitHub-mohameden19961-181717?style=flat-square&logo=github)](https://github.com/mohameden19961)

</div>
