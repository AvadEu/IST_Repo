import datetime
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

    def __getitem__(self, key):
        if isinstance(key, (int, slice)):
            dates_slice = self.dates[key]
            values_slice = self.values[key]
            if isinstance(key, int):
                return (dates_slice, values_slice)
            return list(zip(dates_slice, values_slice))

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

    def _valid_pairs(self) -> list[tuple[datetime.datetime, float]]:
        return [(d, v) for d, v in zip(self.dates, self.values) if v is not None]
