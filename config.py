# /prometalle_app/app/core/config.py

# Konfiguracja podstawowa aplikacji Prometalle

DEFAULT_LANGUAGE = 'pl'   # Domyślny język: polski
DEFAULT_CURRENCY = 'EUR'  # Domyślna waluta: Euro
DEFAULT_UNIT = 'g'        # Domyślna jednostka: gramy

# Dostępne opcje
AVAILABLE_LANGUAGES = ['pl', 'en', 'de']
AVAILABLE_CURRENCIES = ['PLN', 'EUR', 'USD']
AVAILABLE_UNITS = ['g', 'oz']

# Roczne inflacje domyślne (jeśli brak danych w CSV)
DEFAULT_INFLATION = {
    'PLN': 0.06,    # 6% rocznie
    'EUR': 0.02,    # 2% rocznie
    'USD': 0.025    # 2,5% rocznie
}

# Przelicznik jednostek
GRAMS_PER_OUNCE = 31.1035
