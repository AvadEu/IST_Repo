# src/parser/log_parser.py
"""Wydajny parser logów serwera HTTP (warstwa logiki).

Parser jest dostosowany do struktury logów dostarczonych wraz z zadaniem –
plików w formacie Zeek/Bro ``http.log``, w których pola rozdzielone są znakami
tabulacji. Istotne kolumny mają stałe pozycje, co pozwala na bardzo szybkie
parsowanie metodą ``str.split('\\t')`` bez użycia wyrażeń regularnych.

Układ kolumn (indeksowanie od 0):
    0  ts                 – znacznik czasu (epoch, sekundy)
    2  id.orig_h          – adres hosta zdalnego (klient)
    7  method             – metoda HTTP
    9  uri                – żądany zasób
    13 response_body_len  – rozmiar odpowiedzi (bajty)
    14 status_code        – kod statusu HTTP

Parser jest w pełni niezależny od warstwy GUI i może być użyty samodzielnie.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Callable, List, Optional

from .models import LogEntry

# Indeksy kolumn w wierszu logu (format Zeek http.log, rozdzielany tabulacją).
_COL_TIMESTAMP = 0
_COL_REMOTE_HOST = 2
_COL_METHOD = 7
_COL_URI = 9
_COL_RESPONSE_SIZE = 13
_COL_STATUS = 14

# Minimalna liczba kolumn, aby wiersz uznać za poprawny.
_MIN_COLUMNS = 15

# Wartość oznaczająca brak danych w logach Zeek.
_EMPTY_TOKENS = frozenset({"-", "(empty)", ""})


class LogParseError(Exception):
    """Wyjątek zgłaszany, gdy pliku logu nie da się odczytać lub sparsować."""


class LogParser:
    """Parser przekształcający plik tekstowy logów w listę :class:`LogEntry`."""

    def __init__(self, min_columns: int = _MIN_COLUMNS) -> None:
        """Inicjalizuje parser.

        Args:
            min_columns: Minimalna liczba kolumn w wierszu, poniżej której
                wiersz jest pomijany jako niepoprawny.
        """
        self._min_columns = min_columns

    # ------------------------------------------------------------------ #
    # API publiczne                                                       #
    # ------------------------------------------------------------------ #
    def parse_file(
        self,
        path: str,
        progress_callback: Optional[Callable[[int, int], None]] = None,
        is_cancelled: Optional[Callable[[], bool]] = None,
    ) -> List[LogEntry]:
        """Parsuje cały plik logów i zwraca listę wpisów.

        Args:
            path: Ścieżka do pliku z logami.
            progress_callback: Opcjonalna funkcja wywoływana okresowo z parą
                ``(liczba_przetworzonych_bajtów, rozmiar_pliku)``. Umożliwia
                aktualizację paska postępu w GUI.
            is_cancelled: Opcjonalna funkcja zwracająca ``True``, jeśli
                operacja powinna zostać przerwana.

        Returns:
            Lista sparsowanych wpisów logu.

        Raises:
            LogParseError: Gdy pliku nie można otworzyć lub odczytać.
        """
        entries: List[LogEntry] = []
        try:
            total_size = self._file_size(path)
            processed_bytes = 0
            report_interval = 50_000  # Raportuj postęp co N wierszy.

            with open(path, "r", encoding="utf-8", errors="replace") as handle:
                for line_number, line in enumerate(handle, start=1):
                    processed_bytes += len(line.encode("utf-8", errors="replace"))

                    entry = self.parse_line(line)
                    if entry is not None:
                        entries.append(entry)

                    if line_number % report_interval == 0:
                        if is_cancelled is not None and is_cancelled():
                            break
                        if progress_callback is not None:
                            progress_callback(processed_bytes, total_size)

            if progress_callback is not None:
                progress_callback(total_size, total_size)
        except OSError as exc:
            raise LogParseError(f"Nie można odczytać pliku '{path}': {exc}") from exc

        return entries

    def parse_line(self, line: str) -> Optional[LogEntry]:
        """Parsuje pojedynczy wiersz logu.

        Args:
            line: Surowy wiersz tekstu.

        Returns:
            Obiekt :class:`LogEntry` lub ``None``, jeśli wiersz jest pusty,
            jest komentarzem Zeek (``#``) albo nie zawiera dość kolumn.
        """
        stripped = line.rstrip("\n").rstrip("\r")
        if not stripped or stripped.startswith("#"):
            return None

        fields = stripped.split("\t")
        if len(fields) < self._min_columns:
            return None

        return LogEntry(
            raw=stripped,
            timestamp=self._parse_timestamp(fields[_COL_TIMESTAMP]),
            remote_host=self._clean(fields[_COL_REMOTE_HOST]),
            method=self._clean(fields[_COL_METHOD]),
            resource=self._clean(fields[_COL_URI]),
            status_code=self._parse_int(fields[_COL_STATUS]),
            size=self._parse_int(fields[_COL_RESPONSE_SIZE]) or 0,
        )

    # ------------------------------------------------------------------ #
    # Metody pomocnicze (prywatne)                                        #
    # ------------------------------------------------------------------ #
    @staticmethod
    def _file_size(path: str) -> int:
        """Zwraca rozmiar pliku w bajtach (0, jeśli nie da się go ustalić)."""
        import os

        try:
            return os.path.getsize(path)
        except OSError:
            return 0

    @staticmethod
    def _clean(token: str) -> str:
        """Normalizuje token, zamieniając znaczniki braku danych na pusty łańcuch."""
        return "" if token in _EMPTY_TOKENS else token

    @staticmethod
    def _parse_int(token: str) -> Optional[int]:
        """Bezpiecznie konwertuje token na liczbę całkowitą."""
        if token in _EMPTY_TOKENS:
            return None
        try:
            return int(token)
        except ValueError:
            return None

    @staticmethod
    def _parse_timestamp(token: str) -> Optional[datetime]:
        """Konwertuje znacznik czasu epoch (sekundy) na obiekt ``datetime`` (UTC)."""
        if token in _EMPTY_TOKENS:
            return None
        try:
            return datetime.fromtimestamp(float(token), tz=timezone.utc)
        except (ValueError, OverflowError, OSError):
            return None
