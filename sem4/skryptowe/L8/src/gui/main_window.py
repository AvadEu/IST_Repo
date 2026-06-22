# main window, master-detail layout matching the spec sketch.
# heavy parsing goes to a worker thread, GUI only reacts to its signals.
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
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Log browser")
        self.resize(1000, 600)

        # keep refs so the thread/worker don't get garbage collected mid-run
        self._thread: Optional[QThread] = None
        self._worker: Optional[LogLoaderWorker] = None

        self._model = LogListModel(self)

        self._build_ui()
        self._connect_signals()
        self._update_navigation_state()

    # ---- ui building ----
    def _build_ui(self) -> None:
        root_layout = QVBoxLayout(self)

        root_layout.addLayout(self._build_top_bar())

        content_layout = QHBoxLayout()
        content_layout.addWidget(self._build_master_panel(), stretch=1)
        content_layout.addWidget(self._build_detail_panel(), stretch=1)
        root_layout.addLayout(content_layout, stretch=1)

        root_layout.addLayout(self._build_bottom_bar())

        self._progress_bar = QProgressBar()
        self._progress_bar.setVisible(False)  # only shown while loading
        root_layout.addWidget(self._progress_bar)

    def _build_top_bar(self) -> QHBoxLayout:
        # path field + Open button
        layout = QHBoxLayout()
        self._path_edit = QLineEdit()
        self._path_edit.setReadOnly(True)
        self._path_edit.setPlaceholderText("Wybierz plik z logami…")
        self._open_button = QPushButton("Open")
        layout.addWidget(self._path_edit, stretch=1)
        layout.addWidget(self._open_button)
        return layout

    def _build_master_panel(self) -> QWidget:
        # left side: From/To date filter + the log list
        panel = QWidget()
        layout = QVBoxLayout(panel)

        filter_layout = QHBoxLayout()
        self._date_from = QDateEdit()
        self._date_to = QDateEdit()
        self.url_filter = QLineEdit()
        self.url_filter.setEnabled(True)
        for editor in (self._date_from, self._date_to):
            editor.setCalendarPopup(True)
            editor.setDisplayFormat("yyyy-MM-dd")
            editor.setEnabled(False)  # nothing to filter until a file is loaded
        filter_layout.addWidget(QLabel("From"))
        filter_layout.addWidget(self._date_from)
        filter_layout.addSpacing(12)
        filter_layout.addWidget(QLabel("To"))
        filter_layout.addWidget(self._date_to)
        filter_layout.addStretch(1)
        filter_layout.addWidget(self.url_filter)
        layout.addLayout(filter_layout)

        self._list_view = QListView()
        self._list_view.setModel(self._model)
        self._list_view.setUniformItemSizes(True)  # speeds up big lists
        self._list_view.setEditTriggers(QListView.NoEditTriggers)
        layout.addWidget(self._list_view, stretch=1)

        return panel

    def _build_detail_panel(self) -> QWidget:
        # right side: details of the selected log
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

        # read-only, these just show data
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
        # Previous / Next nav buttons
        layout = QHBoxLayout()
        self._prev_button = QPushButton("Previous")
        self._next_button = QPushButton("Next")
        layout.addWidget(self._prev_button)
        layout.addStretch(1)
        layout.addWidget(self._next_button)
        return layout

    # ---- signal wiring ----
    def _connect_signals(self) -> None:
        self._open_button.clicked.connect(self._on_open_clicked)
        self._prev_button.clicked.connect(self._on_previous_clicked)
        self._next_button.clicked.connect(self._on_next_clicked)
        self._date_from.dateChanged.connect(self._on_filter_changed)
        self._date_to.dateChanged.connect(self._on_filter_changed)
        self.url_filter.textChanged.connect(self._on_url_filter_changed)

        selection_model = self._list_view.selectionModel()
        selection_model.currentChanged.connect(self._on_selection_changed)

    # ---- file loading (threaded) ----
    def _on_open_clicked(self) -> None:
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
        # spin up the worker thread and hook its signals
        self._open_button.setEnabled(False)  # block re-open while busy
        self._progress_bar.setValue(0)
        self._progress_bar.setVisible(True)

        self._thread = QThread(self)
        self._worker = LogLoaderWorker(path)
        self._worker.moveToThread(self._thread)

        self._thread.started.connect(self._worker.run)
        self._worker.progress.connect(self._progress_bar.setValue)
        self._worker.finished.connect(self._on_loading_finished)
        self._worker.error.connect(self._on_loading_error)
        # cleanup once done
        self._worker.finished.connect(self._thread.quit)
        self._worker.error.connect(self._thread.quit)
        self._thread.finished.connect(self._cleanup_thread)

        self._thread.start()

    def _on_loading_finished(self, entries: list) -> None:
        self._progress_bar.setVisible(False)
        self._open_button.setEnabled(True)

        self._model.set_entries(entries)
        self._configure_date_filters()
        self._clear_detail()

        if self._model.rowCount() > 0:
            self._select_row(0)  # auto-pick first row
        self._update_navigation_state()

    def _on_loading_error(self, message: str) -> None:
        self._progress_bar.setVisible(False)
        self._open_button.setEnabled(True)
        QMessageBox.critical(self, "Błąd wczytywania", message)

    def _cleanup_thread(self) -> None:
        # drop refs to the finished thread/worker
        if self._worker is not None:
            self._worker.deleteLater()
            self._worker = None
        if self._thread is not None:
            self._thread.deleteLater()
            self._thread = None

    # ---- date range filter ----
    def _configure_date_filters(self) -> None:
        # set picker range + defaults from the data
        date_range = self._model.full_date_range()
        # block signals so setting defaults doesn't trigger a filter pass
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
        if self._model.is_empty():
            return

        date_from = self._qdate_to_date(self._date_from.date())
        date_to = self._qdate_to_date(self._date_to.date())
        self._model.set_time_filter(date_from, date_to)
        self._model.set_url_filter(self.url_filter.text())

        self._clear_detail()
        if self._model.rowCount() > 0:
            self._select_row(0)
        self._update_navigation_state()

    def _on_url_filter_changed(self, text: str) -> None:
        # refresh the list every time the resource text filter changes
        if self._model.is_empty():
            return

        self._model.set_url_filter(text)

        self._clear_detail()
        if self._model.rowCount() > 0:
            self._select_row(0)
        self._update_navigation_state()

    # ---- master-detail selection ----
    def _on_selection_changed(self, current, _previous) -> None:
        if current is None or not current.isValid():
            self._clear_detail()
        else:
            entry = self._model.entry_at(current.row())
            if entry is not None:
                self._show_detail(entry)
        self._update_navigation_state()

    def _show_detail(self, entry: LogEntry) -> None:
        self._detail_remote_host.setText(entry.remote_host)
        self._detail_date.setText(entry.date_text)
        self._detail_time.setText(entry.time_text)
        self._detail_timezone.setText(entry.timezone_text)
        self._detail_method.setText(entry.method)
        self._detail_resource.setText(entry.resource)
        self._detail_size.setText(f"{entry.size} Bytes")
        self._status_indicator.set_status_code(entry.status_code)

    def _clear_detail(self) -> None:
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

    # ---- Previous / Next ----
    def _on_previous_clicked(self) -> None:
        current_row = self._current_row()
        if current_row > 0:
            self._select_row(current_row - 1)

    def _on_next_clicked(self) -> None:
        current_row = self._current_row()
        if 0 <= current_row < self._model.rowCount() - 1:
            self._select_row(current_row + 1)

    def _update_navigation_state(self) -> None:
        # disable Previous on first row and Next on last row
        row_count = self._model.rowCount()
        current_row = self._current_row()
        has_selection = 0 <= current_row < row_count

        self._prev_button.setEnabled(has_selection and current_row > 0)
        self._next_button.setEnabled(has_selection and current_row < row_count - 1)

    # ---- helpers ----
    def _current_row(self) -> int:
        index = self._list_view.currentIndex()
        return index.row() if index.isValid() else -1

    def _select_row(self, row: int) -> None:
        # select + scroll into view
        index = self._model.index(row, 0)
        if index.isValid():
            self._list_view.setCurrentIndex(index)
            self._list_view.scrollTo(index)

    @staticmethod
    def _qdate_to_date(q_date: QDate) -> Optional[date]:
        # QDate -> datetime.date
        if not q_date.isValid():
            return None
        return date(q_date.year(), q_date.month(), q_date.day())
