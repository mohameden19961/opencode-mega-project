# API Reference

## Core API

```python
from codeguard import analyze
from codeguard.config import Config

config = Config.default()
results = analyze(["src/"], config=config)
print(results.count_by_severity())
```

## CLI API

```python
from codeguard.cli import cli
from click.testing import CliRunner

runner = CliRunner()
result = runner.invoke(cli, ["analyze", "src/"])
```

## Check API

```python
from codeguard.checks.base import BaseCheck, CheckRegistry
from codeguard.core.engine import Violation
```
