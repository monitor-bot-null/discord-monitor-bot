import json
from pathlib import Path

DATA_FILE = Path("data.json")

def load_data():
    if not DATA_FILE.exists():
        return {"monitors": {}}
    return json.loads(DATA_FILE.read_text())

def save_data(data):
    DATA_FILE.write_text(json.dumps(data, indent=2))

def add_monitor(user_id, channel_id, username, interval):
    data = load_data()
    key = f"{user_id}:{username}"

    data["monitors"][key] = {
        "user_id": user_id,
        "channel_id": channel_id,
        "username": username,
        "interval": interval,
        "last_checked": 0,
        "status": "unknown"
    }

    save_data(data)

def remove_monitor(user_id, username):
    data = load_data()
    key = f"{user_id}:{username}"

    if key in data["monitors"]:
        del data["monitors"][key]
        save_data(data)
        return True
    return False
