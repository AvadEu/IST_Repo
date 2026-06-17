from __future__ import annotations

import csv
import io
import os
import zipfile
from contextlib import contextmanager
from typing import Iterator


def time_to_seconds(value: str | None) -> int | None:
    if value is None:
        return None
    value = value.strip()
    if not value:
        return None
    parts = value.split(":")
    if len(parts) != 3:
        return None
    try:
        h, m, s = (int(p) for p in parts)
    except ValueError:
        return None
    return h * 3600 + m * 60 + s


class GtfsSource:
    def __init__(self, path: str):
        if not os.path.exists(path):
            raise FileNotFoundError(f"Nie znaleziono źródła GTFS: {path}")
        self.path = path
        self.is_zip = zipfile.is_zipfile(path) and not os.path.isdir(path)

    def has(self, filename: str) -> bool:
        if self.is_zip:
            with zipfile.ZipFile(self.path) as zf:
                return filename in zf.namelist()
        return os.path.exists(os.path.join(self.path, filename))

    @contextmanager
    def open_text(self, filename: str):
        """Otwiera plik tekstowy GTFS w kodowaniu utf-8 (z obsługą BOM)."""
        if self.is_zip:
            with zipfile.ZipFile(self.path) as zf:
                with zf.open(filename) as raw:
                    yield io.TextIOWrapper(raw, encoding="utf-8-sig", newline="")
        else:
            full = os.path.join(self.path, filename)
            with open(full, "r", encoding="utf-8-sig", newline="") as fh:
                yield fh

    def read_rows(self, filename: str) -> Iterator[dict[str, str]]:
        """Iteruje po wierszach pliku jako słowniki {kolumna: wartość}."""
        with self.open_text(filename) as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                yield row
