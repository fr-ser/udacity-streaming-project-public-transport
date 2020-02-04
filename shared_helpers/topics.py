# weather data retrieved from an API and forwared via rest proxy with an avro schema
WEATHER_STATUS = "cta.weather.status"
# train arrival data with an avro schema for all trains in one topic
TRAIN_ARRIVAL = "cta.station.arrival"
# turnstile data from stations with an avro schema
TURNSTILE_COUNT_UPDATE = "cta.station.turnstile"

# master data about stations (from a postgres database) retrieved via kafka connect in json
CONNECT_PREFIX = "cta.connect.db."
CONNECT_STATION_TABLE = "stations"
DB_STATION_RAW = f"{CONNECT_PREFIX}{CONNECT_STATION_TABLE}"

# parsed master data abotu stations (transformed via faust) in json
STATION_MASTER_DATA = "cta.station.master-data"

# aggregate (via ksql) of turnstile turns in json
TURNSTILE_ENTRIES_TABLE = "CTA_STATION_TURNSTILE_ENTRIES"
