import json
import pika

ROUND_MAX = 10


class ScoreKeeper:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
        self.channel = self.connection.channel()

        self.channel.queue_declare(queue="messages_to_clients")
        self.channel.queue_declare(queue="score_keeper_queue")

        self.channel.basic_consume(
            queue="score_keeper_queue",
            on_message_callback=self.callback,
            auto_ack=True,
        )

        self.scores = {}
        self.round_number = 0
        self.max_round_number = ROUND_MAX

        print("SCORE_KEEPER: Waiting for messages needing new questions...")
        self.channel.start_consuming()

    def process_round(self, message):
        self.round_number += 1
        if self.round_number > self.max_round_number:
            self.new_game()
            self.round_number = 0
            new_message = {"type": "round", "number": self.round_number}
            channel.queue_declare(queue="messages_to_clients")
            channel.basic_publish(
                exchange="",
                routing_key="fetch_question_queue",
                body=json.dumps(new_message),
            )
        else:
            new_message = {"type": "round", "number": self.round_number}

        print("SK : sent:", new_message)

        channel = self.connection.channel()
        channel.queue_declare(queue="messages_to_clients")
        channel.basic_publish(
            exchange="",
            routing_key="messages_to_clients",
            body=json.dumps(new_message),
        )

    def process_score(self, message):
        if self.scores == {}:
            result = message.get("result")
            print(result)
            for k, v in result.items():
                if v["is_correct"] == True:
                    self.scores[k] = 1
                else:
                    self.scores[k] = 0
        else:
            result = message.get("result")
            print(result)
            for k, v in result.items():
                if v["is_correct"] == True:
                    self.scores[k] += 1
                else:
                    self.scores[k] += 0

        result_message = {"type": "result_score", "results": self.scores}
        print("SK : sent:", result_message)
        channel = self.connection.channel()
        channel.queue_declare(queue="messages_to_clients")
        channel.basic_publish(
            exchange="",
            routing_key="messages_to_clients",
            body=json.dumps(result_message),
        )

    def new_game(self, message):
        self.scores = {}
        self.round_number = 0

    def callback(self, ch, method, properties, body):
        message = json.loads(body.decode())
        print(f"SCORE_KEEPER: Received message: {message}")
        type = message.get("type")

        if type == "score":
            print("SCORE_KEEPER: Score received")
            self.process_score(message)
        elif type == "fetch_question":
            print("SCORE_KEEPER: Question started : new round in place")
            self.process_round(message)
        elif type == "player_count":
            print("SCORE_KEEPER: Received count : new game started")
            self.new_game(message)
        else:
            print("SCORE_KEEPER: Unknown message:", message)


if __name__ == "__main__":
    score_keeper = ScoreKeeper()
