#!/bin/bash

set -e

seed_ksql () {
    # wait until the ksql server starts
    until docker-compose exec ksql-interactive nc -z localhost 8088; do
        echo "waiting for ksql server to start"
        sleep 1
    done

    docker-compose exec ksql-interactive \
        sh -c 'echo "RUN SCRIPT /app/queries.sql;\n exit" | ksql' > /dev/null
    printf "\nseeded ksql server with sql file \n\n"
}

# starts kafka and creates topics
docker-compose build > /dev/null
printf "\nBuilt images\n\n"

docker-compose run --rm kafka-cli
docker-compose up -d producers ksql-interactive faust-stream
seed_ksql
docker-compose up -d connect-ui topics-ui schema-registry-ui
docker-compose up consumer-server
