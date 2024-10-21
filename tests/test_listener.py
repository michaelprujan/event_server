
import pytest
import asyncio
from server.event import Event
from server.listener import Listener
import time


@pytest.mark.asyncio
async def test_rcv_event():
    rcv_queue: asyncio.Queue[Event] = asyncio.Queue()
    tx_queue : asyncio.Queue[Event] = asyncio.Queue()
    
    _ = Listener(rcv_queue=rcv_queue, tx_queue=tx_queue)
    
    for i in range(5):
        event = Event(f"Event {i}", start_time=time.time())
        await rcv_queue.put(event)
    
    await asyncio.sleep(0.1)
    
    assert tx_queue.qsize() == 5


@pytest.mark.asyncio
async def test_close():
    rcv_queue: asyncio.Queue[Event] = asyncio.Queue()
    tx_queue : asyncio.Queue[Event] = asyncio.Queue()
    
    listener = Listener(rcv_queue=rcv_queue, tx_queue=tx_queue)
    
    await asyncio.sleep(0.1)
    await listener.close()
    
    assert tx_queue.qsize() == 0