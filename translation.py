# /prometalle_app/app/core/translation.py

# Obsługa tłumaczeń aplikacji Prometalle

TRANSLATIONS = {
    "welcome": {
        "pl": "Witaj w Prometalle!",
        "en": "Welcome to Prometalle!",
        "de": "Willkommen bei Prometalle!"
    },
    "choose_language": {
        "pl": "Wybierz język",
        "en": "Choose language",
        "de": "Sprache wählen"
    },
    "choose_currency": {
        "pl": "Wybierz walutę",
        "en": "Choose currency",
        "de": "Währung wählen"
    },
    "choose_unit": {
        "pl": "Wybierz jednostkę wagi",
        "en": "Choose weight unit",
        "de": "Gewichtseinheit wählen"
    },
    "continue": {
        "pl": "Kontynuuj",
        "en": "Continue",
        "de": "Weiter"
    }
}

def translate(key: str, language: str = DEFAULT_LANGUAGE) -> str:
    """Zwraca tłumaczenie danego klucza w wybranym języku."""
    return TRANSLATIONS.get(key, {}).get(language, key)
