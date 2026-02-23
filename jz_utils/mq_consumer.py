import threading
import time
from abc import abstractmethod
from queue import Queue

import pika
from pika.exceptions import AMQPHeartbeatTimeout

from jz_utils import logger_factory
from jz_utils.telegram_msg_bot import SimpleTelegramBot

logger = logger_factory.get_logger(__name__)


def create_channel(amqp_url, routing_key, callback):
    logger.info("receving mq using config: %s", amqp_url)

    # 解析 URL 连接 RabbitMQ
    params = pika.URLParameters(amqp_url)
    # 心跳，若超过心跳时间则会报错, 服务器超时时间好像是60s, 所以这里设置为50s
    params.heartbeat = 30
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    # 声明队列（如果队列不存在，则创建）
    result = channel.queue_declare(queue="", exclusive=True)
    # channel.exchange_declare(exchange='logs_topic', exchange_type='topic')
    queue_name = result.method.queue  # Get the generated queue name

    logger.info(f"开始MQ连接: {routing_key}")
    channel.queue_bind(exchange="shark.topic", queue=queue_name, routing_key=routing_key)

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    return channel


def close_conn(channel, routing_key):
    def _close():
        channel.stop_consuming()
        channel.close()
        logger.info(f"关闭MQ连接 {routing_key}")

    return _close


def receive(amqp_url, routing_key, callback):
    while True:
        try:
            channel = create_channel(amqp_url, routing_key, callback)
            SimpleTelegramBot().send(f"开始消费MQ {routing_key}")
            channel.start_consuming()
        except AMQPHeartbeatTimeout as e:
            logger.info(f"{routing_key} 心跳超时, exception: {e}")
            SimpleTelegramBot().send(f"{routing_key} 心跳超时, exception: {e}")
        except Exception as e:
            logger.info(f"消费MQ退出 {routing_key}, exception: {e}")
            SimpleTelegramBot().send(f"消费MQ退出 {routing_key}, exception: {e}")
        time.sleep(3)


class MQConsumer:
    def __init__(self, amqp_url: str, topic: str):
        self.amqp_url = amqp_url
        self.topic = topic
        self.queue = Queue(1000)
        self.start_updater()
        self.start_listener()

    def start_listener(self):
        self.listener_thread = threading.Thread(target=receive, args=(self.amqp_url, self.topic, self.handle_raw_msg))
        self.listener_thread.start()

    def start_updater(self):
        self.updater_thread = threading.Thread(target=self.updater)
        self.updater_thread.start()

    def updater(self):
        while True:
            self.handle_queue_msg(self.queue.get())

    @abstractmethod
    def handle_raw_msg(self, ch, method, properties, body):
        pass

    @abstractmethod
    def handle_queue_msg(self, msg):
        pass
