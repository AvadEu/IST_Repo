import math
import datetime

import pandas as pd

from TimeSeries import TimeSeries


def parse_measurement_csv(path: str) -> list[TimeSeries]:
    raw = pd.read_csv(path, header=None, dtype=str)

    station_row = 1
    param_row = 2
    avg_row = 3
    unit_row = 4

    data = raw.iloc[6:].copy()
    data = data.reset_index(drop=True)

    timestamps: list[datetime.datetime | None] = []
    for ts_str in data.iloc[:, 0]:
        try:
            timestamps.append(datetime.datetime.strptime(str(ts_str).strip(), "%d/%m/%y %H:%M"))
        except ValueError:
            timestamps.append(None)

    series_list: list[TimeSeries] = []
    for col_idx in range(1, len(raw.columns)):
        station_code = str(raw.iloc[station_row, col_idx]).strip()
        parameter_name = str(raw.iloc[param_row, col_idx]).strip()
        averaging_time = str(raw.iloc[avg_row, col_idx]).strip()
        unit = str(raw.iloc[unit_row, col_idx]).strip()

        raw_vals = data.iloc[:, col_idx]
        values: list[float | None] = []
        for v in raw_vals:
            try:
                fv = float(v)
                values.append(None if math.isnan(fv) else fv)
            except (ValueError, TypeError):
                values.append(None)

        valid_dates: list[datetime.datetime] = []
        valid_values: list[float | None] = []
        for dt, val in zip(timestamps, values):
            if dt is not None:
                valid_dates.append(dt)
                valid_values.append(val)

        series_list.append(
            TimeSeries(
                parameter_name=parameter_name,
                station_code=station_code,
                averaging_time=averaging_time,
                dates=valid_dates,
                values=valid_values,
                unit=unit,
            )
        )
    return series_list
