#!/bin/bash

# starts kafka and creates topics
docker-compose run --rm kafka-cli
docker-compose up -d producers ksql faust-stream