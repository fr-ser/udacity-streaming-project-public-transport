"""Contains functionality related to Weather"""
from shared_helpers.logging import logger


class Weather:
    """Defines the Weather model"""

    def __init__(self):
        """Creates the weather model"""
        self.temperature = 70.0
        self.status = "sunny"

    def process_message(self, message):
        """Handles incoming weather data"""
        self.temperature = message.value()["temperature"]
        self.status = message.value()["status"]
        logger.debug(f"Updated weather conditions to {message.value()}")
