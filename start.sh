#!/bin/sh

echo "🚀 Iniciando Gunicorn..."
gunicorn --bind 0.0.0.0:8000 core.wsgi:application &

echo "🔄 Iniciando Celery Worker..."
celery -A core worker --loglevel=info --queues=generate_certificate,send_notification --uid=celery --gid=celery &


echo "✅ Todos os processos foram iniciados!"
while :; do sleep 3600; done