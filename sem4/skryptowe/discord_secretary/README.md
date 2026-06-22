# Discord Secretary Bot

Wirtualna sekretarka Discord — spotkania, przypomnienia, nagrania audio.
Bot discord.py i panel webowy FastAPI działają w jednym kontenerze, jako
jeden proces Python spięty przez `asyncio.gather`.

## Wymagania

- Docker >= 24.0 i Docker Compose >= 2.0
- Token bota Discord (patrz: [Jak uzyskać token](#jak-uzyskać-token))

## Szybki start

```bash
cp .env.example .env
# uzupełnij DISCORD_TOKEN i DISCORD_GUILD_ID w .env
make up
```

Panel webowy: http://0.0.0.0

## Komendy Discord

| Komenda          | Opis                                          |
|------------------|-----------------------------------------------|
| `/meeting create`| Zaplanuj spotkanie; opcjonalnie `role` + `minutes_before` (DM dla roli) |
| `/meeting list`  | Lista nadchodzących spotkań                   |
| `/meeting cancel`| Anuluj spotkanie po ID                        |
| `/remind set`    | Ustaw przypomnienie (dla usera lub roli)      |
| `/remind list`   | Lista przypomnień dla spotkania               |
| `/record start`  | Rozpocznij nagrywanie kanału **Stage**         |
| `/record stop`   | Zatrzymaj i zapisz nagranie                   |

Format daty w komendach: `2025-06-15 14:00`. Koniec spotkania jest opcjonalny
— gdy pominięty, przyjmowane jest 60 minut od startu.

> **Nagrywanie tylko na kanałach Stage.** Discord wymusza szyfrowanie
> end-to-end (DAVE) na zwykłych kanałach głosowych od marca 2026 i odbieranego
> audio nie da się odszyfrować w żadnej obecnej bibliotece. Kanały Stage są
> zwolnione z E2EE (broadcast), więc bot nagrywa wyłącznie je. Na zwykłym
> kanale `/record start` zwróci stosowny komunikat.

## Struktura projektu

```
discord-secretary/
├── main.py                 # asyncio.gather: bot + web + scheduler
├── config.py               # pydantic-settings, zmienne .env
├── bot/
│   ├── client.py           # instancja bota, intents
│   ├── cogs/               # /meeting, /remind, /record
│   └── scheduler.py        # APScheduler — wysyłka przypomnień (DM)
├── web/
│   ├── app.py              # FastAPI, routery, StaticFiles /audio
│   ├── routers/            # pages.py (HTML) + api.py (JSON)
│   └── templates/          # Bootstrap 5 (CDN)
├── services/               # logika biznesowa (bez Discord/FastAPI)
├── models/models.py        # SQLAlchemy ORM
├── schemas/schemas.py      # pydantic v2
├── db/session.py           # async engine, sesje
├── migrations/             # Alembic
└── tests/                  # pytest + pytest-asyncio + httpx
```

## Zmienne środowiskowe

| Zmienna           | Opis                       | Domyślnie                                |
|-------------------|----------------------------|------------------------------------------|
| `DISCORD_TOKEN`   | Token bota Discord         | —                                        |
| `DISCORD_GUILD_ID`| ID serwera Discord         | —                                        |
| `DATABASE_URL`    | URL bazy (async SQLite)    | `sqlite+aiosqlite:////data/secretary.db` |
| `AUDIO_DIR`       | Katalog na pliki `.ogg`    | `/data/audio`                            |
| `WEB_HOST`        | Host serwera webowego      | `0.0.0.0`                                |
| `WEB_PORT`        | Port serwera webowego      | `80`                                     |
| `SECRET_KEY`      | Klucz aplikacji            | `change_me`                              |

## Jak uzyskać token

1. Wejdź na https://discord.com/developers/applications i utwórz aplikację.
2. W zakładce **Bot** wygeneruj token i włącz **Message Content**,
   **Server Members** oraz **Voice** intents.
3. Zaproś bota na serwer z uprawnieniami do wysyłania wiadomości i łączenia
   się z kanałami głosowymi.

## Uruchomienie testów

```bash
make test
```

## Migracje bazy danych

```bash
make migrate   # alembic upgrade head
```
