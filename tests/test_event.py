
from typing import Generator, Any
from server.event import Event
import pytest
import time



class SimpleEventCreator:
    def create(self, msg: str, *args: Any, **kwargs: Any) -> Event:
        return Event(msg=msg, start_time=time.time(), args=args, kwargs=kwargs)
    
    
    

@pytest.fixture
def create_simple_event()-> Generator[SimpleEventCreator, None, None]:
    yield SimpleEventCreator()

def test_event_create(create_simple_event: SimpleEventCreator):
    isinstance(create_simple_event.create("Sample event"), Event)
    


    
    