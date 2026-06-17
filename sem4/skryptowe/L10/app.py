from __future__ import annotations

import argparse
import os
import sys

from flask import Flask, jsonify, render_template, request

import queries
from create_database import db_filename

app = Flask(__name__)
app.config["DB_PATH"] = None


def get_conn():
    return queries.connect(app.config["DB_PATH"])


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/stops")
def api_stops():
    term = request.args.get("q", "").strip()
    conn = get_conn()
    try:
        rows = queries.list_stops(conn, term or None)
    finally:
        conn.close()
    # Ograniczenie liczby zwracanych pozycji dla czytelności.
    data = [
        {
            "stop_id": r["stop_id"],
            "stop_code": r["stop_code"],
            "stop_name": r["stop_name"],
        }
        for r in rows[:200]
    ]
    return jsonify({"count": len(rows), "stops": data})


@app.route("/api/stop/<stop_id>")
def api_stop(stop_id: str):
    conn = get_conn()
    try:
        stop = queries.get_stop(conn, stop_id)
        if stop is None:
            return jsonify({"error": "Nie znaleziono przystanku"}), 404

        earliest, latest = queries.earliest_latest_departure(conn, stop_id)
        result = {
            "stop": {
                "stop_id": stop["stop_id"],
                "stop_code": stop["stop_code"],
                "stop_name": stop["stop_name"],
                "stop_lat": stop["stop_lat"],
                "stop_lon": stop["stop_lon"],
            },
            "routes_count": queries.distinct_routes_count(conn, stop_id),
            "departures_count": queries.departures_count(conn, stop_id),
            "earliest": earliest,
            "latest": latest,
            "headsigns": [
                {"headsign": r["headsign"], "departures": r["departures"]}
                for r in queries.top_headsigns(conn, stop_id, limit=10)
            ],
            "breakdown": [
                {
                    "line": r["line"],
                    "line_name": r["line_name"],
                    "departures": r["departures"],
                    "directions": r["directions"],
                    "first": queries.seconds_to_time(r["first_sec"]),
                    "last": queries.seconds_to_time(r["last_sec"]),
                }
                for r in queries.routes_breakdown(conn, stop_id)
            ],
        }
        return jsonify(result)
    finally:
        conn.close()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Webowy interfejs analizy przystanków GTFS.")
    parser.add_argument("database", help="nazwa bazy danych (np. my_timetable)")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args(argv)

    db_path = db_filename(args.database)
    if not os.path.exists(db_path):
        print(f"Błąd: nie znaleziono bazy '{db_path}'. "
              f"Najpierw uruchom create_database.py i load_data.py.", file=sys.stderr)
        return 1

    app.config["DB_PATH"] = db_path
    print(f"Serwer uruchomiony: http://{args.host}:{args.port}  (baza: {db_path})")
    app.run(host=args.host, port=args.port, debug=args.debug)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
