import json
import random
import os
import pika


class QuestionFetcher:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
        self.channel = self.connection.channel()

        self.channel.queue_declare(queue="fetch_question_queue")
        self.channel.queue_declare(queue="messages_to_clients")
        self.channel.queue_declare(queue="answer_queue")

        self.channel.basic_consume(
            queue="fetch_question_queue",
            on_message_callback=self.callback,
            auto_ack=True,
        )

        self.data_path = os.path.join(os.getcwd(), "data", "questions.json")

        self.channel.start_consuming()

    def fetch_random_question(self):
        with open(self.data_path, "r") as file:
            questions = json.load(file)
            question_list = questions.get("questions", [])
            if not question_list:
                return None
            return random.choice(question_list)

    def callback(self, ch, method, properties, body):
        print("QF : received:", body)

        new_question = self.fetch_random_question()
        question_message = {
            "type": "question",
            "data": new_question,
        }
        self.channel.basic_publish(
            exchange="",
            routing_key="messages_to_clients",
            body=json.dumps(question_message),
        )

        self.channel.basic_publish(
            exchange="",
            routing_key="answer_queue",
            body=json.dumps(question_message),
        )


if __name__ == "__main__":
    question_fetcher = QuestionFetcher()
