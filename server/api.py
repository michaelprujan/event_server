
import logging
import httpx
from typing import Dict, Any

async def post(url: str, payload: Dict[str, Any], retries: int, logger: logging.Logger) -> int: # type: ignore
    for _ in range(retries):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload) # type: ignore
                if response.status_code == 200:
                    logger.info(f"Send to {url} {payload} succeeded !!!")
                    return response.status_code
                else:
                    logger.error(f"Send to {url} {payload} failed with code {response.status_code} {response.text} ")
        except httpx.RequestError as e:
            logging.error(f"Error occurred: {e}")
            raise
    
    logger.error(f"The number of retries excededed {retries}")
    raise ValueError(f"The number of retries excededed {retries}")
    
            