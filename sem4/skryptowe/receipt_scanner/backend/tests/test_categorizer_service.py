from decimal import Decimal

from app.services import categorizer_service


def test_categorize_by_store_name():
    """Rozpoznany sklep przypisuje swoją kategorię wszystkim pozycjom."""
    items = [
        {"name": "jakiś dziwny produkt xyz", "amount": Decimal("4.50")},
        {"name": "inny nieznany towar", "amount": Decimal("2.00")},
    ]
    result = categorizer_service.categorize_receipt("Biedronka", items)
    assert all(item["category"] == "Jedzenie" for item in result)


def test_categorize_item_keyword():
    assert categorizer_service.categorize_item("Apteka DOZ leki") == "Zdrowie"


def test_categorize_item_ml_fallback():
    """Nieznany sklep/produkt → klasyfikacja ML zwraca jedną ze znanych kategorii."""
    category = categorizer_service.categorize_item("filet z kurczaka świeży")
    assert category in {
        "Jedzenie", "Transport", "Dom", "Zdrowie", "Rozrywka",
    }


def test_case_insensitive():
    assert categorizer_service.categorize_item("ORLEN PALIWO") == "Transport"
    assert categorizer_service.categorize_item("orlen paliwo") == "Transport"


def test_default_category_for_empty():
    assert categorizer_service.categorize_item("") == "Inne"
    assert categorizer_service.categorize_item("   ") == "Inne"


def test_categorize_receipt_unknown_store_per_item():
    """Nierozpoznany sklep → każda pozycja kategoryzowana osobno."""
    items = [
        {"name": "orlen paliwo", "amount": Decimal("200.00")},
        {"name": "apteka leki", "amount": Decimal("30.00")},
    ]
    result = categorizer_service.categorize_receipt("Sklep Janusz 24h", items)
    categories = {item["category"] for item in result}
    assert "Transport" in categories
    assert "Zdrowie" in categories
