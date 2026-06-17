from __future__ import annotations

import argparse
import os
import sqlite3

SCHEMA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "schema.sql")


def db_filename(name: str) -> str:
    if name.endswith(".sqlite3") or name.endswith(".db") or name.endswith(".sqlite"):
        return name
    return f"{name}.db"


def create_database(name: str) -> str:
    path = db_filename(name)

    if os.path.exists(path):
        os.remove(path)

    with open(SCHEMA_FILE, "r", encoding="utf-8") as fh:
        ddl = fh.read()

    conn = sqlite3.connect(path)
    try:
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.executescript(ddl)
        conn.commit()
    finally:
        conn.close()

    return path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Tworzy pustą strukturę bazy danych SQLite dla rozkładu GTFS."
    )
    parser.add_argument(
        "database",
        help="nazwa bazy danych (bez rozszerzenia powstanie plik <nazwa>.sqlite3)",
    )
    args = parser.parse_args(argv)

    path = create_database(args.database)
    print(f"Utworzono strukturę bazy danych: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
