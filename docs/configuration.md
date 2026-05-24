# Configuration

CodeGuard can be configured using a YAML configuration file.

## Configuration File

By default, CodeGuard looks for `.codeguard.yml` or `.codeguard.yaml` in the current directory or `~/.codeguard.yml`.

## Options

```yaml
# General settings
verbose: false
use_cache: true
cache_dir: .codeguard_cache
severity_threshold: low
max_workers: 4
timeout: 60

# Checks to enable
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

# Patterns to exclude
exclude_patterns:
  - "*.pyc"
  - __pycache__
  - .git
  - venv
  - build
  - dist

# Complexity check settings
complexity:
  max_cyclomatic: 10
  max_cognitive: 15
  max_nesting: 4
  max_lines_per_function: 50
  max_parameters: 6

# Style check settings
style:
  max_line_length: 100
  indent: 4
  trailing_whitespace: false

# Security check settings
security:
  level: high
  check_sql_injection: true
  check_path_traversal: true
  check_command_injection: true

# Performance check settings
performance:
  check_nested_loops: true
  check_large_allocations: true
  check_slow_imports: true

# Documentation check settings
documentation:
  require_docstrings: true
  min_docstring_length: 10
  check_public_api: true
