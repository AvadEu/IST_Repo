# data holder for one log line, kept separate from any Qt stuff
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional


@dataclass(slots=True)  # slots -> smaller memory footprint, file can be huge
class LogEntry:
    raw: str
    timestamp: Optional[datetime]
    remote_host: str
    method: str
    resource: str
    status_code: Optional[int]
    size: int

    @property
    def date_text(self) -> str:
        # YYYY-MM-DD, empty if we couldn't read the timestamp
        if self.timestamp is None:
            return ""
        return self.timestamp.strftime("%Y-%m-%d")

    @property
    def time_text(self) -> str:
        if self.timestamp is None:
            return ""
        return self.timestamp.strftime("%H:%M:%S")

    @property
    def timezone_text(self) -> str:
        if self.timestamp is None or self.timestamp.tzinfo is None:
            return ""
        return "UTC" if self.timestamp.tzinfo == timezone.utc else str(self.timestamp.tzinfo)

    def summary(self, max_length: int = 100) -> str:
        # short version for the master list: cut to 30 chars + "..."
        text = self.raw.strip()
        if len(text) <= max_length:
            return text
        return text[:max_length].rstrip() + "..."
