from flask import Flask
import threading
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "BOT IS ALIVE"

def run():
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)))

def start():
    threading.Thread(target=run, daemon=True).start()
