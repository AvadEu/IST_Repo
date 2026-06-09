import os
from typing import Iterator, Sequence

from TimeSeries import TimeSeries
from SeriesValidator import Analyzer
from utils import parse_measurement_csv

import pandas as pd


class Measurements:

    def __init__(self, directory: str) -> None:
        self._directory = directory
        self._files: dict[str, list[TimeSeries] | None] = {}

        for fname in os.listdir(directory):
            if fname.lower().endswith(".csv"):
                self._files[fname] = None   # lazy placeholder

    def _load_file(self, fname: str) -> list[TimeSeries]:
        cached = self._files[fname]
        if cached is None:
            path = os.path.join(self._directory, fname)
            cached = parse_measurement_csv(path)
            self._files[fname] = cached
        return cached

    def _all_loaded(self) -> Iterator[TimeSeries]:
        for fname, series_list in self._files.items():
            if series_list is not None:
                yield from series_list

    def _all_series(self) -> Iterator[TimeSeries]:
        for fname in self._files:
            yield from self._load_file(fname)

    def __len__(self) -> int:
        total = 0
        for fname in self._files:
            path = os.path.join(self._directory, fname)
            header = pd.read_csv(path, header=None, nrows=1, dtype=str)
            total += len(header.columns) - 1
        return total

    def __contains__(self, parameter_name: str) -> bool:
        for ts in self._all_series():
            if ts.parameter_name == parameter_name:
                return True
        return False

    def get_by_parameter(self, param_name: str) -> list[TimeSeries]:
        return [ts for ts in self._all_series() if ts.parameter_name == param_name]

    def get_by_station(self, station_code: str) -> list[TimeSeries]:
        return [ts for ts in self._all_series() if ts.station_code == station_code]

    def detect_all_anomalies(
        self,
        validators: Sequence[Analyzer],
        preload: bool = False,
    ) -> dict[str, list[str]]:
        if preload:
            iterator = self._all_series()
        else:
            iterator = self._all_loaded()

        results: dict[str, list[str]] = {}
        for ts in iterator:
            key = f"{ts.station_code}/{ts.parameter_name}"
            messages: list[str] = []
            for validator in validators:
                messages.extend(validator.analyze(ts))
            if messages:
                results[key] = messages
        return results
