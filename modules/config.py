# /modules/config.py
# Konfiguracja aplikacji Prometalle

# Ustawienia domyślne
DEFAULT_LANGUAGE = 'pl'   # Domyślny język: polski
DEFAULT_CURRENCY = 'EUR'  # Domyślna waluta: Euro
DEFAULT_UNIT = 'g'        # Domyślna jednostka: gramy

# Dostępne opcje
AVAILABLE_LANGUAGES = ['pl', 'en', 'de']
AVAILABLE_CURRENCIES = ['PLN', 'EUR', 'USD']
AVAILABLE_UNITS = ['g', 'oz']

# Etykiety językowe
LANGUAGE_LABELS = {
    "pl": "Polski",
    "en": "English",
    "de": "Deutsch"
}

# Roczne inflacje domyślne (jeśli brak danych w CSV)
DEFAULT_INFLATION = {
    'PLN': 0.06,    # 6% rocznie
    'EUR': 0.02,    # 2% rocznie
    'USD': 0.025    # 2,5% rocznie
}

# Przeliczniki jednostek
UNITS_CONVERSION = {
    'g_to_oz': 0.03215,      # gramy na uncje
    'oz_to_g': 31.1035       # uncje na gramy
}

# Kolory metali do wykresów
METAL_COLORS = {
    'Gold': '#FFD700',      # Złoto
    'Silver': '#C0C0C0',    # Srebro
    'Platinum': '#E5E4E2',  # Platyna
    'Palladium': '#8A8B8C'  # Pallad
}

# Domyślna alokacja metali
DEFAULT_ALLOCATION = {
    'gold': 40,      # 40% złoto
    'silver': 30,    # 30% srebro
    'platinum': 15,  # 15% platyna
    'palladium': 15  # 15% pallad
}

# Wagi metali dla wyliczenia indeksu zbiorczego
METAL_WEIGHTS = {
    'Gold': 0.60,      # 60% waga złota w indeksie
    'Silver': 0.20,    # 20% waga srebra
    'Platinum': 0.10,  # 10% waga platyny
    'Palladium': 0.10  # 10% waga palladu
}

# Domyślne koszty magazynowania dla różnych dostawców
DEFAULT_STORAGE_PROVIDERS = {
    'Provider A': 0.50,  # 0.50% rocznie
    'Provider B': 0.65,  # 0.65% rocznie
    'Provider C': 0.40,  # 0.40% rocznie, ale tylko dla złota
    'Provider D': 0.75   # 0.75% rocznie, ale bez minimalnej opłaty
}

# Domyślne marże sprzedaży i kupna dla różnych metali
DEFAULT_MARGINS = {
    'Gold': {
        'buy': 2.0,   # 2.0% marża przy zakupie
        'sell': 1.5   # 1.5% marża przy sprzedaży
    },
    'Silver': {
        'buy': 3.0,   # 3.0% marża przy zakupie
        'sell': 2.0   # 2.0% marża przy sprzedaży
    },
    'Platinum': {
        'buy': 4.0,   # 4.0% marża przy zakupie
        'sell': 3.0   # 3.0% marża przy sprzedaży
    },
    'Palladium': {
        'buy': 5.0,   # 5.0% marża przy zakupie
        'sell': 4.0   # 4.0% marża przy sprzedaży
    }
}

# Historyczne wydarzenia na wykresach
HISTORICAL_EVENTS = {
    '2008-09-15': 'Upadek Lehman Brothers',
    '2011-08-22': 'Szczyt ceny złota',
    '2020-03-23': 'Krach COVID-19',
    '2022-02-24': 'Inwazja Rosji na Ukrainę'
}

# Predefiniowane strategie inwestycyjne
INVESTMENT_STRATEGIES = {
    'Standardowa': {
        'gold': 40,
        'silver': 30,
        'platinum': 15,
        'palladium': 15
    },
    'Bezpieczna': {
        'gold': 70,
        'silver': 20,
        'platinum': 5,
        'palladium': 5
    },
    'Agresywna': {
        'gold': 20,
        'silver': 30,
        'platinum': 25,
        'palladium': 25
    },
    'Tylko złoto': {
        'gold': 100,
        'silver': 0,
        'platinum': 0,
        'palladium': 0
    },
    'Przemysłowa': {
        'gold': 10,
        'silver': 40,
        'platinum': 25,
        'palladium': 25
    }
}

# Ustawienia aplikacji
APP_SETTINGS = {
    'charts_theme': 'plotly_white',
    'cache_expiry_hours': 24,
    'max_forecast_years': 30,
    'debug_mode': False,
    'show_experimental': False
}

# Ścieżki do plików danych
DATA_PATHS = {
    'metal_prices': 'data/metal_prices.csv',
    'exchange_rates': 'data/exchange_rates.csv',
    'inflation_rates': 'data/inflation_rates_ready.csv'
}

# Funkcje pomocnicze
def get_metal_price_column(metal_name: str, currency: str = 'EUR') -> str:
    """
    Zwraca nazwę kolumny z ceną danego metalu w zależności od waluty.
    
    Args:
        metal_name: Nazwa metalu (gold, silver, platinum, palladium)
        currency: Waluta (EUR, USD, PLN)
        
    Returns:
        Nazwa kolumny w DataFrame
    """
    metal_name = metal_name.lower()
    
    if metal_name in ['gold', 'złoto']:
        base_name = 'Gold'
    elif metal_name in ['silver', 'srebro']:
        base_name = 'Silver'
    elif metal_name in ['platinum', 'platyna']:
        base_name = 'Platinum'
    elif metal_name in ['palladium', 'pallad']:
        base_name = 'Palladium'
    else:
        return None
    
    # W zależności od waluty dodajemy sufiks
    if currency == 'EUR':
        return base_name
    else:
        return f"{base_name}_{currency}"

def convert_unit(value: float, from_unit: str, to_unit: str) -> float:
    """
    Konwertuje wartość między jednostkami (g <-> oz).
    
    Args:
        value: Wartość do konwersji
        from_unit: Jednostka źródłowa ('g' lub 'oz')
        to_unit: Jednostka docelowa ('g' lub 'oz')
        
    Returns:
        Skonwertowana wartość
    """
    if from_unit == to_unit:
        return value
    
    if from_unit == 'g' and to_unit == 'oz':
        return value * UNITS_CONVERSION['g_to_oz']
    elif from_unit == 'oz' and to_unit == 'g':
        return value * UNITS_CONVERSION['oz_to_g']
    else:
        # Nieznane jednostki, zwracamy oryginalną wartość
        return value
