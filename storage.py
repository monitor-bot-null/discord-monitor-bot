import json
import os

DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"monitors": []}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def add_monitor(user_id, channel_id, username, interval):
    data = load_data()
    data["monitors"].append({
        "user_id": user_id,
        "channel_id": channel_id,
        "username": username,
        "interval": interval,
        "elapsed": 0,
        "status": "unknown"
    })
    save_data(data)

def remove_monitor(user_id, username):
    data = load_data()
    before = len(data["monitors"])
    data["monitors"] = [
        m for m in data["monitors"]
        if not (m["user_id"] == user_id and m["username"] == username)
    ]
    save_data(data)
    return len(data["monitors"]) < before
