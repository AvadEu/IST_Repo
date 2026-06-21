# Receipt Scanner — kontekst projektu dla Claude Code

## Opis projektu

Aplikacja webowa do skanowania i kategoryzowania paragonów. Użytkownik wrzuca
zdjęcie paragonu przez drag & drop, system wykonuje OCR, wyciąga dane (sklep,
data, kwoty, pozycje), kategoryzuje wydatki i zapisuje do bazy danych.
Dashboard pokazuje podsumowanie wydatków w postaci wykresów Chart.js.

Projekt realizowany na zaliczenie kursu "Języki skryptowe". Wymagania:
- separacja warstw (UI / logika biznesowa / dane)
- zasady SOLID, DRY
- testy jednostkowe kluczowych serwisów
- obsługa błędów i walidacja (pydantic v2)
- dokumentacja i instrukcja wdrożenia
- Docker jako metoda pakietowania

---

## Stos technologiczny

| Warstwa | Technologia |
|---|---|
| Backend | FastAPI, Python 3.12, pydantic v2 |
| OCR | pytesseract, Pillow, opencv-python-headless |
| Kategoryzacja | reguły słownikowe + scikit-learn fallback |
| Baza danych | MariaDB, SQLAlchemy 2.x ORM, Alembic |
| Frontend | Vanilla JS, Chart.js (CDN), HTML/CSS |
| Serwer frontendu | nginx (proxy /api → backend) |
| Manager pakietów | pip + requirements.txt |
| Konteneryzacja | Docker, docker-compose |
| Testy | pytest, httpx, pytest-asyncio |

---

## Architektura — trzy kontenery Docker

```
┌─────────────────────────────────────────────┐
│  Frontend (nginx)                           │
│  upload.html · receipts.html · dashboard.html│
│  js/api.js · upload.js · receipts.js · dashboard.js │
└──────────────┬──────────────────────────────┘
               │ REST /api/*
┌──────────────▼──────────────────────────────┐
│  Backend (FastAPI uvicorn)                  │
│  api/receipts.py  →  POST /receipts/upload  │
│                   →  GET  /receipts         │
│                   →  GET  /receipts/{id}    │
│                   →  DELETE /receipts/{id}  │
│  api/dashboard.py →  GET  /dashboard/summary│
│                                             │
│  services/ocr_service.py        (PIL+tess.) │
│  services/parser_service.py     (regex)     │
│  services/categorizer_service.py(rules+ML)  │
└──────────────┬──────────────────────────────┘
               │ SQLAlchemy ORM
┌──────────────▼──────────────────────────────┐
│  MariaDB                                    │
│  receipts · receipt_items                   │
└─────────────────────────────────────────────┘
               + Docker volume /uploads (zdjęcia paragonów)
```

---

## Hierarchia katalogów (docelowa)

```
receipt-scanner/
├── docker-compose.yml
├── .env.example
├── Makefile
├── README.md
├── CLAUDE.md
│
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app/
│   │   ├── main.py               # FastAPI app, CORS, mount /uploads
│   │   ├── config.py             # pydantic-settings (.env)
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── receipts.py       # endpointy paragonów
│   │   │   └── dashboard.py      # endpoint podsumowania
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── ocr_service.py
│   │   │   ├── parser_service.py
│   │   │   └── categorizer_service.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── receipt.py        # Receipt + ReceiptItem ORM
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   └── receipt.py        # pydantic schemas
│   │   └── db/
│   │       ├── __init__.py
│   │       └── session.py        # engine, SessionLocal, get_db()
│   ├── migrations/
│   │   ├── env.py
│   │   └── versions/
│   └── tests/
│       ├── conftest.py
│       ├── test_ocr_service.py
│       ├── test_parser_service.py
│       ├── test_categorizer_service.py
│       └── test_api.py
│
└── frontend/
    ├── Dockerfile
    ├── nginx.conf
    └── src/
        ├── index.html
        ├── upload.html
        ├── receipts.html
        ├── dashboard.html
        └── js/
            ├── api.js
            ├── upload.js
            ├── receipts.js
            └── dashboard.js
```

---

## Modele bazy danych

