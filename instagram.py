import os
import aiohttp

PROXY = os.getenv("WINDSCRIBE_PROXY")

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

async def check_instagram_status(username):
    url = f"https://www.instagram.com/{username}/"

    async with aiohttp.ClientSession(headers=HEADERS) as session:
        async with session.get(
            url,
            proxy=PROXY,
            timeout=aiohttp.ClientTimeout(total=15)
        ) as resp:
            return resp.status == 200
