from shutil import ExecError
from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends, APIRouter
from repository.db import get_db
from typing import List
from confluent_kafka.admin import AdminClient
import threading
import os
import logging
from consumers import consumer_thread_prefixs

logger = logging.getLogger(__name__)

router = APIRouter()


_KAFKA_HOST = os.getenv("KAFKA_HOSTS", "kafka:29092")


def is_database_online(db: Session) -> bool:
    try:
        db.execute("SELECT 1")
    except Exception as e:
        logger.error(f"Unable to connect to Database: {e}")
        return False
    return True


def is_kafka_online(broker: str) -> bool:
    try:
        kafka_broker = {"bootstrap.servers": broker}
        admin_client = AdminClient(kafka_broker)
        topics = admin_client.list_topics().topics
        logger.info(f"Available topics: {topics}")
        if len(topics) == 0:
            raise Exception("No topic found in Kafka")
    except Exception as e:
        logger.error(f"Unable to connect to Kafka: {e}")
        return False
    return True


def is_consumer_online(prefix: str):
    live_thread_names: List[str] = []
    for thread in threading.enumerate():
        if thread.is_alive():
            live_thread_names.append(thread.name)
    logger.info(f"Live threads: {live_thread_names}")
    if not any(prefix in s for s in live_thread_names):
        logger.error(f"Thread with prefix {prefix=} not found")
        return False
    return True


@router.get("/")
def alive(db: Session = Depends(get_db)):
    if is_database_online(db) == False:
        raise HTTPException(status_code=500, detail="Database not available")
    if is_kafka_online(_KAFKA_HOST) == False:
        raise HTTPException(status_code=500, detail="Kafka connection not available")
    for prefix in consumer_thread_prefixs:
        if is_consumer_online(prefix) == False:
            raise HTTPException(
                status_code=500, detail=f"Kafka Consumer {prefix} not available"
            )
    return {
        "is_database_online": True,
        "is_kafka_online": True,
        "is_consumer_online": True,
    }
