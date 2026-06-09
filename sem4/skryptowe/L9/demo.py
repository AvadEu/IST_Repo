import os
import math
import datetime

from Station import Station
from TimeSeries import TimeSeries
from Measurements import Measurements
from SimpleReporter import SimpleReporter
from SeriesValidator import (
    Analyzer,
    OutlierDetector,
    ZeroSpikeDetector,
    ThresholdDetector,
)

import pandas as pd


def main() -> None:
    DATA_DIR = "./data"

    print("Zad 1")
    stations = Station.load_all(os.path.join(DATA_DIR, "stacje.csv"))
    first_code = next(iter(stations))
    st = stations[first_code]
    print("str :", st)
    print("repr:", repr(st))
    st2 = Station(code=first_code, name="copy")
    print(f"st == st2 (same code): {st == st2}")
    print(f"Total stations loaded: {len(stations)}\n")

    print("Zad 2, 3")
    raw = pd.read_csv(os.path.join(DATA_DIR, "measurements/2023_PM10_1g.csv"), header=None, dtype=str)
    col = 2
    station_code = str(raw.iloc[1, col]).strip()
    parameter_name = str(raw.iloc[2, col]).strip()
    averaging_time = str(raw.iloc[3, col]).strip()
    unit = str(raw.iloc[4, col]).strip()

    data_rows = raw.iloc[6:]
    timestamps, values = [], []
    for _, row in data_rows.iterrows():
        try:
            timestamps.append(datetime.datetime.strptime(str(row.iloc[0]).strip(), "%d/%m/%y %H:%M"))
        except ValueError:
            continue
        try:
            fv = float(row.iloc[col])
            values.append(None if math.isnan(fv) else fv)
        except (ValueError, TypeError):
            values.append(None)

    ts = TimeSeries(parameter_name, station_code, averaging_time, timestamps, values, unit)
    print(repr(ts))
    print(f"Mean  : {ts.mean:.4f} {ts.unit}")
    print(f"StdDev: {ts.stddev:.4f} {ts.unit}")
    print(f"ts[0] (index)  : {ts[0]}")
    print(f"ts[1:3] (slice): {ts[1:3]}")
    first_date = timestamps[0]
    print(f"ts[datetime]   : {ts[first_date]} (value at {first_date})")
    print(f"ts[date]       : {ts[first_date.date()]} (value(s) on {first_date.date()})\n")

    print("Zad 4")
    detectors = [
        OutlierDetector(k=3.0),
        ZeroSpikeDetector(min_run=3),
        ThresholdDetector(threshold=200.0),
    ]
    for d in detectors:
        msgs = d.analyze(ts)
        label = type(d).__name__
        print(f"{label}: {len(msgs)} anomaly/anomalies found")
        for m in msgs[:3]:
            print("  ", m)
    print()

    print("Zad 5")
    meas = Measurements(DATA_DIR + '/measurements')
    print(f"Files found       : {list(meas._files.keys())}")
    print(f"TimeSeries count  : {len(meas)}")
    print(f"'PM10' in meas    : {'PM10' in meas}")
    station_sample = list(stations.keys())[5]
    by_station = meas.get_by_station(station_sample)
    print(f"get_by_station({station_sample!r}): {len(by_station)} series")
    by_param = meas.get_by_parameter("PM10")
    print(f"get_by_parameter('PM10'): {len(by_param)} series\n")

    print("Zad 6")
    anomalies = meas.detect_all_anomalies(detectors, preload=True)
    print(f"Series with anomalies: {len(anomalies)}")
    for key, msgs in list(anomalies.items())[:3]:
        print(f"  {key}: {len(msgs)} message(s)")
        for m in msgs[:2]:
            print("    ", m)
    print()

    print("Zad 7")
    from collections import defaultdict
    per_validator: dict[str, int] = defaultdict(int)
    for msgs in anomalies.values():
        for m in msgs:
            tag = m.split("]")[0].lstrip("[")
            per_validator[tag] += 1
    for tag, count in per_validator.items():
        print(f"  {tag}: {count} anomaly message(s)")
    print()

    print("Zad 8")
    reporter = SimpleReporter()
    analyzers: list[Analyzer] = [
        OutlierDetector(k=2.5),
        ZeroSpikeDetector(min_run=3),
        ThresholdDetector(threshold=150.0),
        reporter,
    ]
    for analyzer in analyzers:
        result = analyzer.analyze(ts)      # pure duck typing
        print(f"  {type(analyzer).__name__}: {result[0] if result else '(no messages)'}")


if __name__ == "__main__":
    main()
