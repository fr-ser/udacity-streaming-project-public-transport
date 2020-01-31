import time
from functools import wraps

from confluent_kafka import admin, KafkaException
import requests

from shared_helpers.logging import logger
from shared_helpers.topics import WEATHER_STATUS, TURNSTILE_ENTRIES_TABLE
from shared_helpers.config import (
    KAFKA_BOOTSTRAP_SERVERS,
    KAFKA_SCHEMA_REGISTRY_URL,
    KAKFA_REST_PROXY_URL,
    KAFKA_CONNECT_URL,
    FAUST_URL,
)


def _wait_until_or_crash(timeout=30, caught_exception=None):
    """
    A decorator to wait until a function suceeds and returns true in time.
    Otherwhise an error is raised.

    This should be used to wait for dependencies (e.g. check until a database is up)

    :param timeout: Maximum wait time in seconds (Does not interrupt blocking code!)
    :param caught_exception: Exception to catch (and retry)
    """
    def argumentless_decorator(decorated_function):
        @wraps(decorated_function)
        def wrapper(*args, **kwargs):
            logger.info(f"Waiting for {decorated_function.__name__}")
            result = None
            stored_exception = None
            end_time = time.time() + timeout
            while time.time() < end_time:
                try:
                    result = decorated_function(*args, **kwargs)
                    stored_exception = None
                except Exception as e:
                    if caught_exception is None or not isinstance(e, caught_exception):
                        raise

                    stored_exception = e
                    time.sleep(0.3)
                    continue

                if result:
                    return
                else:
                    time.sleep(0.3)
                    continue

            if not result:
                if stored_exception:
                    raise stored_exception
                else:
                    raise Exception("Dependency not ready")

        return wrapper
    return argumentless_decorator


@_wait_until_or_crash(timeout=30, caught_exception=KafkaException)
def check_kafka():
    client = admin.AdminClient({"bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS})

    cluster_meta_data = client.list_topics(timeout=1)
    # fail if custom topic is not present
    return WEATHER_STATUS in cluster_meta_data.topics.keys()


@_wait_until_or_crash(timeout=45, caught_exception=Exception)
def check_schema_registry():
    resp = requests.get(
        f"{KAFKA_SCHEMA_REGISTRY_URL}/config",
        headers={"Accept": "application/json"},
    )
    resp.raise_for_status()
    return True


@_wait_until_or_crash(timeout=30, caught_exception=Exception)
def check_rest_proxy():
    resp = requests.get(
        f"{KAKFA_REST_PROXY_URL}/brokers",
        headers={"Accept": "application/json"},
    )
    resp.raise_for_status()
    # list of brokers should not be empty
    return resp.json()["brokers"]


@_wait_until_or_crash(timeout=30, caught_exception=Exception)
def check_kafka_connect():
    resp = requests.get(f"{KAFKA_CONNECT_URL}/connector-plugins")
    resp.raise_for_status()
    # list of plugins should not be empty
    return resp.json()


@_wait_until_or_crash(timeout=45, caught_exception=Exception)
def check_faust_stream():
    resp = requests.get(f"{FAUST_URL}/health/")
    resp.raise_for_status()
    # at least one rebalance should be completed
    return resp.json()["rebalances"] > 0


@_wait_until_or_crash(timeout=30, caught_exception=Exception)
def check_ksql():
    client = admin.AdminClient({"bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS})

    cluster_meta_data = client.list_topics(timeout=1)
    # fail if custom topic is not present
    return TURNSTILE_ENTRIES_TABLE in cluster_meta_data.topics.keys()
