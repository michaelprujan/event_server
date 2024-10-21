

import argparse
import asyncio
import time
from typing import List

from asset import Asset, Status
from event import Event
from listener import Listener
from matcher import SampleMatcher
from poller import SamplePoller
from cserver import Cserver


def condition1(event: Event, asset: Asset) -> bool:
    return event.msg in asset.status.value

def condition2(event: Event, asset: Asset) -> bool:
    return event.msg  in "error ... "


async def main():
    parser = argparse.ArgumentParser(description="Process a log file and send data to a URL.")
    
    # Add arguments
    parser.add_argument("-l", "--log_file", type=str, required=True, help="Path to the log file")
    parser.add_argument("-u", "--url", type=str, required=True, help="URL to send the log data to")
    parser.add_argument("-i", "--interval", type=float, required=True, help="Polling assets interval in seconds")
    
    args = parser.parse_args()
    
    
    
    rcv_queue: asyncio.Queue[Event] = asyncio.Queue()
    tx_queue : asyncio.Queue[Event] = asyncio.Queue()
    listener = Listener(rcv_queue=rcv_queue, tx_queue=tx_queue)
    for i in range(10):
        event = Event(msg= f"error", start_time=time.time())
        await rcv_queue.put(event)
    
    
    queue: asyncio.Queue[Asset] = asyncio.Queue()
    assets_queue: asyncio.Queue[List[Asset]] = asyncio.Queue()
    poller = SamplePoller(queue=queue, tx_queue=assets_queue, interval=args.interval)
    
    sample_matcher = SampleMatcher(queue=assets_queue)
    sample_matcher.add_rule(condition=condition1,
                     description="event message in asset status",
                     priority=1)
    
    sample_matcher.add_rule(condition=condition2,
                     description="event message in error string",
                     priority=1)
    
    
    
    
    for i in range(5):
        asset = Asset(name= f"asset{i}", status=Status.ERROR)
        await queue.put(asset)
    
    
    
    cserver = Cserver(listener=listener,
                      poller=poller,
                      matcher=sample_matcher, # type: ignore
                      log_file=args.log_file,
                      url = args.url)
    
    
    try:
        task = None
        print(f"Server started !!!")
        task = cserver.start()
        await task
    except Exception as ex:
        print(f"Server finished ith exception {ex}")
    finally:
        await cserver.close()
           
    
    
if __name__ == "__main__":
    asyncio.run(main())