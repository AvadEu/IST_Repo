# Log browser — dokumentacja techniczna

Dokumentacja całego programu: opis modułów, wszystkich klas i funkcji
zaimplementowanych w projekcie oraz zestawienie wykorzystanych funkcji/klas
zewnętrznych (biblioteka standardowa Pythona i PySide6).

---

## 1. Przegląd

Aplikacja desktopowa (PySide6) do przeglądania logów serwera HTTP w formacie
Zeek/Bro (`http.log`, pola rozdzielone tabulacją). Interfejs realizuje wzorzec
**master-detail**: lista logów (master) po lewej, szczegóły zaznaczonego wpisu
(detail) po prawej.

Przepływ danych:

```
plik .log ──► LogParser ──► list[LogEntry] ──► LogListModel ──► QListView (master)
                  ▲                                  │
            LogLoaderWorker                           └──► panel detail (MainWindow)
            (osobny QThread)
```

Podział warstw:

| Warstwa   | Pakiet        | Zależy od Qt? |
|-----------|---------------|:-------------:|
| Logika    | `src.parser`  | nie           |
| Prezentacja | `src.gui`   | tak (PySide6) |
| Wejście   | `main.py`     | tak           |

---

## 2. `main.py`

Punkt wejścia aplikacji.

### `main() -> int`
Tworzy `QApplication`, instancję `MainWindow`, pokazuje okno i uruchamia pętlę
zdarzeń Qt. Zwraca kod wyjścia procesu (z `app.exec()`).

Blok `if __name__ == "__main__"` przekazuje wynik `main()` do `sys.exit()`.

---

## 3. `src/parser/models.py`

### klasa `LogEntry` (`@dataclass(slots=True)`)
Niemodyfikowalny w zamyśle kontener na jeden wpis logu. `slots=True` ogranicza
zużycie pamięci (plik może mieć setki tysięcy wierszy).

Pola:

| Pole          | Typ                  | Znaczenie                                |
|---------------|----------------------|------------------------------------------|
| `raw`         | `str`                | surowa treść wiersza                     |
| `timestamp`   | `Optional[datetime]` | czas zdarzenia (UTC) lub `None`          |
| `remote_host` | `str`                | adres hosta zdalnego (klient)            |
| `method`      | `str`                | metoda HTTP                              |
| `resource`    | `str`                | żądany zasób (URI)                       |
| `status_code` | `Optional[int]`      | kod statusu HTTP lub `None`              |
| `size`        | `int`                | rozmiar odpowiedzi w bajtach             |

Właściwości / metody:

- **`date_text -> str`** — data jako `YYYY-MM-DD` (pusty łańcuch przy braku czasu).
- **`time_text -> str`** — czas jako `HH:MM:SS` (pusty łańcuch przy braku czasu).
- **`timezone_text -> str`** — nazwa strefy (`"UTC"`) lub pusty łańcuch.
- **`summary(max_length=30) -> str`** — skrócona treść do widoku master:
  surowy wiersz ucięty do `max_length` znaków, a jeśli był dłuższy — zakończony
  `"..."`.

---

## 4. `src/parser/log_parser.py`

Stałe modułowe: indeksy kolumn (`_COL_TIMESTAMP=0`, `_COL_REMOTE_HOST=2`,
`_COL_METHOD=7`, `_COL_URI=9`, `_COL_RESPONSE_SIZE=13`, `_COL_STATUS=14`),
`_MIN_COLUMNS=15` (minimalna liczba kolumn) oraz `_EMPTY_TOKENS`
(`"-"`, `"(empty)"`, `""` — znaczniki braku danych Zeek).

### klasa `LogParseError(Exception)`
Wyjątek zgłaszany, gdy pliku nie da się odczytać/sparsować.

### klasa `LogParser`

- **`__init__(min_columns=_MIN_COLUMNS)`** — zapamiętuje próg minimalnej liczby
  kolumn.
