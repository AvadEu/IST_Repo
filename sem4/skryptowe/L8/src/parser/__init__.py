# logic layer: data model + log parser, no Qt imports in here
from .models import LogEntry
from .log_parser import LogParser, LogParseError

__all__ = ["LogEntry", "LogParser", "LogParseError"]