### Tabela `receipts`
| Kolumna | Typ | Opis |
|---|---|---|
| id | INT PK autoincrement | |
| store_name | VARCHAR(255) | nazwa sklepu z OCR |
| receipt_date | DATE nullable | data z paragonu |
| total_amount | DECIMAL(10,2) | kwota total |
| image_path | VARCHAR(512) | ścieżka do pliku na woluminie |
| raw_text | TEXT | surowy tekst z OCR |
| created_at | DATETIME | timestamp dodania |

### Tabela `receipt_items`
| Kolumna | Typ | Opis |
|---|---|---|
| id | INT PK autoincrement | |
| receipt_id | INT FK → receipts.id | |
| name | VARCHAR(255) | nazwa pozycji |
| amount | DECIMAL(10,2) | kwota pozycji |
| category | VARCHAR(100) | przypisana kategoria |

---

## requirements.txt (backend)

```
fastapi==0.115.0
uvicorn[standard]==0.30.0
pydantic==2.8.0
pydantic-settings==2.4.0
sqlalchemy==2.0.35
alembic==1.13.3
pymysql==1.1.1
cryptography==43.0.1
pytesseract==0.3.13
pillow==10.4.0
opencv-python-headless==4.10.0.84
scikit-learn==1.5.2
numpy==1.26.4
python-multipart==0.0.12
pytest==8.3.3
pytest-asyncio==0.24.0
httpx==0.27.2
```

---

## Autorzy commitów

Projekt jest realizowany przez dwie osoby. Przy każdym commicie używaj
flagi `--author` zgodnie z poniższym podziałem. **Nigdy nie commituj bez
jawnego `--author`.**

```
Osoba A: AvadEu <dutwik44@wp.pl>
Osoba B: xLyciaX <ala.wieczorek.0805@gmail.com>
```

Format commita:
```bash
git add .
git commit --author="Imię Nazwisko <email>" -m "typ: opis"
```

Typy commitów (conventional commits):
- `feat:` nowa funkcjonalność
- `test:` testy jednostkowe
- `infra:` Docker, konfiguracja, CI
- `docs:` dokumentacja

---

## Plan implementacji — kroki i autorzy

Implementuj **jeden krok na raz**. Po każdym kroku wykonaj commit z podanym
autorem i **czekaj na potwierdzenie** przed przejściem do następnego.

---

### Krok 1 — Autor: Anna Kowalska
**Inicjalizacja projektu i infrastruktura**

Utwórz:
- `docker-compose.yml` z trzema serwisami: `backend`, `frontend`, `mariadb`
  oraz woluminem `uploads_data` i `mariadb_data`
- `.env.example` ze zmiennymi: `DB_URL`, `SECRET_KEY`, `UPLOAD_DIR=/uploads`
- `Makefile` z targetami: `up`, `down`, `migrate`, `test`, `lint`
- `backend/Dockerfile` — python:3.12-slim, instalacja tesseract-ocr,
  tesseract-ocr-pol, libgl1 przez apt, potem pip install -r requirements.txt
- `backend/requirements.txt` — zgodnie z listą powyżej
- `frontend/Dockerfile` — nginx:alpine
- `frontend/nginx.conf` — serwowanie plików statycznych + proxy
  `location /api/ { proxy_pass http://backend:8000/; }`
- pusty `README.md`

Commit:
```
git commit --author="Anna Kowalska <anna.kowalska@student.pwr.edu.pl>" -m "infra: project scaffold, docker-compose, Dockerfiles, Makefile"
```

---

### Krok 2 — Autor: Anna Kowalska
**Baza danych — modele i migracje**

Utwórz:
- `backend/app/config.py` — klasa `Settings` z pydantic-settings,
  pola: `db_url`, `upload_dir`, `secret_key`
- `backend/app/db/session.py` — `engine`, `SessionLocal`, `Base`, `get_db()`
- `backend/app/models/receipt.py` — klasy `Receipt` i `ReceiptItem`
  zgodnie ze schematem tabel powyżej, relacja `Receipt.items`
- `backend/app/models/__init__.py`
- inicjalizacja Alembic (`alembic init migrations`), konfiguracja `env.py`
  żeby używał `Base.metadata` i `Settings().db_url`
- pierwsza migracja: `alembic revision --autogenerate -m "initial"`

Commit:
```
git commit --author="Anna Kowalska <anna.kowalska@student.pwr.edu.pl>" -m "feat: database models Receipt and ReceiptItem, Alembic migrations"
```

---

### Krok 3 — Autor: Anna Kowalska
**Serwis OCR**

