import os
import datetime
import logging
from auth_gsheet import auth_gsheet
from tcg_scraper import TCGScraper

def update_sheet():
    logging.info("Updating gsheet")
    client = auth_gsheet()
    url = os.environ.get("GSHEET_URL")
    sheet = client.open_by_url(url).sheet1

    data = sheet.get_all_values()
    headers = data[0]
    rows = data[1:]

    link_col = headers.index("Link")
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    new_price_col = f"Price-{current_date}"

    scraper = TCGScraper()
    price_col_index = len(headers)

    sheet.update_cell(1, price_col_index + 1, new_price_col)

    for i, row in enumerate(rows, start=2):
        link = row[link_col]
        new_price = scraper.get_market_price(link)
        logging.info(f"New price: {new_price}")
        if new_price is None:
            continue
        sheet.update_cell(i, price_col_index + 1, new_price)

    scraper.close()
