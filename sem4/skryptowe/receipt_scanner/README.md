# Receipt Scanner

Aplikacja webowa do skanowania i kategoryzowania paragonów. Użytkownik wrzuca
zdjęcie paragonu (drag & drop), system wykonuje OCR (Tesseract), wyciąga dane
(sklep, data, kwoty, pozycje), kategoryzuje wydatki i zapisuje do bazy.
Dashboard prezentuje podsumowanie wydatków na wykresach Chart.js.

## Wymagania

- Docker >= 24.0
- Docker Compose >= 2.0

## Uruchomienie

```bash
cp .env.example .env
make up
# aplikacja dostępna na http://localhost:80
```

Po uruchomieniu zastosuj migracje bazy danych:

```bash
make migrate
```

## Migracje bazy danych

```bash
make migrate     # alembic upgrade head wewnątrz kontenera backend
```

## Testy

```bash
make test        # pytest wewnątrz kontenera backend
```

Testy nie wymagają zainstalowanego Tesseracta — wywołania `pytesseract` są
mockowane.

## Endpointy API

| Metoda | Ścieżka | Opis |
|---|---|---|
| POST | `/api/receipts/upload` | upload zdjęcia paragonu (JPEG/PNG, max 10 MB) |
| GET | `/api/receipts` | lista paragonów (paginacja `skip`, `limit`) |
| GET | `/api/receipts/{id}` | szczegóły paragonu z pozycjami |
| DELETE | `/api/receipts/{id}` | usunięcie paragonu i pliku |
| GET | `/api/dashboard/summary` | podsumowanie wydatków |

Dokumentacja interaktywna (Swagger): `http://localhost/api/docs` *(po stronie
backendu pod `/docs`).*

## Struktura projektu

```
receipt-scanner/
├── docker-compose.yaml
├── .env.example
├── Makefile
├── README.md
├── CLAUDE.md
│
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── pytest.ini
│   ├── alembic.ini
│   ├── app/
│   │   ├── main.py               # FastAPI app, CORS, mount /uploads
│   │   ├── config.py             # pydantic-settings (.env)
│   │   ├── api/
│   │   │   ├── receipts.py       # endpointy paragonów
│   │   │   └── dashboard.py      # endpoint podsumowania
│   │   ├── services/
│   │   │   ├── ocr_service.py
│   │   │   ├── parser_service.py
│   │   │   └── categorizer_service.py
│   │   ├── models/
│   │   │   └── receipt.py        # Receipt + ReceiptItem ORM
│   │   ├── schemas/
│   │   │   └── receipt.py        # pydantic schemas
│   │   └── db/
│   │       └── session.py        # engine, SessionLocal, get_db()
│   ├── migrations/               # Alembic
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
        ├── css/style.css
        └── js/
            ├── api.js
            ├── upload.js
            ├── receipts.js
            └── dashboard.js
```

## Technologie

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

## Architektura

Trzy kontenery: **frontend** (nginx, pliki statyczne + proxy `/api`),
**backend** (FastAPI/uvicorn z pipeline OCR → parser → kategoryzacja),
**mariadb** (baza). Zdjęcia paragonów przechowywane na woluminie Docker
`uploads_data` montowanym jako `UPLOAD_DIR`.

Separacja warstw: `api/` wywołuje serwisy z `services/`, serwisy nie zależą
od warstwy `api/`. Walidacja danych wejściowych/wyjściowych przez pydantic v2.
