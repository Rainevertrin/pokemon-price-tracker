import os
from flask import Flask
import logging

from update_gsheet import update_sheet

def run_scraper():
    logging.info("Running update_sheet...")
    update_sheet()
    logging.info("Finished update_sheet.")

if __name__ == "__main__":
    run_scraper()

    app = Flask(__name__)
    @app.route("/")
    def home():
        return "Pokemon Price Tracker is running!"

    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
