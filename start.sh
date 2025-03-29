adduser -D celeryuser

chown -R celeryuser:celeryuser /app

su-exec celeryuser gunicorn --bind 0.0.0.0:8000 core.wsgi:application &
su-exec celeryuser celery -A core worker -l INFO --uid=celeryuser --gid=celeryuser &
su-exec celeryuser celery -A core beat -l INFO --uid=celeryuser --gid=celeryuser &

su-exec celeryuser python /app/consumers/generate_certificate.py &
su-exec celeryuser python /app/consumers/send_notification.py &

tail -f /dev/null