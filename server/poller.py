
from __future__ import annotations
import asyncio
from typing import List

from asset import Asset

class SamplePoller:
    def __init__(self, queue: asyncio.Queue[Asset], tx_queue: asyncio.Queue[List[Asset]], interval: float):
        self._stop_event = asyncio.Event()
        self._task = asyncio.create_task(self.poll(interval))
        self._queue = queue
        self._tx_queue = tx_queue
        
    
    async def poll(self, interval: float = 0) -> None:
        polled_assets: List[Asset] = []
        while not self._stop_event.is_set():
            try:
                asset = await asyncio.wait_for(self._queue.get(), timeout=interval)
                polled_assets.append(asset)
            except asyncio.TimeoutError:
                await self._tx_queue.put(polled_assets)
    
    
    async def assets(self) -> List[Asset]:
        assets = await self._tx_queue.get()
        
        return assets
                
            
    
    async def close(self) -> None:
        self._stop_event.set()
        await self._task