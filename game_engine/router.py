import pika
import json


class MessageRouter:
    def __init__(self, host="rabbitmq"):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host))
        self.channel = self.connection.channel()

        self.answer_queue = "answer_queue"
        self.fetch_question_queue = "fetch_question_queue"
        self.score_keeper_queue = "score_keeper_queue"
        self.channel.queue_declare(queue=self.answer_queue)
        self.channel.queue_declare(queue=self.fetch_question_queue)
        self.channel.queue_declare(queue=self.score_keeper_queue)

        self.player_count = 0
        self.start_consuming()

    def start_consuming(self):
        queue = "messages_from_clients"  # Queue for messages from WebSocket clients
        self.channel.queue_declare(queue=queue)
        self.channel.basic_consume(
            queue=queue, on_message_callback=self.callback, auto_ack=True
        )
        print("ROUTER: Waiting for messages from WebSocket server...")
        self.channel.start_consuming()

    def callback(self, ch, method, properties, body):
        message = body.decode("utf-8")
        data = json.loads(message)
        print("ROUTER: Received message from WebSocket:", message)

        message_type = self.get_message_type(data)
        print("ROUTER: Message type:", message_type)

        if message_type == "player_count":
            self.player_count = data["count"]
            print("ROUTER: Total players:", self.player_count)
            self.send_to_queue(self.score_keeper_queue, message)
        elif message_type == "fetch_question":
            self.send_to_queue(self.fetch_question_queue, message)
            self.send_to_queue(self.score_keeper_queue, message)
            print("ROUTER: Fetching question...")
        elif message_type == "answer":
            print("ROUTER: Received answer")
            self.send_to_queue(self.answer_queue, message)

    def get_message_type(self, json):
        try:
            return json["type"]
        except json.JSONDecodeError:
            return None

    def send_to_queue(self, queue_name, message):
        self.channel.basic_publish(exchange="", routing_key=queue_name, body=message)

    def close(self):
        self.channel.stop_consuming()
        self.connection.close()
        print("Connection to RabbitMQ closed.")
