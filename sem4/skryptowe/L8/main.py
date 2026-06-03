# main.py
"""Punkt wejścia aplikacji Log Browser.

Uruchamia pętlę zdarzeń Qt i wyświetla główne okno aplikacji.

Użycie:
    python main.py
"""

from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from src.gui.main_window import MainWindow


def main() -> int:
    """Inicjalizuje aplikację Qt i uruchamia główne okno.

    Returns:
        Kod wyjścia procesu zwrócony przez pętlę zdarzeń Qt.
    """
    app = QApplication(sys.argv)
    app.setApplicationName("Log browser")

    window = MainWindow()
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
