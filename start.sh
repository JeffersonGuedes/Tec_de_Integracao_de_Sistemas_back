#!/bin/sh

echo "🚀 Iniciando Gunicorn..."
gunicorn --bind 0.0.0.0:8000 core.wsgi:application &

echo "🔄 Iniciando Celery Worker..."
celery -A core worker --uid= --gid= --loglevel=info &

echo "🔄 Iniciando Celery Beat..."
celery -A core beat --uid= --gid= &

echo "📨 Iniciando Consumer: generate_certificate.py..."
python /app/consumers/generate_certificate.py &

echo "📩 Iniciando Consumer: send_notification.py..."
python /app/consumers/send_notification.py &

echo "✅ Todos os processos foram iniciados!"
while :; do sleep 3600; done