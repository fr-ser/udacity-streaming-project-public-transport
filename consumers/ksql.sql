SET 'auto.offset.reset' = 'earliest';

CREATE STREAM CTA_STATION_TURNSTILE_STREAM (
    station_id INT, station_name VARCHAR, line INT, num_entries INT
) WITH (
    KAFKA_TOPIC = 'cta_station_turnstile', VALUE_FORMAT = 'AVRO'
);

CREATE TABLE CTA_STATION_TURNSTILE_TABLE WITH (VALUE_FORMAT='JSON') AS
    SELECT station_id, station_name, line, SUM(num_entries) AS count
    FROM CTA_STATION_TURNSTILE_STREAM
    GROUP BY station_id, station_name, line
;
