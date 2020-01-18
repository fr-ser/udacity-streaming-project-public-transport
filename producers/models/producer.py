"""Producer base-class providing common utilites and functionality"""

import time

from confluent_kafka.avro import AvroProducer, CachedSchemaRegistryClient

from shared_helpers.logging import logger
from shared_helpers.config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_SCHEMA_REGISTRY_URL


class Producer:
    """Defines and provides common functionality amongst Producers"""

    def __init__(self, group_id=None):
        """Initializes a Producer object with basic settings"""

        schema_registry = CachedSchemaRegistryClient({"url": KAFKA_SCHEMA_REGISTRY_URL})

        producer_config = {"bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS}
        if group_id:
            producer_config["client.id"] = group_id

        self.producer = AvroProducer(producer_config, schema_registry=schema_registry)
        logger.debug(f"Created producer with id {group_id}")

    def close(self):
        """Prepares the producer for exit by cleaning up the producer"""

        self.producer.flush(timeout=60)

    def time_millis(self):
        """Use this function to get the key for Kafka Events"""
        return int(round(time.time() * 1000))
