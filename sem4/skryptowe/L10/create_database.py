#!/usr/bin/env python3
"""Zadanie 1b: utworzenie pustej struktury bazy danych SQLite.

Wywołanie:
    python create_database.py my_timetable

tworzy plik ``my_timetable.sqlite3`` zawierający pustą strukturę
(tabele i klucze obce zdefiniowane w pliku ``schema.sql``).
"""
from __future__ import annotations

import argparse
import os
import sqlite3
import sys

SCHEMA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "schema.sql")


def db_filename(name: str) -> str:
    """Zwraca nazwę pliku bazy z rozszerzeniem .sqlite3 (jeśli go brak)."""
    if name.endswith(".sqlite3") or name.endswith(".db") or name.endswith(".sqlite"):
        return name
    return f"{name}.sqlite3"


def create_database(name: str, *, overwrite: bool = False) -> str:
    """Tworzy plik bazy i uruchamia polecenia DDL ze ``schema.sql``."""
    path = db_filename(name)

    if os.path.exists(path):
        if overwrite:
            os.remove(path)
        else:
            print(f"Uwaga: plik '{path}' już istnieje – "
                  f"polecenia CREATE TABLE IF NOT EXISTS zostaną zastosowane "
                  f"do istniejącej bazy.", file=sys.stderr)

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
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="usuń istniejący plik bazy przed utworzeniem struktury",
    )
    args = parser.parse_args(argv)

    path = create_database(args.database, overwrite=args.overwrite)
    print(f"Utworzono strukturę bazy danych: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