- **`parse_file(path, progress_callback=None, is_cancelled=None) -> list[LogEntry]`**
  Czyta plik wiersz po wierszu i buduje listę wpisów.
  - `progress_callback(processed_bytes, total_size)` — wywoływana co 50 000
    wierszy oraz na końcu (gwarancja 100%).
  - `is_cancelled() -> bool` — sprawdzana okresowo; jeśli `True`, parsowanie się
    przerywa.
  - Zgłasza `LogParseError` przy błędzie `OSError`.
- **`parse_line(line) -> Optional[LogEntry]`** — parsuje pojedynczy wiersz.
  Zwraca `None` dla pustych wierszy, komentarzy Zeek (`#...`) oraz wierszy z
  liczbą kolumn mniejszą niż `min_columns`. W przeciwnym razie tworzy `LogEntry`.
- **`_file_size(path) -> int`** *(staticmethod)* — rozmiar pliku w bajtach
  (0 przy błędzie); używany do paska postępu.
- **`_clean(token) -> str`** *(staticmethod)* — zamienia znaczniki braku danych
  na pusty łańcuch.
- **`_parse_int(token) -> Optional[int]`** *(staticmethod)* — bezpieczna
  konwersja na `int` (`None` przy braku/niepoprawnej wartości).
- **`_parse_timestamp(token) -> Optional[datetime]`** *(staticmethod)* —
  konwertuje epoch (sekundy) na świadomy `datetime` w UTC; `None` przy błędzie.

---

## 5. `src/gui/log_list_model.py`

Stała `_SUMMARY_LENGTH = 30` — liczba znaków treści pokazywanej na liście.

### klasa `LogListModel(QAbstractListModel)`
Model danych dla widoku master. Przechowuje pełen zbiór wpisów oraz listę
widoczną (po filtrze dat).

Metody interfejsu Qt:

- **`rowCount(parent=QModelIndex()) -> int`** — liczba widocznych wpisów.
- **`data(index, role=Qt.DisplayRole)`** — dla `DisplayRole` zwraca
  `entry.summary()`, dla `ToolTipRole` pełny `raw`; w innych przypadkach `None`.

Metody domenowe:

- **`set_entries(entries)`** — ustawia nowy zbiór i czyści filtr; opakowane w
  `beginResetModel()` / `endResetModel()`.
- **`set_time_filter(date_from, date_to)`** — przebudowuje listę widoczną dla
  przedziału dat (oba krańce włącznie).
- **`entry_at(row) -> Optional[LogEntry]`** — widoczny wpis dla danego wiersza.
- **`is_empty() -> bool`** — czy nie wczytano żadnych danych.
- **`full_date_range() -> Optional[tuple[date, date]]`** — min/max data w całym
  zbiorze (do skonfigurowania pól wyboru daty).
- **`_matches_filter(entry) -> bool`** — czy wpis mieści się w aktualnym
  przedziale dat (wpisy bez czasu są ukrywane przy aktywnym filtrze).

---

## 6. `src/gui/log_loader.py`

### klasa `LogLoaderWorker(QObject)`
Obiekt roboczy parsujący plik w osobnym wątku (wzorzec *worker-object* +
`QThread`). Komunikacja z GUI wyłącznie przez sygnały.

Sygnały:

- **`progress = Signal(int)`** — postęp 0–100%.
- **`finished = Signal(list)`** — `list[LogEntry]` po zakończeniu.
- **`error = Signal(str)`** — komunikat błędu.

Metody:

- **`__init__(path)`** — zapamiętuje ścieżkę, tworzy `LogParser`, ustawia flagę
  anulowania na `False`.
- **`cancel()`** — ustawia flagę anulowania (sprawdzaną w pętli parsowania).
- **`run()`** — uruchamiana w wątku; woła `parser.parse_file(...)`, emituje
  `finished`/`error`. Łapie `LogParseError` oraz nieoczekiwane wyjątki.
- **`_on_progress(processed, total)`** — przelicza bajty na procenty i emituje
  `progress`.

---

## 7. `src/gui/status_indicator.py`

Stałe kolorów: `_COLOR_OK` (zielony), `_COLOR_CLIENT_ERR` (pomarańczowy),
`_COLOR_SERVER_ERR` (czerwony), `_COLOR_UNKNOWN` (szary).

