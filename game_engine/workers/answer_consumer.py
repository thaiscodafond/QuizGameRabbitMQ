import pika
import json


class AnswerConsumer:
    def __init__(self, queue_name="answer_queue"):
        self.queue_name = queue_name
        self.answers = {}
        self.users = {}

        self.connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name)
        self.channel.basic_consume(
            queue=self.queue_name, on_message_callback=self.callback, auto_ack=True
        )
        print("AC: Waiting for answers...")
        self.channel.start_consuming()

    def callback(self, ch, method, properties, body):
        message = json.loads(body.decode())
        print(f"AC: Received message: {message}")
        if message.get("type") == "question":
            print("AC: Received correct answer")
            self.store_correct_answer(message.get("data"))
            self.users = {}
            self.result = {}
        else:
            print("AC: Received user answer")
            self.process_user_answer(message)

    def store_correct_answer(self, question_message):
        question = question_message.get("question")
        correct_answer = question_message.get("correct_answer")
        self.answers = {}
        self.users = {}
        self.answers[question] = correct_answer

    def process_user_answer(self, answer_message):
        answer = answer_message.get("answer")
        user_id = answer_message.get("answerId")
        users_id = json.loads(answer_message.get("connectedUserIds"))

        if user_id not in self.users:
            self.users[user_id] = {}

        for user_id_all in users_id:
            if user_id_all not in self.users:
                self.users[user_id_all] = {}

        self.users[user_id]["answer"] = answer
        self.answers[user_id] = answer

        print(f"AC: Users: {self.users}")
        print(len(self.users), len(self.answers))
        if len(self.users) == (len(self.answers) - 1):
            print("AC: All users have answered")
            self.evaluate_answers()

    def evaluate_answers(self):
        for user_id, user_data in self.users.items():
            user_answer = user_data.get("answer")
            question = list(self.answers.keys())[0]
            correct_answer = self.answers[question]
            is_correct = user_answer == correct_answer
            self.result[user_id] = {"answer": user_answer, "is_correct": is_correct}
        self.send_result_to_clients(self.result)

    def send_result_to_clients(self, final_result):
        print("AC: Sending result to clients")
        score_message = {"type": "score", "result": final_result}
        print(f"AC: Score: {score_message}")
        result_message = {"type": "result_each", "results": final_result}
        print(f"AC: Result: {score_message}")

        channel = self.connection.channel()
        channel.queue_declare(queue="score_keeper_queue")
        channel.basic_publish(
            exchange="",
            routing_key="score_keeper_queue",
            body=json.dumps(score_message),
        )

        channel = self.connection.channel()
        channel.queue_declare(queue="messages_to_clients")
        channel.basic_publish(
            exchange="",
            routing_key="messages_to_clients",
            body=json.dumps(result_message),
        )

    def start_consuming(self):
        print(f"AC:: Waiting for {self.queue_name} messages...")
        self.channel.start_consuming()


if __name__ == "__main__":
    answer_consumer = AnswerConsumer()
    answer_consumer.start_consuming()
