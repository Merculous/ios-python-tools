
import aiohttp
import asyncio

from .utils import showProgress


async def getURLData(session, url: str) -> str:
    async with session.get(url) as r:
        if r.status == 404:
            print('Server returned no response... are you blacklisted?')
        elif r.status == 429: # We shouldn't hit this, but for sanity...
            print('Server is asking us to slow down...')
            wait = int(r.headers['Retry-After'])
            print(f'Waiting {wait} seconds...')
            asyncio.sleep(wait)
            getURLData(session, url)
        elif r.status == 200:
            return await r.text()
        else:
            print(f'Server error: {r.code}')
