# Public Transit Status with Apache Kafka

For the description and further information see the [file](instructions.md) in
[Github](https://github.com/fr-ser/udacity_stream_exercise_public_transport)

## Running the Simulation

To run the whole thing:

```bash
./start.sh
```

Once the simulation is running, you may hit `Ctrl+C` at any time to exit.

## Weird Hack Announcement

Creating a lot of topics for is very taxing for the disk space (and kafka probably).
Due to reproducible, but not easily explainable or understandable circumstances on startup
(when a lot of topics are created) the topic creation results in applications errors due to
timeouts.

These errors only happened when the whole docker stack is started as one
(no matter how long each service gives the previous ones time to start up).
The errors vanish into thin air, when kafka is started alone and immediately afterwards the rest
of the stack.
Therefore see the miraculous hack:

```bash
docker-compose up -d kafka0
docker-compose up producer
```
