#!/usr/bin/env python3
import sys
import aiohttp
import asyncio

async def fetch(session, url):
    try:
        async with session.get(url) as response:
            status = response.status
    except aiohttp.ClientError:
        status = 'aiohttp.ClientError'
    return (status, url)

async def get_urls(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(fetch(session, url)) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results
    
if __name__ == '__main__':
    urls = ['https://www.fit.vutbr.cz', 'https://www.szn.cz', 'https://www.alza.cz', 'https://office.com', 'https://aukro.cz']

    if sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    res = asyncio.run(get_urls(urls))

    print(res)