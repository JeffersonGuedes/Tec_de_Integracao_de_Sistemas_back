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
    
    connection_url = "amqps://vwikzqcb:fTW3QlPy2o6Ob-OskLxIxyBTP2-qpdf6@jackal.rmq.cloudamqp.com/vwikzqcb"
    connection = pika.BlockingConnection(pika.URLParameters(connection_url))

    channel = connection.channel()

    channel.queue_declare(queue='send_notification', durable=True)

    channel.basic_consume(
        queue='send_notification',
        on_message_callback=send_notification,
    )

    channel.start_consuming()
