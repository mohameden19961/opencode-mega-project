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
