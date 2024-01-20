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

        self.previous_questions = []

        self.data_path = os.path.join(os.getcwd(), "data", "questions.json")

        self.channel.start_consuming()

    def fetch_random_question(self):
        with open(self.data_path, "r") as file:
            questions = json.load(file)
            question_list = questions.get("questions", [])
            if not question_list:
                return None
            random_question = random.choice(question_list)
            if random_question not in self.previous_questions:
                self.previous_questions.append(random_question)
                return random_question
            else:
                return self.fetch_random_question()

    def callback(self, ch, method, properties, body):
        print("QF : received:", body)
        message = json.loads(body.decode())
        if message.get("type") == "fetch_question":
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
        elif message.get("type") == "round":
            print("QF: ROUND MAX")
            self.previous_questions = []
        else:
            print("QF: message of unknown type")


if __name__ == "__main__":
    question_fetcher = QuestionFetcher()
