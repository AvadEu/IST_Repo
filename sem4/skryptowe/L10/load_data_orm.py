#!/usr/bin/env python3
"""Wersja dla ambitnych – Zadanie 2 z użyciem ORM (SQLAlchemy).

Importuje dane GTFS przy użyciu modeli ORM oraz wykonuje na koniec
przykładowe zapytanie agregujące zrealizowane środkami ORM.

Wywołanie:
    python load_data_orm.py data my_timetable_orm
    python load_data_orm.py OtwartyWroclaw_GTFS.zip my_timetable_orm
"""
from __future__ import annotations

import argparse
import os
import sys

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from create_database import db_filename
from create_database_orm import create_database_orm, make_engine
from gtfs_common import GtfsSource, time_to_seconds
from orm_models import Agency, Calendar, Route, Stop, StopTime, Trip

BATCH_SIZE = 10_000


def _i(value, default=None):
    if value is None or str(value).strip() == "":
        return default
    try:
        return int(value)
    except ValueError:
        return default


def _f(value):
    if value is None or str(value).strip() == "":
        return None
    try:
        return float(value)
    except ValueError:
        return None


def _s(value):
    if value is None:
        return None
    value = value.strip()
    return value or None


def import_simple(session: Session, src: GtfsSource, filename: str, builder) -> int:
    """Import niewielkich tabel: budowa obiektów ORM i bulk-zapis."""
    if not src.has(filename):
        return 0
    objects = [builder(r) for r in src.read_rows(filename)]
    session.bulk_save_objects(objects)
    session.commit()
    return len(objects)


def import_stop_times(session: Session, src: GtfsSource) -> int:
    """Import dużej tabeli stop_times partiami (mappings = wydajniej)."""
    batch: list[dict] = []
    total = 0

    def flush():
        nonlocal total
        if batch:
            session.bulk_insert_mappings(StopTime, batch)
            session.commit()
            total += len(batch)
            batch.clear()

    for r in src.read_rows("stop_times.txt"):
        departure = _s(r.get("departure_time"))
        batch.append(
            {
                "trip_id": r.get("trip_id"),
                "stop_sequence": _i(r.get("stop_sequence")),
                "arrival_time": _s(r.get("arrival_time")),
                "departure_time": departure,
                "departure_seconds": time_to_seconds(departure),
                "stop_id": r.get("stop_id"),
            }
        )
        if len(batch) >= BATCH_SIZE:
            flush()
    flush()
    return total


def load_all_orm(db_path: str, gtfs_path: str) -> None:
    src = GtfsSource(gtfs_path)
    engine = make_engine(db_path)
    with Session(engine) as session:
        n = import_simple(session, src, "agency.txt", lambda r: Agency(
            agency_id=r.get("agency_id"),
            agency_name=_s(r.get("agency_name")) or "",
            agency_url=_s(r.get("agency_url")),
            agency_timezone=_s(r.get("agency_timezone")),
            agency_phone=_s(r.get("agency_phone")),
            agency_lang=_s(r.get("agency_lang")),
        ))
        print(f"  agency      : wczytano {n} rekordów")

        n = import_simple(session, src, "calendar.txt", lambda r: Calendar(
            service_id=r.get("service_id"),
            monday=_i(r.get("monday"), 0), tuesday=_i(r.get("tuesday"), 0),
            wednesday=_i(r.get("wednesday"), 0), thursday=_i(r.get("thursday"), 0),
            friday=_i(r.get("friday"), 0), saturday=_i(r.get("saturday"), 0),
            sunday=_i(r.get("sunday"), 0),
            start_date=_s(r.get("start_date")), end_date=_s(r.get("end_date")),
        ))
        print(f"  calendar    : wczytano {n} rekordów")

        n = import_simple(session, src, "stops.txt", lambda r: Stop(
            stop_id=r.get("stop_id"), stop_code=_s(r.get("stop_code")),
            stop_name=_s(r.get("stop_name")) or "",
            stop_lat=_f(r.get("stop_lat")), stop_lon=_f(r.get("stop_lon")),
        ))
        print(f"  stops       : wczytano {n} rekordów")

        n = import_simple(session, src, "routes.txt", lambda r: Route(
            route_id=r.get("route_id"), agency_id=_s(r.get("agency_id")),
            route_short_name=_s(r.get("route_short_name")),
            route_long_name=_s(r.get("route_long_name")),
            route_desc=_s(r.get("route_desc")), route_type=_i(r.get("route_type")),
        ))
        print(f"  routes      : wczytano {n} rekordów")

        n = import_simple(session, src, "trips.txt", lambda r: Trip(
            trip_id=r.get("trip_id"), route_id=r.get("route_id"),
            service_id=_s(r.get("service_id")),
            trip_headsign=_s(r.get("trip_headsign")),
            direction_id=_i(r.get("direction_id")),
        ))
        print(f"  trips       : wczytano {n} rekordów")

        n = import_stop_times(session, src)
        print(f"  stop_times  : wczytano {n} rekordów")

    engine.dispose()


def demo_aggregate_query(db_path: str, limit: int = 10) -> None:
    """Przykładowe zapytanie agregujące w ORM:
    10 przystanków o największej liczbie odjazdów (JOIN + GROUP BY + COUNT).
    """
    engine = make_engine(db_path)
    with Session(engine) as session:
        stmt = (
            select(Stop.stop_name, func.count(StopTime.trip_id).label("departures"))
            .join(StopTime, StopTime.stop_id == Stop.stop_id)
            .group_by(Stop.stop_id, Stop.stop_name)
            .order_by(func.count(StopTime.trip_id).desc())
            .limit(limit)
        )
        print(f"\nZapytanie agregujące ORM – top {limit} przystanków wg liczby odjazdów:")
        for name, departures in session.execute(stmt):
            print(f"  {departures:>6}  {name}")
    engine.dispose()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Import GTFS do bazy SQLite przy użyciu ORM (SQLAlchemy)."
    )
    parser.add_argument("gtfs", help="paczka GTFS (.zip) lub katalog z plikami .txt")
    parser.add_argument("database", help="nazwa bazy danych (np. my_timetable_orm)")
    parser.add_argument("--create", action="store_true",
                        help="utwórz strukturę bazy (ORM) przed importem")
    args = parser.parse_args(argv)

    db_path = db_filename(args.database)

    if args.create or not os.path.exists(db_path):
        create_database_orm(db_path, overwrite=args.create)
        print(f"Utworzono strukturę bazy (ORM): {db_path}")

    try:
        GtfsSource(args.gtfs)
    except FileNotFoundError as exc:
        print(f"Błąd: {exc}", file=sys.stderr)
        return 1

    print(f"Import danych z '{args.gtfs}' do '{db_path}' (ORM)...")
    load_all_orm(db_path, args.gtfs)
    print("Import zakończony.")
    demo_aggregate_query(db_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