Utwórz `backend/app/services/ocr_service.py`:
- funkcja `preprocess_image(image_path: str) -> Image`:
  - wczytaj PIL Image
  - konwertuj do skali szarości
  - zastosuj cv2 threshold (THRESH_BINARY + THRESH_OTSU)
  - przeskaluj do min. 1800px szerokości jeśli mniejszy
- funkcja `extract_text(image_path: str) -> str`:
  - wywołaj preprocess_image
  - pytesseract.image_to_string z lang='pol+eng'
  - zwróć oczyszczony tekst (strip)
- obsługa wyjątków: `TesseractNotFoundError` → raise `RuntimeError`

Utwórz `backend/tests/conftest.py`:
- fixture `sample_image_path` tworząca tymczasowy prosty obrazek PNG

Utwórz `backend/tests/test_ocr_service.py`:
- test że `extract_text` zwraca string
- test że pusty plik rzuca wyjątek
- test preprocessingu (mock pytesseract)

Commit:
```
git commit --author="Anna Kowalska <anna.kowalska@student.pwr.edu.pl>" -m "feat: ocr_service with Tesseract preprocessing, unit tests"
```

---

### Krok 4 — Autor: Anna Kowalska
**Serwis parsowania**

Utwórz `backend/app/services/parser_service.py`:
- funkcja `parse_receipt(text: str) -> dict`:
  - `extract_date(text)` — regex dla formatów: DD.MM.YYYY, YYYY-MM-DD,
    DD/MM/YYYY; zwraca `datetime.date` lub `None`
  - `extract_store_name(text)` — pierwsza niepusta linia tekstu,
    max 60 znaków, stripped
  - `extract_total(text)` — regex szukający wzorców: `SUMA`, `RAZEM`,
    `DO ZAPŁATY`, `TOTAL` + kwota `\d+[.,]\d{2}`; zwraca `Decimal` lub `None`
  - `extract_items(text)` — lista słowników `{name, amount}` z linii
    pasujących do wzorca: tekst + kwota na końcu linii
  - zwraca `{store_name, date, total_amount, items}`

Utwórz `backend/tests/test_parser_service.py`:
- testy z przykładowymi tekstami paragonów (Biedronka, Lidl)
- test ekstrakcji daty w każdym formacie
- test gdy brak kwoty total → None
- test przypadku brzegowego: pusty tekst

Commit:
```
git commit --author="Anna Kowalska <anna.kowalska@student.pwr.edu.pl>" -m "feat: parser_service regex extraction, date/total/items, unit tests"
```

---

### Krok 5 — Autor: Piotr Nowak
**Serwis kategoryzacji**

Utwórz `backend/app/services/categorizer_service.py`:

Słownik słów kluczowych (etap 1):
```python
CATEGORY_KEYWORDS = {
    "Jedzenie": ["biedronka", "lidl", "aldi", "żabka", "carrefour",
                 "kaufland", "netto", "tesco", "intermarche", "spar",
                 "chleb", "mleko", "mięso", "warzywa", "owoce", "nabiał"],
    "Transport": ["orlen", "bp", "shell", "lotos", "circle k",
                  "paliwo", "parking", "mpk", "bilety", "pkp", "pks"],
    "Dom": ["ikea", "leroy merlin", "obi", "castorama",
            "media markt", "rtv euro agd", "prąd", "gaz", "czynsz"],
    "Zdrowie": ["apteka", "rossmann", "super-pharm", "leki",
                "dr max", "gemini", "przychodnia"],
    "Rozrywka": ["cinema city", "multikino", "steam", "empik",
                 "allegro", "netflix", "spotify", "book"],
}
```

- funkcja `categorize_item(item_name: str) -> str`:
  - etap 1: sprawdź słownik (case-insensitive, contains)
  - etap 2 (fallback): TF-IDF + MultinomialNB na małym zbiorze
    treningowym zakodowanym w pliku (min. 30 przykładów)
  - domyślna kategoria: `"Inne"`

- funkcja `categorize_receipt(store_name: str, items: list) -> list`:
  - najpierw próbuj kategoryzować po nazwie sklepu
  - jeśli sklep rozpoznany → przypisz tę kategorię wszystkim pozycjom
  - jeśli nie → kategoryzuj każdą pozycję osobno

