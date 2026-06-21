"""Serwis kategoryzacji — reguły słownikowe (etap 1) + fallback ML (etap 2)."""

from functools import lru_cache

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

DEFAULT_CATEGORY = "Inne"

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


def _match_keywords(text: str) -> str | None:
    """Zwraca kategorię, jeśli tekst zawiera któreś ze słów kluczowych."""
    lowered = text.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
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
    """Kategoryzuje pozycje paragonu.

    Jeśli sklep jest rozpoznany po słowach kluczowych → przypisz tę kategorię
    wszystkim pozycjom. W przeciwnym razie kategoryzuj każdą pozycję osobno.
    """
    store_category = _match_keywords(store_name) if store_name else None

    result: list[dict] = []
    for item in items:
        category = store_category or categorize_item(item.get("name", ""))
        result.append({**item, "category": category})
    return result
