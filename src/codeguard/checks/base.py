from abc import ABC, abstractmethod
from typing import List, Dict, Type
from codeguard.config import Config
from codeguard.core.types import Violation


class BaseCheck(ABC):
    name: str = "base"
    description: str = ""

    def __init__(self, config: Config):
        self.config = config

    @abstractmethod
    def check(self, file_path: str, content: str, lines: List[str]) -> List[Violation]:
        pass


class CheckRegistry:
    _checks: Dict[str, Type[BaseCheck]] = {}

    @classmethod
    def register(cls, check_cls: Type[BaseCheck]):
        name = getattr(check_cls, "name", check_cls.__name__)
        cls._checks[name] = check_cls

    @classmethod
    def get(cls, name: str) -> Type[BaseCheck]:
        if name not in cls._checks:
            raise KeyError(f"Check '{name}' not found")
        return cls._checks[name]

    @classmethod
    def get_enabled(cls, enabled_names: List[str]) -> List[Type[BaseCheck]]:
        return [
            cls._checks[name]
            for name in enabled_names
            if name in cls._checks
        ]

    @classmethod
    def all(cls) -> Dict[str, Type[BaseCheck]]:
        return dict(cls._checks)