Utwórz `backend/tests/test_categorizer_service.py`:
- test rozpoznania po nazwie sklepu
- test fallbacku ML dla nieznanego sklepu
- test case-insensitive
- test kategorii domyślnej `"Inne"`

Commit:
```
git commit --author="Piotr Nowak <piotr.nowak@student.pwr.edu.pl>" -m "feat: categorizer_service keyword rules + sklearn fallback, unit tests"
```

---

### Krok 6 — Autor: Piotr Nowak
**Pydantic schemas i endpointy FastAPI**

Utwórz `backend/app/schemas/receipt.py`:
- `ReceiptItemRead` — id, name, amount, category
- `ReceiptRead` — id, store_name, receipt_date, total_amount,
  image_path, created_at, items: list[ReceiptItemRead]
- `ReceiptListItem` — uproszczony widok listy (bez items)
- `DashboardSummary` — total_spent, receipt_count,
  by_category: dict[str, float], by_month: dict[str, float]

Utwórz `backend/app/api/receipts.py`:
- `POST /receipts/upload` — przyjmuje `UploadFile`:
  1. zapisz plik na `UPLOAD_DIR/{uuid}.jpg`
  2. `ocr_service.extract_text(path)`
  3. `parser_service.parse_receipt(text)`
  4. `categorizer_service.categorize_receipt(...)`
  5. zapisz `Receipt` + `ReceiptItem[]` do bazy
  6. zwróć `ReceiptRead`
  - walidacja: tylko image/jpeg i image/png, max 10MB
  - obsługa błędu OCR: zapisz paragon z `raw_text` i pustymi pozycjami
- `GET /receipts` — lista `ReceiptListItem`, paginacja (skip, limit=20)
- `GET /receipts/{id}` — pełny `ReceiptRead` z items
- `DELETE /receipts/{id}` — usuń z bazy i plik z dysku

Utwórz `backend/app/api/dashboard.py`:
- `GET /dashboard/summary` — zwraca `DashboardSummary`:
  - `total_spent`: SUM(total_amount)
  - `receipt_count`: COUNT(*)
  - `by_category`: SUM per category z receipt_items
  - `by_month`: SUM per miesiąc (ostatnie 6 miesięcy)

Utwórz `backend/app/main.py`:
- instancja FastAPI z tytułem i wersją
- CORS middleware (origins=["*"] dla dev)
- include_router dla receipts i dashboard z prefixem `/api`
- StaticFiles mount: `/uploads` → `UPLOAD_DIR`

Commit:
```
git commit --author="Piotr Nowak <piotr.nowak@student.pwr.edu.pl>" -m "feat: FastAPI endpoints receipts CRUD and dashboard summary"
```

---

### Krok 7 — Autor: Piotr Nowak
**Testy integracyjne API**

Uzupełnij `backend/tests/conftest.py`:
- fixture `client` — `TestClient(app)` z podmienioną bazą SQLite in-memory
- fixture `sample_receipt_payload` — słownik z przykładowymi danymi

Utwórz `backend/tests/test_api.py`:
- test `POST /api/receipts/upload` z mockowanym `ocr_service`
  (żeby nie wymagać Tesseract w CI)
- test `GET /api/receipts` — zwraca listę
- test `GET /api/receipts/{id}` — zwraca szczegóły
- test `DELETE /api/receipts/{id}` — usuwa rekord
- test `GET /api/dashboard/summary` — zwraca poprawną strukturę
- test walidacji: upload pliku PDF → 422

Commit:
```
git commit --author="Piotr Nowak <piotr.nowak@student.pwr.edu.pl>" -m "test: integration tests for receipts and dashboard API endpoints"
```

---

### Krok 8 — Autor: Piotr Nowak
**Frontend — upload i lista paragonów**

Utwórz `frontend/src/js/api.js`:
- `const BASE = '/api'`
- `async function apiFetch(path, options)` — fetch wrapper,
  rzuca Error gdy response nie ok, parsuje JSON

Utwórz `frontend/src/upload.html` + `frontend/src/js/upload.js`:
- strefa drag & drop (`dragover`, `drop`, `change` na input[file])
- podgląd zdjęcia przed wysłaniem (`FileReader`)
- pasek postępu (`<progress>`) podczas uploadu
- po sukcesie: komunikat z nazwą sklepu i kwotą, link do listy
- obsługa błędów: alert z treścią błędu z API

