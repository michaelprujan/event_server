
from __future__ import annotations
import asyncio
from contextlib import suppress

from event import Event


class Listener:
    def __init__(self, rcv_queue: asyncio.Queue[Event], tx_queue: asyncio.Queue[Event]):
        self._stop_event = asyncio.Event()
        self._task = asyncio.create_task(self._listener_loop())
        self._rcv_queue = rcv_queue
        self._tx_queue = tx_queue
    
    async def _listener_loop(self)->None:
        while not self._stop_event.is_set():
            event = await self.receive()
            await self._tx_queue.put(event)
            
    async def receive(self) -> Event:
        return await self._rcv_queue.get()
    
    async def event(self) -> Event:
        return await self._tx_queue.get()
    
    async def close(self) -> None:
        with suppress(asyncio.CancelledError):
            self._stop_event.set()
            self._task.cancel()
        