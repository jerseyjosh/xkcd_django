from typing import Optional
import logging
from dotenv import load_dotenv, find_dotenv
import os
load_dotenv(find_dotenv())

import aiohttp
import asyncio
import aiolimiter

import openai
openai.api_key = os.getenv("OPENAI_API_KEY")

from tqdm.asyncio import tqdm_asyncio

logger = logging.getLogger(__name__)

XKCD_URL_TEMPLATE = "https://xkcd.com/{}/info.0.json"
BAD_COMICS = [404] # comic ids that don't exist (for comedic effect)
TIMEOUT = 20
LIMITER = aiolimiter.AsyncLimiter(max_rate=200, time_period=10)

async def generate_embedding(text: str) -> list:
    """Generate embedding for text"""
    async with LIMITER:
        try:
            client = openai.AsyncClient()
            response = await client.embeddings.create(
                input=text,
                model='text-embedding-3-small'
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            return None
    
async def generate_embeddings(texts: list[str]) -> list[list]:
    """Generate embeddings for multiple texts"""
    return await tqdm_asyncio.gather(*[generate_embedding(text) for text in texts])

def format_date(comic: dict) -> str:
    """Format date from XKCD comic"""
    return f"{comic['year']}-{comic['month']}-{comic['day']}"

async def fetch_latest_comic() -> dict:
    """Fetch latest comic from XKCD"""
    url = XKCD_URL_TEMPLATE.format('')
    # no limiter context as this is only ever called once
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=TIMEOUT)) as session:
        async with session.get(url) as response:
            try:
                response.raise_for_status()
                return await response.json()
            except Exception as e:
                logger.error(f"Error fetching latest comic: {e}")
                return None

async def fetch_comic_by_number(n: int) -> Optional[dict]:
    """Fetch comic by id from XKCD, return None if comic does not exist."""
    if n in BAD_COMICS:
        return None  # Skip known bad comics
    url = XKCD_URL_TEMPLATE.format(n)
    async with LIMITER:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=TIMEOUT)) as session:
            try:
                async with session.get(url) as response:
                    if response.status == 404:
                        return None
                    response.raise_for_status()
                    return await response.json()
            except Exception as e:
                logger.error(f"Error fetching comic #{n}: {e.__class__.__name__} - {e}")
                return None
        
async def fetch_comics_range(start: int, end: int) -> Optional[list[Optional[dict]]]:
    """Fetch a range of comics from XKCD"""
    results = await tqdm_asyncio.gather(
        *[fetch_comic_by_number(i) for i in range(start, end+1)],
        desc=f"Fetching comics {start}-{end}",
        )
    return [r for r in results if r is not None]

async def fetch_all_comics() -> Optional[list[Optional[dict]]]:
    """Fetch all comics from XKCD"""
    latest_comic = await fetch_latest_comic()
    latest_comic_number = int(latest_comic['num'])
    results = await fetch_comics_range(1, latest_comic_number - 1)
    total_results = results + [latest_comic]
    return [r for r in total_results if r is not None]

if __name__ == "__main__":
    #comics = asyncio.run(fetch_all_comics())
    comic = asyncio.run(fetch_comic_by_number(100))
    breakpoint()