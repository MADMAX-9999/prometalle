# /modules/translation.py
# Moduł tłumaczeń dla aplikacji Prometalle

from modules.config import DEFAULT_LANGUAGE

# Słownik tłumaczeń
TRANSLATIONS = {
    # Ogólne ustawienia
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
    
    # Sekcje konfiguracji
    "general_settings": {
        "pl": "Ustawienia ogólne",
        "en": "General settings",
        "de": "Allgemeine Einstellungen"
    },
    "simulation_settings": {
        "pl": "Ustawienia symulacji",
        "en": "Simulation settings",
        "de": "Simulationseinstellungen"
    },
    "allocation_settings": {
        "pl": "Ustawienia alokacji kapitału",
        "en": "Capital allocation settings",
        "de": "Kapitalallokationseinstellungen"
    },
    
    # Kwoty inwestycji
    "start_amount": {
        "pl": "Kwota początkowa inwestycji",
        "en": "Initial investment amount",
        "de": "Anfangsinvestition"
    },
    "recurring_amount": {
        "pl": "Kwota zakupu systematycznego",
        "en": "Recurring purchase amount",
        "de": "Regelmäßiger Kaufbetrag"
    },
    
    # Częstotliwości zakupów
    "frequency": {
        "pl": "Częstotliwość zakupów",
        "en": "Purchase frequency",
        "de": "Kaufhäufigkeit"
    },
    "purchase_day_weekly": {
        "pl": "Dzień tygodnia zakupu (0=Poniedziałek, ..., 4=Piątek)",
        "en": "Day of the week to purchase (0=Monday, ..., 4=Friday)",
        "de": "Wochentag des Kaufs (0=Montag, ..., 4=Freitag)"
    },
    "purchase_day_monthly": {
        "pl": "Dzień miesiąca zakupu (1-28)",
        "en": "Day of the month to purchase (1-28)",
        "de": "Kauftag des Monats (1-28)"
    },
    "purchase_day_quarterly": {
        "pl": "Dzień kwartału zakupu (1-90)",
        "en": "Day of the quarter to purchase (1-90)",
        "de": "Kauftag des Quartals (1-90)"
    },
    
    # Daty
    "start_date": {
        "pl": "Data rozpoczęcia inwestycji",
        "en": "Investment start date",
        "de": "Anfangsdatum der Investition"
    },
    "end_date": {
        "pl": "Data zakończenia inwestycji",
        "en": "Investment end date",
        "de": "Enddatum der Investition"
    },
    
    # Alokacja
    "total_allocation": {
        "pl": "Łączna alokacja",
        "en": "Total allocation",
        "de": "Gesamtallokation"
    },
    "allocation_error": {
        "pl": "⚠️ Łączna alokacja musi wynosić 100%!",
        "en": "⚠️ Total allocation must be 100%!",
        "de": "⚠️ Die Gesamtallokation muss 100% betragen!"
    },
    
    # Zakupy systematyczne
    "recurring_purchase_settings": {
        "pl": "Ustawienia zakupów systematycznych",
        "en": "Recurring purchase settings",
        "de": "Einstellungen für regelmäßige Käufe"
    },
    "one_time": {
        "pl": "Jednorazowy",
        "en": "One-time",
        "de": "Einmalig"
    },
    "weekly": {
        "pl": "Co tydzień",
        "en": "Weekly",
        "de": "Wöchentlich"
    },
    "monthly": {
        "pl": "Co miesiąc",
        "en": "Monthly",
        "de": "Monatlich"
    },
    "quarterly": {
        "pl": "Co kwartał",
        "en": "Quarterly",
        "de": "Vierteljährlich"
    },
    
    # Koszty magazynowe
    "storage_cost_settings": {
        "pl": "Koszty magazynowe",
        "en": "Storage cost settings",
        "de": "Lagerkosteneinstellungen"
    },
    "storage_base": {
        "pl": "Podstawa naliczania kosztu",
        "en": "Storage cost base",
        "de": "Berechnungsgrundlage Lagerkosten"
    },
    "storage_frequency": {
        "pl": "Częstotliwość naliczania",
        "en": "Storage frequency",
        "de": "Häufigkeit der Lagerkosten"
    },
    "storage_rate": {
        "pl": "Stawka magazynowania (%)",
        "en": "Storage rate (%)",
        "de": "Lagerkostensatz (%)"
    },
    "vat_rate": {
        "pl": "Stawka VAT (%)",
        "en": "VAT rate (%)",
        "de": "Mehrwertsteuersatz (%)"
    },
    "cover_method": {
        "pl": "Pokrycie kosztów magazynowych",
        "en": "Storage cost coverage",
        "de": "Deckung der Lagerkosten"
    },
    
    # Sposoby pokrycia kosztów
    "cash": {
        "pl": "Gotówka",
        "en": "Cash",
        "de": "Bargeld"
    },
    "gold": {
        "pl": "Złoto",
        "en": "Gold",
        "de": "Gold"
    },
    "silver": {
        "pl": "Srebro",
        "en": "Silver",
        "de": "Silber"
    },
    "platinum": {
        "pl": "Platyna",
        "en": "Platinum",
        "de": "Platin"
    },
    "palladium": {
        "pl": "Pallad",
        "en": "Palladium",
        "de": "Palladium"
    },
    "all_metals": {
        "pl": "Wszystkie metale",
        "en": "All metals",
        "de": "Alle Metalle"
    },
    
    # Marże
    "margin_settings": {
        "pl": "Marże i koszty transakcyjne",
        "en": "Margins and Transaction Costs",
        "de": "Margen und Transaktionskosten"
    },
    "purchase_margin": {
        "pl": "Marża przy zakupie (%)",
        "en": "Purchase Margin (%)",
        "de": "Kaufmarge (%)"
    },
    "sale_margin": {
        "pl": "Marża przy sprzedaży (%)",
        "en": "Sale Margin (%)",
        "de": "Verkaufsmarge (%)"
    },
    
    # Przyciski akcji
    "start_simulation": {
        "pl": "Rozpocznij symulację",
        "en": "Start simulation",
        "de": "Simulation starten"
    },
    "reset_simulation": {
        "pl": "Resetuj symulację",
        "en": "Reset simulation",
        "de": "Simulation zurücksetzen"
    },
    "export_data": {
        "pl": "Eksportuj dane",
        "en": "Export data",
        "de": "Daten exportieren"
    },
    "generate_report": {
        "pl": "Generuj raport",
        "en": "Generate report",
        "de": "Bericht erstellen"
    },
    
    # Wyniki symulacji
    "transaction_register": {
        "pl": "Rejestr operacji",
        "en": "Transaction Register",
        "de": "Transaktionsregister"
    },
    "portfolio_summary": {
        "pl": "Podsumowanie portfela",
        "en": "Portfolio summary",
        "de": "Portfoliozusammenfassung"
    },
    "storage_costs": {
        "pl": "Łączne koszty magazynowania",
        "en": "Total storage costs",
        "de": "Gesamte Lagerkosten"
    },
    "portfolio_chart": {
        "pl": "Wykres wartości portfela",
        "en": "Portfolio value chart",
        "de": "Wertdiagramm des Portfolios"
    },
    "purchase_schedule": {
        "pl": "Harmonogram zakupów",
        "en": "Purchase schedule",
        "de": "Kaufplan"
    },
    
    # Metryki portfela
    "portfolio_value": {
        "pl": "Wartość portfela",
        "en": "Portfolio value",
        "de": "Portfoliowert"
    },
    "invested_amount": {
        "pl": "Zainwestowana kwota",
        "en": "Invested amount",
        "de": "Investierter Betrag"
    },
    "return_on_investment": {
        "pl": "Stopa zwrotu",
        "en": "Return on investment",
        "de": "Anlagerendite"
    },
    "annualized_return": {
        "pl": "Roczna stopa zwrotu",
        "en": "Annualized return",
        "de": "Jährliche Rendite"
    },
    
    # Komunikaty o błędach
    "error_loading_data": {
        "pl": "Błąd ładowania danych",
        "en": "Error loading data",
        "de": "Fehler beim Laden der Daten"
    },
    "no_data_to_display": {
        "pl": "Brak danych do wyświetlenia",
        "en": "No data to display",
        "de": "Keine Daten zum Anzeigen"
    },
    
    # Zakładki wyników
    "visualizations_tab": {
        "pl": "Wizualizacje",
        "en": "Visualizations",
        "de": "Visualisierungen"
    },
    "transaction_register_tab": {
        "pl": "Rejestr operacji",
        "en": "Transaction Register",
        "de": "Transaktionsregister"
    },
    "portfolio_summary_tab": {
        "pl": "Podsumowanie portfela",
        "en": "Portfolio Summary",
        "de": "Portfolioübersicht"
    },
    "purchase_schedule_tab": {
        "pl": "Harmonogram zakupów",
        "en": "Purchase Schedule",
        "de": "Kaufplan"
    },
    
    # Strona startowa
    "welcome_message": {
        "pl": "Witaj w Prometalle",
        "en": "Welcome to Prometalle",
        "de": "Willkommen bei Prometalle"
    },
    "app_description": {
        "pl": "Inteligentny symulator inwestycji w metale szlachetne",
        "en": "Intelligent precious metals investment simulator",
        "de": "Intelligenter Simulator für Investitionen in Edelmetalle"
    },
    "main_features": {
        "pl": "Główne funkcje",
        "en": "Main features",
        "de": "Hauptfunktionen"
    },
    
    # Jednostki metali
    "grams": {
        "pl": "Gramy (g)",
        "en": "Grams (g)",
        "de": "Gramm (g)"
    },
    "ounces": {
        "pl": "Uncje (oz)",
        "en": "Ounces (oz)",
        "de": "Unzen (oz)"
    },
    
    # Podstawy naliczania kosztów magazynowania
    "value_base": {
        "pl": "Wartość metali",
        "en": "Metal value",
        "de": "Metallwert"
    },
    "invested_amount_base": {
        "pl": "Zainwestowana kwota",
        "en": "Invested amount",
        "de": "Investierter Betrag"
    },
    
    # Zaawansowane funkcje
    "advanced_settings": {
        "pl": "Ustawienia zaawansowane",
        "en": "Advanced settings",
        "de": "Erweiterte Einstellungen"
    },
    "compare_with_other_assets": {
        "pl": "Porównaj z innymi aktywami",
        "en": "Compare with other assets",
        "de": "Vergleich mit anderen Anlagen"
    },
    "rebalancing_simulation": {
        "pl": "Symulacja rebalancingu",
        "en": "Rebalancing simulation",
        "de": "Rebalancing-Simulation"
    },
    "tax_implications": {
        "pl": "Implikacje podatkowe",
        "en": "Tax implications",
        "de": "Steuerliche Auswirkungen"
    },
    
    # Stopka
    "footer_disclaimer": {
        "pl": "Prometalle - Symulator inwestycji w metale szlachetne. Symulacja nie stanowi porady inwestycyjnej.",
        "en": "Prometalle - Precious metals investment simulator. Simulation does not constitute investment advice.",
        "de": "Prometalle - Simulator für Investitionen in Edelmetalle. Die Simulation stellt keine Anlageberatung dar."
    }
}

