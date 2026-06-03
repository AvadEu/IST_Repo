# src/gui/log_loader.py
"""Wątek roboczy do asynchronicznego wczytywania i parsowania logów.

Zgodnie z wymaganiami, ciężkie operacje wejścia/wyjścia oraz parsowanie nie
mogą blokować głównego wątku GUI. Realizujemy to wzorcem *worker-object*:
obiekt :class:`LogLoaderWorker` (dziedziczący po ``QObject``) jest przenoszony
do osobnego :class:`QThread`, a komunikacja z GUI odbywa się wyłącznie przez
sygnały i sloty (bezpieczne wątkowo w Qt).
"""

from __future__ import annotations

from typing import List

from PySide6.QtCore import QObject, Signal

from src.parser.log_parser import LogParseError, LogParser
from src.parser.models import LogEntry


class LogLoaderWorker(QObject):
    """Obiekt roboczy parsujący plik logów w osobnym wątku.

    Signals:
        progress: Emitowany z wartością postępu w procentach (0–100).
        finished: Emitowany po pomyślnym zakończeniu z listą wpisów.
        error: Emitowany z komunikatem błędu, gdy parsowanie się nie powiedzie.
    """

    progress = Signal(int)
    finished = Signal(list)
    error = Signal(str)

    def __init__(self, path: str) -> None:
        super().__init__()
        self._path = path
        self._parser = LogParser()
        self._cancelled = False

    def cancel(self) -> None:
        """Zleca przerwanie trwającego parsowania (sprawdzane okresowo)."""
        self._cancelled = True

    def run(self) -> None:
        """Wykonuje parsowanie pliku; przeznaczone do uruchomienia w wątku."""
        try:
            entries: List[LogEntry] = self._parser.parse_file(
                self._path,
                progress_callback=self._on_progress,
                is_cancelled=lambda: self._cancelled,
            )
            if self._cancelled:
                # Przerwano – nie emitujemy wyniku, jedynie kończymy cicho.
                self.finished.emit([])
                return
            self.finished.emit(entries)
        except LogParseError as exc:
            self.error.emit(str(exc))
        except Exception as exc:  # noqa: BLE001 – zabezpieczenie ostatniej szansy
            self.error.emit(f"Nieoczekiwany błąd podczas parsowania: {exc}")

    def _on_progress(self, processed: int, total: int) -> None:
        """Przelicza postęp na procenty i emituje sygnał."""
        if total <= 0:
            return
        percent = int(processed * 100 / total)
        self.progress.emit(max(0, min(100, percent)))
