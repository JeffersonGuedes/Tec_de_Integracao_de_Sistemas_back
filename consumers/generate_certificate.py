from celery import shared_task
import time

@shared_task
def generate(data):
    name = data.get('name')
    email = data.get('email')
    course = data.get('course')
    time.sleep(5)
    print(f'Certificado gerado: {name} - {email} - {course}')
