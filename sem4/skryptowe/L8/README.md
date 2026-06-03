# Log browser

Aplikacja desktopowa (PySide6) do przeglądania logów serwera HTTP, zbudowana
w oparciu o wzorzec **master-detail**. Powstała na potrzeby Laboratorium 8 –
Programowanie GUI (Języki skryptowe w Python).

## Funkcjonalności

Aplikacja realizuje dokładnie wymagania ze specyfikacji:

1. **Wczytanie pliku z logami** – przycisk `Open` otwiera okno wyboru pliku.
2. **Lista logów (master)** – po wczytaniu pliku wiersze prezentowane są na
   liście; każdy wpis to surowa treść logu ucięta do 30 znaków i zakończona
   wielokropkiem.
3. **Wzorzec master-detail** – zaznaczenie wpisu na liście (master) aktualizuje
   panel szczegółów (detail) prezentujący atrybuty logu: adres hosta zdalnego,
   datę, czas, strefę czasową, kod statusu (kolorowy wskaźnik), metodę HTTP,
   zasób oraz rozmiar odpowiedzi.
4. **Filtrowanie po przedziale czasowym** – pola `From` / `To` (wybór daty)
   ograniczają listę do wpisów z wybranego zakresu dat.
5. **Nawigacja `Previous` / `Next`** – przyciski przechodzą do poprzedniego /
   następnego logu (równoważne zaznaczeniu go na liście). Dla pierwszego /
   ostatniego wpisu odpowiedni przycisk jest nieaktywny.

## Architektura

Projekt zachowuje wyraźny podział na warstwę logiki i warstwę prezentacji
(GUI), zgodnie z wzorcem zbliżonym do MVC:

```
L8/
├── main.py                       # Punkt wejścia – uruchamia aplikację Qt
├── requirements.txt
├── README.md
└── src/
    ├── parser/                   # Warstwa logiki (niezależna od GUI)
    │   ├── models.py             # LogEntry – model danych pojedynczego wpisu
    │   └── log_parser.py         # LogParser – wydajne parsowanie pliku logów
    └── gui/                      # Warstwa prezentacji (PySide6)
        ├── log_list_model.py     # LogListModel – QAbstractListModel (master)
        ├── log_loader.py         # LogLoaderWorker – parsowanie w QThread
        ├── status_indicator.py   # StatusIndicator – kolorowy wskaźnik statusu
        └── main_window.py        # MainWindow – złożenie widoku master-detail
```

Kluczowe decyzje projektowe:

- **Separacja warstw.** Pakiet `src.parser` nie importuje żadnych modułów Qt –
  logikę parsowania można testować i wykorzystywać niezależnie od GUI.
- **Wydajność.** Lista logów korzysta z własnego modelu
  `QAbstractListModel` (`LogListModel`). Dane pobierane są leniwie (tylko dla
  widocznych elementów), a wpisy przechowywane są raz, bez kopiowania do
  widżetów – dzięki temu obsługa setek tysięcy wierszy pozostaje płynna.
  Rekordy `LogEntry` używają `slots=True` dla ograniczenia zużycia pamięci.
- **Wielowątkowość.** Wczytywanie i parsowanie pliku odbywa się w osobnym
  wątku (`LogLoaderWorker` przeniesiony do `QThread`), z raportowaniem postępu
  przez sygnały. Główny wątek GUI nie jest blokowany.

## Format logów

Parser jest dostosowany do logów HTTP w formacie Zeek/Bro (`http.log`) –
pola rozdzielone tabulacją. Wykorzystywane kolumny (indeksowane od 0):

| Indeks | Pole                | Prezentacja w panelu detail |
|-------:|---------------------|-----------------------------|
| 0      | `ts` (epoch)        | Date / Time / Timezone      |
| 2      | `id.orig_h`         | Remote host                 |
| 7      | `method`            | Method                      |
| 9      | `uri`               | Resource                    |
| 13     | `response_body_len` | Size                        |
| 14     | `status_code`       | Status code                 |

Wiersze komentarzy Zeek (rozpoczynające się od `#`) oraz wiersze z niepełną
liczbą kolumn są pomijane.

## Wymagania

- Python 3.10+
- PySide6 (patrz `requirements.txt`)

## Uruchomienie

```bash
# (opcjonalnie) wirtualne środowisko
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# instalacja zależności
pip install -r requirements.txt

# uruchomienie aplikacji
python main.py
```

Po uruchomieniu kliknij `Open` i wskaż plik z logami (np. dołączony
`http_first_100k.log`).
