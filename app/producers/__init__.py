import os
from .BaseProducer import BaseProducer
from utils.singleton import Singleton

_KAFKA_HOST = os.getenv("KAFKA_HOSTS", "kafka:29092")
_CUSTOMER_NOTIFICATION_TOPIC = os.getenv(
    "CUSTOMER_NOTIFICATION_TOPIC", "customer-notification-topic"
)
_ITEM_NOTIFICATION_TOPIC = os.getenv(
    "ITEM_NOTIFICATION_TOPIC", "item-notification-topic"
)


class BaseProducer_Singleton(BaseProducer, metaclass=Singleton):
    pass


NotifyCustomerProducer = BaseProducer_Singleton(
    config={"bootstrap.servers": _KAFKA_HOST, "security.protocol": "PLAINTEXT"},
    topic=_CUSTOMER_NOTIFICATION_TOPIC,
    producer_name="NotifyCustomerProducer",
)


NotifyItemProducer = BaseProducer_Singleton(
    config={"bootstrap.servers": _KAFKA_HOST, "security.protocol": "PLAINTEXT"},
    topic=_ITEM_NOTIFICATION_TOPIC,
    producer_name="NotifyItemProducer",
)
