from celery import shared_task
import time

@shared_task
def send(data):
    name = data.get('name')
    email = data.get('email')
    time.sleep(3)
    print(f'Notificação enviada: {name} - {email}')
