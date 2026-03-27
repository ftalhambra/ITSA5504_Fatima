import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost')
)
channel = connection.channel()

channel.queue_declare(queue='orders')

def callback(ch, method, properties, body):
    print("📩 Received:", body.decode())

channel.basic_consume(
    queue='orders',
    on_message_callback=callback,
    auto_ack=True
)

print("✅ Waiting for messages...")
channel.start_consuming()