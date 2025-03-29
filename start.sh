#!/bin/sh

echo "🚀 Iniciando Gunicorn..."
gunicorn --bind 0.0.0.0:8000 core.wsgi:application &

echo "🔄 Iniciando Celery Worker..."
celery -A your_project beat --uid= &
celery -A your_project worker --uid= &

echo "📨 Iniciando Consumer: generate_certificate.py..."
python /app/consumers/generate_certificate.py &

echo "📩 Iniciando Consumer: send_notification.py..."
python /app/consumers/send_notification.py &

echo "✅ Todos os processos foram iniciados!"
while :; do sleep 3600; done