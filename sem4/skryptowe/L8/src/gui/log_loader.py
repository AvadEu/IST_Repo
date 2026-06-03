# worker that parses the file off the main thread so the GUI doesn't freeze.
# pattern: QObject worker moved into a QThread, talks back via signals.
from __future__ import annotations

from typing import List

from PySide6.QtCore import QObject, Signal

from src.parser.log_parser import LogParseError, LogParser
from src.parser.models import LogEntry


class LogLoaderWorker(QObject):
    progress = Signal(int)    # 0-100
    finished = Signal(list)   # list[LogEntry]
    error = Signal(str)

    def __init__(self, path: str) -> None:
        super().__init__()
        self._path = path
        self._parser = LogParser()
        self._cancelled = False

    def cancel(self) -> None:
        # checked every now and then inside the parse loop
        self._cancelled = True

    def run(self) -> None:
        # entry point that runs inside the thread
        try:
            entries: List[LogEntry] = self._parser.parse_file(
                self._path,
                progress_callback=self._on_progress,
                is_cancelled=lambda: self._cancelled,
            )
            if self._cancelled:
                self.finished.emit([])  # bailed out, just finish quietly
                return
            self.finished.emit(entries)
        except LogParseError as exc:
            self.error.emit(str(exc))
        except Exception as exc:  # noqa: BLE001 - last resort so the thread never dies silently
            self.error.emit(f"Nieoczekiwany błąd podczas parsowania: {exc}")

    def _on_progress(self, processed: int, total: int) -> None:
        # bytes -> percent
        if total <= 0:
            return
        percent = int(processed * 100 / total)
        self.progress.emit(max(0, min(100, percent)))
