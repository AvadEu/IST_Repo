"""Serwis kategoryzacji — reguły słownikowe (etap 1) + fallback ML (etap 2)."""

from functools import lru_cache

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

DEFAULT_CATEGORY = "Inne"

# Słowa kluczowe rozpoznające markę sklepu (po nazwie sklepu)
STORE_KEYWORDS = {
    "Jedzenie": ["biedronka", "lidl", "aldi", "żabka", "zabka", "carrefour",
                 "kaufland", "netto", "tesco", "intermarche", "spar", "dino",
                 "stokrotka", "auchan"],
    "Transport": ["orlen", "bp", "shell", "lotos", "circle k", "moya", "amic"],
    "Dom": ["ikea", "leroy merlin", "obi", "castorama", "jysk",
            "media markt", "rtv euro agd"],
    "Zdrowie": ["apteka", "rossmann", "super-pharm", "dr max",
                "gemini", "hebe", "przychodnia"],
    "Rozrywka": ["cinema city", "multikino", "steam", "empik",
                 "allegro", "netflix", "spotify"],
}

# Słowa kluczowe rozpoznające typ produktu (po nazwie pozycji)
PRODUCT_KEYWORDS = {
    "Jedzenie": ["chleb", "bułk", "bulk", "mleko", "mięso", "mieso", "warzyw",
                 "owoc", "nabiał", "nabial", "ser", "jogurt", "masło", "maslo",
                 "jajk", "sok", "woda", "napój", "napoj", "kawa", "herbat",
                 "cukier", "makaron", "ryż", "ryz", "płatki", "platki", "kaszk",
                 "banan", "jabłk", "jablk", "pomidor", "kurczak", "szynk",
                 "parów", "parow", "czekolad", "kakao", "ketchup", "olej",
                 "truskaw", "marchew", "ziemniak", "pieczyw", "wędlin", "wedlin"],
    "Transport": ["paliwo", "benzyn", "diesel", "olej napęd", "parking",
                  "bilet", "mpk", "pkp", "pks", "autostrad", "myjni"],
    "Dom": ["chust", "higien", "papier", "ręcznik", "recznik", "proszek",
            "płyn", "plyn", "mydło", "mydlo", "szampon", "pasta", "worki",
            "ścier", "scier", "gąbk", "gabk", "żarówk", "zarowk", "bateri",
            "świec", "swiec", "chemia", "detergent"],
    "Zdrowie": ["leki", "tablet", "witamin", "syrop", "plaster", "maść",
                "masc", "krem", "opatrun", "apteczn"],
    "Rozrywka": ["książk", "ksiazk", "gra ", "gry ", "film", "płyta", "plyta",
                 "zabawk", "puzzle"],
}

# Stała kolejność kategorii — determinizm przy nakładających się słowach
_CATEGORY_ORDER = ["Jedzenie", "Transport", "Dom", "Zdrowie", "Rozrywka"]

# Zachowane dla zgodności: pełny słownik (sklepy + produkty) używany przez
# kategoryzację pojedynczej pozycji i nazwy sklepu.
CATEGORY_KEYWORDS = {
    category: STORE_KEYWORDS.get(category, []) + PRODUCT_KEYWORDS.get(category, [])
    for category in _CATEGORY_ORDER
}

# Mały zbiór treningowy dla fallbacku ML (min. 30 przykładów)
_TRAINING_DATA = [
    ("bułka pszenna", "Jedzenie"),
    ("jogurt naturalny", "Jedzenie"),
    ("ser gouda", "Jedzenie"),
    ("pomidory malinowe", "Jedzenie"),
    ("jabłka", "Jedzenie"),
    ("woda mineralna", "Jedzenie"),
    ("kurczak filet", "Jedzenie"),
    ("makaron spaghetti", "Jedzenie"),
    ("ryż basmati", "Jedzenie"),
    ("czekolada mleczna", "Jedzenie"),
    ("olej napędowy diesel", "Transport"),
    ("benzyna 95", "Transport"),
    ("opłata za autostradę", "Transport"),
    ("bilet miesięczny", "Transport"),
    ("przejazd taxi", "Transport"),
    ("myjnia samochodowa", "Transport"),
    ("żarówka led", "Dom"),
    ("farba ścienna biała", "Dom"),
    ("wkręty montażowe", "Dom"),
    ("ręcznik kuchenny", "Dom"),
    ("doniczka ceramiczna", "Dom"),
    ("proszek do prania", "Dom"),
    ("tabletki przeciwbólowe", "Zdrowie"),
    ("witamina c", "Zdrowie"),
    ("syrop na kaszel", "Zdrowie"),
    ("plaster opatrunkowy", "Zdrowie"),
    ("maść rozgrzewająca", "Zdrowie"),
    ("krem nawilżający", "Zdrowie"),
    ("bilet do kina", "Rozrywka"),
    ("gra planszowa", "Rozrywka"),
    ("książka kryminał", "Rozrywka"),
    ("subskrypcja muzyczna", "Rozrywka"),
    ("karta podarunkowa gra", "Rozrywka"),
]


@lru_cache(maxsize=1)
def _get_model() -> Pipeline:
    """Trenuje (raz) i zwraca pipeline TF-IDF + MultinomialNB."""
    texts = [text for text, _ in _TRAINING_DATA]
    labels = [label for _, label in _TRAINING_DATA]
    model = Pipeline([
        ("tfidf", TfidfVectorizer()),
        ("clf", MultinomialNB()),
    ])
    model.fit(texts, labels)
    return model


def _match_keywords(text: str, keyword_map: dict | None = None) -> str | None:
    """Zwraca kategorię, jeśli tekst zawiera któreś ze słów kluczowych."""
    if not text:
        return None
    keyword_map = keyword_map if keyword_map is not None else CATEGORY_KEYWORDS
    lowered = text.lower()
    for category, keywords in keyword_map.items():
        if any(keyword in lowered for keyword in keywords):
            return category
    return None


def categorize_item(item_name: str) -> str:
    """Kategoryzuje pojedynczą pozycję: słownik → ML fallback → 'Inne'."""
    if not item_name or not item_name.strip():
        return DEFAULT_CATEGORY

    matched = _match_keywords(item_name)
    if matched:
        return matched

    prediction = _get_model().predict([item_name])[0]
    return prediction or DEFAULT_CATEGORY


def categorize_receipt(store_name: str | None, items: list[dict]) -> list[dict]:
    """Kategoryzuje pozycje paragonu — priorytet ma treść pozycji, nie sklep.

    Kolejność decyzji dla każdej pozycji:
      1. słowo kluczowe produktu w nazwie pozycji (np. "sok" → Jedzenie),
      2. kategoria sklepu jako fallback (np. paragon z Biedronki → Jedzenie),
      3. fallback ML na nazwie pozycji,
      4. domyślnie "Inne".

    Dzięki temu pozycje takie jak chusteczki czy leki nie są hurtem
    klasyfikowane jako Jedzenie tylko dlatego, że paragon jest ze sklepu spożywczego.
    """
    store_category = _match_keywords(store_name, STORE_KEYWORDS) if store_name else None

    result: list[dict] = []
    for item in items:
        name = item.get("name", "")
        product_category = _match_keywords(name, PRODUCT_KEYWORDS)
        if product_category:
            category = product_category
        elif store_category:
            category = store_category
        else:
            category = categorize_item(name)
        result.append({**item, "category": category})
    return result
