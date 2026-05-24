# Pre-commit Integration

## Using with pre-commit framework
Add to `.pre-commit-config.yaml`:
```yaml
repos:
  - repo: https://github.com/mohameden19961/opencode-mega-project
    rev: v0.1.0
    hooks:
      - id: codeguard
```

## Manual installation
```bash
ln -s ../../scripts/pre-commit.sh .git/hooks/pre-commit
```
