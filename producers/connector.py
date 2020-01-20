"""Configures a Kafka Connector for Postgres Station data"""

import json

import requests

from shared_helpers.logging import logger
from shared_helpers.config import KAFKA_CONNECT_URL, STATION_DB_JDBC_URL
from shared_helpers.topics import CONNECT_PREFIX, CONNECT_STATION_TABLE

CONNECTOR_NAME = "stations"


def configure_connector():
    """Starts and configures the Kafka Connect connector"""
    logger.debug("creating or updating kafka connect connector...")

    resp = requests.get(f"{KAFKA_CONNECT_URL}/connectors/{CONNECTOR_NAME}")
    if resp.status_code == 200:
        logger.info("Kafka Connect JDBC connector already created skipping recreation")
        return

    resp = requests.post(
        f"{KAFKA_CONNECT_URL}/connectors",
        headers={"Content-Type": "application/json"},
        data=json.dumps({
            "name": CONNECTOR_NAME,
            "config": {
                "connector.class": "io.confluent.connect.jdbc.JdbcSourceConnector",
                "key.converter": "org.apache.kafka.connect.json.JsonConverter",
                "key.converter.schemas.enable": "false",
                "value.converter": "org.apache.kafka.connect.json.JsonConverter",
                "value.converter.schemas.enable": "false",
                "batch.max.rows": "500",
                "connection.url": STATION_DB_JDBC_URL,
                "table.whitelist": CONNECT_STATION_TABLE,
                "mode": "incrementing",
                "incrementing.column.name": "stop_id",
                "topic.prefix": CONNECT_PREFIX,
                "poll.interval.ms": "86400000",  # 1 day
            }
        }),
    )

    resp.raise_for_status()
    logger.info("Kafka Connect JDBC connector created successfully")


if __name__ == "__main__":
    configure_connector()
