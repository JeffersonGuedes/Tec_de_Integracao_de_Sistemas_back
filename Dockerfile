FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    dos2unix \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY start.sh /start.sh
RUN dos2unix /start.sh && \
    chmod +x /start.sh

ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["sh", "/start.sh"]
