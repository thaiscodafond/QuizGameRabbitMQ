import pika


class QueueCreator:
    def __init__(self, host="rabbitmq"):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host))
        self.channel = self.connection.channel()

        self.message_queue = "messages_from_clients"
        self.message_to_queue = "messages_to_clients"
        self.answer_queue = "answer_queue"
        self.fetch_question_queue = "fetch_question_queue"
        self.score_keeper_queue = "score_keeper_queue"

    def create_queues(self):
        # Declare all the queues
        self.channel.queue_declare(queue=self.message_queue)
        self.channel.queue_declare(queue=self.answer_queue)
        self.channel.queue_declare(queue=self.fetch_question_queue)
        self.channel.queue_declare(queue=self.score_keeper_queue)
        self.channel.queue_declare(queue=self.message_to_queue)
        print("Queues created in RabbitMQ.")

    def close_connection(self):
        self.connection.close()
        print("Connection to RabbitMQ closed.")
