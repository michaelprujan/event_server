

from typing import Any, Dict, Protocol, Tuple, Union
from dataclasses import dataclass, field

Destination = Union[str, Tuple[str, int]]

@dataclass(frozen=True)
class Event:
    msg: str
    start_time: float
    args: Tuple[Any, ...] = field(default_factory=tuple)
    kwargs: Dict[str, Any] = field(default_factory=dict)
    
    def __str__(self) -> str:
        args_str = ', '.join(repr(arg) for arg in self.args)
        kwargs_str = ', '.join(f"{key}={value!r}" for key, value in self.kwargs.items())
        return (f"Event(msg={self.msg!r}, start_time={self.start_time}, "
                f"args=({args_str}), kwargs={{ {kwargs_str} }})")
    

class EventCreater(Protocol):
    def create(self, msg: str, *args: Any, **kwargs: Any) -> Event:
        raise NotImplementedError


class EventSender(Protocol):
    async def send(self, event: Event, to: Destination) -> None:
        raise NotImplementedError


class EventListener(Protocol):
    async def receive(self) -> Event:
        raise NotImplementedError
    async def close(self) -> None:
        raise NotImplementedError
    async def event(self) -> Event:
        raise NotImplementedError