# Getting Started with CodeGuard

## Installation

```bash
pip install codeguard
```

## Basic Usage

```bash
# Analyze a single file
codeguard analyze myfile.py

# Analyze an entire directory
codeguard analyze src/

# Generate an HTML report
codeguard analyze src/ --format html --output report.html

# Run only security checks
codeguard analyze src/ --checks security

# Set severity threshold
codeguard analyze src/ --severity high
```

## Quick Configuration

```bash
# Generate a default configuration file
codeguard init
```

This creates a `.codeguard.yml` file in your project root.
