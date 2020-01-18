"""Producer base-class providing common utilites and functionality"""

import time


from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka.avro import AvroProducer, CachedSchemaRegistryClient

from shared_helpers.logging import logger
from shared_helpers.config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_SCHEMA_REGISTRY_URL


class Producer:
    """Defines and provides common functionality amongst Producers"""

    # Tracks existing topics across all Producer instances
    existing_topics = set([])

    def __init__(
        self,
        topic_name,
        key_schema,
        value_schema=None,
        num_partitions=1,
        num_replicas=1,
    ):
        """Initializes a Producer object with basic settings"""
        self.topic_name = topic_name
        self.key_schema = key_schema
        self.value_schema = value_schema
        self.num_partitions = num_partitions
        self.num_replicas = num_replicas

        # If the topic does not already exist, try to create it
        if self.topic_name not in Producer.existing_topics:
            self.create_topic()
            Producer.existing_topics.add(self.topic_name)

        schema_registry = CachedSchemaRegistryClient({"url": KAFKA_SCHEMA_REGISTRY_URL})
        self.producer = AvroProducer(
            {
                "client.id": self.topic_name,
                "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
            },
            schema_registry=schema_registry
        )

    def create_topic(self):
        """Creates the producer topic if it does not already exist"""

        client = AdminClient({"bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS})

        cluster_meta_data = client.list_topics(timeout=10)

        # fill existing topics when first connecting
        if len(self.existing_topics) == 0:
            self.existing_topics.update(cluster_meta_data.topics.keys())

        if self.topic_name in cluster_meta_data.topics.keys():
            self.existing_topics.add(self.topic_name)
            logger.debug(f"Topic {self.topic_name} already exists")
            return

        futures = client.create_topics(
            [
                NewTopic(
                    self.topic_name,
                    num_partitions=self.num_partitions,
                    replication_factor=self.num_replicas,
                )
            ]
        )

        try:
            futures[self.topic_name].result(timeout=10)
            self.existing_topics.add(self.topic_name)
            logger.info(f"Created topic: {self.topic_name}")
        except Exception:
            logger.exception(f"failed to create topic {self.topic_name}")
            raise

    def close(self):
        """Prepares the producer for exit by cleaning up the producer"""

        self.producer.flush(timeout=60)

    def time_millis(self):
        """Use this function to get the key for Kafka Events"""
        return int(round(time.time() * 1000))
