
from dataclasses import dataclass
from enum import Enum
from typing import List, Protocol


class Status(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"
    
@dataclass(frozen=True)
class Asset:
    name: str
    status : Status
    
    def __str__(self) -> str:
        return f"Asset(name={self.name}, status={self.status})"


class Poller(Protocol):
    async def poll(self, interval: float = 0) -> None:
        raise NotImplementedError
    
    async def assets(self) -> List[Asset]:
        raise NotImplementedError
    
    async def close(self) -> None:
        raise NotImplementedError