Utwórz `frontend/src/receipts.html` + `frontend/src/js/receipts.js`:
- tabela z kolumnami: miniatura, sklep, data, kwota, kategorie, akcje
- miniatura: `<img src="/uploads/{image_path}">` 48x48px
- przycisk "szczegóły" → modal z listą pozycji i kategoriami
- przycisk "usuń" → `DELETE /api/receipts/{id}` + odświeżenie listy
- paginacja: przyciski Poprzednia / Następna

Utwórz `frontend/src/index.html`:
- nawigacja: Upload · Paragony · Dashboard
- przekierowanie na upload.html

Commit:
```
git commit --author="Piotr Nowak <piotr.nowak@student.pwr.edu.pl>" -m "feat: frontend upload drag&drop, receipts list with pagination"
```

---

### Krok 9 — Autor: Anna Kowalska
**Frontend — dashboard z Chart.js**

Utwórz `frontend/src/dashboard.html` + `frontend/src/js/dashboard.js`:

Ładuj Chart.js z CDN:
```html
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
```

Karty podsumowania (pobierz z `GET /api/dashboard/summary`):
- Łączne wydatki (total_spent formatowane jako PLN)
- Liczba paragonów (receipt_count)
- Największa kategoria (max z by_category)
- Wydatki w bieżącym miesiącu

Wykres 1 — Donut: wydatki per kategoria (`by_category`):
- kolory: Jedzenie=#7F77DD, Transport=#1D9E75, Dom=#D85A30,
  Zdrowie=#378ADD, Rozrywka=#BA7517, Inne=#888780
- legenda po prawej stronie

Wykres 2 — Bar: wydatki per miesiąc (`by_month`):
- ostatnie 6 miesięcy na osi X
- kolor słupków: #7F77DD
- oś Y zaczyna się od 0, etykiety w PLN

Obsługa stanu pustego (brak paragonów):
- komunikat "Brak danych — dodaj pierwszy paragon"
- ukryj wykresy, pokaż komunikat

Commit:
```
git commit --author="Anna Kowalska <anna.kowalska@student.pwr.edu.pl>" -m "feat: dashboard with Chart.js donut and bar charts, summary cards"
```

---

### Krok 10 — Autor: Anna Kowalska
**Dokumentacja i finalizacja**

Uzupełnij `README.md`:

```markdown
# Receipt Scanner

Aplikacja do skanowania i kategoryzowania paragonów.

## Wymagania
- Docker >= 24.0
- Docker Compose >= 2.0

## Uruchomienie
cp .env.example .env
make up
# aplikacja dostępna na http://localhost:80

## Migracje bazy danych
make migrate

## Testy
make test

## Struktura projektu
(wklej hierarchię katalogów)

## Technologie
(wklej tabelę stosu technologicznego)
```

Sprawdź że wszystkie pliki `__init__.py` istnieją.
Sprawdź że `docker-compose.yml` ma healthcheck dla MariaDB.
Sprawdź że `.env.example` ma wszystkie potrzebne zmienne.

Commit:
```
git commit --author="Anna Kowalska <anna.kowalska@student.pwr.edu.pl>" -m "docs: README with setup instructions, deployment guide, project structure"
```

---

## Zasady których Claude Code musi przestrzegać

1. **Jeden krok na raz** — zaimplementuj krok, wykonaj commit, czekaj na
   potwierdzenie użytkownika zanim przejdziesz dalej.

2. **Zawsze używaj --author** — każdy commit musi mieć jawny `--author`
   zgodnie z planem. Nigdy `git commit` bez tej flagi.

3. **Separacja warstw** — `api/` nie zawiera logiki biznesowej, tylko
   wywołuje serwisy. Serwisy w `services/` nie importują nic z `api/`.

4. **Obsługa błędów** — każdy endpoint zwraca sensowny HTTP status i
   komunikat JSON `{"detail": "..."}` przy błędzie.

5. **Nie używaj MinIO** — pliki przechowuj lokalnie w `UPLOAD_DIR`
   montowanym jako Docker volume.

6. **Nie implementuj autentykacji** — aplikacja jest single-user,
   brak JWT, brak tabeli users.

7. **pip + requirements.txt** — nie używaj poetry, uv ani conda.

8. **Testy nie wymagają Tesseract** — mockuj `pytesseract.image_to_string`
   w testach żeby działały w środowisku bez Tesseract.
