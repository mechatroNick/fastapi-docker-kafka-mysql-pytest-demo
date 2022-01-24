import os
import threading
import uuid
from .BaseConsumer import BaseConsumer
from typing import List

_KAFKA_HOST = os.getenv("KAFKA_HOSTS", "kafka:29092")
_CONSUMER_GROUP_NAME = os.getenv("KAFKA_CONSUMER_GROUP", "default-consumer-group")
_CUSTOMER_NOTIFICATION_TOPIC = os.getenv(
    "CUSTOMER_NOTIFICATION_TOPIC", "customer-notification-topic"
)
_ITEM_NOTIFICATION_TOPIC = os.getenv(
    "ITEM_NOTIFICATION_TOPIC", "item-notification-topic"
)
_NOTIFY_CUSTOMER_THREAD_NAME = "NotifyCustomerConsumer"
_NOTIFY_ITEM_THREAD_NAME = "NotifyItemConsumer"


def create_NotifyCustomerConsumer_thread():
    consumer = BaseConsumer(
        config={
            "bootstrap.servers": _KAFKA_HOST,
            "group.id": _CONSUMER_GROUP_NAME,
            "security.protocol": "PLAINTEXT",
        },
        topics=_CUSTOMER_NOTIFICATION_TOPIC,
        consumer_name=_NOTIFY_CUSTOMER_THREAD_NAME,
    )

    consumerThread = threading.Thread(
        target=consumer.run,
        name=f"{_NOTIFY_CUSTOMER_THREAD_NAME} THREAD - {uuid.uuid4()}",
    )
    return consumerThread


def create_NotifyItemConsumer_thread():
    consumer = BaseConsumer(
        config={
            "bootstrap.servers": _KAFKA_HOST,
            "group.id": _CONSUMER_GROUP_NAME,
            "security.protocol": "PLAINTEXT",
        },
        topics=_ITEM_NOTIFICATION_TOPIC,
        consumer_name=_NOTIFY_ITEM_THREAD_NAME,
    )

    consumerThread = threading.Thread(
        target=consumer.run, 
        name=f"{_NOTIFY_ITEM_THREAD_NAME} THREAD - {uuid.uuid4()}"
    )
    return consumerThread


consumer_thread_prefixs: List[str] = [
    _NOTIFY_CUSTOMER_THREAD_NAME,
    _NOTIFY_ITEM_THREAD_NAME,
]


def start_consumers():
    theard1 = create_NotifyCustomerConsumer_thread()
    theard1.start()
    thread2 = create_NotifyItemConsumer_thread()
    thread2.start()