def translate(key: str, language: str = DEFAULT_LANGUAGE) -> str:
    """
    Zwraca tłumaczenie danego klucza w wybranym języku.
    
    Args:
        key: Klucz tłumaczenia.
        language: Kod języka ('pl', 'en', 'de').
        
    Returns:
        Przetłumaczony tekst lub klucz, jeśli brak tłumaczenia.
    """
    # Sprawdzamy, czy klucz istnieje w słowniku tłumaczeń
    if key in TRANSLATIONS:
        # Sprawdzamy, czy język istnieje dla danego klucza
        if language in TRANSLATIONS[key]:
            return TRANSLATIONS[key][language]
        # Jeśli nie ma tłumaczenia dla wybranego języka, używamy angielskiego
        elif 'en' in TRANSLATIONS[key]:
            return TRANSLATIONS[key]['en']
    
    # Jeśli nie znaleziono tłumaczenia, zwracamy oryginalny klucz
    return key

def get_all_translations(language: str = DEFAULT_LANGUAGE) -> dict:
    """
    Zwraca wszystkie tłumaczenia dla wybranego języka.
    
    Args:
        language: Kod języka ('pl', 'en', 'de').
        
    Returns:
        Słownik z wszystkimi tłumaczeniami dla wybranego języka.
    """
    translations = {}
    
    for key, translations_dict in TRANSLATIONS.items():
        if language in translations_dict:
            translations[key] = translations_dict[language]
        elif 'en' in translations_dict:
            # Jeśli nie ma tłumaczenia dla wybranego języka, używamy angielskiego
            translations[key] = translations_dict['en']
    
    return translations

