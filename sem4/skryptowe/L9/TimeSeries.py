import datetime
from typing import overload

import numpy as np


class TimeSeries:

    def __init__(
        self,
        parameter_name: str,
        station_code: str,
        averaging_time: str,
        dates: list[datetime.datetime],
        values: list[float | None],
        unit: str = "",
    ) -> None:
        if len(dates) != len(values):
            raise ValueError("dates and values must have the same length")
        self.parameter_name = parameter_name
        self.station_code = station_code
        self.averaging_time = averaging_time
        self.dates = dates
        self.values = values
        self.unit = unit
        self._date_index: dict[datetime.datetime, int] = {
            dt: i for i, dt in enumerate(dates)
        }

    @overload
    def __getitem__(self, key: int) -> tuple[datetime.datetime, float | None]: ...
    @overload
    def __getitem__(self, key: slice) -> list[tuple[datetime.datetime, float | None]]: ...
    @overload
    def __getitem__(self, key: datetime.date) -> float | None | list[float | None]: ...

    def __getitem__(
        self, key: int | slice | datetime.date
    ) -> (
        tuple[datetime.datetime, float | None]
        | list[tuple[datetime.datetime, float | None]]
        | float
        | None
        | list[float | None]
    ):
        if isinstance(key, int):
            return (self.dates[key], self.values[key])

        if isinstance(key, slice):
            return list(zip(self.dates[key], self.values[key]))

        if isinstance(key, datetime.datetime):
            if key not in self._date_index:
                raise KeyError(key)
            return self.values[self._date_index[key]]

        if isinstance(key, datetime.date):
            results = [
                self.values[i]
                for i, dt in enumerate(self.dates)
                if dt.date() == key
            ]
            if not results:
                raise KeyError(key)
            return results if len(results) > 1 else results[0]

        raise TypeError(f"Unsupported key type: {type(key)}")

    def __len__(self) -> int:
        return len(self.dates)

    def __repr__(self) -> str:
        return (
            f"TimeSeries(parameter={self.parameter_name!r}, "
            f"station={self.station_code!r}, "
            f"n={len(self)}, unit={self.unit!r})"
        )

    @property
    def mean(self) -> float | None:
        valid = [v for v in self.values if v is not None]
        return float(np.mean(valid)) if valid else None

    @property
    def stddev(self) -> float | None:
        valid = [v for v in self.values if v is not None]
        return float(np.std(valid, ddof=0)) if len(valid) > 1 else None

    @property
    def min_value(self) -> float | None:
        valid = [v for v in self.values if v is not None]
        return min(valid) if len(valid) > 1 else None

    @property
    def max_value(self) -> float | None:
        valid = [v for v in self.values if v is not None]
        return max(valid) if len(valid) > 1 else None

    def _valid_pairs(self) -> list[tuple[datetime.datetime, float]]:
        return [(d, v) for d, v in zip(self.dates, self.values) if v is not None]
