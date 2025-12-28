import asyncio
from storage import load_data, save_data

async def scheduler_loop(monitor_task):
    while True:
        data = load_data()
        for monitor in data["monitors"]:
            monitor["elapsed"] += 1
            if monitor["elapsed"] >= monitor["interval"]:
                monitor["elapsed"] = 0
                await monitor_task(monitor)
        save_data(data)
        await asyncio.sleep(1)
