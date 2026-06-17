# Laboratorium 10 – Obsługa baz danych (GTFS, SQLite)

Rozwiązanie obsługuje rozkład jazdy transportu publicznego w formacie **GTFS**
(paczka plików CSV o rozszerzeniu `.txt`) z wykorzystaniem bazy **SQLite**.
Zawiera wersję podstawową (czysty `sqlite3`) oraz **wersję dla ambitnych**
(ORM SQLAlchemy + webowy interfejs Flask).

## Struktura projektu

| Plik | Zadanie | Opis |
|------|---------|------|
| `schema.sql` | 1a | Polecenia DDL (CREATE TABLE + klucze obce) |
| `create_database.py` | 1b | Tworzy pusty plik bazy `<nazwa>.sqlite3` |
| `load_data.py` | 2 | Importuje GTFS (ZIP lub katalog) do bazy |
| `query_stop.py` | 3 | Interaktywna analiza przystanku (CLI) |
| `gtfs_common.py` | 1–2 | Wspólne narzędzia (czytanie GTFS, parsowanie godzin) |
| `queries.py` | 3 | Zapytania SQL współdzielone przez CLI i web |
| `orm_models.py` | ambitna | Modele ORM (SQLAlchemy) + relacje |
| `create_database_orm.py` | ambitna 1 | Tworzenie struktury z poziomu kodu (ORM) |
| `load_data_orm.py` | ambitna 2 | Import przez ORM + zapytanie agregujące |
| `app.py` + `templates/` | ambitna 3 | Webowy interfejs (Flask) |

## Model danych

```
agency ──< routes ──< trips ──< stop_times >── stops
                         │
              calendar ──┘
```

Klucze obce realizują więzy integralności referencyjnej. Godziny przyjazdu/odjazdu
przechowywane są jako `TEXT` (`HH:MM:SS`, GTFS dopuszcza wartości > 24:00:00 dla
kursów po północy) wraz z pomocniczą kolumną `departure_seconds` (liczba sekund
od początku doby) ułatwiającą sortowanie i porównania.

## Instalacja

Wersja podstawowa (Zadania 1–3) używa wyłącznie biblioteki standardowej.
Wersja dla ambitnych wymaga dodatkowych pakietów:

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Wersja podstawowa (Zadania 1–3)

```bash
# 1. Utworzenie pustej struktury bazy -> my_timetable.sqlite3
python create_database.py my_timetable

# 2. Import danych GTFS (paczka ZIP albo katalog z plikami .txt)
python load_data.py data my_timetable
#   lub:
python load_data.py OtwartyWroclaw_rozklad_jazdy_GTFS.zip my_timetable

# 3. Interaktywna analiza wybranego przystanku
python query_stop.py my_timetable
```

Zadanie 3 dla wybranego przystanku oblicza i wyświetla:
- **a)** liczbę różnych linii zatrzymujących się na przystanku,
- **b)** liczbę odjazdów z przystanku,
- **c)** najwcześniejszy i najpóźniejszy odjazd,
- **d)** najczęstsze kierunki odjazdów,
- **e)** nietrywialne zestawienie linii (połączenie 3 tabel + grupowanie i agregacja).

## Wersja dla ambitnych

### ORM (Zadania 1–2 z SQLAlchemy)

```bash
# Tworzy strukturę z poziomu kodu (Base.metadata.create_all) i importuje dane,
# a na koniec wykonuje zapytanie agregujące (top przystanków wg liczby odjazdów).
python load_data_orm.py data my_timetable_orm --create
```

Wersja ORM obejmuje: definicję klas modeli (`orm_models.py`), odwzorowanie
relacji (`relationship` + klucze obce), tworzenie struktury z poziomu Pythona,
import danych przez modele oraz zapytanie agregujące (`func.count` + `group_by`).

### Webowy interfejs (Zadanie 3)

```bash
python app.py my_timetable
# otwórz http://127.0.0.1:5000
```

Interfejs pozwala wyszukać i wybrać przystanek, a następnie prezentuje te same
statystyki (a–e) w formie kart i tabel.
