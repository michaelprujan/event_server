
from __future__ import annotations
from typing import Callable, List, Protocol, Set, TypeVar
import uuid

from asset import Asset
from event import Event

T = TypeVar('T')
V = TypeVar('V')

Condition = Callable[[T, V], bool]
class Rule:
    def __init__(self, 
                 condition: Condition[T, V], 
                 description: str, 
                 priority: int = 0
    ):
        self._condition = condition
        self._description = description
        self._priority = priority
        self._uuid = uuid.uuid4()

    
    def condition(self, t: T, v: V) -> bool: # type: ignore
        return self._condition(t, v) # type: ignore
    
    @property
    def uuid(self) -> uuid.UUID:
        return self._uuid
    
class Matcher(Protocol):
    def add_rule(self, condition: Callable[[T], bool], description: str, priority: int) -> None:
        raise NotImplementedError
    
    def match_rules(self, event: Event, assets: List[Asset]) -> Set[uuid.UUID]:
        raise NotImplementedError
     
    def match_assets(self, event: Event, assets: List[Asset]) -> Set[Asset]:
        raise NotImplementedError
    
