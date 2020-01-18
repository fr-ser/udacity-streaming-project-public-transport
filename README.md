# Public Transit Status with Apache Kafka

For the description and further information see the [file](instructions.md) in
[Github](https://github.com/fr-ser/udacity_stream_exercise_public_transport)

## Running the Simulation

To run the whole thing:

```bash
docker-compose up producers
```

Once the simulation is running, you may hit `Ctrl+C` at any time to exit.

## Topic creation

Personally I do not like creating topics dynamically. In like the topics to exist before the
application starts running.
This is of course not possible when dynamic information (such as a station name) is part of the
topic name.

Therefore I decided to avoid using such dynamic names and create the topics as part of the
docker startup with a docker-cli image. In the real world I would also create the topics separate
from the application logic, so I prefer this appraoch.
