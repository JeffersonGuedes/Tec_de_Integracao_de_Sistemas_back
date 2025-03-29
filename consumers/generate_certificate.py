import json, pika, time
from decouple import config, Csv


def generate_certificate(ch, method, properties, body):
    data = json.loads(body)
    name = data.get('name')
    email = data.get('email')
    course = data.get('course')
    time.sleep(5)
    print(f'Certificado gerado: {name} - {email} - {course}')
    ch.basic_ack(delivery_tag=method.delivery_tag)

if __name__ == '__main__':
    connection = pika.BlockingConnection(
        pika.URLParameters(
            f"amqps://{config('RABBITMQ_USER')}:{config('RABBITMQ_PASSWORD')}@{config('RABBITMQ_HOST')}:{config('RABBITMQ_PORT')}/{config('RABBITMQ_VIRTUAL_HOST', default='vwikzqcb')}"
        )
    )

    channel = connection.channel()

    channel.queue_declare(queue='generate_certificate', durable=True)

    channel.basic_consume(
        queue='generate_certificate',
        on_message_callback=generate_certificate
    )

    channel.start_consuming()
