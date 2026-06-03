# src/gui/log_list_model.py
"""Wydajny model listy logów dla widoku master (QListView).

Model dziedziczy po :class:`QAbstractListModel`, dzięki czemu prezentacja setek
tysięcy wierszy jest wydajna – widok pobiera dane leniwie (tylko dla widocznych
elementów), a same wpisy przechowywane są raz, bez kopiowania do widżetów.

Model przechowuje pełen zbiór wpisów (``master``) oraz – wynikającą z aktualnego
filtra czasowego – listę wpisów widocznych. Filtrowanie po przedziale dat jest
realizowane wewnątrz modelu i sygnalizowane przez ``beginResetModel`` /
``endResetModel``.
"""

from __future__ import annotations

from datetime import date
from typing import List, Optional

from PySide6.QtCore import QAbstractListModel, QModelIndex, Qt

from src.parser.models import LogEntry

# Maksymalna długość skróconej treści logu w widoku master (wg specyfikacji).
_SUMMARY_LENGTH = 30


class LogListModel(QAbstractListModel):
    """Model wystawiający skróconą treść logów do widoku listy (master)."""

    def __init__(self, parent: Optional[object] = None) -> None:
        super().__init__(parent)
        self._all_entries: List[LogEntry] = []
        self._visible_entries: List[LogEntry] = []
        self._date_from: Optional[date] = None
        self._date_to: Optional[date] = None

    # ------------------------------------------------------------------ #
    # Implementacja interfejsu QAbstractListModel                         #
    # ------------------------------------------------------------------ #
    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:  # noqa: N802
        """Zwraca liczbę aktualnie widocznych (przefiltrowanych) wpisów."""
        if parent.isValid():
            return 0
        return len(self._visible_entries)

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):  # noqa: N802
        """Dostarcza dane dla widoku.

        Dla roli ``DisplayRole`` zwraca skróconą treść logu (do 30 znaków
        zakończonych wielokropkiem). Dla ``ToolTipRole`` zwraca pełny surowy
        wiersz, co ułatwia podgląd długich wpisów.
        """
        if not index.isValid() or not (0 <= index.row() < len(self._visible_entries)):
            return None

        entry = self._visible_entries[index.row()]
        if role == Qt.DisplayRole:
            return entry.summary(_SUMMARY_LENGTH)
        if role == Qt.ToolTipRole:
            return entry.raw
        return None

    # ------------------------------------------------------------------ #
    # API domenowe                                                        #
    # ------------------------------------------------------------------ #
    def set_entries(self, entries: List[LogEntry]) -> None:
        """Ustawia nowy, pełny zbiór wpisów i resetuje filtr czasowy.

        Args:
            entries: Lista wszystkich sparsowanych wpisów logu.
        """
        self.beginResetModel()
        self._all_entries = entries
        self._date_from = None
        self._date_to = None
        self._visible_entries = list(entries)
        self.endResetModel()

    def set_time_filter(self, date_from: Optional[date], date_to: Optional[date]) -> None:
        """Filtruje widoczne wpisy wg przedziału dat (włącznie z krańcami).

        Args:
            date_from: Data początkowa lub ``None`` (brak ograniczenia od dołu).
            date_to: Data końcowa lub ``None`` (brak ograniczenia od góry).
        """
        self.beginResetModel()
        self._date_from = date_from
        self._date_to = date_to
        self._visible_entries = [
            entry for entry in self._all_entries if self._matches_filter(entry)
        ]
        self.endResetModel()

    def entry_at(self, row: int) -> Optional[LogEntry]:
        """Zwraca widoczny wpis o podanym indeksie wiersza (lub ``None``)."""
        if 0 <= row < len(self._visible_entries):
            return self._visible_entries[row]
        return None

    def is_empty(self) -> bool:
        """Zwraca ``True``, jeśli model nie zawiera żadnych wpisów źródłowych."""
        return not self._all_entries

    def full_date_range(self) -> Optional[tuple[date, date]]:
        """Zwraca parę ``(min_data, max_data)`` dla całego zbioru wpisów.

        Returns:
            Krotka skrajnych dat lub ``None``, jeśli żaden wpis nie ma czasu.
        """
        dates = [
            entry.timestamp.date()
            for entry in self._all_entries
            if entry.timestamp is not None
        ]
        if not dates:
            return None
        return min(dates), max(dates)

    # ------------------------------------------------------------------ #
    # Metody pomocnicze                                                   #
    # ------------------------------------------------------------------ #
    def _matches_filter(self, entry: LogEntry) -> bool:
        """Sprawdza, czy wpis mieści się w aktualnym przedziale dat."""
        if entry.timestamp is None:
            # Wpisy bez znacznika czasu są ukrywane przy aktywnym filtrze.
            return self._date_from is None and self._date_to is None

        entry_date = entry.timestamp.date()
        if self._date_from is not None and entry_date < self._date_from:
            return False
        if self._date_to is not None and entry_date > self._date_to:
            return False
        return True
