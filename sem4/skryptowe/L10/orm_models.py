"""Wersja dla ambitnych: definicja modeli ORM (SQLAlchemy 2.0).

Modele odpowiadają tabelom bazy danych GTFS i odwzorowują relacje
między nimi (klucze obce + relationship). Ta sama struktura, co w
``schema.sql``, ale wyrażona w kodzie Pythona.
"""
from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, Float, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Agency(Base):
    __tablename__ = "agency"

    agency_id: Mapped[str] = mapped_column(Text, primary_key=True)
    agency_name: Mapped[str] = mapped_column(Text, nullable=False)
    agency_url: Mapped[str | None] = mapped_column(Text)
    agency_timezone: Mapped[str | None] = mapped_column(Text)
    agency_phone: Mapped[str | None] = mapped_column(Text)
    agency_lang: Mapped[str | None] = mapped_column(Text)

    routes: Mapped[list["Route"]] = relationship(back_populates="agency")


class Calendar(Base):
    __tablename__ = "calendar"

    service_id: Mapped[str] = mapped_column(Text, primary_key=True)
    monday: Mapped[int] = mapped_column(Integer, default=0)
    tuesday: Mapped[int] = mapped_column(Integer, default=0)
    wednesday: Mapped[int] = mapped_column(Integer, default=0)
    thursday: Mapped[int] = mapped_column(Integer, default=0)
    friday: Mapped[int] = mapped_column(Integer, default=0)
    saturday: Mapped[int] = mapped_column(Integer, default=0)
    sunday: Mapped[int] = mapped_column(Integer, default=0)
    start_date: Mapped[str | None] = mapped_column(Text)
    end_date: Mapped[str | None] = mapped_column(Text)

    trips: Mapped[list["Trip"]] = relationship(back_populates="calendar")


class Stop(Base):
    __tablename__ = "stops"

    stop_id: Mapped[str] = mapped_column(Text, primary_key=True)
    stop_code: Mapped[str | None] = mapped_column(Text)
    stop_name: Mapped[str] = mapped_column(Text, nullable=False)
    stop_lat: Mapped[float | None] = mapped_column(Float)
    stop_lon: Mapped[float | None] = mapped_column(Float)

    stop_times: Mapped[list["StopTime"]] = relationship(back_populates="stop")


class Route(Base):
    __tablename__ = "routes"

    route_id: Mapped[str] = mapped_column(Text, primary_key=True)
    agency_id: Mapped[str | None] = mapped_column(ForeignKey("agency.agency_id"))
    route_short_name: Mapped[str | None] = mapped_column(Text)
    route_long_name: Mapped[str | None] = mapped_column(Text)
    route_desc: Mapped[str | None] = mapped_column(Text)
    route_type: Mapped[int | None] = mapped_column(Integer)

    agency: Mapped["Agency | None"] = relationship(back_populates="routes")
    trips: Mapped[list["Trip"]] = relationship(back_populates="route")


class Trip(Base):
    __tablename__ = "trips"

    trip_id: Mapped[str] = mapped_column(Text, primary_key=True)
    route_id: Mapped[str] = mapped_column(ForeignKey("routes.route_id"), nullable=False)
    service_id: Mapped[str | None] = mapped_column(ForeignKey("calendar.service_id"))
    trip_headsign: Mapped[str | None] = mapped_column(Text)
    direction_id: Mapped[int | None] = mapped_column(Integer)

    route: Mapped["Route"] = relationship(back_populates="trips")
    calendar: Mapped["Calendar | None"] = relationship(back_populates="trips")
    stop_times: Mapped[list["StopTime"]] = relationship(back_populates="trip")


class StopTime(Base):
    __tablename__ = "stop_times"

    trip_id: Mapped[str] = mapped_column(ForeignKey("trips.trip_id"), primary_key=True)
    stop_sequence: Mapped[int] = mapped_column(Integer, primary_key=True)
    arrival_time: Mapped[str | None] = mapped_column(Text)
    departure_time: Mapped[str | None] = mapped_column(Text)
    departure_seconds: Mapped[int | None] = mapped_column(Integer)
    stop_id: Mapped[str] = mapped_column(ForeignKey("stops.stop_id"), nullable=False)

    trip: Mapped["Trip"] = relationship(back_populates="stop_times")
    stop: Mapped["Stop"] = relationship(back_populates="stop_times")
