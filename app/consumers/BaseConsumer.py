import threading
from confluent_kafka import Consumer
import sys
import logging
from datetime import datetime
from ddtrace import tracer

logger = logging.getLogger(__name__)


class BaseConsumer:
    def __init__(self, config: dict, topics: str, consumer_name: str = __name__):

        if not config["bootstrap.servers"]:
            raise Exception("Exception -- Kafka bootstrap.servers not specified.")
        if not config["group.id"]:
            raise Exception("Exception -- Kafka group.id group not specified.")
        if not topics:
            raise Exception("Exception -- Kafka topics not specified.")

        useConfig = dict()
        defaultConfig = {
            "auto.offset.reset": "earliest",
            "heartbeat.interval.ms": 1000,
            "enable.auto.commit": False,
        }
        useConfig.update(defaultConfig)
        useConfig.update(config)

        logger.info(f"{consumer_name} config: {useConfig}")
        self.config = useConfig
        self.topics = topics
        self.consumer_name = consumer_name

        try:
            logger.info(f"Creating {consumer_name} ....")
            self.consumer = Consumer(useConfig)
        except Exception as e:
            logger.exception(e)
            raise Exception(f"Exception -- Cannot create {consumer_name}: {e}")

        try:
            logger.info(f"Subscribing to topics {topics}")
            self.consumer.subscribe([topics])
        except Exception as e:
            logger.exception(e)
            raise Exception(
                f"Exception -- {consumer_name} cannot subscribe to topics: {e}"
            )

        logger.info("Starting Kafka consumer at {}".format(datetime.utcnow()))

    @tracer.wrap(name=f"{__name__}.process_msg()")
    def process_msg(self, msg: str):
        print(
            f"{self.consumer_name} PLACEHOLDER - Do something to sync with DB or other places for message {msg}"
        )
        return "OK"

    def run(self):
        t = threading.current_thread()
        try:
            while getattr(t, "keep_running", True):
                msg = self.consumer.poll(1.0)
                consumptionError = False
                syncCommitError = False

                if msg is None:
                    continue

                if msg.error():
                    logger.error(f"{self.consumer_name} error: {msg.error()}")
                    continue

                logger.info(f"---------- START {self.consumer_name} -----------")

                logger.info(
                    f"{self.consumer_name} Received message decoded raw: {msg.value()}"
                )
                try:
                    status = self.process_msg(msg.value())
                except Exception as e:
                    logger.exception(
                        f"{self.consumer_name} DATA CONSUMPTION error: {e}"
                    )
                    consumptionError = True
                else:
                    logger.info(f"{self.consumer_name} status: {status}")
                    try:
                        self.consumer.commit(asynchronous=False)
                        logger.info(f"{self.consumer_name} Successfully SYNC commit")
                    except Exception as e:
                        logger.exception(
                            f"{self.consumer_name} unable to Sync commit: {e}"
                        )
                        syncCommitError = True

                logger.info(f"----------- END {self.consumer_name} ------------")

                if consumptionError:
                    raise Exception(
                        f"{self.consumer_name} Escalate exception due to message consumption error"
                    )

                if syncCommitError:
                    raise Exception(
                        f"{self.consumer_name} Escalate exception due to SYNC commit error"
                    )

        finally:
            logger.error(f"Stopping {self.consumer_name} at {datetime.utcnow()}")
            self.consumer.close()
            sys.exit()
