from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable
from TimeSeries import TimeSeries

import datetime


@runtime_checkable
class Analyzer(Protocol):
    def analyze(self, series: TimeSeries) -> list[str]:
        ...


class SeriesValidator(ABC):

    @abstractmethod
    def analyze(self, series: TimeSeries) -> list[str]:
        ...


class OutlierDetector(SeriesValidator):

    def __init__(self, k: float = 3.0) -> None:
        self.k = k

    def analyze(self, series: TimeSeries) -> list[str]:
        mean = series.mean
        std = series.stddev
        if mean is None or std is None or std == 0:
            return []
        messages: list[str] = []
        for dt, val in series._valid_pairs():
            if abs(val - mean) > self.k * std:
                messages.append(
                    f"[OutlierDetector] {series.parameter_name}@{series.station_code} "
                    f"{dt}: value={val:.2f} is {abs(val - mean)/std:.1f}σ from mean "
                    f"(mean={mean:.2f}, std={std:.2f}, k={self.k})"
                )
        return messages


class ZeroSpikeDetector(SeriesValidator):

    def __init__(self, min_run: int = 3) -> None:
        self.min_run = min_run

    def analyze(self, series: TimeSeries) -> list[str]:
        messages: list[str] = []
        run_start: datetime.datetime | None = None
        run_len = 0

        def close_run():
            nonlocal run_start, run_len
            if run_len >= self.min_run:
                messages.append(
                    f"[ZeroSpikeDetector] {series.parameter_name}@{series.station_code} "
                    f"run of {run_len} zero/None values starting at {run_start}"
                )
            run_start = None
            run_len = 0

        for dt, val in zip(series.dates, series.values):
            if val is None or val == 0.0:
                if run_len == 0:
                    run_start = dt
                run_len += 1
            else:
                close_run()
        close_run()
        return messages


class ThresholdDetector(SeriesValidator):

    def __init__(self, threshold: float) -> None:
        self.threshold = threshold

    def analyze(self, series: TimeSeries) -> list[str]:
        messages: list[str] = []
        for dt, val in series._valid_pairs():
            if val > self.threshold:
                messages.append(
                    f"[ThresholdDetector] {series.parameter_name}@{series.station_code} "
                    f"{dt}: value={val:.2f} exceeds threshold={self.threshold}"
                )
        return messages
