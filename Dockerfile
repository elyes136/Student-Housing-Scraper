FROM python:3.10-slim

# Install Chromium and Chromedriver only
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set environment variables so Selenium can find Chromium
ENV CHROME_BIN=/usr/bin/chromium
ENV PATH="/usr/lib/chromium:/usr/lib/chromium/chromedriver:$PATH"

# Set working directory
WORKDIR /app

# Copy code and install Python dependencies
COPY Logement_headless_edits.py .
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Run the script
CMD ["python", "Logement_headless_edits.py"]
