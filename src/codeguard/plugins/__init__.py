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
