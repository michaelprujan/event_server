
import time
from typing import List
from server.asset import Asset, Status
from server.event import Event
from server.matcher import SampleMatcher


def condition1(event: Event, asset: Asset) -> bool:
    return event.msg in asset.status.value

def condition2(event: Event, asset: Asset) -> bool:
    return event.msg  in "error ... "

def test_rule():
    
    assets:List[Asset] = [
        Asset(name="ports", status=Status.ACTIVE),
        Asset(name="cards", status=Status.INACTIVE),
        Asset(name="process", status=Status.ERROR)]
    matcher = SampleMatcher(assets)
    
    matcher.add_rule(condition=condition1,
                     description="event message in asset status",
                     priority=1)
    
    matcher.add_rule(condition=condition2,
                     description="event message in error string",
                     priority=1)
    
    
    event = Event(msg="error", start_time=time.time())
    rules = matcher.match_rules(event)
    assert rules
    assert len(rules) == 2
    
    