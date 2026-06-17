#!/usr/bin/env python3
"""Zadanie 2: import danych GTFS do bazy SQLite.

Wywołanie:
    python load_data.py OtwartyWroclaw_rozklad_jazdy_GTFS.zip my_timetable

Źródłem danych może być paczka ZIP albo katalog z plikami ``*.txt``.
Dane wstawiane są w kolejności zgodnej z kluczami obcymi:
    agency -> calendar -> stops -> routes -> trips -> stop_times
Duże pliki (stop_times) wstawiane są partiami w obrębie transakcji.
"""
from __future__ import annotations

import argparse
import sqlite3
import sys

from create_database import db_filename
from gtfs_common import GtfsSource, time_to_seconds

BATCH_SIZE = 10_000


def _i(value: str | None) -> int | None:
    if value is None or value.strip() == "":
        return None
    try:
        return int(value)
    except ValueError:
        return None


def _f(value: str | None) -> float | None:
    if value is None or value.strip() == "":
        return None
    try:
        return float(value)
    except ValueError:
        return None


def _s(value: str | None) -> str | None:
    if value is None:
        return None
    value = value.strip()
    return value if value else None


def load_agency(conn: sqlite3.Connection, src: GtfsSource) -> int:
    rows = [
        (
            r.get("agency_id"),
            _s(r.get("agency_name")) or "",
            _s(r.get("agency_url")),
            _s(r.get("agency_timezone")),
            _s(r.get("agency_phone")),
            _s(r.get("agency_lang")),
        )
        for r in src.read_rows("agency.txt")
    ]
    conn.executemany(
        "INSERT OR REPLACE INTO agency "
        "(agency_id, agency_name, agency_url, agency_timezone, agency_phone, agency_lang) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        rows,
    )
    return len(rows)


def load_calendar(conn: sqlite3.Connection, src: GtfsSource) -> int:
    if not src.has("calendar.txt"):
        return 0
    rows = [
        (
            r.get("service_id"),
            _i(r.get("monday")) or 0,
            _i(r.get("tuesday")) or 0,
            _i(r.get("wednesday")) or 0,
            _i(r.get("thursday")) or 0,
            _i(r.get("friday")) or 0,
            _i(r.get("saturday")) or 0,
            _i(r.get("sunday")) or 0,
            _s(r.get("start_date")),
            _s(r.get("end_date")),
        )
        for r in src.read_rows("calendar.txt")
    ]
    conn.executemany(
        "INSERT OR REPLACE INTO calendar "
        "(service_id, monday, tuesday, wednesday, thursday, friday, saturday, sunday, "
        "start_date, end_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        rows,
    )
    return len(rows)


def load_stops(conn: sqlite3.Connection, src: GtfsSource) -> int:
    rows = [
        (
            r.get("stop_id"),
            _s(r.get("stop_code")),
            _s(r.get("stop_name")) or "",
            _f(r.get("stop_lat")),
            _f(r.get("stop_lon")),
        )
        for r in src.read_rows("stops.txt")
    ]
    conn.executemany(
        "INSERT OR REPLACE INTO stops "
        "(stop_id, stop_code, stop_name, stop_lat, stop_lon) VALUES (?, ?, ?, ?, ?)",
        rows,
    )
    return len(rows)


def load_routes(conn: sqlite3.Connection, src: GtfsSource) -> int:
    rows = [
        (
            r.get("route_id"),
            _s(r.get("agency_id")),
            _s(r.get("route_short_name")),
            _s(r.get("route_long_name")),
            _s(r.get("route_desc")),
            _i(r.get("route_type")),
        )
        for r in src.read_rows("routes.txt")
    ]
    conn.executemany(
        "INSERT OR REPLACE INTO routes "
        "(route_id, agency_id, route_short_name, route_long_name, route_desc, route_type) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        rows,
    )
    return len(rows)


def load_trips(conn: sqlite3.Connection, src: GtfsSource) -> int:
    rows = [
        (
            r.get("trip_id"),
            r.get("route_id"),
            _s(r.get("service_id")),
            _s(r.get("trip_headsign")),
            _i(r.get("direction_id")),
        )
        for r in src.read_rows("trips.txt")
    ]
    conn.executemany(
        "INSERT OR REPLACE INTO trips "
        "(trip_id, route_id, service_id, trip_headsign, direction_id) "
        "VALUES (?, ?, ?, ?, ?)",
        rows,
    )
    return len(rows)


def load_stop_times(conn: sqlite3.Connection, src: GtfsSource) -> int:
    """Wstawianie partiami – stop_times.txt bywa bardzo duży."""
    sql = (
        "INSERT OR REPLACE INTO stop_times "
        "(trip_id, stop_sequence, arrival_time, departure_time, departure_seconds, stop_id) "
        "VALUES (?, ?, ?, ?, ?, ?)"
    )
    batch: list[tuple] = []
    total = 0
    for r in src.read_rows("stop_times.txt"):
        departure = _s(r.get("departure_time"))
        batch.append(
            (
                r.get("trip_id"),
                _i(r.get("stop_sequence")),
                _s(r.get("arrival_time")),
                departure,
                time_to_seconds(departure),
                r.get("stop_id"),
            )
        )
        if len(batch) >= BATCH_SIZE:
            conn.executemany(sql, batch)
            total += len(batch)
            batch.clear()
    if batch:
        conn.executemany(sql, batch)
        total += len(batch)
    return total


def load_all(db_path: str, gtfs_path: str) -> None:
    src = GtfsSource(gtfs_path)
    conn = sqlite3.connect(db_path)
    try:
        conn.execute("PRAGMA foreign_keys = ON;")
        # Przyspieszenie masowego importu.
        conn.execute("PRAGMA journal_mode = WAL;")
        conn.execute("PRAGMA synchronous = NORMAL;")

        steps = [
            ("agency", load_agency),
            ("calendar", load_calendar),
            ("stops", load_stops),
            ("routes", load_routes),
            ("trips", load_trips),
            ("stop_times", load_stop_times),
        ]
        for name, fn in steps:
            conn.execute("BEGIN;")
            count = fn(conn, src)
            conn.commit()
            print(f"  {name:<12}: wczytano {count} rekordów")
    finally:
        conn.close()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Importuje dane GTFS (ZIP lub katalog) do bazy SQLite."
    )
    parser.add_argument("gtfs", help="paczka GTFS (.zip) lub katalog z plikami .txt")
    parser.add_argument("database", help="nazwa bazy danych (np. my_timetable)")
    args = parser.parse_args(argv)

    db_path = db_filename(args.database)

    try:
        src = GtfsSource(args.gtfs)
    except FileNotFoundError as exc:
        print(f"Błąd: {exc}", file=sys.stderr)
        return 1
    del src  # walidacja tylko; load_all otworzy ponownie

    print(f"Import danych z '{args.gtfs}' do '{db_path}'...")
    load_all(db_path, args.gtfs)
    print("Import zakończony.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
