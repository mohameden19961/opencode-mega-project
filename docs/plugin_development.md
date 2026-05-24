# Plugin Development Guide

## Overview

CodeGuard supports plugins - custom checks that extend analysis capabilities.

## Creating a Plugin

1. Create a Python file in `~/.codeguard/plugins/`
2. Define a class inheriting from `BaseCheck`
3. Set `name` and `description` attributes
4. Implement the `check` method

## Example

```python
from codeguard.checks.base import BaseCheck
from codeguard.core.engine import Violation

class MyCheck(BaseCheck):
    name = "my_check"
    description = "My custom check"

    def check(self, file_path, content, lines):
        return []
```
