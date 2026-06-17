from __future__ import annotations

import sqlite3
from typing import Any


def connect(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def list_stops(conn: sqlite3.Connection, name_filter: str | None = None) -> list[sqlite3.Row]:
    """Lista przystanków (opcjonalnie filtrowana po fragmencie nazwy)."""
    sql = "SELECT stop_id, stop_code, stop_name, stop_lat, stop_lon FROM stops"
    params: list[Any] = []
    if name_filter:
        sql += " WHERE stop_name LIKE ?"
        params.append(f"%{name_filter}%")
    sql += " ORDER BY stop_name, stop_id"
    return conn.execute(sql, params).fetchall()


def get_stop(conn: sqlite3.Connection, stop_id: str) -> sqlite3.Row | None:
    return conn.execute(
        "SELECT stop_id, stop_code, stop_name, stop_lat, stop_lon "
        "FROM stops WHERE stop_id = ?",
        (stop_id,),
    ).fetchone()


# 3a. Liczba różnych linii zatrzymujących się na przystanku.
def distinct_routes_count(conn: sqlite3.Connection, stop_id: str) -> int:
    row = conn.execute(
        """
        SELECT COUNT(DISTINCT t.route_id) AS n
        FROM stop_times st
        JOIN trips t ON t.trip_id = st.trip_id
        WHERE st.stop_id = ?
        """,
        (stop_id,),
    ).fetchone()
    return row["n"]


# 3b. Liczba odjazdów z przystanku.
def departures_count(conn: sqlite3.Connection, stop_id: str) -> int:
    row = conn.execute(
        """
        SELECT COUNT(*) AS n
        FROM stop_times
        WHERE stop_id = ? AND departure_time IS NOT NULL
        """,
        (stop_id,),
    ).fetchone()
    return row["n"]


# 3c. Najwcześniejszy i najpóźniejszy odjazd (sortowanie po sekundach od północy).
def earliest_latest_departure(conn: sqlite3.Connection, stop_id: str) -> tuple[str | None, str | None]:
    row = conn.execute(
        """
        SELECT
            (SELECT departure_time FROM stop_times
             WHERE stop_id = :sid AND departure_seconds IS NOT NULL
             ORDER BY departure_seconds ASC  LIMIT 1) AS earliest,
            (SELECT departure_time FROM stop_times
             WHERE stop_id = :sid AND departure_seconds IS NOT NULL
             ORDER BY departure_seconds DESC LIMIT 1) AS latest
        """,
        {"sid": stop_id},
    ).fetchone()
    return row["earliest"], row["latest"]


# 3d. Najczęstsze kierunki odjazdów (trip_headsign) z przystanku.
def top_headsigns(conn: sqlite3.Connection, stop_id: str, limit: int = 10) -> list[sqlite3.Row]:
    return conn.execute(
        """
        SELECT t.trip_headsign AS headsign, COUNT(*) AS departures
        FROM stop_times st
        JOIN trips t ON t.trip_id = st.trip_id
        WHERE st.stop_id = ? AND t.trip_headsign IS NOT NULL
        GROUP BY t.trip_headsign
        ORDER BY departures DESC, headsign ASC
        LIMIT ?
        """,
        (stop_id, limit),
    ).fetchall()


# 3e. Zapytanie nietrywialne:
#   Dla każdej linii zatrzymującej się na przystanku zestawia liczbę odjazdów
#   oraz godziny pierwszego i ostatniego odjazdu. Łączy 3 tabele
#   (stop_times + trips + routes), grupuje i agreguje.
def routes_breakdown(conn: sqlite3.Connection, stop_id: str) -> list[sqlite3.Row]:
    return conn.execute(
        """
        SELECT
            r.route_short_name                         AS line,
            r.route_long_name                          AS line_name,
            COUNT(*)                                   AS departures,
            COUNT(DISTINCT t.trip_headsign)            AS directions,
            MIN(st.departure_seconds)                  AS first_sec,
            MAX(st.departure_seconds)                  AS last_sec
        FROM stop_times st
        JOIN trips t  ON t.trip_id  = st.trip_id
        JOIN routes r ON r.route_id = t.route_id
        WHERE st.stop_id = ?
        GROUP BY r.route_id, r.route_short_name, r.route_long_name
        ORDER BY departures DESC, line ASC
        """,
        (stop_id,),
    ).fetchall()


def seconds_to_time(value: int | None) -> str:
    """Liczba sekund od północy -> 'HH:MM' (dla prezentacji)."""
    if value is None:
        return "—"
    h, rem = divmod(value, 3600)
    m = rem // 60
    return f"{h:02d}:{m:02d}"
