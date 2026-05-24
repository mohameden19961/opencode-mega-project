# CodeGuard

A comprehensive Python code quality and security analysis tool.

## Features

- Code complexity analysis
- Style checking and linting
- Security vulnerability detection
- Performance bottleneck identification
- Documentation coverage analysis
- Import organization checking
- Code duplication detection
- Type annotation verification
- Multiple output formats (JSON, HTML, Markdown, Terminal)
- Parallel analysis support
- Caching for improved performance

## Installation

```bash
pip install codeguard
```

## Quick Start

```bash
codeguard analyze src/
codeguard check --security high
codeguard report --format html
```

## Configuration

Create a `.codeguard.yml` file in your project root:

```yaml
checks:
  complexity:
    max_cyclomatic: 10
    max_cognitive: 15
  style:
    max_line_length: 100
    indent: 4
  security:
    level: high
    exclude:
      - "tests/**"
```

## Output Formats

- Terminal (default, colorized)
- JSON (machine-readable)
- HTML (detailed report)
- Markdown (documentation-friendly)

## CI/CD Integration

```yaml
# GitHub Actions example
- name: Run CodeGuard
  run: |
    pip install codeguard
    codeguard analyze src/ --format json --output report.json
```
