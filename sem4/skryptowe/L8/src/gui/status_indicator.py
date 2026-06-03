# src/gui/status_indicator.py
"""Widżet kolorowego wskaźnika kodu statusu HTTP.

Zgodnie ze szkicem interfejsu kod statusu jest prezentowany w formie kolorowego
„kółka” z wpisaną wartością liczbową. Kolor zależy od klasy odpowiedzi HTTP:

    * 1xx / 2xx / 3xx → zielony (odpowiedź poprawna / przekierowanie),
    * 4xx             → pomarańczowy (błąd po stronie klienta),
    * 5xx             → czerwony (błąd po stronie serwera),
    * brak danych     → szary.
"""

from __future__ import annotations

from typing import Optional

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QColor, QFont, QPainter, QPaintEvent
from PySide6.QtWidgets import QWidget

_COLOR_OK = QColor("#3ec46d")        # zielony
_COLOR_CLIENT_ERR = QColor("#f0a020")  # pomarańczowy
_COLOR_SERVER_ERR = QColor("#e04545")  # czerwony
_COLOR_UNKNOWN = QColor("#9e9e9e")     # szary


class StatusIndicator(QWidget):
    """Okrągły wskaźnik prezentujący kod statusu HTTP wraz z kolorem klasy."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._status_code: Optional[int] = None
        self.setMinimumSize(QSize(54, 54))

    def sizeHint(self) -> QSize:  # noqa: N802
        """Sugerowany rozmiar widżetu."""
        return QSize(54, 54)

    def set_status_code(self, status_code: Optional[int]) -> None:
        """Ustawia prezentowany kod statusu i odświeża widżet.

        Args:
            status_code: Kod statusu HTTP lub ``None`` przy braku danych.
        """
        self._status_code = status_code
        self.update()

    def _color_for_status(self) -> QColor:
        """Dobiera kolor wskaźnika na podstawie klasy kodu statusu."""
        if self._status_code is None:
            return _COLOR_UNKNOWN
        if self._status_code < 400:
            return _COLOR_OK
        if self._status_code < 500:
            return _COLOR_CLIENT_ERR
        return _COLOR_SERVER_ERR

    def paintEvent(self, event: QPaintEvent) -> None:  # noqa: N802
        """Rysuje wypełnione kółko z wpisanym kodem statusu."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Kwadratowy, wyśrodkowany obszar rysowania.
        side = min(self.width(), self.height()) - 4
        x = (self.width() - side) // 2
        y = (self.height() - side) // 2

        painter.setPen(Qt.NoPen)
        painter.setBrush(self._color_for_status())
        painter.drawEllipse(x, y, side, side)

        text = "—" if self._status_code is None else str(self._status_code)
        font = QFont(painter.font())
        font.setBold(True)
        font.setPointSizeF(max(8.0, side * 0.30))
        painter.setFont(font)
        painter.setPen(QColor("#ffffff"))
        painter.drawText(self.rect(), Qt.AlignCenter, text)
        painter.end()
