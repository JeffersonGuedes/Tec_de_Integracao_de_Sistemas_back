# gunicorn --bind 0.0.0.0:8000 core.wsgi:application &

# celery -A core beat -l INFO &

# python /consumers/generate_certificate.py &
# python /consumers/send_notification.py &

# tail -f /dev/null

docker-compose up --build
