FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    dos2unix \
    gosu \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY start.sh /start.sh
RUN dos2unix /start.sh && \
    chmod +x /start.sh

RUN groupadd -r celeryuser && \
    useradd -r -g celeryuser celeryuser && \
    chown -R celeryuser:celeryuser /app

EXPOSE 8000

CMD ["/start.sh"]