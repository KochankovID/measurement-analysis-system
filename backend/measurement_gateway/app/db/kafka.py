import logging

from aiokafka import AIOKafkaProducer
from pydantic import BaseModel
from sqlalchemy.orm import declarative_base

logger = logging.getLogger(__name__)
Base = declarative_base()


class Kafka:
    def __init__(self, bootstrap_servers: str) -> None:
        self._producer = AIOKafkaProducer(bootstrap_servers=bootstrap_servers)

    async def setup(self) -> None:
        await self._producer.start()

    async def send_message(self, topic, message: BaseModel):
        await self._producer.send_and_wait(topic, message.json().encode("utf-8"))
