"""Creates a turnstile data producer"""

from confluent_kafka import avro

from shared_helpers.logging import logger
from shared_helpers.config import SCHEMA_PATH
from .producer import Producer
from .turnstile_hardware import TurnstileHardware


class Turnstile(Producer):
    key_schema = avro.load(SCHEMA_PATH / "turnstile_key.json")
    value_schema = avro.load(SCHEMA_PATH / "turnstile_value.json")

    def __init__(self, station):
        """Create the Turnstile"""
        station_name = (
            station.name.lower()
            .replace("/", "_and_")
            .replace(" ", "-")
            .replace("'", "")
        )

        super().__init__(
            f"station.turnstile.{station_name}",
            key_schema=Turnstile.key_schema,
            value_schema=Turnstile.value_schema,
            num_partitions=5,
        )
        self.station = station
        self.turnstile_hardware = TurnstileHardware(station)

    def run(self, timestamp, time_step):
        """Simulates riders entering through the turnstile."""

        num_entries = self.turnstile_hardware.get_entries(timestamp, time_step)
        self.producer.produce(
            topic=self.topic_name,
            key={"timestamp": self.time_millis()},
            value={
                "station_id": self.station.station_id,
                "station_name": self.station.name,
                "line": self.station.color,
                "num_entries": num_entries,
            },
            key_schema=self.key_schema,
            value_schema=self.value_schema,
        )

        logger.debug(f"produced turnstile event at station {self.station.name}")
