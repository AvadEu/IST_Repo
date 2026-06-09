import datetime

import pytest

from Station import Station
from TimeSeries import TimeSeries
from SeriesValidator import OutlierDetector, ZeroSpikeDetector, ThresholdDetector
from SimpleReporter import SimpleReporter
from Measurements import Measurements


# Helpers
def make_dates(n: int, start: datetime.datetime | None = None) -> list[datetime.datetime]:
    start = start or datetime.datetime(2023, 1, 1, 0, 0)
    return [start + datetime.timedelta(hours=i) for i in range(n)]


def make_series(values: list[float | None], **kwargs) -> TimeSeries:
    dates = make_dates(len(values))
    return TimeSeries(
        parameter_name=kwargs.get("parameter_name", "PM10"),
        station_code=kwargs.get("station_code", "ST01"),
        averaging_time=kwargs.get("averaging_time", "1g"),
        dates=dates,
        values=values,
        unit=kwargs.get("unit", "ug/m3"),
    )


# 3a
def test_station_eq_same_code() -> None:
    a = Station(code="ST01", name="Alfa")
    b = Station(code="ST01", name="Beta")
    assert a == b


def test_station_eq_different_code() -> None:
    a = Station(code="ST01", name="Alfa")
    b = Station(code="ST02", name="Alfa")
    assert a != b


def test_station_eq_other_type() -> None:
    a = Station(code="ST01", name="Alfa")
    assert (a == "ST01") is False


# 3b
def test_getitem_int_index() -> None:
    ts = make_series([10.0, 20.0, 30.0])
    date, value = ts[0]
    assert date == datetime.datetime(2023, 1, 1, 0, 0)
    assert value == 10.0


def test_getitem_slice() -> None:
    ts = make_series([10.0, 20.0, 30.0])
    result = ts[0:2]
    assert result == [
        (datetime.datetime(2023, 1, 1, 0, 0), 10.0),
        (datetime.datetime(2023, 1, 1, 1, 0), 20.0),
    ]


def test_getitem_datetime_existing() -> None:
    ts = make_series([10.0, 20.0, 30.0])
    assert ts[datetime.datetime(2023, 1, 1, 1, 0)] == 20.0


def test_getitem_date_existing() -> None:
    ts = make_series([10.0, 20.0, 30.0])
    assert ts[datetime.date(2023, 1, 1)] == [10.0, 20.0, 30.0]


def test_getitem_date_missing_raises_keyerror() -> None:
    ts = make_series([10.0, 20.0, 30.0])
    with pytest.raises(KeyError):
        _ = ts[datetime.date(1999, 12, 31)]


def test_getitem_datetime_missing_raises_keyerror() -> None:
    ts = make_series([10.0, 20.0, 30.0])
    with pytest.raises(KeyError):
        _ = ts[datetime.datetime(1999, 12, 31, 23, 0)]


# 3c
def test_mean_stddev_complete_data() -> None:
    ts = make_series([2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0])
    assert ts.mean == pytest.approx(5.0)
    assert ts.stddev == pytest.approx(2.0)


def test_mean_stddev_ignore_none() -> None:
    with_none = make_series([2.0, None, 4.0, 4.0, None, 4.0, 5.0, 5.0, None, 7.0, 9.0])
    reference = make_series([2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0])
    assert with_none.mean == pytest.approx(reference.mean)
    assert with_none.stddev == pytest.approx(reference.stddev)


def test_mean_stddev_all_none() -> None:
    ts = make_series([None, None, None])
    assert ts.mean is None
    assert ts.stddev is None


# 3d
def test_outlier_detector_flags_outlier() -> None:
    # Stabilny szereg + jedna duża wartość odstająca.
    values: list[float | None] = [10.0] * 20
    values.append(1000.0)
    ts = make_series(values)
    msgs = OutlierDetector(k=3.0).analyze(ts)
    assert len(msgs) == 1
    assert "OutlierDetector" in msgs[0]
    assert "1000" in msgs[0]


def test_outlier_detector_no_outlier() -> None:
    ts = make_series([10.0, 11.0, 9.0, 10.0, 11.0, 9.0, 10.0])
    assert OutlierDetector(k=3.0).analyze(ts) == []


# 3e
def test_zero_spike_detector_three_zeros() -> None:
    ts = make_series([10.0, 0.0, 0.0, 0.0, 12.0])
    msgs = ZeroSpikeDetector(min_run=3).analyze(ts)
    assert len(msgs) == 1
    assert "ZeroSpikeDetector" in msgs[0]


def test_zero_spike_detector_zeros_and_none() -> None:
    ts = make_series([10.0, 0.0, None, 0.0, 12.0])
    msgs = ZeroSpikeDetector(min_run=3).analyze(ts)
    assert len(msgs) == 1


def test_zero_spike_detector_below_min_run() -> None:
    ts = make_series([10.0, 0.0, 0.0, 12.0])
    assert ZeroSpikeDetector(min_run=3).analyze(ts) == []


# 3f
def test_threshold_detector_exceeds() -> None:
    ts = make_series([100.0, 250.0, 50.0, 300.0])
    msgs = ThresholdDetector(threshold=200.0).analyze(ts)
    assert len(msgs) == 2
    assert all("ThresholdDetector" in m for m in msgs)


def test_threshold_detector_none_exceed() -> None:
    ts = make_series([100.0, 150.0, 50.0])
    assert ThresholdDetector(threshold=200.0).analyze(ts) == []


# 3g
@pytest.fixture
def measurements(tmp_path) -> Measurements:
    csv = (
        "Nr,Kod stacji\n"
        ",ST01\n"
        ",PM10\n"
        ",1g\n"
        ",ug/m3\n"
        ",\n"
        "01/01/23 01:00,300.0\n"
        "01/01/23 02:00,0.0\n"
        "01/01/23 03:00,0.0\n"
        "01/01/23 04:00,0.0\n"
        "01/01/23 05:00,10.0\n"
    )
    path = tmp_path / "2023_PM10_1g.csv"
    path.write_text(csv, encoding="utf-8")
    return Measurements(str(tmp_path))


@pytest.mark.parametrize(
    "analyzer",
    [
        OutlierDetector(k=2.0),
        ZeroSpikeDetector(min_run=3),
        ThresholdDetector(threshold=100.0),
        SimpleReporter(),
    ],
)
def test_analyzer_returns_list_of_messages(analyzer) -> None:
    ts = make_series([300.0, 0.0, 0.0, 0.0, 10.0])
    result = analyzer.analyze(ts)
    assert isinstance(result, list)
    assert all(isinstance(m, str) for m in result)


@pytest.mark.parametrize(
    "validators",
    [
        [OutlierDetector(k=1.0)],
        [ZeroSpikeDetector(min_run=3)],
        [ThresholdDetector(threshold=100.0)],
        [OutlierDetector(k=1.0), ZeroSpikeDetector(min_run=3), SimpleReporter()],
    ],
)
def test_detect_all_anomalies_parametrized(measurements, validators) -> None:
    result = measurements.detect_all_anomalies(validators, preload=True)
    assert isinstance(result, dict)
    key = "ST01/PM10"
    assert key in result
    assert len(result[key]) >= 1
    assert all(isinstance(m, str) for m in result[key])
