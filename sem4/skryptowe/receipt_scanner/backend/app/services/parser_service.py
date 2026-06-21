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
_AMOUNT_RE = r"-?\d+[.,]\d{2}"

# Linie, które nie są pozycjami (podsumowania, nagłówki, stopka paragonu)
_NON_ITEM_KEYWORDS = [
    "SUMA", "RAZEM", "DO ZAPŁATY", "DO ZAPLATY", "TOTAL", "PTU",
    "SPRZEDAŻ", "SPRZEDAZ", "RABAT", "KARTA", "GOTÓWKA", "GOTOWKA",
    "RESZTA", "NUMER", "KASA", "NIP", "NIEFISKALNY", "FISKALNY",
    "NAZWA", "PARAGON",
]

# Strukturalny wzorzec pozycji: "... ilość[,.]xxx x cena wartość" (wartość na końcu)
_QTY_PRICE_RE = re.compile(
    r"\d+[.,]\d{3}\s*[xX*]\s*\d+[.,]\d{2}\s+(?P<amount>-?\d+[.,]\d{2})\s*$"
)

# Uproszczony wzorzec pozycji: nazwa + kwota na końcu linii (paragony bez kolumn)
_ITEM_RE = re.compile(r"^(?P<name>.+?)\s+(?P<amount>\d+[.,]\d{2})\s*[A-Za-z]?$")

# Końcowy symbol PTU / kaucji do odcięcia z nazwy (np. "A", "C", "Cc", "brak", "|")
_TRAILING_TAG_RE = re.compile(r"\s+([A-Za-z]{1,2}|brak|\|)$", re.IGNORECASE)

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
    """Pierwsza sensowna linia (min. 3 litery), po usunięciu śmieci OCR z brzegów."""
    for line in text.splitlines():
        stripped = line.strip()
        if sum(ch.isalpha() for ch in stripped) < 3:
            continue
        # usuń wiodące/końcowe znaki niealfanumeryczne (artefakty logo OCR)
        cleaned = re.sub(r"^[^0-9A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż]+", "", stripped)
        cleaned = cleaned.strip()
        if cleaned:
            return cleaned[:MAX_STORE_NAME_LEN]
    return None


def extract_total(text: str) -> Decimal | None:
    """Kwota końcowa: linie ze słowem kluczowym (z pominięciem PTU), bierzemy max."""
    candidates: list[Decimal] = []
    for line in text.splitlines():
        upper = line.upper()
        if "PTU" in upper:  # "Suma PTU" to nie jest kwota końcowa
            continue
        if any(keyword in upper for keyword in _TOTAL_KEYWORDS):
            for raw in re.findall(_AMOUNT_RE, line):
                value = _to_decimal(raw)
                if value is not None:
                    candidates.append(value)
    return max(candidates) if candidates else None


def _is_non_item(upper_line: str) -> bool:
    return any(keyword in upper_line for keyword in _NON_ITEM_KEYWORDS)


def extract_items(text: str) -> list[dict]:
    """Lista pozycji {name, amount}.

    Najpierw próbuje wykryć strukturę kolumnową (ilość x cena wartość). Jeśli
    paragon jej nie ma, stosuje uproszczony wzorzec "nazwa + kwota".
    """
    structured: list[dict] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        match = _QTY_PRICE_RE.search(stripped)
        if not match:
            continue
        amount = _to_decimal(match.group("amount"))
        name = stripped[: match.start()].strip()
        name = _TRAILING_TAG_RE.sub("", name).strip()
        if name and amount is not None:
            structured.append({"name": name, "amount": amount})

    if structured:
        return structured

    # Fallback dla paragonów bez kolumn (np. proste formaty)
    items: list[dict] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or _is_non_item(stripped.upper()):
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
