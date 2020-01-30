"""Defines core consumer functionality"""

from confluent_kafka import Consumer, OFFSET_BEGINNING
from confluent_kafka.avro import AvroConsumer
from tornado import gen

from shared_helpers.logging import logger
from shared_helpers.config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_SCHEMA_REGISTRY_URL


class KafkaConsumer:
    """Defines the base kafka consumer class"""

    def __init__(
        self,
        topic_name_pattern,
        message_handler,
        is_avro=True,
        offset_earliest=False,
        sleep_secs=1.0,
        consume_timeout=0.1,
    ):
        """Creates a consumer object for asynchronous use"""
        self.topic_name_pattern = topic_name_pattern
        self.message_handler = message_handler
        self.sleep_secs = sleep_secs
        self.consume_timeout = consume_timeout
        self.offset_earliest = offset_earliest

        self.broker_properties = {
            "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
            "group.id": "tornado-server-consumer",
        }

        consumer_class = None
        if is_avro is True:
            self.broker_properties["schema.registry.url"] = KAFKA_SCHEMA_REGISTRY_URL
            consumer_class = AvroConsumer
        else:
            consumer_class = Consumer

        self.consumer = consumer_class(self.broker_properties)
        self.consumer.subscribe([self.topic_name_pattern], on_assign=self.on_assign)

    def on_assign(self, consumer, partitions):
        """Callback for when topic assignment takes place"""
        if self.offset_earliest:
            for partition in partitions:
                partition.offset = OFFSET_BEGINNING

        logger.info(f"partitions assigned for {self.topic_name_pattern}")
        consumer.assign(partitions)

    async def consume(self):
        """Asynchronously consumes data from kafka topic"""
        while True:
            num_results = 1
            while num_results > 0:
                num_results = self._consume()
            await gen.sleep(self.sleep_secs)

    def _consume(self):
        """Polls for a message. Returns 1 if a message was received, 0 otherwise"""
        message = self.consumer.poll(self.consume_timeout)
        if message is None:
            logger.trace("no message received by consumer")
            return 0
        elif message.error() is not None:
            logger.error(f"error from consumer {message.error()}")
            raise Exception(message.error())
        else:
            logger.trace(f"Received: {message.key()}: {message.value()}")
            self.message_handler(message)
            return 1

    def close(self):
        """Cleans up any open kafka consumers"""
        self.consumer.close()
