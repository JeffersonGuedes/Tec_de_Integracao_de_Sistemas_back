echo "🔧 Configurando permissões..."
chown -R celeryuser:celeryuser /app

echo "🚀 Iniciando serviços como celeryuser..."

gosu celeryuser gunicorn --bind 0.0.0.0:8000 core.wsgi:application &

gosu celeryuser celery -A core worker -l INFO --uid=celeryuser --gid=celeryuser &

gosu celeryuser celery -A core beat -l INFO --uid=celeryuser --gid=celeryuser &

gosu celeryuser python /app/consumers/generate_certificate.py &
gosu celeryuser python /app/consumers/send_notification.py &

echo "✅ Todos os serviços iniciados!"
while true; do
    sleep 60
    if ! pgrep -f "gunicorn|celery" > /dev/null; then
        echo "⚠️ Nenhum processo principal encontrado, encerrando..."
        exit 1
    fi
done