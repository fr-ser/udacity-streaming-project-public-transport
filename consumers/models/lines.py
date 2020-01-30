"""Contains functionality related to Lines"""
import json

from models import Line


class Lines:
    """Contains all train lines"""

    def __init__(self):
        """Creates the Lines object"""
        self.red_line = Line("red")
        self.green_line = Line("green")
        self.blue_line = Line("blue")

    def process_message(self, message):
        """Processes a station message"""

        value = message.value()
        # Content might be JSON (as byte string) or AVRO (as dict)
        if isinstance(value, bytes):
            value = json.loads(message.value())

        # KSQL likes to uppercase things
        if "LINE" in value.keys():
            value["line"] = value.get("LINE")

        if value.get("line") == "green":
            self.green_line.process_message(message)
        elif value.get("line") == "red":
            self.red_line.process_message(message)
        elif value.get("line") == "blue":
            self.blue_line.process_message(message)
        else:
            raise Exception(f"unknown line msg {value}")
