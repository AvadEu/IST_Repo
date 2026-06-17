from __future__ import annotations

import argparse
import os

from sqlalchemy import create_engine, event

from create_database import db_filename
from orm_models import Base


def make_engine(db_path: str):
    engine = create_engine(f"sqlite:///{db_path}")

    # Włączenie egzekwowania kluczy obcych dla każdego połączenia SQLite.
    @event.listens_for(engine, "connect")
    def _fk_pragma(dbapi_conn, _record):  # noqa: ANN001
        cur = dbapi_conn.cursor()
        cur.execute("PRAGMA foreign_keys=ON")
        cur.close()

    return engine


def create_database_orm(name: str) -> str:
    path = db_filename(name)
    if os.path.exists(path):
        os.remove(path)
    engine = make_engine(path)
    Base.metadata.create_all(engine)
    engine.dispose()
    return path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Tworzy strukturę bazy GTFS z użyciem ORM (SQLAlchemy)."
    )
    parser.add_argument("database", help="nazwa bazy danych (np. my_timetable_orm)")
    args = parser.parse_args(argv)

    path = create_database_orm(args.database)
    print(f"Utworzono strukturę bazy danych (ORM): {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
