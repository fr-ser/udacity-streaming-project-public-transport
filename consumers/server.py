"""Defines a Tornado Server that consumes Kafka Event data for display"""
from pathlib import Path

import tornado.ioloop
import tornado.template
import tornado.web

from shared_helpers.logging import logger
from shared_helpers.topics import (
    TURNSTILE_ENTRIES_TABLE, STATION_MASTER_DATA, WEATHER_STATUS, TRAIN_ARRIVAL,
)

from consumer import KafkaConsumer
from models import Lines, Weather
import topic_check


class MainHandler(tornado.web.RequestHandler):
    """Defines a web request handler class"""

    template_dir = tornado.template.Loader(f"{Path(__file__).parents[0]}/templates")
    template = template_dir.load("status.html")

    def initialize(self, weather, lines):
        """Initializes the handler with required configuration"""
        self.weather = weather
        self.lines = lines

    def get(self):
        """Responds to get requests"""
        logger.debug("rendering and writing handler template")
        self.write(
            MainHandler.template.generate(weather=self.weather, lines=self.lines)
        )


def run_server():
    """Runs the Tornado Server and begins Kafka consumption"""
    if not topic_check.topic_exists(TURNSTILE_ENTRIES_TABLE):
        logger.error(
            "Ensure that the KSQL Command has run successfully before running the web server!"
        )
        raise Exception("Ensure that the KSQL Command has run")
    if not topic_check.topic_exists(STATION_MASTER_DATA):
        logger.error(
            "Ensure that Faust Streaming is running successfully before running the web server!"
        )
        raise Exception("Ensure that Faust Streaming is running successfully")

    weather_model = Weather()
    lines = Lines()

    application = tornado.web.Application(
        [(r"/", MainHandler, {"weather": weather_model, "lines": lines})]
    )
    application.listen(8888)

    consumers = [
        KafkaConsumer(WEATHER_STATUS, weather_model.process_message, offset_earliest=True),
        KafkaConsumer(STATION_MASTER_DATA, lines.process_message,
                      offset_earliest=True, is_avro=False),
        KafkaConsumer(TRAIN_ARRIVAL, lines.process_message, offset_earliest=True),
        KafkaConsumer(
            TURNSTILE_ENTRIES_TABLE, lines.process_message, offset_earliest=True, is_avro=False,
        ),
    ]

    logger.info("Open a web browser to http://localhost:8888 to see the Transit Status Page")
    try:
        for consumer in consumers:
            tornado.ioloop.IOLoop.current().spawn_callback(consumer.consume)

        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        logger.info("shutting down server")
        tornado.ioloop.IOLoop.current().stop()
        for consumer in consumers:
            consumer.close()


if __name__ == "__main__":
    run_server()