### klasa `StatusIndicator(QWidget)`
Rysuje kolorowe kółko z wpisanym kodem statusu (jak na szkicu).

- **`__init__(parent=None)`** — minimalny rozmiar 54×54.
- **`sizeHint() -> QSize`** — sugerowany rozmiar 54×54.
- **`set_status_code(status_code)`** — zapisuje kod i woła `update()` (repaint).
- **`_color_for_status() -> QColor`** — dobiera kolor: `<400` zielony,
  `<500` pomarańczowy, reszta czerwony, `None` szary.
- **`paintEvent(event)`** — rysuje wypełniony okrąg i wyśrodkowany tekst kodu.

---

## 8. `src/gui/main_window.py`

### klasa `MainWindow(QWidget)`
Główne okno spinające całość; układ master-detail wg szkicu.

Konstruktor — tytuł okna, rozmiar, referencje na wątek/worker (chronione przed
GC), model `LogListModel`, wywołania `_build_ui()`, `_connect_signals()`,
`_update_navigation_state()`.

**Budowa UI:**

- **`_build_ui()`** — układ główny (pasek górny, treść master+detail, pasek
  dolny, pasek postępu).
- **`_build_top_bar() -> QHBoxLayout`** — pole ścieżki (read-only) + `Open`.
- **`_build_master_panel() -> QWidget`** — filtr `From`/`To` (`QDateEdit`) +
  `QListView` z modelem; `setUniformItemSizes(True)` dla wydajności.
- **`_build_detail_panel() -> QWidget`** — `QGroupBox` + `QFormLayout` z polami
  read-only (host, data, czas, strefa, metoda, zasób, rozmiar) i
  `StatusIndicator`.
- **`_build_bottom_bar() -> QHBoxLayout`** — przyciski `Previous` / `Next`.

**Sygnały:**

- **`_connect_signals()`** — podpina `Open`, `Previous`, `Next`, zmiany dat oraz
  `currentChanged` modelu zaznaczenia listy.

**Wczytywanie (wielowątkowe):**

- **`_on_open_clicked()`** — okno wyboru pliku, start ładowania.
- **`_start_loading(path)`** — tworzy `QThread` + `LogLoaderWorker`,
  `moveToThread`, podpina sygnały (start, progress, finished, error, sprzątanie)
  i startuje wątek.
- **`_on_loading_finished(entries)`** — ładuje dane do modelu, konfiguruje filtr
  dat, zaznacza pierwszy wiersz.
- **`_on_loading_error(message)`** — pokazuje `QMessageBox.critical`.
- **`_cleanup_thread()`** — `deleteLater()` na workerze i wątku, czyści
  referencje.

**Filtr dat:**

- **`_configure_date_filters()`** — ustawia zakres i wartości domyślne pól dat z
  `full_date_range()`; sygnały zablokowane na czas ustawiania.
- **`_on_filter_changed()`** — stosuje `set_time_filter()`, czyści detal,
  zaznacza pierwszy wiersz.

**Master-detail i nawigacja:**

- **`_on_selection_changed(current, _previous)`** — aktualizuje panel detail.
- **`_show_detail(entry)`** — wypełnia pola detail; rozmiar jako `"{n} Bytes"`.
- **`_clear_detail()`** — czyści pola i wskaźnik statusu.
- **`_on_previous_clicked()` / `_on_next_clicked()`** — przesuwają zaznaczenie.
- **`_update_navigation_state()`** — wyłącza `Previous` na pierwszym i `Next` na
  ostatnim wierszu.
- **`_current_row() -> int`** — indeks zaznaczonego wiersza (lub -1).
- **`_select_row(row)`** — ustawia zaznaczenie i przewija widok.
- **`_qdate_to_date(q_date) -> Optional[date]`** *(staticmethod)* — konwersja
  `QDate` → `datetime.date`.

---

## 9. Wykorzystane funkcje i klasy zewnętrzne

### Biblioteka standardowa Pythona

