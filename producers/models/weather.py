"""Methods pertaining to weather data"""

from enum import IntEnum
import json
import random
import time

import requests

from shared_helpers.logging import logger
from shared_helpers.config import SCHEMA_PATH, KAKFA_REST_PROXY_URL


class Weather:
    """Defines a simulated weather model"""

    status = IntEnum(
        "status", "sunny partly_cloudy cloudy windy precipitation", start=0
    )

    key_schema = None
    value_schema = None

    winter_months = set((0, 1, 2, 3, 10, 11))
    summer_months = set((6, 7, 8))

    topic_name = "cta-weather"

    def __init__(self, month):
        self.status = Weather.status.sunny
        self.temp = 70.0
        if month in Weather.winter_months:
            self.temp = 40.0
        elif month in Weather.summer_months:
            self.temp = 85.0

        if Weather.key_schema is None:
            with open(SCHEMA_PATH / "weather_key.json") as f:
                Weather.key_schema = f.read()

        if Weather.value_schema is None:
            with open(SCHEMA_PATH / "weather_value.json") as f:
                Weather.value_schema = f.read()

    def _set_weather(self, month):
        """Returns the current weather"""
        mode = 0.0
        if month in Weather.winter_months:
            mode = -1.0
        elif month in Weather.summer_months:
            mode = 1.0
        self.temp += min(max(-20.0, random.triangular(-10.0, 10.0, mode)), 100.0)
        self.status = random.choice(list(Weather.status))

    def run(self, month):
        self._set_weather(month)

        resp = requests.post(
            f"{KAKFA_REST_PROXY_URL}/topics/{Weather.topic_name}",
            headers={"Content-Type": "application/vnd.kafka.avro.v2+json"},
            data=json.dumps({
                "value_schema": Weather.value_schema,
                "key_schema": Weather.key_schema,
                "records": [
                    {
                        "key": {"timestamp": int(time.time())},
                        "value": {"temperature": self.temp, "status": self.status},
                    },
                ],
            }),
        )
        resp.raise_for_status()

        logger.debug(f"sent weather data to kafka, temp: {self.temp}, status: {self.status.name}")
