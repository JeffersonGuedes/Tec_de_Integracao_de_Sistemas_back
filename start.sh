#!/bin/sh

echo "🚀 Iniciando Gunicorn..."
gunicorn --bind 0.0.0.0:8000 core.wsgi:application &

echo "🔄 Iniciando Celery Worker..."
celery -A core worker --uid=celery --gid=celery --loglevel=info --logfile=/var/log/celery/worker.log --statedb=/var/run/celery/worker.state &

echo "🔄 Iniciando Celery Beat..."
celery -A core beat --uid=celery --gid=celery --logfile=/var/log/celery/beat.log &

echo "📨 Iniciando Consumer: generate_certificate.py..."
su -c "python /app/consumers/generate_certificate.py &" celery

echo "📩 Iniciando Consumer: send_notification.py..."
su -c "python /app/consumers/send_notification.py &" celery

echo "✅ Todos os processos foram iniciados!"
while :; do sleep 3600; done