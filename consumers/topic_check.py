from confluent_kafka.admin import AdminClient

from shared_helpers.config import KAFKA_BOOTSTRAP_SERVERS


def topic_exists(topic):
    """Checks if the given topic exists in Kafka"""
    client = AdminClient({"bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS})
    topic_metadata = client.list_topics(timeout=5)
    return topic in set(t.topic for t in iter(topic_metadata.topics.values()))
