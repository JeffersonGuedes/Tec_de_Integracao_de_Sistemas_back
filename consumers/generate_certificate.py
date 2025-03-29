import json, pika, time
from decouple import config, Csv
import ssl

def generate_certificate(ch, method, properties, body):
    data = json.loads(body)
    name = data.get('name')
    email = data.get('email')
    course = data.get('course')
    time.sleep(5)
    print(f'Certificado gerado: {name} - {email} - {course}')
    ch.basic_ack(delivery_tag=method.delivery_tag)

if __name__ == '__main__':
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=config('RABBITMQ_HOST'),
            port=int(config('RABBITMQ_PORT')),
            virtual_host=config('RABBITMQ_HOST', default='vwikzqcb'),
            credentials=pika.PlainCredentials(
                config('RABBITMQ_USER', default='vwikzqcb'),
                config('RABBITMQ_PASSWORD')
            ),
            ssl_options=pika.SSLOptions(context=ssl_context)
        )
    )

    channel = connection.channel()

    channel.queue_declare(queue='generate_certificate', durable=True)

    channel.basic_consume(
        queue='generate_certificate',
        on_message_callback=generate_certificate
    )

    channel.start_consuming()
