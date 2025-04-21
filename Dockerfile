# Use an official Python slim image
FROM python:3.12

WORKDIR /app

RUN apt-get update && apt-get install -y wget gnupg2 curl ca-certificates fonts-liberation libappindicator3-1 libasound2 libatk-bridge2.0-0 libatk1.0-0 libcups2 libdbus-1-3 libgdk-pixbuf2.0-0 libnspr4 libnss3 libx11-xcb1 libxcomposite1 libxdamage1 libxrandr2 xdg-utils --no-install-recommends

RUN curl -sSL https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o chrome.deb && \
    apt-get install -y ./chrome.deb && \
    rm chrome.deb

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application files
COPY scraper.py auth_gsheet.py update_gsheet.py tcg_scraper.py ./

ENV PORT=8080

# Start app
CMD ["python", "scraper.py"]