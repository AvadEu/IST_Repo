# parser for Zeek/Bro http.log files (tab separated). no Qt here on purpose.
from __future__ import annotations

from datetime import datetime, timezone
from typing import Callable, List, Optional

from .models import LogEntry

# column indexes we actually care about (0-based)
_COL_TIMESTAMP = 0
_COL_REMOTE_HOST = 2
_COL_METHOD = 7
_COL_URI = 9
_COL_RESPONSE_SIZE = 13
_COL_STATUS = 14

_MIN_COLUMNS = 15  # below this the line is junk / not a real http log row

# zeek uses these for "no value"
_EMPTY_TOKENS = frozenset({"-", "(empty)", ""})


class LogParseError(Exception):
    # thrown when the file can't be read/parsed
    pass


class LogParser:
    def __init__(self, min_columns: int = _MIN_COLUMNS) -> None:
        self._min_columns = min_columns

    def parse_file(
        self,
        path: str,
        progress_callback: Optional[Callable[[int, int], None]] = None,
        is_cancelled: Optional[Callable[[], bool]] = None,
    ) -> List[LogEntry]:
        # reads the whole file line by line, reports progress every so often
        entries: List[LogEntry] = []
        try:
            total_size = self._file_size(path)
            processed_bytes = 0
            report_interval = 50_000  # don't spam the progress signal

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
                progress_callback(total_size, total_size)  # make sure we hit 100%
        except OSError as exc:
            raise LogParseError(f"Nie można odczytać pliku '{path}': {exc}") from exc

        return entries

    def parse_line(self, line: str) -> Optional[LogEntry]:
        # returns None for blanks, zeek comments (#...) and short lines
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

    @staticmethod
    def _file_size(path: str) -> int:
        # used for the progress bar, 0 if we can't stat it
        import os

        try:
            return os.path.getsize(path)
        except OSError:
            return 0

    @staticmethod
    def _clean(token: str) -> str:
        # turn zeek "no value" markers into empty string
        return "" if token in _EMPTY_TOKENS else token

    @staticmethod
    def _parse_int(token: str) -> Optional[int]:
        if token in _EMPTY_TOKENS:
            return None
        try:
            return int(token)
        except ValueError:
            return None

    @staticmethod
    def _parse_timestamp(token: str) -> Optional[datetime]:
        # ts is epoch seconds -> aware UTC datetime
        if token in _EMPTY_TOKENS:
            return None
        try:
            return datetime.fromtimestamp(float(token), tz=timezone.utc)
        except (ValueError, OverflowError, OSError):
            return None
