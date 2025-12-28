import time
import asyncio
from storage import load_data, save_data

TICK = 15

async def scheduler_loop(check_fn):
    while True:
        data = load_data()
        now = time.time()
        updated = False

        for monitor in data["monitors"].values():
            if now - monitor["last_checked"] >= monitor["interval"]:
                await check_fn(monitor)
                monitor["last_checked"] = now
                updated = True

        if updated:
            save_data(data)

        await asyncio.sleep(TICK)
