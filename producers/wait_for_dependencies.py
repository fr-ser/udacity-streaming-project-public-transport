"""Used in local development (and docker) to wait until all services started"""


from confluent_kafka import admin, KafkaException
import requests
from loguru import logger


from shared_helpers.wait_until import wait_until_or_crash
from shared_helpers.config import (
    KAFKA_BOOTSTRAP_SERVERS,
    KAFKA_SCHEMA_REGISTRY_URL,
    KAKFA_REST_PROXY_URL,
    KAFKA_CONNECT_URL,
)


@wait_until_or_crash(timeout=30, caught_exception=KafkaException)
def check_kafka():
    client = admin.AdminClient({"bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS})

    cluster_meta_data = client.list_topics(timeout=1)
    # fail if not topics are created
    return cluster_meta_data.topics.keys()


@wait_until_or_crash(timeout=30, caught_exception=Exception)
def check_schema_registry():
    resp = requests.get(
        f"{KAFKA_SCHEMA_REGISTRY_URL}/config",
        headers={"Accept": "application/json"},
    )
    resp.raise_for_status()
    return True


@wait_until_or_crash(timeout=30, caught_exception=Exception)
def check_rest_proxy():
    resp = requests.get(
        f"{KAKFA_REST_PROXY_URL}/brokers",
        headers={"Accept": "application/json"},
    )
    resp.raise_for_status()
    # list of brokers should not be empty
    return resp.json()["brokers"]


@wait_until_or_crash(timeout=30, caught_exception=Exception)
def check_kafka_connect():
    resp = requests.get(f"{KAFKA_CONNECT_URL}/connector-plugins")
    resp.raise_for_status()
    # list of plugins should not be empty
    return resp.json()


if __name__ == "__main__":
    logger.info(f"Checking for topics in kafka at {KAFKA_BOOTSTRAP_SERVERS}")
    check_kafka()

    logger.info(f"Checking for config in schema registry at {KAFKA_SCHEMA_REGISTRY_URL}")
    check_schema_registry()

    logger.info(f"Checking for rest proxy at {KAKFA_REST_PROXY_URL}")
    check_rest_proxy()

    logger.info(f"Checking for kafka connect at {KAFKA_CONNECT_URL}")
    check_kafka_connect()

    logger.info(f"All dependencies are there!")
