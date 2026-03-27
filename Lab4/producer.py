import pika
import requests
import json

response = requests.get("http://127.0.0.1:5000/orders")
orders = response.json()

connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost')
)
channel = connection.channel()

channel.queue_declare(queue='orders')

for order in orders:
    channel.basic_publish(
        exchange='',
        routing_key='orders',
        body=json.dumps(order)
    )

print("✅ Orders sent to RabbitMQ")
connection.close()