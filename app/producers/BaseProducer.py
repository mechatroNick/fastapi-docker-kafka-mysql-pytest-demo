import os
from confluent_kafka import Producer
import logging
from ddtrace import tracer

logger = logging.getLogger(__name__)


class BaseProducer:
    def __init__(
        self,
        config: dict,
        topic: str,
        producer_name: str = __name__,
    ):

        if not config["bootstrap.servers"]:
            raise Exception(
                f"{producer_name} Exception -- Kafka bootstrap.servers not specified."
            )
        if not topic:
            raise Exception(f"{producer_name} Exception -- Kafka topics not specified.")

        useConfig = dict()
        defaultConfig = {"acks": 1, "heartbeat.interval.ms": 1000}
        useConfig.update(defaultConfig)
        useConfig.update(config)

        logger.info(f"{producer_name} config: {useConfig}")
        self.config = useConfig
        self.topic = topic
        self.producer_name = producer_name

        try:
            logger.info(f"Creating {producer_name} ....")
            self.producer = Producer(useConfig)
        except Exception as e:
            logger.exception(e)
            raise Exception(f"Exception -- Cannot create {producer_name}: {e}")

    @tracer.wrap(name=f"{__name__}.delivery_report_callback()")
    def delivery_report_callback(self, err, msg):
        if err is not None:
            errMessage = f"Message delivery for [{msg.value()}] FAILED: {err}"

            logger.error(f"{self.producer_name} Flush callback error - {errMessage}")
            raise Exception(errMessage)
        else:
            logger.info(
                f"{self.producer_name} delivered to {msg.topic()} [{ msg.partition()}]: { msg.value()}"
            )

    @tracer.wrap(name=f"{__name__}.produce()")
    def produce(self, msg):
        logger.info(f"-------- START {self.producer_name} ---------")
        self.producer.poll(0)
        record = msg.encode("utf-8")
        self.producer.produce(
            self.topic, record, callback=self.delivery_report_callback
        )
        self.producer.flush()
        logger.info(f"--------- END {self.producer_name} ----------")