| Element                          | Moduł        | Gdzie / po co                                  |
|----------------------------------|--------------|------------------------------------------------|
| `dataclass`, `field` (`slots`)   | `dataclasses`| definicja `LogEntry`                           |
| `datetime`                       | `datetime`   | znacznik czasu wpisu                           |
| `datetime.fromtimestamp`         | `datetime`   | epoch → `datetime`                             |
| `datetime.strftime`              | `datetime`   | formatowanie daty/czasu                        |
| `datetime.date()`                | `datetime`   | wyciągnięcie daty do filtra                    |
| `timezone.utc`                   | `datetime`   | strefa UTC dla znaczników                      |
| `date`                           | `datetime`   | typ daty filtra                                |
| `Optional`, `List`, `Callable`   | `typing`     | podpowiedzi typów                              |
| `os.path.getsize`                | `os`         | rozmiar pliku (pasek postępu)                  |
| `open`, `str.split`, `str.strip` | wbudowane    | czytanie i rozbijanie wierszy                  |
| `int`, `float`, `len`, `min/max` | wbudowane    | konwersje i obliczenia                         |
| `sys.argv`, `sys.exit`           | `sys`        | argumenty i kod wyjścia                        |
| `frozenset`                      | wbudowane    | zbiór znaczników braku danych                  |

### PySide6 — `QtWidgets`

| Klasa            | Gdzie / po co                                         |
|------------------|-------------------------------------------------------|
| `QApplication`   | pętla zdarzeń aplikacji (`main.py`)                   |
| `QWidget`        | klasa bazowa `MainWindow`, `StatusIndicator`          |
| `QVBoxLayout`, `QHBoxLayout` | układy pionowe/poziome                    |
| `QFormLayout`    | układ panelu detail (etykieta → pole)                 |
| `QGroupBox`      | ramka panelu szczegółów                               |
| `QLabel`         | etykiety `From` / `To`                                |
| `QLineEdit`      | ścieżka pliku i pola szczegółów (read-only)           |
| `QPushButton`    | `Open`, `Previous`, `Next`                            |
| `QListView`      | widok master (lista logów)                            |
| `QDateEdit`      | wybór dat filtra (`From` / `To`)                      |
| `QProgressBar`   | pasek postępu wczytywania                             |
| `QFileDialog.getOpenFileName` | okno wyboru pliku                        |
| `QMessageBox.critical` | komunikat o błędzie                             |

### PySide6 — `QtCore`

| Element               | Gdzie / po co                                          |
|-----------------------|--------------------------------------------------------|
| `QAbstractListModel`  | bazowa klasa `LogListModel`                            |
| `QModelIndex`         | indeksy wierszy w modelu                               |
| `Qt` (role/flagi)     | `DisplayRole`, `ToolTipRole`, `AlignCenter`, `NoPen`…  |
| `QObject`             | bazowa klasa `LogLoaderWorker`                         |
| `Signal`              | sygnały `progress` / `finished` / `error`              |
| `QThread`             | wątek roboczy parsowania                               |
| `QDate`               | daty w `QDateEdit`; konwersja do `datetime.date`       |
| `QSize`               | rozmiary `StatusIndicator`                             |
| `moveToThread`        | przeniesienie workera do wątku                         |
| `beginResetModel` / `endResetModel` | sygnalizacja zmiany danych modelu       |
| `blockSignals`        | tymczasowe wyciszenie sygnałów pól dat                 |
| `deleteLater`         | bezpieczne usuwanie obiektów Qt                        |

### PySide6 — `QtGui`

| Element                | Gdzie / po co                                  |
|------------------------|------------------------------------------------|
| `QPainter`             | rysowanie wskaźnika statusu                     |
| `QColor`               | kolory kółka i tekstu                           |
| `QFont`                | pogrubiona, skalowana czcionka kodu             |
| `QPaintEvent`          | typ zdarzenia `paintEvent`                       |
| `QPainter.Antialiasing`| wygładzanie krawędzi okręgu                     |
| `drawEllipse`, `drawText` | rysowanie kółka i tekstu                     |
```
