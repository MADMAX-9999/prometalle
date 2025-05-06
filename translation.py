# /main/translation.py

from config import DEFAULT_LANGUAGE

TRANSLATIONS = {
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
    "start_amount": {
        "pl": "Kwota początkowa inwestycji (EUR)",
        "en": "Initial investment amount (EUR)",
        "de": "Anfangsinvestition (EUR)"
    },
    "recurring_amount": {
        "pl": "Kwota zakupu systematycznego (EUR)",
        "en": "Recurring purchase amount (EUR)",
        "de": "Regelmäßiger Kaufbetrag (EUR)"
    },
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
    "investment_period": {
        "pl": "Okres inwestycji (lata)",
        "en": "Investment period (years)",
        "de": "Investitionszeitraum (Jahre)"
    },
    "start_simulation": {
        "pl": "Rozpocznij symulację",
        "en": "Start simulation",
        "de": "Simulation starten"
    },
    "purchase_schedule": {
        "pl": "Harmonogram zakupów",
        "en": "Purchase schedule",
        "de": "Kaufplan"
    },
    "portfolio_values": {
        "pl": "Zakupy i wartości metali",
        "en": "Metal purchases and values",
        "de": "Käufe und Werte der Metalle"
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
    "allocation_settings": {
        "pl": "Ustawienia alokacji kapitału",
        "en": "Capital allocation settings",
        "de": "Kapitalallokationseinstellungen"
    },
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
    "recurring_purchase_settings": {
        "pl": "Ustawienia zakupów systematycznych",
        "en": "Recurring purchase settings",
        "de": "Einstellungen für regelmäßige Käufe"
    },
    "one_time": {
        "pl": "Jednorazowy",
        "en": "One-time",
        "de": "Einmalig"
    }
    
}

def translate(key: str, language: str = DEFAULT_LANGUAGE) -> str:
    """Zwraca tłumaczenie danego klucza w wybranym języku."""
    return TRANSLATIONS.get(key, {}).get(language, key)
