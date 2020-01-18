"""Creates a turnstile data producer"""

from confluent_kafka import avro

from shared_helpers.logging import logger
from shared_helpers.config import SCHEMA_PATH
from .producer import Producer
from .turnstile_hardware import TurnstileHardware


class Turnstile(Producer):
    key_schema = avro.load(SCHEMA_PATH / "turnstile_key.json")
    value_schema = avro.load(SCHEMA_PATH / "turnstile_value.json")

    topic_name = "cta.station.turnstile"

    def __init__(self, station):
        cleaned_station_name = (
            station.name.lower()
            .replace("/", "_and_")
            .replace(" ", "_")
            .replace("-", "_")
            .replace("'", "")
        )

        super().__init__(group_id=f"{Turnstile.topic_name}-{cleaned_station_name}")

        self.station = station
        self.turnstile_hardware = TurnstileHardware(station)

    def run(self, timestamp, time_step):
        """Simulates riders entering through the turnstile."""

        num_entries = self.turnstile_hardware.get_entries(timestamp, time_step)
        try:
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
        except Exception:
            logger.exception(f"Error producing for turnstile at {self.station.name}")
            raise

        logger.debug(f"produced turnstile event at station {self.station.name}")
