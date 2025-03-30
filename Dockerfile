FROM python:3.11-slim


RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    dos2unix \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd -r celery && useradd -r -g celery celery

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /var/log/celery /var/run/celery && \
    chown -R celery:celery /var/log/celery /var/run/celery

COPY start.sh /start.sh
RUN dos2unix /start.sh && \
    chmod +x /start.sh

EXPOSE 8000

CMD ["sh", "/start.sh"]
