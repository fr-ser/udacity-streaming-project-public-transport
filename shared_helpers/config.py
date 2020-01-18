import os
from pathlib import Path


SCHEMA_PATH = Path(os.environ["BASE_PATH"]) / "models" / "schemas"
DATA_PATH = Path(os.environ["BASE_PATH"]) / "data"

KAFKA_CONNECT_URL = os.environ.get("KAFKA_CONNECT_URL", "http://localhost:8083/connectors")

STATION_DB_JDBC_URL = os.environ.get(
    "STATION_DB_JDBC_URL",
    "jdbc:postgresql://postgres:5432/cta?user=cta_admin&password=chicago"
)
