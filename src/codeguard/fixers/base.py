from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List
from codeguard.config import Config

@dataclass
class FixResult:
    file_path: str
    fixed: bool
    changes_made: int
    description: str

class BaseFixer(ABC):
    name: str = "base"
    def __init__(self, config: Config):
        self.config = config
    @abstractmethod
    def fix(self, file_path: str, content: str, lines: List[str]) -> FixResult:
        pass
