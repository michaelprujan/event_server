


import asyncio
from contextlib import suppress
from dataclasses import asdict
from typing import Any, Dict, Optional, TypeVar

from asset import Poller
from event import EventListener
from rule import Matcher
import logging

from api import post

T = TypeVar('T')

class Cserver:
    
    def __init__(self, listener: EventListener, poller: Poller, matcher: Matcher, log_file: str, url: str):
        self._listener = listener
        self._poller = poller
        self._matcher = matcher
        self._url = url
        self._log_file = log_file
    
         # Create and configure logger
        logging.basicConfig(
        level=logging.INFO,  # Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL
        format='%(asctime)s - %(levelname)s - %(message)s',  # Log format
        handlers=[
            logging.FileHandler(f"{log_file}"),  # Log to file
        ]
    )

        # Create a logger instance
        self._logger = logging.getLogger()
        
        self._stop_event = asyncio.Event()
        
        self._task: Optional[asyncio.Task[T]] = None # type: ignore
    
    
    def start(self) -> asyncio.Task[str]:
        self._task = asyncio.create_task(self._start())
        
        return self._task
        
        
        
    async def _start(self) -> str:
        while not self._stop_event.is_set():
            event = await self._listener.event()
            assets = await self._poller.assets()
            matched_assets = self._matcher.match_assets(event, assets)
            if matched_assets:
                assets_str = ', '.join(str(asset) for asset in matched_assets)
                line = f"{event} \n {assets_str}"
                self._logger.info(f"{line}")
                
                payload: Dict[str, Any] = {
                            "event": asdict(event),
                            "assets": [asdict(asset) for asset in matched_assets]
                }
                
                await post(url=self._url,
                     payload=payload,
                     retries=2,
                     logger=self._logger)
        
        return "loop_finished"

    async def close(self) -> None:
        await self._listener.close()
        await self._poller.close()
        await self._close()
        
        
    async def _close(self) -> None:
        with suppress(asyncio.CancelledError):
            self._stop_event.set()
            if self._task:
                self._task.cancel()      
            
            
    
