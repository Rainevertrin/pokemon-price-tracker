import time

import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager

from parse_price import parse_price

class TCGScraper:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--blink-settings=imagesEnabled=false")
        options.page_load_strategy = "eager"

        capabilities = DesiredCapabilities.CHROME.copy()
        capabilities["acceptSslCerts"] = True
        capabilities["acceptInsecureCerts"] = True

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.wait = WebDriverWait(self.driver, 20)

    def get_market_price(self, link, retries=3, delay=3):
        logging.info(f"Attempting to scrape: {link}")

        for attempt in range(1, retries + 1):
            try:
                self.driver.get(link)

                price_elem = self.wait.until(
                    EC.presence_of_element_located((By.CLASS_NAME, "price-points__upper__price"))
                )
                price_text_raw = price_elem.text
                logging.info(f"Raw price text found: '{price_text_raw}' for {link}")

                price_value = parse_price(price_text_raw)

                if price_value is not None:
                    return price_value
                else:
                    logging.warning(f"Parsed price is None (Attempt {attempt}/{retries})")

            except Exception as e:
                logging.error(f"Error scraping {link} (Attempt {attempt}/{retries}): {e}")

            if attempt < retries:
                logging.info(f"Retrying after {delay} seconds...")
                time.sleep(delay)

        logging.error(f"Failed to get a valid price after {retries} attempts for {link}")
        return None

    def close(self):
        self.driver.quit()
