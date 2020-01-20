"""Defines trends calculations for stations"""

import re
import faust

from shared_helpers.logging import logger
from shared_helpers.config import KAFKA_BOOTSTRAP_SERVERS
from shared_helpers.topics import CONNECT_DB_STATIONS, STATION_INFO

# Faust will ingest records from Kafka in this format


class Station(faust.Record):
    stop_id: int
    direction_id: str
    stop_name: str
    station_name: str
    station_descriptive_name: str
    station_id: int
    order: int
    red: bool
    blue: bool
    green: bool


# Faust will produce records to Kafka in this format
class TransformedStation(faust.Record):
    station_id: int
    station_name: str
    order: int
    line: str


cleaned_broker_list = re.sub(r"[A-Za-z]+://", "", KAFKA_BOOTSTRAP_SERVERS)
faust_broker_list = [f"kafka://{broker}" for broker in cleaned_broker_list.split(",")]

app = faust.App(
    "stations-stream",
    broker=faust_broker_list,
    store="memory://",
    options={
        "topic_disable_leader": True,
    },
)

in_topic = app.topic(CONNECT_DB_STATIONS, value_type=Station)

out_topic = app.topic(STATION_INFO, value_type=TransformedStation)
table = app.Table(
    "station-info-table",
    default=TransformedStation,
    changelog_topic=out_topic,
)


@app.agent(in_topic)
async def transform_stations(stations):
    logger.info("Station transform stream started")
    async for station in stations:
        line_color = None
        if station.red:
            line_color = "red"
        elif station.blue:
            line_color = "blue"
        elif station.green:
            line_color = "green"

        transformed_station = TransformedStation(
            station_id=station.station_id,
            station_name=station.station_name,
            order=station.order,
            line=line_color,
        )
        table[station.station_id] = transformed_station


if __name__ == "__main__":
    app.main()
