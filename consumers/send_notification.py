import json, pika, time
from decouple import config, Csv
import ssl


def send_notification(ch, method, properties, body):
    data = json.loads(body)
    name = data.get('name')
    email = data.get('email')
    time.sleep(3)
    print(f'Notificação enviada: {name} - {email}')
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

    channel.queue_declare(queue='send_notification', durable=True)

    channel.basic_consume(
        queue='send_notification',
        on_message_callback=send_notification,
    )

    channel.start_consuming()
