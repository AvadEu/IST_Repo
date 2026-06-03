# src/parser/models.py
"""Definicja modelu pojedynczego wpisu logu (warstwa danych).

Klasa :class:`LogEntry` jest czystym obiektem danych (POPO) niezależnym od GUI.
Wykorzystuje ``slots=True`` w celu ograniczenia zużycia pamięci – plik logów
może zawierać setki tysięcy wierszy, więc każdy bajt na rekord ma znaczenie.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional


@dataclass(slots=True)
class LogEntry:
    """Reprezentuje pojedynczy wiersz logu serwera HTTP.

    Atrybuty odpowiadają informacjom prezentowanym w widoku szczegółów
    (*detail*) zgodnie ze specyfikacją:

    Attributes:
        raw: Surowa, niezmodyfikowana treść wiersza logu.
        timestamp: Znacznik czasu zdarzenia (w strefie UTC) lub ``None``,
            jeśli nie udało się go odczytać.
        remote_host: Adres hosta zdalnego (klienta), który wykonał żądanie.
        method: Metoda HTTP (np. ``GET``, ``POST``, ``HEAD``).
        resource: Zasób (URI), którego dotyczyło żądanie.
        status_code: Kod statusu odpowiedzi HTTP lub ``None`` przy braku danych.
        size: Rozmiar treści odpowiedzi w bajtach.
    """

    raw: str
    timestamp: Optional[datetime]
    remote_host: str
    method: str
    resource: str
    status_code: Optional[int]
    size: int

    # ------------------------------------------------------------------ #
    # Pomocnicze właściwości prezentacyjne                                #
    # ------------------------------------------------------------------ #
    @property
    def date_text(self) -> str:
        """Zwraca datę zdarzenia w formacie ``YYYY-MM-DD`` (lub pusty łańcuch)."""
        if self.timestamp is None:
            return ""
        return self.timestamp.strftime("%Y-%m-%d")

    @property
    def time_text(self) -> str:
        """Zwraca czas zdarzenia w formacie ``HH:MM:SS`` (lub pusty łańcuch)."""
        if self.timestamp is None:
            return ""
        return self.timestamp.strftime("%H:%M:%S")

    @property
    def timezone_text(self) -> str:
        """Zwraca nazwę strefy czasowej znacznika czasu."""
        if self.timestamp is None or self.timestamp.tzinfo is None:
            return ""
        return "UTC" if self.timestamp.tzinfo == timezone.utc else str(self.timestamp.tzinfo)

    def summary(self, max_length: int = 30) -> str:
        """Zwraca skróconą treść logu na potrzeby widoku master.

        Surowy wiersz jest ucinany do ``max_length`` znaków i – jeśli był
        dłuższy – zakończony wielokropkiem (zgodnie ze specyfikacją).

        Args:
            max_length: Maksymalna liczba znaków przed wielokropkiem.

        Returns:
            Skrócona, jednowierszowa reprezentacja wpisu.
        """
        text = self.raw.strip()
        if len(text) <= max_length:
            return text
        return text[:max_length].rstrip() + "..."
