# Public Transit Status with Apache Kafka

For the description and further information see [instructions.md](instructions.md)

## Running the Simulation

KSQL is used in non interactive mode in order to be closer to production. But this creates a timing
problem with topic creation. Therefore a simple docker-compose up is not possible.
A fix for this is to startup kafka and topic creation first. KSQL and the rest of the stack start
afterwards.

To run the pipeline use one of the following commands:

- (minimal) pipeline: `./run.sh`
- whole pipeline including various UI containers and KSQL in interactive mode: `./run_all.sh`

In order to have a clean start after a problem the following commands are recommended (especially
to clear the kafka volume): `docker-compose down --volumes --timeout 10`

## Topics

For a list and description of the topics see [shared_helpers/topics.py](shared_helpers/topics.py)

## Topic creation

Personally, I do not like creating topics dynamically, but prefer the topics to exist before the
application starts running.
This is of course not possible when dynamic information (such as a station name) is part of the
topic name.

Therefore I decided to avoid using such dynamic names and create the topics as part of the
docker startup with a docker-cli image. In the real world I would also create the topics separate
from the application logic, so I prefer this appraoch.
