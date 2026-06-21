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


def test_extract_total_missing_returns_none():
    text = "Chleb 4,50\nMleko 3,99\n"
    assert parser_service.extract_total(text) is None


def test_empty_text():
    result = parser_service.parse_receipt("")
    assert result["store_name"] is None
    assert result["date"] is None
    assert result["total_amount"] is None
    assert result["items"] == []
