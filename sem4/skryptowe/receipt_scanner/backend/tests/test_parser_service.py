from datetime import date
from decimal import Decimal

import pytest

from app.services import parser_service

BIEDRONKA = """BIEDRONKA
ul. Kwiatowa 5
2024-03-15
Chleb razowy 4,50
Mleko 3,2% 3,99
Maslo extra 7,49
SUMA PLN 15,98
"""

LIDL = """LIDL Sp. z o.o.
15.03.2024
Banany 5,20
Ser zolty 12,00
RAZEM 17,20
"""

# Realny układ kolumnowy (OCR PSM 4): nazwa PTU ilość x cena wartość
COLUMNAR = """(Ge Biedronka
Codziennie niskie ceny
Sklep 5805 DUBOIS 9
18.06.2026 21:34
NIEFISKALNY
Nazwa PTU Ilość Cena Wartość
ChustHigDelik150szt A 1.000 x 3,99 3,99
KaszkaNestleMore300 | 1.000 x 12,99 12,99
But Plastik kaucja brak 1.000 x 0,50 0,50
Duet Truskaw 94g Cc 2.000 x 1,79 3,58
Sprzedaż opodatkowana A 7,98
PTU A 23% 1,49
Suma PTU 2,63
Suma PLN 33,02
Karta płatnicza 33,02
"""


def test_parse_biedronka():
    result = parser_service.parse_receipt(BIEDRONKA)
    assert result["store_name"] == "BIEDRONKA"
    assert result["date"] == date(2024, 3, 15)
    assert result["total_amount"] == Decimal("15.98")
    assert len(result["items"]) == 3
    assert result["items"][0]["name"] == "Chleb razowy"
    assert result["items"][0]["amount"] == Decimal("4.50")


def test_parse_lidl():
    result = parser_service.parse_receipt(LIDL)
    assert result["store_name"] == "LIDL Sp. z o.o."
    assert result["date"] == date(2024, 3, 15)
    assert result["total_amount"] == Decimal("17.20")
    assert {"name": "Banany", "amount": Decimal("5.20")} in result["items"]


@pytest.mark.parametrize(
    "text,expected",
    [
        ("Data: 15.03.2024", date(2024, 3, 15)),
        ("2024-03-15", date(2024, 3, 15)),
        ("Zakup 15/03/2024 godz", date(2024, 3, 15)),
        ("15-03-2024", date(2024, 3, 15)),
        ("brak daty tutaj", None),
    ],
)
def test_extract_date_formats(text, expected):
    assert parser_service.extract_date(text) == expected


def test_parse_columnar_receipt():
    """Układ kolumnowy: pozycje z 'ilość x cena wartość', total mimo 'Suma PTU'."""
    result = parser_service.parse_receipt(COLUMNAR)
    # total to Suma PLN (33,02), a nie Suma PTU (2,63)
    assert result["total_amount"] == Decimal("33.02")
    # cztery realne pozycje, bez linii podsumowań/PTU/Sprzedaż
    assert len(result["items"]) == 4
    names = [it["name"] for it in result["items"]]
    assert "ChustHigDelik150szt" in names
    assert "But Plastik kaucja" in names          # odcięte "brak"
    assert "Duet Truskaw 94g" in names            # odcięte "Cc"
    assert {"name": "KaszkaNestleMore300", "amount": Decimal("12.99")} in result["items"]
    # nazwa sklepu bez śmieci z logo
    assert "Biedronka" in result["store_name"]


def test_extract_total_missing_returns_none():
    text = "Chleb 4,50\nMleko 3,99\n"
    assert parser_service.extract_total(text) is None


def test_empty_text():
    result = parser_service.parse_receipt("")
    assert result["store_name"] is None
    assert result["date"] is None
    assert result["total_amount"] is None
    assert result["items"] == []
