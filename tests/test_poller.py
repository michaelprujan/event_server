
from typing import List
import pytest
import asyncio
from server.asset import Asset, Status
from server.poller import SamplePoller


@pytest.mark.asyncio
async def test_poller_close():
    queue: asyncio.Queue[Asset] = asyncio.Queue()
    tx_queue: asyncio.Queue[List[Asset]] = asyncio.Queue()

    
    poller = SamplePoller(queue=queue, tx_queue=tx_queue, interval=0.2)
    
    for i in range(10):
        asset = Asset(name= f"asset{i}", status=Status.ACTIVE)
        await queue.put(asset)
    
    await asyncio.sleep(0.1)
    
    await poller.close()
    
    assert True
