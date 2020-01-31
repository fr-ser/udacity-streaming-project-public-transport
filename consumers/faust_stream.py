"""Defines trends calculations for stations"""

import re
import faust

from shared_helpers.logging import logger
from shared_helpers.config import KAFKA_BOOTSTRAP_SERVERS
from shared_helpers.topics import DB_STATION_RAW, STATION_MASTER_DATA


class Station(faust.Record):
    """Incoming message format"""
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


class TransformedStation(faust.Record):
    """Outgoing message format"""
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

in_topic = app.topic(DB_STATION_RAW, value_type=Station)

out_topic = app.topic(STATION_MASTER_DATA, value_type=TransformedStation)
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
        else:
            logger.warning(f"Received unknown line: {station}")
            continue

        transformed_station = TransformedStation(
            station_id=station.station_id,
            station_name=station.station_name,
            order=station.order,
            line=line_color,
        )
        table[station.stop_id] = transformed_station


@app.page('/health/')
class HealthCheck(faust.web.View):
    async def get(self, request):
        return self.json({"rebalances": app.monitor.rebalances})


if __name__ == "__main__":
    app.main()
