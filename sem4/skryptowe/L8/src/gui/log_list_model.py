# model behind the master QListView. keeps all entries + the filtered view.
from __future__ import annotations

from datetime import date
from typing import List, Optional

from PySide6.QtCore import QAbstractListModel, QModelIndex, Qt

from src.parser.models import LogEntry

_SUMMARY_LENGTH = 30  # how many chars of the raw line we show in the list


class LogListModel(QAbstractListModel):
    def __init__(self, parent: Optional[object] = None) -> None:
        super().__init__(parent)
        self._all_entries: List[LogEntry] = []
        self._visible_entries: List[LogEntry] = []  # what's left after the date filter
        self._date_from: Optional[date] = None
        self._date_to: Optional[date] = None

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:  # noqa: N802
        if parent.isValid():
            return 0
        return len(self._visible_entries)

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):  # noqa: N802
        # display = short summary, tooltip = full raw line
        if not index.isValid() or not (0 <= index.row() < len(self._visible_entries)):
            return None

        entry = self._visible_entries[index.row()]
        if role == Qt.DisplayRole:
            return entry.summary(_SUMMARY_LENGTH)
        if role == Qt.ToolTipRole:
            return entry.raw
        return None

    def set_entries(self, entries: List[LogEntry]) -> None:
        # new file loaded -> reset everything, drop the filter
        self.beginResetModel()
        self._all_entries = entries
        self._date_from = None
        self._date_to = None
        self._visible_entries = list(entries)
        self.endResetModel()

    def set_time_filter(self, date_from: Optional[date], date_to: Optional[date]) -> None:
        # rebuild the visible list for the given date range (both ends inclusive)
        self.beginResetModel()
        self._date_from = date_from
        self._date_to = date_to
        self._visible_entries = [
            entry for entry in self._all_entries if self._matches_filter(entry)
        ]
        self.endResetModel()

    def entry_at(self, row: int) -> Optional[LogEntry]:
        if 0 <= row < len(self._visible_entries):
            return self._visible_entries[row]
        return None

    def is_empty(self) -> bool:
        return not self._all_entries

    def full_date_range(self) -> Optional[tuple[date, date]]:
        # min/max date across all entries, used to set up the date pickers
        dates = [
            entry.timestamp.date()
            for entry in self._all_entries
            if entry.timestamp is not None
        ]
        if not dates:
            return None
        return min(dates), max(dates)

    def _matches_filter(self, entry: LogEntry) -> bool:
        if entry.timestamp is None:
            # no timestamp -> only show it when there's no filter at all
            return self._date_from is None and self._date_to is None

        entry_date = entry.timestamp.date()
        if self._date_from is not None and entry_date < self._date_from:
            return False
        if self._date_to is not None and entry_date > self._date_to:
            return False
        return True
