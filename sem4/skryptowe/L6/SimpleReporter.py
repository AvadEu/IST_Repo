from TimeSeries import TimeSeries


class SimpleReporter:

    def analyze(self, series: TimeSeries) -> list[str]:
        mean_str = f"{series.mean:.4f}" if series.mean is not None else "N/A"
        return [
            f"[Info] {series.parameter_name} at {series.station_code} "
            f"has mean = {mean_str} {series.unit}"
        ]
