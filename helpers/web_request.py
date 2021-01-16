import aiohttp

async def web_request(url, headers=None):
    async with aiohttp.ClientSession() as session:
        if headers:
            async with session.get(url, headers=headers) as r:
                return (r.status, await r.json())
        else:
            async with session.get(url) as r:
                return (r.status, await r.json())
            