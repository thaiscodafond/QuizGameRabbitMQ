import unittest
import pika
import json
import time

from ..workers.question_fetcher import QuestionFetcher


class TestQuestionFetcher(unittest.TestCase):
    def setUp(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue="fetch_question_queue")
        self.channel.queue_declare(queue="messages_from_clients")

    def test_question_fetcher(self):
        question_fetcher = QuestionFetcher()

        message = {"type": "fetch_question", "data": "Your question here"}

        self.channel.basic_publish(
            exchange="", routing_key="fetch_question_queue", body=json.dumps(message)
        )

        time.sleep(5)

        method_frame, header_frame, body = self.channel.basic_get(
            queue="messages_from_clients"
        )
        self.assertIsNotNone(method_frame)
        self.assertEqual(json.loads(body), message)


if __name__ == "__main__":
    unittest.main()
