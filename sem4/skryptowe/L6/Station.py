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
