echo "🔄 Iniciando Celery Worker..."
celery -A core worker --loglevel=info --queues=generate_certificate,send_notification --uid=celery --gid=celery &

echo "📨 Iniciando Consumer: generate_certificate.py..."
su -c "python /app/consumers/generate_certificate.py &" celery &

echo "📩 Iniciando Consumer: send_notification.py..."
su -c "python /app/consumers/send_notification.py &" celery &

echo "🚀 Iniciando Gunicorn..."
gunicorn --bind 0.0.0.0:8000 core.wsgi:application 

echo "✅ Todos os processos foram iniciados!"
while :; do sleep 3600; done