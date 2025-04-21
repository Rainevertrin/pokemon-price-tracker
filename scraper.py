import os
from flask import Flask
import logging
from threading import Thread
from update_gsheet import update_sheet

def run_scraper():
    logging.info("Running update_sheet...")
    update_sheet()
    logging.info("Finished update_sheet.")

app = Flask(__name__)

@app.route("/")
def home():
    return "Pokemon Price Tracker is running!"

if __name__ == "__main__":
    scraper_thread = Thread(target=run_scraper)
    scraper_thread.start()

    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)