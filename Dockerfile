FROM python:3.11-slim

# Install dependencies
RUN apt-get update && apt-get install -y chromium chromium-driver && \
    pip install --upgrade pip

# Set environment variables for Chromium
ENV CHROME_BIN=/usr/bin/chromium
ENV PATH="/usr/lib/chromium:/usr/lib/chromium/chromedriver:$PATH"

# Set working directory
WORKDIR /app

# Copy your project files
COPY . .

# Install Python requirements
RUN pip install -r requirements.txt

CMD ["python", "Logement_headless_edits.py"]
