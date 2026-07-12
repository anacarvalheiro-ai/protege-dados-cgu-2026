from __future__ import annotations
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

class Connector(ABC):
    id: str
    @abstractmethod
    def fetch(self, destination: Path) -> Path: ...
    @abstractmethod
    def metadata(self) -> dict[str, Any]: ...
