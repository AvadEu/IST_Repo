# little colored circle with the status code in it (like on the spec sketch)
from __future__ import annotations

from typing import Optional

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QColor, QFont, QPainter, QPaintEvent
from PySide6.QtWidgets import QWidget

# color per http class: ok=green, client err=orange, server err=red, none=grey
_COLOR_OK = QColor("#3ec46d")
_COLOR_CLIENT_ERR = QColor("#f0a020")
_COLOR_SERVER_ERR = QColor("#e04545")
_COLOR_UNKNOWN = QColor("#9e9e9e")


class StatusIndicator(QWidget):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._status_code: Optional[int] = None
        self.setMinimumSize(QSize(54, 54))

    def sizeHint(self) -> QSize:  # noqa: N802
        return QSize(54, 54)

    def set_status_code(self, status_code: Optional[int]) -> None:
        self._status_code = status_code
        self.update()  # triggers a repaint

    def _color_for_status(self) -> QColor:
        if self._status_code is None:
            return _COLOR_UNKNOWN
        if self._status_code < 400:
            return _COLOR_OK
        if self._status_code < 500:
            return _COLOR_CLIENT_ERR
        return _COLOR_SERVER_ERR

    def paintEvent(self, event: QPaintEvent) -> None:  # noqa: N802
        # draw a filled circle + centered code text
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # square drawing area, centered in the widget
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
