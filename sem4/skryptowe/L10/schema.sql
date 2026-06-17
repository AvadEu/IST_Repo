-- Struktura relacyjnej bazy danych dla rozkładu jazdy GTFS (SQLite).
-- Zadanie 1a: polecenia DDL tworzące tabele oraz klucze obce
-- realizujące więzy integralności referencyjnej.
--
-- Kolejność definicji odpowiada zależnościom kluczy obcych:
--   agency  <-  routes  <-  trips  <-  stop_times
--   calendar <- trips
--   stops    <- stop_times

PRAGMA foreign_keys = ON;

-- Przewoźnicy (agency.txt)
CREATE TABLE IF NOT EXISTS agency (
    agency_id        TEXT PRIMARY KEY,
    agency_name      TEXT NOT NULL,
    agency_url       TEXT,
    agency_timezone  TEXT,
    agency_phone     TEXT,
    agency_lang      TEXT
);

-- Kalendarze kursowania (calendar.txt)
CREATE TABLE IF NOT EXISTS calendar (
    service_id   TEXT PRIMARY KEY,
    monday       INTEGER NOT NULL DEFAULT 0,
    tuesday      INTEGER NOT NULL DEFAULT 0,
    wednesday    INTEGER NOT NULL DEFAULT 0,
    thursday     INTEGER NOT NULL DEFAULT 0,
    friday       INTEGER NOT NULL DEFAULT 0,
    saturday     INTEGER NOT NULL DEFAULT 0,
    sunday       INTEGER NOT NULL DEFAULT 0,
    start_date   TEXT,
    end_date     TEXT
);

-- Przystanki (stops.txt)
CREATE TABLE IF NOT EXISTS stops (
    stop_id    TEXT PRIMARY KEY,
    stop_code  TEXT,
    stop_name  TEXT NOT NULL,
    stop_lat   REAL,
    stop_lon   REAL
);

-- Linie komunikacyjne (routes.txt)
CREATE TABLE IF NOT EXISTS routes (
    route_id          TEXT PRIMARY KEY,
    agency_id         TEXT,
    route_short_name  TEXT,
    route_long_name   TEXT,
    route_desc        TEXT,
    route_type        INTEGER,
    FOREIGN KEY (agency_id) REFERENCES agency (agency_id)
);

-- Kursy (trips.txt)
CREATE TABLE IF NOT EXISTS trips (
    trip_id        TEXT PRIMARY KEY,
    route_id       TEXT NOT NULL,
    service_id     TEXT,
    trip_headsign  TEXT,
    direction_id   INTEGER,
    FOREIGN KEY (route_id)   REFERENCES routes (route_id),
    FOREIGN KEY (service_id) REFERENCES calendar (service_id)
);

-- Zatrzymania na przystankach (stop_times.txt)
-- departure_seconds: pomocnicza liczba sekund od początku doby,
-- ułatwiająca sortowanie i porównywanie godzin (GTFS dopuszcza > 24:00:00).
CREATE TABLE IF NOT EXISTS stop_times (
    trip_id            TEXT NOT NULL,
    stop_sequence      INTEGER NOT NULL,
    arrival_time       TEXT,
    departure_time     TEXT,
    departure_seconds  INTEGER,
    stop_id            TEXT NOT NULL,
    PRIMARY KEY (trip_id, stop_sequence),
    FOREIGN KEY (trip_id) REFERENCES trips (trip_id),
    FOREIGN KEY (stop_id) REFERENCES stops (stop_id)
);

-- Indeksy wspierające zapytania z Zadania 3 (po przystanku).
CREATE INDEX IF NOT EXISTS idx_stop_times_stop_id ON stop_times (stop_id);
CREATE INDEX IF NOT EXISTS idx_stop_times_trip_id ON stop_times (trip_id);
CREATE INDEX IF NOT EXISTS idx_trips_route_id     ON trips (route_id);
