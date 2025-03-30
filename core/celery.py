import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(['consumers'])
app.conf.task_routes = {
    'consumers.generate_certificate.generate': {'queue': 'generate_certificate'},
    'consumers.send_notification.send': {'queue': 'send_notification'},
}