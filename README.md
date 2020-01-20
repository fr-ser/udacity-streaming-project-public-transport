# Public Transit Status with Apache Kafka

For the description and further information see the [file](instructions.md) in
[Github](https://github.com/fr-ser/udacity_stream_exercise_public_transport)

## Running the Simulation

In order to be closer to production KSQL is used in non interactive mode. But this creates a timing
problem with topic creation. Therefore a simple docker-compose up is not possible.
A fix for this is to startup kafka and topic creation before and afterwards the rest of the stack.

To run the whole thing:

```bash
./startup.sh
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
