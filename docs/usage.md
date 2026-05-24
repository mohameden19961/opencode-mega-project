# Usage Guide

## Commands

### analyze

The main command to analyze your code:

```bash
codeguard analyze [OPTIONS] PATHS...
```

Options:

| Option | Description |
|--------|-------------|
| `--format, -f` | Output format: terminal, json, html, markdown |
| `--output, -o` | Output file path |
| `--checks, -C` | Comma-separated checks to run |
| `--severity, -s` | Minimum severity: low, medium, high, critical |
| `--verbose, -v` | Enable verbose output |
| `--no-cache` | Disable caching |

### check

Run checks and exit with error code if violations found:

```bash
codeguard check [OPTIONS] PATHS...
```

### report

Generate a detailed report:

```bash
codeguard report --format html --output ./report
```

### init

Generate a default configuration file:

```bash
codeguard init --output .codeguard.yml
```