def translate_metal_name(metal_name: str, language: str = DEFAULT_LANGUAGE) -> str:
    """
    Tłumaczy nazwę metalu na wybrany język.
    
    Args:
        metal_name: Nazwa metalu w dowolnym języku lub formacie.
        language: Kod języka docelowego ('pl', 'en', 'de').
        
    Returns:
        Przetłumaczona nazwa metalu.
    """
    # Normalizacja nazwy metalu
    metal_name_lower = metal_name.lower()
    
    # Słownik tłumaczeń nazw metali
    metal_translations = {
        # Złoto
        'gold': {'pl': 'Złoto', 'en': 'Gold', 'de': 'Gold'},
        'złoto': {'pl': 'Złoto', 'en': 'Gold', 'de': 'Gold'},
        'gold_eur': {'pl': 'Złoto', 'en': 'Gold', 'de': 'Gold'},
        
        # Srebro
        'silver': {'pl': 'Srebro', 'en': 'Silver', 'de': 'Silber'},
        'srebro': {'pl': 'Srebro', 'en': 'Silver', 'de': 'Silber'},
        'silver_eur': {'pl': 'Srebro', 'en': 'Silver', 'de': 'Silber'},
        
        # Platyna
        'platinum': {'pl': 'Platyna', 'en': 'Platinum', 'de': 'Platin'},
        'platyna': {'pl': 'Platyna', 'en': 'Platinum', 'de': 'Platin'},
        'platinum_eur': {'pl': 'Platyna', 'en': 'Platinum', 'de': 'Platin'},
        
        # Pallad
        'palladium': {'pl': 'Pallad', 'en': 'Palladium', 'de': 'Palladium'},
        'pallad': {'pl': 'Pallad', 'en': 'Palladium', 'de': 'Palladium'},
        'palladium_eur': {'pl': 'Pallad', 'en': 'Palladium', 'de': 'Palladium'}
    }
    
    # Sprawdzamy, czy nazwa metalu istnieje w słowniku
    if metal_name_lower in metal_translations:
        # Sprawdzamy, czy język istnieje dla danej nazwy metalu
        if language in metal_translations[metal_name_lower]:
            return metal_translations[metal_name_lower][language]
        # Jeśli nie ma tłumaczenia dla wybranego języka, używamy angielskiego
        elif 'en' in metal_translations[metal_name_lower]:
            return metal_translations[metal_name_lower]['en']
    
    # Jeśli nie znaleziono tłumaczenia, zwracamy oryginalną nazwę z dużą pierwszą literą
    return metal_name.capitalize()

