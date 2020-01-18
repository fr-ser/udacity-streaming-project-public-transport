import os
from pathlib import Path


SCHEMA_PATH = Path(os.environ["BASE_PATH"]) / "models" / "schemas"
DATA_PATH = Path(os.environ["BASE_PATH"]) / "data"


STATION_DB_JDBC_URL = os.environ.get(
    "STATION_DB_JDBC_URL",
    "jdbc:postgresql://postgres:5432/cta?user=cta_admin&password=chicago"
)

KAFKA_BOOTSTRAP_SERVERS = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
KAFKA_SCHEMA_REGISTRY_URL = os.environ.get("KAFKA_SCHEMA_REGISTRY_URL", "http://localhost:8081")
KAFKA_CONNECT_URL = os.environ.get("KAFKA_CONNECT_URL", "http://localhost:8083")
KAKFA_REST_PROXY_URL = os.environ.get("KAKFA_REST_PROXY_URL", "http://localhost:8082")
