#!/bin/bash

# starts kafka and creates topics
docker-compose build > /dev/null
printf "\nBuilt images\n\n"

docker-compose run --rm kafka-cli
docker-compose up -d producers ksql faust-stream
docker-compose up consumer-server