def get_weekday_name(day_number: int, language: str = DEFAULT_LANGUAGE) -> str:
    """
    Zwraca nazwę dnia tygodnia dla danego numeru (0=poniedziałek, 6=niedziela).
    
    Args:
        day_number: Numer dnia tygodnia (0-6).
        language: Kod języka ('pl', 'en', 'de').
        
    Returns:
        Nazwa dnia tygodnia w wybranym języku.
    """
    weekdays = {
        'pl': ['Poniedziałek', 'Wtorek', 'Środa', 'Czwartek', 'Piątek', 'Sobota', 'Niedziela'],
        'en': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        'de': ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']
    }
    
    # Sprawdzamy, czy numer dnia jest prawidłowy
    if 0 <= day_number <= 6:
        # Sprawdzamy, czy język istnieje
        if language in weekdays:
            return weekdays[language][day_number]
        # Jeśli nie ma tłumaczenia dla wybranego języka, używamy angielskiego
        else:
            return weekdays['en'][day_number]
    
    # Jeśli numer dnia jest nieprawidłowy, zwracamy pusty string
    return ""

def get_month_name(month_number: int, language: str = DEFAULT_LANGUAGE) -> str:
    """
    Zwraca nazwę miesiąca dla danego numeru (1=styczeń, 12=grudzień).
    
    Args:
        month_number: Numer miesiąca (1-12).
        language: Kod języka ('pl', 'en', 'de').
        
    Returns:
        Nazwa miesiąca w wybranym języku.
    """
    months = {
        'pl': ['Styczeń', 'Luty', 'Marzec', 'Kwiecień', 'Maj', 'Czerwiec', 'Lipiec', 'Sierpień', 'Wrzesień', 'Październik', 'Listopad', 'Grudzień'],
        'en': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
        'de': ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']
    }
    
    # Sprawdzamy, czy numer miesiąca jest prawidłowy
    if 1 <= month_number <= 12:
        # Sprawdzamy, czy język istnieje
        if language in months:
            return months[language][month_number - 1]  # -1, bo indeksowanie od 0
        # Jeśli nie ma tłumaczenia dla wybranego języka, używamy angielskiego
        else:
            return months['en'][month_number - 1]
    
    # Jeśli numer miesiąca jest nieprawidłowy, zwracamy pusty string
    return ""

def format_date(date, language: str = DEFAULT_LANGUAGE) -> str:
    """
    Formatuje datę zgodnie z konwencją danego języka.
    
    Args:
        date: Obiekt daty (datetime).
        language: Kod języka ('pl', 'en', 'de').
        
    Returns:
        Sformatowana data jako string.
    """
    if language == 'pl':
        # Format polski: dzień.miesiąc.rok
        return date.strftime('%d.%m.%Y')
    elif language == 'de':
        # Format niemiecki: dzień.miesiąc.rok
        return date.strftime('%d.%m.%Y')
    else:
        # Format angielski: miesiąc/dzień/rok
        return date.strftime('%m/%d/%Y')
