import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(['consumers'])
app.conf.task_routes = {
    'generate_certificate.*': {'queue': 'generate_certificate'},
    'send_notification.*': {'queue': 'send_notification'},
}
