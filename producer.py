#!/usr/bin/env python
from faker import Faker

import pika
import json

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='Push App Hold', exchange_type='direct')
channel.queue_declare(queue='push_app_123', durable=True)
channel.queue_bind(exchange='Push App Hold', queue='push_app_123')

def generate_fake_contact():
    fake = Faker()
    full_name = fake.name()
    email = fake.email()
    return full_name, email


def main():
    for i in range(10):
        full_name, email = generate_fake_contact()
        msg = {
            "fullname": full_name,
            "email": email
        }

        channel.basic_publish(exchange='Push App Hold', routing_key='push_app_123', body=json.dumps(msg).encode(),
                              properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))

    connection.close()


if __name__ == '__main__':
    main()