# src/parser/__init__.py
"""Warstwa logiki: model danych oraz parser logów HTTP.

Ten pakiet nie importuje żadnych modułów GUI – dzięki temu logika parsowania
może być testowana i używana niezależnie od PySide6.
"""

from .models import LogEntry
from .log_parser import LogParser, LogParseError

__all__ = ["LogEntry", "LogParser", "LogParseError"]
