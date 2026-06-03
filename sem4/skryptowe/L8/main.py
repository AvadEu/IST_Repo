# app entry point. run: python main.py
from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from src.gui.main_window import MainWindow


def main() -> int:
    # boot Qt, show the window, hand over to the event loop
    app = QApplication(sys.argv)
    app.setApplicationName("Log browser")

    window = MainWindow()
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
