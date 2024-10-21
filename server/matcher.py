from typing import Callable, List, Set, TypeVar
from uuid import UUID
import asyncio

from asset import Asset
from event import Event
from rule import Rule

T = TypeVar('T')
V = TypeVar('V')
class SampleMatcher:
    def __init__(self, queue: asyncio.Queue[List[Asset]]):
        self._queue = queue
        self._rules: List[Rule[T]] = []

    def add_rule(self, condition: Callable[[T, V], bool], description: str, priority: int) -> None:
        rule = Rule(condition=condition,
                    description=description,
                    priority=priority)
        
        self._rules.append(rule)

    def match_rules(self, event: Event, assets: List[Asset]) -> Set[UUID]:
        rules: Set[UUID] = set()

        for rule in self._rules:
            for asset in assets:
                if rule.condition(event, asset):
                    rules.add(rule.uuid)

        return rules
    
    def match_assets(self, event: Event, assets: List[Asset]) -> Set[Asset]:
        matched_assets: Set[Asset] = set()
       
        for rule in self._rules:
            for asset in assets:
                if rule.condition(event, asset):
                    try:
                        matched_assets.add(asset)
                    except Exception as ex:
                        print(f"{ex}")
                    
        return matched_assets
    
    