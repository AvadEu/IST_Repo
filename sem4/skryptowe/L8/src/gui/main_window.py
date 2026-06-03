# src/gui/main_window.py
"""Główne okno aplikacji Log Browser (warstwa GUI, wzorzec master-detail).

Okno odwzorowuje układ ze szkicu specyfikacji:

    * górny pasek – ścieżka do pliku oraz przycisk „Open”,
    * panel master (lewa strona) – pola wyboru dat „From”/„To” oraz lista logów,
    * panel detail (prawa strona) – szczegóły zaznaczonego logu,
    * dolny pasek – przyciski „Previous” i „Next”.

Logika parsowania jest delegowana do warstwy ``src.parser`` i uruchamiana w
osobnym wątku (``LogLoaderWorker`` + ``QThread``), aby nie blokować GUI.
"""

from __future__ import annotations

from datetime import date
from typing import Optional

from PySide6.QtCore import QDate, Qt, QThread
from PySide6.QtWidgets import (
    QDateEdit,
    QFileDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListView,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.gui.log_list_model import LogListModel
from src.gui.log_loader import LogLoaderWorker
from src.gui.status_indicator import StatusIndicator
from src.parser.models import LogEntry


class MainWindow(QWidget):
    """Główne okno aplikacji realizujące wzorzec master-detail."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Log browser")
        self.resize(1000, 600)

        # Stan wątku roboczego (utrzymywany jako pola, by nie został usunięty).
        self._thread: Optional[QThread] = None
        self._worker: Optional[LogLoaderWorker] = None

        # Model danych dla widoku master.
        self._model = LogListModel(self)

        self._build_ui()
        self._connect_signals()
        self._update_navigation_state()

    # ------------------------------------------------------------------ #
    # Budowa interfejsu                                                   #
    # ------------------------------------------------------------------ #
    def _build_ui(self) -> None:
        """Tworzy i rozmieszcza wszystkie widżety okna."""
        root_layout = QVBoxLayout(self)

        root_layout.addLayout(self._build_top_bar())

        content_layout = QHBoxLayout()
        content_layout.addWidget(self._build_master_panel(), stretch=1)
        content_layout.addWidget(self._build_detail_panel(), stretch=1)
        root_layout.addLayout(content_layout, stretch=1)

        root_layout.addLayout(self._build_bottom_bar())

        self._progress_bar = QProgressBar()
        self._progress_bar.setVisible(False)
        root_layout.addWidget(self._progress_bar)

    def _build_top_bar(self) -> QHBoxLayout:
        """Buduje górny pasek: ścieżka pliku + przycisk otwierania."""
        layout = QHBoxLayout()
        self._path_edit = QLineEdit()
        self._path_edit.setReadOnly(True)
        self._path_edit.setPlaceholderText("Wybierz plik z logami…")
        self._open_button = QPushButton("Open")
        layout.addWidget(self._path_edit, stretch=1)
        layout.addWidget(self._open_button)
        return layout

    def _build_master_panel(self) -> QWidget:
        """Buduje panel master: filtr dat oraz listę logów."""
        panel = QWidget()
        layout = QVBoxLayout(panel)

        # Pasek filtra czasowego (From / To).
        filter_layout = QHBoxLayout()
        self._date_from = QDateEdit()
        self._date_to = QDateEdit()
        for editor in (self._date_from, self._date_to):
            editor.setCalendarPopup(True)
            editor.setDisplayFormat("yyyy-MM-dd")
            editor.setEnabled(False)
        filter_layout.addWidget(QLabel("From"))
        filter_layout.addWidget(self._date_from)
        filter_layout.addSpacing(12)
        filter_layout.addWidget(QLabel("To"))
        filter_layout.addWidget(self._date_to)
        filter_layout.addStretch(1)
        layout.addLayout(filter_layout)

        # Lista logów (widok master).
        self._list_view = QListView()
        self._list_view.setModel(self._model)
        self._list_view.setUniformItemSizes(True)  # wydajność dla wielu wierszy
        self._list_view.setEditTriggers(QListView.NoEditTriggers)
        layout.addWidget(self._list_view, stretch=1)

        return panel

    def _build_detail_panel(self) -> QWidget:
        """Buduje panel detail: szczegóły zaznaczonego logu."""
        group = QGroupBox("Szczegóły")
        form = QFormLayout(group)
        form.setLabelAlignment(Qt.AlignRight)

        self._detail_remote_host = QLineEdit()
        self._detail_date = QLineEdit()
        self._detail_time = QLineEdit()
        self._detail_timezone = QLineEdit()
        self._detail_method = QLineEdit()
        self._detail_resource = QLineEdit()
        self._detail_size = QLineEdit()
        self._status_indicator = StatusIndicator()

        # Pola szczegółów są tylko do odczytu – prezentują dane, nie edytują ich.
        for field in (
            self._detail_remote_host,
            self._detail_date,
            self._detail_time,
            self._detail_timezone,
            self._detail_method,
            self._detail_resource,
            self._detail_size,
        ):
            field.setReadOnly(True)

        form.addRow("Remote host:", self._detail_remote_host)
        form.addRow("Date:", self._detail_date)
        form.addRow("Time:", self._detail_time)
        form.addRow("Timezone:", self._detail_timezone)
        form.addRow("Status code:", self._status_indicator)
        form.addRow("Method:", self._detail_method)
        form.addRow("Resource:", self._detail_resource)
        form.addRow("Size:", self._detail_size)

        return group

    def _build_bottom_bar(self) -> QHBoxLayout:
        """Buduje dolny pasek nawigacji: przyciski Previous / Next."""
        layout = QHBoxLayout()
        self._prev_button = QPushButton("Previous")
        self._next_button = QPushButton("Next")
        layout.addWidget(self._prev_button)
        layout.addStretch(1)
        layout.addWidget(self._next_button)
        return layout

    # ------------------------------------------------------------------ #
    # Połączenia sygnałów                                                 #
    # ------------------------------------------------------------------ #
    def _connect_signals(self) -> None:
        """Łączy sygnały widżetów z odpowiednimi slotami."""
        self._open_button.clicked.connect(self._on_open_clicked)
        self._prev_button.clicked.connect(self._on_previous_clicked)
        self._next_button.clicked.connect(self._on_next_clicked)
        self._date_from.dateChanged.connect(self._on_filter_changed)
        self._date_to.dateChanged.connect(self._on_filter_changed)

        selection_model = self._list_view.selectionModel()
        selection_model.currentChanged.connect(self._on_selection_changed)

    # ------------------------------------------------------------------ #
    # Obsługa wczytywania pliku (wielowątkowość)                          #
    # ------------------------------------------------------------------ #
    def _on_open_clicked(self) -> None:
        """Otwiera okno wyboru pliku i uruchamia asynchroniczne parsowanie."""
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Otwórz plik z logami",
            "",
            "Pliki logów (*.log *.txt);;Wszystkie pliki (*)",
        )
        if not path:
            return

        self._path_edit.setText(path)
        self._start_loading(path)

    def _start_loading(self, path: str) -> None:
        """Konfiguruje i uruchamia wątek roboczy parsujący plik."""
        # Blokujemy ponowne otwarcie do czasu zakończenia bieżącej operacji.
        self._open_button.setEnabled(False)
        self._progress_bar.setValue(0)
        self._progress_bar.setVisible(True)

        self._thread = QThread(self)
        self._worker = LogLoaderWorker(path)
        self._worker.moveToThread(self._thread)

        # Start parsowania po uruchomieniu wątku.
        self._thread.started.connect(self._worker.run)
        # Komunikacja worker → GUI.
        self._worker.progress.connect(self._progress_bar.setValue)
        self._worker.finished.connect(self._on_loading_finished)
        self._worker.error.connect(self._on_loading_error)
        # Sprzątanie po zakończeniu pracy.
        self._worker.finished.connect(self._thread.quit)
        self._worker.error.connect(self._thread.quit)
        self._thread.finished.connect(self._cleanup_thread)

        self._thread.start()

    def _on_loading_finished(self, entries: list) -> None:
        """Slot wywoływany po pomyślnym wczytaniu wpisów."""
        self._progress_bar.setVisible(False)
        self._open_button.setEnabled(True)

        self._model.set_entries(entries)
        self._configure_date_filters()
        self._clear_detail()

        if self._model.rowCount() > 0:
            # Automatyczne zaznaczenie pierwszego wpisu (master-detail).
            self._select_row(0)
        self._update_navigation_state()

    def _on_loading_error(self, message: str) -> None:
        """Slot wywoływany w razie błędu parsowania."""
        self._progress_bar.setVisible(False)
        self._open_button.setEnabled(True)
        QMessageBox.critical(self, "Błąd wczytywania", message)

    def _cleanup_thread(self) -> None:
        """Usuwa referencje do zakończonego wątku i workera."""
        if self._worker is not None:
            self._worker.deleteLater()
            self._worker = None
        if self._thread is not None:
            self._thread.deleteLater()
            self._thread = None

    # ------------------------------------------------------------------ #
    # Filtrowanie po przedziale czasowym                                  #
    # ------------------------------------------------------------------ #
    def _configure_date_filters(self) -> None:
        """Ustawia zakres i wartości domyślne pól dat na podstawie danych."""
        date_range = self._model.full_date_range()
        # Tymczasowo blokujemy sygnały, aby nie wyzwolić filtrowania w trakcie
        # ustawiania wartości początkowych.
        self._date_from.blockSignals(True)
        self._date_to.blockSignals(True)

        if date_range is None:
            self._date_from.setEnabled(False)
            self._date_to.setEnabled(False)
        else:
            min_date, max_date = date_range
            q_min = QDate(min_date.year, min_date.month, min_date.day)
            q_max = QDate(max_date.year, max_date.month, max_date.day)
            for editor in (self._date_from, self._date_to):
                editor.setEnabled(True)
                editor.setDateRange(q_min, q_max)
            self._date_from.setDate(q_min)
            self._date_to.setDate(q_max)

        self._date_from.blockSignals(False)
        self._date_to.blockSignals(False)

    def _on_filter_changed(self) -> None:
        """Stosuje filtr czasowy po zmianie którejkolwiek z dat."""
        if self._model.is_empty():
            return

        date_from = self._qdate_to_date(self._date_from.date())
        date_to = self._qdate_to_date(self._date_to.date())
        self._model.set_time_filter(date_from, date_to)

        self._clear_detail()
        if self._model.rowCount() > 0:
            self._select_row(0)
        self._update_navigation_state()

    # ------------------------------------------------------------------ #
    # Master-detail: zaznaczenie i prezentacja szczegółów                 #
    # ------------------------------------------------------------------ #
    def _on_selection_changed(self, current, _previous) -> None:
        """Aktualizuje panel detail po zmianie zaznaczenia w liście."""
        if current is None or not current.isValid():
            self._clear_detail()
        else:
            entry = self._model.entry_at(current.row())
            if entry is not None:
                self._show_detail(entry)
        self._update_navigation_state()

    def _show_detail(self, entry: LogEntry) -> None:
        """Wypełnia pola panelu detail danymi wybranego wpisu."""
        self._detail_remote_host.setText(entry.remote_host)
        self._detail_date.setText(entry.date_text)
        self._detail_time.setText(entry.time_text)
        self._detail_timezone.setText(entry.timezone_text)
        self._detail_method.setText(entry.method)
        self._detail_resource.setText(entry.resource)
        self._detail_size.setText(f"{entry.size} Bytes")
        self._status_indicator.set_status_code(entry.status_code)

    def _clear_detail(self) -> None:
        """Czyści wszystkie pola panelu detail."""
        for field in (
            self._detail_remote_host,
            self._detail_date,
            self._detail_time,
            self._detail_timezone,
            self._detail_method,
            self._detail_resource,
            self._detail_size,
        ):
            field.clear()
        self._status_indicator.set_status_code(None)

    # ------------------------------------------------------------------ #
    # Nawigacja: Previous / Next                                          #
    # ------------------------------------------------------------------ #
    def _on_previous_clicked(self) -> None:
        """Przechodzi do poprzedniego logu na liście."""
        current_row = self._current_row()
        if current_row > 0:
            self._select_row(current_row - 1)

    def _on_next_clicked(self) -> None:
        """Przechodzi do następnego logu na liście."""
        current_row = self._current_row()
        if 0 <= current_row < self._model.rowCount() - 1:
            self._select_row(current_row + 1)

    def _update_navigation_state(self) -> None:
        """Aktywuje/dezaktywuje przyciski nawigacji zależnie od pozycji.

        Przyciski są nieaktywne dla pierwszego (Previous) i ostatniego (Next)
        elementu listy – zgodnie ze specyfikacją.
        """
        row_count = self._model.rowCount()
        current_row = self._current_row()
        has_selection = 0 <= current_row < row_count

        self._prev_button.setEnabled(has_selection and current_row > 0)
        self._next_button.setEnabled(has_selection and current_row < row_count - 1)

    # ------------------------------------------------------------------ #
    # Metody pomocnicze                                                   #
    # ------------------------------------------------------------------ #
    def _current_row(self) -> int:
        """Zwraca indeks aktualnie zaznaczonego wiersza (lub -1)."""
        index = self._list_view.currentIndex()
        return index.row() if index.isValid() else -1

    def _select_row(self, row: int) -> None:
        """Zaznacza wiersz o podanym indeksie i przewija do niego widok."""
        index = self._model.index(row, 0)
        if index.isValid():
            self._list_view.setCurrentIndex(index)
            self._list_view.scrollTo(index)

    @staticmethod
    def _qdate_to_date(q_date: QDate) -> Optional[date]:
        """Konwertuje :class:`QDate` na standardowy ``datetime.date``."""
        if not q_date.isValid():
            return None
        return date(q_date.year(), q_date.month(), q_date.day())
