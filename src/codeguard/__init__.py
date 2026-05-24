from codeguard.version import VERSION
from codeguard.core.engine import analyze
from codeguard.cli import main

__version__ = VERSION
__all__ = ["analyze", "main", "__version__"]
