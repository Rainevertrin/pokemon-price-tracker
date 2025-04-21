import os
from flask import Flask, request
import logging
from threading import Thread
from update_gsheet import update_sheet

logging.basicConfig(level=logging.INFO)

def run_scraper():
    logging.info("Running update_sheet...")
    update_sheet()
    logging.info("Finished update_sheet.")

app = Flask(__name__)

@app.route("/")
def home():
    return "Pokemon Price Tracker is running!"

@app.route("/tasks/schedule", methods=["POST"])
def schedule_task():
    envelope = request.get_json()
    if not envelope:
        return "Bad Request: No Pub/Sub message received", 400

    scraper_thread = Thread(target=run_scraper)
    scraper_thread.start()

    return "Task executed", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)