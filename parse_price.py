import logging

logging.basicConfig(level=logging.INFO)

def parse_price(price_text):
    try:
        clean = price_text.replace("$", "").replace(",", "").strip()
        return float(clean) if clean else None
    except Exception as e:
        logging.info(f"Could not parse price from '{price_text}': {e}")
        return None
