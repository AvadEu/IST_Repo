from typing import Any

import pandas as pd


class Station:

    def __init__(
        self,
        code: str,
        name: str,
        international_code: str = "",
        station_type: str = "",
        area_type: str = "",
        voivodeship: str = "",
        city: str = "",
        address: str = "",
        lat: float | None = None,
        lon: float | None = None,
        opened: str = "",
        closed: str = "",
    ) -> None:
        self.code = code
        self.name = name
        self.international_code = international_code
        self.station_type = station_type
        self.area_type = area_type
        self.voivodeship = voivodeship
        self.city = city
        self.address = address
        self.lat = lat
        self.lon = lon
        self.opened = opened
        self.closed = closed

    def __str__(self) -> str:
        return f"Station({self.code!r}, {self.name!r}, {self.city!r})"

    def __repr__(self) -> str:
        return (
            f"Station(code={self.code!r}, name={self.name!r}, "
            f"city={self.city!r}, lat={self.lat}, lon={self.lon})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Station):
            return NotImplemented
        return self.code == other.code

    def __hash__(self) -> int:
        return hash(self.code)

    @classmethod
    def from_row(cls, row: pd.Series) -> "Station":
        def safe(val: Any) -> str:
            return "" if pd.isna(val) else str(val).strip()

        def safe_float(val: Any) -> float | None:
            try:
                return float(val)
            except (TypeError, ValueError):
                return None

        return cls(
            code=safe(row.get("Kod stacji", "")),
            name=safe(row.get("Nazwa stacji", "")),
            international_code=safe(row.get("Kod międzynarodowy", "")),
            station_type=safe(row.get("Typ stacji", "")),
            area_type=safe(row.get("Typ obszaru", "")),
            voivodeship=safe(row.get("Województwo", "")),
            city=safe(row.get("Miejscowość", "")),
            address=safe(row.get("Adres", "")),
            lat=safe_float(row.get("WGS84 φ N")),
            lon=safe_float(row.get("WGS84 λ E")),
            opened=safe(row.get("Data uruchomienia", "")),
            closed=safe(row.get("Data zamknięcia", "")),
        )

    @staticmethod
    def load_all(path: str) -> dict[str, "Station"]:
        df = pd.read_csv(path, dtype=str)
        df.columns = [c.strip() for c in df.columns]
        stations: dict[str, Station] = {}
        for _, row in df.iterrows():
            st = Station.from_row(row)
            if st.code:
                stations[st.code] = st
        return stations
