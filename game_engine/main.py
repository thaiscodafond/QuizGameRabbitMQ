from workers.answer_consumer import AnswerConsumer
from workers.question_fetcher import QuestionFetcher
from queue_creator import QueueCreator
from router import MessageRouter
import threading

from workers.score_keeper import ScoreKeeper


def start_consuming_in_thread():
    question_fetcher = QuestionFetcher()


def start_answer_consumer_thread():
    answer_consumer = AnswerConsumer()


def start_score_keeper_thread():
    score_keeper = ScoreKeeper()


if __name__ == "__main__":
    queue_creator = QueueCreator()
    queue_creator.create_queues()
    queue_creator.close_connection()

    thread_question_fetcher = threading.Thread(target=start_consuming_in_thread)
    thread_question_fetcher.start()

    thread_answer_consumer = threading.Thread(target=start_answer_consumer_thread)
    thread_answer_consumer.start()

    thread_score_keeper = threading.Thread(target=start_score_keeper_thread)
    thread_score_keeper.start()

    router = MessageRouter()
