from decimal import Decimal

from app.services import categorizer_service


def test_categorize_by_store_name():
    """Nierozpoznane pozycje dziedziczą kategorię sklepu."""
    items = [
        {"name": "jakiś dziwny produkt xyz", "amount": Decimal("4.50")},
        {"name": "inny nieznany towar", "amount": Decimal("2.00")},
    ]
    result = categorizer_service.categorize_receipt("Biedronka", items)
    assert all(item["category"] == "Jedzenie" for item in result)


def test_item_category_overrides_store():
    """Pozycja rozpoznana po nazwie NIE jest hurtem klasyfikowana jak sklep."""
    items = [
        {"name": "ChustHigDelik 150szt", "amount": Decimal("3.99")},  # higiena → Dom
        {"name": "Sok jabłkowy 1l", "amount": Decimal("4.99")},        # → Jedzenie
        {"name": "Paracetamol tabletki", "amount": Decimal("8.00")},   # leki → Zdrowie
        {"name": "nieznany xyz", "amount": Decimal("1.00")},           # → sklep (Jedzenie)
    ]
    result = categorizer_service.categorize_receipt("Biedronka", items)
    cats = [it["category"] for it in result]
    assert cats == ["Dom", "Jedzenie", "Zdrowie", "Jedzenie"]
    # kluczowe: nie wszystko jest Jedzeniem
    assert len(set(cats)) > 1


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
