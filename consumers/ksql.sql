SET 'auto.offset.reset' = 'earliest';

CREATE STREAM CTA_STATION_TURNSTILE_STREAM (
    station_id INT, station_name VARCHAR, line VARCHAR, num_entries INT
) WITH (
    KAFKA_TOPIC = 'cta.station.turnstile', VALUE_FORMAT = 'AVRO'
);

CREATE TABLE CTA_STATION_TURNSTILE_ENTRIES WITH (VALUE_FORMAT='JSON') AS
    SELECT station_id, station_name, line, SUM(num_entries) AS COUNT
    FROM CTA_STATION_TURNSTILE_STREAM
    GROUP BY station_id, station_name, line
;
