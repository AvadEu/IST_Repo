"""Serwis parsowania — ekstrakcja danych paragonu z surowego tekstu OCR."""

import re
from datetime import date, datetime
from decimal import Decimal, InvalidOperation

# Formaty dat: DD.MM.YYYY, DD/MM/YYYY, DD-MM-YYYY oraz YYYY-MM-DD
_DATE_PATTERNS = [
    (re.compile(r"\b(\d{4})-(\d{2})-(\d{2})\b"), "%Y-%m-%d"),
    (re.compile(r"\b(\d{2})[.\-/](\d{2})[.\-/](\d{4})\b"), "%d-%m-%Y"),
]

# Słowa kluczowe oznaczające kwotę końcową
_TOTAL_KEYWORDS = ["DO ZAPŁATY", "SUMA", "RAZEM", "TOTAL", "DO ZAPLATY"]
_AMOUNT_RE = r"(\d+[.,]\d{2})"

# Linia pozycji: nazwa + kwota na końcu linii
_ITEM_RE = re.compile(r"^(?P<name>.+?)\s+(?P<amount>\d+[.,]\d{2})\s*[A-Za-z]?$")

MAX_STORE_NAME_LEN = 60


def _to_decimal(raw: str) -> Decimal | None:
    try:
        return Decimal(raw.replace(",", ".").replace(" ", ""))
    except (InvalidOperation, AttributeError):
        return None


def extract_date(text: str) -> date | None:
    """Zwraca pierwszą rozpoznaną datę lub None."""
    for pattern, fmt in _DATE_PATTERNS:
        match = pattern.search(text)
        if match:
            if fmt == "%Y-%m-%d":
                candidate = "-".join(match.groups())
            else:
                candidate = "-".join(match.groups())
            try:
                return datetime.strptime(candidate, fmt).date()
            except ValueError:
                continue
    return None


def extract_store_name(text: str) -> str | None:
    """Pierwsza niepusta linia tekstu, przycięta do MAX_STORE_NAME_LEN znaków."""
    for line in text.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped[:MAX_STORE_NAME_LEN]
    return None


def extract_total(text: str) -> Decimal | None:
    """Szuka kwoty przy słowach kluczowych (SUMA/RAZEM/DO ZAPŁATY/TOTAL)."""
    for line in text.splitlines():
        upper = line.upper()
        if any(keyword in upper for keyword in _TOTAL_KEYWORDS):
            amounts = re.findall(_AMOUNT_RE, line)
            if amounts:
                return _to_decimal(amounts[-1])
    return None


def extract_items(text: str) -> list[dict]:
    """Lista pozycji {name, amount} z linii pasujących do wzorca nazwa + kwota."""
    items: list[dict] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        upper = stripped.upper()
        # pomiń linie podsumowania
        if any(keyword in upper for keyword in _TOTAL_KEYWORDS):
            continue
        match = _ITEM_RE.match(stripped)
        if match:
            amount = _to_decimal(match.group("amount"))
            name = match.group("name").strip()
            if name and amount is not None:
                items.append({"name": name, "amount": amount})
    return items


def parse_receipt(text: str) -> dict:
    """Parsuje surowy tekst paragonu do struktury słownikowej."""
    return {
        "store_name": extract_store_name(text),
        "date": extract_date(text),
        "total_amount": extract_total(text),
        "items": extract_items(text),
    }
