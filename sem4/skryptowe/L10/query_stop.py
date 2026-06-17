#!/usr/bin/env python3
"""Zadanie 3: interaktywna analiza wybranego przystanku (interfejs tekstowy).

Wywołanie:
    python query_stop.py my_timetable

Użytkownik wyszukuje i wybiera przystanek z listy, a skrypt – za pomocą
zapytań SQL typu SELECT – wyświetla:
  a) liczbę różnych linii zatrzymujących się na przystanku,
  b) liczbę odjazdów z przystanku,
  c) najwcześniejszy i najpóźniejszy odjazd,
  d) najczęstsze kierunki odjazdów,
  e) nietrywialne zestawienie linii (połączenie 3 tabel + grupowanie).
"""
from __future__ import annotations

import argparse
import os
import sys

import queries
from create_database import db_filename


def choose_stop(conn) -> str | None:
    """Wyszukiwanie i wybór przystanku z listy."""
    while True:
        term = input("\nPodaj fragment nazwy przystanku (Enter = wszystkie, 'q' = wyjście): ").strip()
        if term.lower() == "q":
            return None
        stops = queries.list_stops(conn, term or None)
        if not stops:
            print("  Brak przystanków pasujących do zapytania.")
            continue
        if len(stops) > 40:
            print(f"  Znaleziono {len(stops)} przystanków – uściślij wyszukiwanie.")
            continue

        for idx, s in enumerate(stops, start=1):
            code = s["stop_code"] or "—"
            print(f"  [{idx:>3}] {s['stop_name']}  (kod {code}, id {s['stop_id']})")

        sel = input("Wybierz numer przystanku (Enter = szukaj ponownie): ").strip()
        if not sel:
            continue
        if not sel.isdigit() or not (1 <= int(sel) <= len(stops)):
            print("  Nieprawidłowy numer.")
            continue
        return stops[int(sel) - 1]["stop_id"]


def report(conn, stop_id: str) -> None:
    stop = queries.get_stop(conn, stop_id)
    print("\n" + "=" * 60)
    print(f"Przystanek: {stop['stop_name']}  (kod {stop['stop_code'] or '—'}, id {stop['stop_id']})")
    print("=" * 60)

    # 3a
    print(f"a) Różne linie zatrzymujące się na przystanku: "
          f"{queries.distinct_routes_count(conn, stop_id)}")

    # 3b
    print(f"b) Liczba odjazdów z przystanku: "
          f"{queries.departures_count(conn, stop_id)}")

    # 3c
    earliest, latest = queries.earliest_latest_departure(conn, stop_id)
    print(f"c) Najwcześniejszy odjazd: {earliest or '—'}, "
          f"najpóźniejszy odjazd: {latest or '—'}")

    # 3d
    print("d) Najczęstsze kierunki odjazdów:")
    rows = queries.top_headsigns(conn, stop_id, limit=10)
    if not rows:
        print("   (brak danych)")
    for r in rows:
        print(f"   - {r['headsign']:<35} {r['departures']:>5} odjazdów")

    # 3e
    print("e) Zestawienie linii (liczba odjazdów, kierunki, pierwszy/ostatni odjazd):")
    rows = queries.routes_breakdown(conn, stop_id)
    if not rows:
        print("   (brak danych)")
    print(f"   {'Linia':<8}{'Odjazdy':>9}{'Kier.':>7}  {'Pierwszy':>9} {'Ostatni':>9}  Nazwa trasy")
    for r in rows:
        first = queries.seconds_to_time(r["first_sec"])
        last = queries.seconds_to_time(r["last_sec"])
        name = (r["line_name"] or "")[:40]
        print(f"   {r['line'] or '?':<8}{r['departures']:>9}{r['directions']:>7}  "
              f"{first:>9} {last:>9}  {name}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Interaktywna analiza przystanku z bazy rozkładu GTFS."
    )
    parser.add_argument("database", help="nazwa bazy danych (np. my_timetable)")
    args = parser.parse_args(argv)

    db_path = db_filename(args.database)
    if not os.path.exists(db_path):
        print(f"Błąd: nie znaleziono bazy '{db_path}'. "
              f"Najpierw uruchom create_database.py i load_data.py.", file=sys.stderr)
        return 1

    conn = queries.connect(db_path)
    try:
        while True:
            stop_id = choose_stop(conn)
            if stop_id is None:
                break
            report(conn, stop_id)
    except (KeyboardInterrupt, EOFError):
        print()
    finally:
        conn.close()
    print("Do widzenia.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
