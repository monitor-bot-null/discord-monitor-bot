import aiohttp

async def check_instagram_status(username: str) -> bool:
    url = f"https://www.instagram.com/{username}/"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=10) as resp:
            return resp.status == 200
