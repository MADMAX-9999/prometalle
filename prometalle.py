"""
Prometalle - Zaawansowany Symulator Inwestycji w Metale Szlachetne
Aplikacja Streamlit do analiz i symulacji inwestycji w złoto, srebro,
platynę i pallad na podstawie historycznych danych LBMA.
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Union, Any
import os
import base64
from io import BytesIO

#############################################################################
# KONFIGURACJA
#############################################################################

# Ustawienia domyślne
DEFAULT_LANGUAGE = 'pl'      # Domyślny język: polski
DEFAULT_CURRENCY = 'EUR'     # Domyślna waluta: Euro
DEFAULT_UNIT = 'g'           # Domyślna jednostka: gramy

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

# Historyczne wydarzenia na wykresach
HISTORICAL_EVENTS = {
    '2008-09-15': 'Upadek Lehman Brothers',
    '2011-08-22': 'Szczyt ceny złota',
    '2020-03-23': 'Krach COVID-19',
    '2022-02-24': 'Inwazja Rosji na Ukrainę'
}

#############################################################################
# TŁUMACZENIA
#############################################################################

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
    
    # Stopka
    "footer_disclaimer": {
        "pl": "Prometalle - Symulator inwestycji w metale szlachetne. Symulacja nie stanowi porady inwestycyjnej.",
        "en": "Prometalle - Precious metals investment simulator. Simulation does not constitute investment advice.",
        "de": "Prometalle - Simulator für Investitionen in Edelmetalle. Die Simulation stellt keine Anlageberatung dar."
    }
}

def translate(key: str, language: str = DEFAULT_LANGUAGE) -> str:
    """Zwraca tłumaczenie danego klucza w wybranym języku."""
    if key in TRANSLATIONS:
        if language in TRANSLATIONS[key]:
            return TRANSLATIONS[key][language]
        elif 'en' in TRANSLATIONS[key]:
            return TRANSLATIONS[key]['en']
    return key

#############################################################################
# FUNKCJE POMOCNICZE
#############################################################################

def load_css():
    """Ładuje niestandardowy CSS."""
    st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    h1, h2, h3 {
        color: #1E3A8A;
    }
    .sidebar .sidebar-content {
        background-color: #f0f9ff;
    }
    .st-bw {
        background-color: #ffffff;
        border-radius: 5px;
        padding: 1rem;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }
    .info-box {
        background-color: #e0f7fa;
        border-left: 5px solid #0097a7;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0 5px 5px 0;
    }
    .warning-box {
        background-color: #fff8e1;
        border-left: 5px solid #ffa000;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0 5px 5px 0;
    }
    .metric-card {
        background-color: white;
        border-radius: 5px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12);
        text-align: center;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: bold;
        color: #1E3A8A;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #64748b;
    }
    .chart-container {
        background-color: white;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12);
    }
    .gold-color { color: #FFD700; }
    .silver-color { color: #C0C0C0; }
    .platinum-color { color: #E5E4E2; }
    .palladium-color { color: #8A8B8C; }
    </style>
    """, unsafe_allow_html=True)

def convert_df_to_csv_download_link(df, filename="data.csv"):
    """Generuje link do pobrania DataFrame jako CSV."""
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">Pobierz plik CSV</a>'
    return href

def create_excel_download_link(data_dict, filename="data.xlsx"):
    """Generuje link do pobrania słownika DataFrame jako Excel."""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        for sheet_name, df in data_dict.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    excel_data = output.getvalue()
    b64 = base64.b64encode(excel_data).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}">Pobierz plik Excel</a>'
    return href

@st.cache_data
def load_metal_prices(file_path: str) -> pd.DataFrame:
    """Ładuje ceny metali z pliku CSV."""
    try:
        prices = pd.read_csv(file_path, parse_dates=["Data"])
        prices.sort_values("Data", inplace=True)
        return prices
    except Exception as e:
        st.error(f"Błąd podczas ładowania cen metali: {e}")
        return pd.DataFrame()

@st.cache_data
def load_exchange_rates(file_path: str) -> pd.DataFrame:
    """Ładuje kursy walutowe z pliku CSV."""
    try:
        rates = pd.read_csv(file_path, parse_dates=["Data"])
        rates.sort_values("Data", inplace=True)
        return rates
    except Exception as e:
        st.error(f"Błąd podczas ładowania kursów walut: {e}")
        return pd.DataFrame()

@st.cache_data
def load_inflation_rates(file_path: str) -> pd.DataFrame:
    """Ładuje dane o inflacji z pliku CSV."""
    try:
        df = pd.read_csv(file_path)
        if {'Rok', 'waluta', 'roczna_inflacja'}.issubset(df.columns):
            return df
        else:
            raise ValueError("Brak wymaganych kolumn w pliku CSV.")
    except Exception as e:
        # Zwróć domyślne inflacje w prostym DataFrame
        data = []
        for year in range(1997, 2030):
            for currency, rate in DEFAULT_INFLATION.items():
                data.append({'Rok': year, 'waluta': currency, 'roczna_inflacja': rate})
        return pd.DataFrame(data)

def get_inflation_rate(df_inflation: pd.DataFrame, year: int, currency: str) -> float:
    """Zwraca roczną inflację dla podanego roku i waluty."""
    try:
        rate = df_inflation[(df_inflation['Rok'] == year) & (df_inflation['waluta'] == currency)]['roczna_inflacja'].values
        if len(rate) > 0:
            return float(rate[0])
        else:
            return DEFAULT_INFLATION.get(currency, 0.02)
    except:
        return DEFAULT_INFLATION.get(currency, 0.02)

#############################################################################
# FUNKCJE OBSŁUGI METALI I KURSÓW WALUT
#############################################################################

def convert_prices_to_currency(prices_df: pd.DataFrame, rates_df: pd.DataFrame, currency: str) -> pd.DataFrame:
    """Konwertuje ceny metali na wybraną walutę (EUR, USD, PLN)."""
    if prices_df.empty or rates_df.empty:
        return pd.DataFrame()
        
    merged = pd.merge(prices_df, rates_df, on="Data", how="left")

    if currency == "EUR":
        return merged
    elif currency == "USD":
        merged["Gold"] = merged["Gold"] * merged["EUR_USD"]
        merged["Silver"] = merged["Silver"] * merged["EUR_USD"]
        merged["Platinum"] = merged["Platinum"] * merged["EUR_USD"]
        merged["Palladium"] = merged["Palladium"] * merged["EUR_USD"]
    elif currency == "PLN":
        merged["Gold"] = merged["Gold"] * merged["EUR_PLN"]
        merged["Silver"] = merged["Silver"] * merged["EUR_PLN"]
        merged["Platinum"] = merged["Platinum"] * merged["EUR_PLN"]
        merged["Palladium"] = merged["Palladium"] * merged["EUR_PLN"]
    else:
        raise ValueError(f"Unsupported currency: {currency}")

    return merged

#############################################################################
# FUNKCJE HARMONOGRAMU ZAKUPÓW
#############################################################################

def generate_purchase_schedule(
    start_date: str,
    end_date: str,
    frequency: str,
    purchase_day: int,
    purchase_amount: float
) -> pd.DataFrame:
    """Generuje harmonogram zakupów na podstawie częstotliwości."""
    schedule = []
    
    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)
    
    if frequency == 'weekly':
        # Co tydzień w określony dzień tygodnia
        current = start
        while current <= end:
            if current.weekday() == purchase_day:
                schedule.append({'Data': current, 'Kwota': purchase_amount})
            current += timedelta(days=1)

    elif frequency == 'monthly':
        # Co miesiąc w określony dzień
        current = start.replace(day=1)
        while current <= end:
            try:
                purchase_date = current.replace(day=purchase_day)
            except ValueError:
                # Dzień nie istnieje (np. 30 lutego) -> ostatni dzień miesiąca
                next_month = current + pd.DateOffset(months=1)
                purchase_date = next_month - pd.DateOffset(days=1)
            if purchase_date >= start and purchase_date <= end:
                schedule.append({'Data': purchase_date, 'Kwota': purchase_amount})
            current += pd.DateOffset(months=1)

    elif frequency == 'quarterly':
        # Co kwartał w określony dzień
        current = start.replace(day=1)
        while current <= end:
            try:
                purchase_date = current.replace(day=purchase_day)
            except ValueError:
                next_month = current + pd.DateOffset(months=1)
                purchase_date = next_month - pd.DateOffset(days=1)
            if purchase_date >= start and purchase_date <= end:
                schedule.append({'Data': purchase_date, 'Kwota': purchase_amount})
            current += pd.DateOffset(months=3)

    return pd.DataFrame(schedule)

#############################################################################
# FUNKCJE OBSŁUGI PORTFELA
#############################################################################

def build_portfolio(
    schedule: pd.DataFrame,
    metal_prices: pd.DataFrame,
    allocation: dict,
    purchase_margin: float = 2.0
) -> pd.DataFrame:
    """Buduje rejestr operacji zakupowych na podstawie harmonogramu i alokacji."""
    portfolio_records = []

    if schedule.empty or metal_prices.empty:
        return pd.DataFrame()

    # Upewnij się, że dane są posortowane
    metal_prices = metal_prices.sort_values('Data')

    for _, row in schedule.iterrows():
        date = pd.to_datetime(row['Data'])
        amount = row['Kwota']

        # Szukamy ceny na datę lub najbliższą wcześniejszą
        daily_prices = metal_prices[metal_prices['Data'] == date]

        if daily_prices.empty:
            daily_prices = metal_prices[metal_prices['Data'] < date].sort_values('Data', ascending=False).head(1)

        if daily_prices.empty:
            daily_prices = metal_prices[metal_prices['Data'] > date].sort_values('Data', ascending=True).head(1)

        if daily_prices.empty:
            continue  # Brak danych całkowicie, pomijamy

        for metal, alloc_percent in allocation.items():
            if alloc_percent > 0:
                alloc_amount = amount * (alloc_percent / 100)
                metal_price_col = metal.capitalize()

                if metal_price_col in daily_prices.columns:
                    metal_price = daily_prices[metal_price_col].values[0]
                    price_with_margin = metal_price * (1 + purchase_margin / 100)
                    quantity = alloc_amount / price_with_margin

                    portfolio_records.append({
                        'Data': date,
                        'Typ operacji': 'Zakup',
                        'Metal': metal.capitalize(),
                        'Ilość': quantity,
                        'Cena jednostkowa': price_with_margin,
                        'Kwota operacji': alloc_amount,
                        'Koszt_magazynowania': 0.0,
                        'Kwota_po_kosztach': alloc_amount
                    })

    portfolio_df = pd.DataFrame(portfolio_records)
    return portfolio_df

def aggregate_portfolio(df_portfolio: pd.DataFrame) -> pd.DataFrame:
    """Agreguje wartości końcowe portfela."""
    if df_portfolio.empty:
        return pd.DataFrame()

    current_portfolio = df_portfolio.copy()
    metals_summary = current_portfolio.groupby('Metal').agg({
        'Ilość': 'sum',
        'Kwota operacji': 'sum',
        'Cena jednostkowa': 'last'  # Ostatnia cena
    }).reset_index()
    
    # Dodajemy kolumnę z aktualną wartością
    metals_summary['Wartość aktualna'] = metals_summary['Ilość'] * metals_summary['Cena jednostkowa']
    
    # Obliczamy zysk/stratę
    metals_summary['Zysk/Strata'] = metals_summary['Wartość aktualna'] - metals_summary['Kwota operacji']
    
    # Obliczamy ROI
    metals_summary['ROI (%)'] = (metals_summary['Zysk/Strata'] / metals_summary['Kwota operacji'] * 100)
    metals_summary['ROI (%)'] = metals_summary['ROI (%)'].replace([np.inf, -np.inf], 0)
    metals_summary['ROI (%)'] = metals_summary['ROI (%)'].fillna(0)

    return metals_summary

#############################################################################
# FUNKCJE KOSZTÓW MAGAZYNOWANIA
#############################################################################

def calculate_storage_costs(
    df_portfolio: pd.DataFrame, 
    storage_fee_rate: float = 0.005, 
    storage_base: str = "value", 
    storage_frequency: str = "monthly", 
    vat_rate: float = 19.0, 
    cover_method: str = "cash"
) -> pd.DataFrame:
    """Oblicza koszty magazynowania i uwzględnia sposób ich pokrycia."""
    if df_portfolio.empty:
        return df_portfolio

    df = df_portfolio.copy()

    # Ustalenie podstawy naliczania kosztu
    base_column = "Kwota operacji"

    # Stawka miesięczna lub roczna
    if storage_frequency == "monthly":
        period_rate = storage_fee_rate / 12 / 100
    else:
        period_rate = storage_fee_rate / 100

    vat_multiplier = 1 + vat_rate / 100

    # Grupa po dacie
    grouped = df.groupby('Data')
    results = []

    for date, group in grouped:
        period_cost_net = group[base_column].sum() * period_rate
        period_cost_gross = period_cost_net * vat_multiplier

        group = group.copy()
        group['Koszt_magazynowania'] = 0.0
        group['Kwota_po_kosztach'] = group[base_column]

        if cover_method == "cash":
            # Koszt pokrywany gotówką – bez zmiany metali
            group['Koszt_magazynowania'] = period_cost_gross / len(group)
            group['Kwota_po_kosztach'] = group[base_column] - group['Koszt_magazynowania']

        elif cover_method in ["gold", "silver", "platinum", "palladium"]:
            selected = group[group['Metal'] == cover_method.capitalize()]
            if not selected.empty:
                metal_price = selected.iloc[0]['Cena jednostkowa']
                grams_to_sell = period_cost_gross / metal_price
                group.loc[group['Metal'] == cover_method.capitalize(), 'Ilość'] -= grams_to_sell
                group['Koszt_magazynowania'] = period_cost_gross / len(group)
                group['Kwota_po_kosztach'] = group['Ilość'] * group['Cena jednostkowa']

        elif cover_method == "all_metals":
            total_value = group[base_column].sum()
            for idx, row in group.iterrows():
                share = row[base_column] / total_value if total_value > 0 else 0
                metal_share_cost = period_cost_gross * share
                metal_price = row['Cena jednostkowa']
                grams_to_sell = metal_share_cost / metal_price
                group.at[idx, 'Ilość'] -= grams_to_sell
                group.at[idx, 'Koszt_magazynowania'] = metal_share_cost
                group.at[idx, 'Kwota_po_kosztach'] = group.at[idx, 'Ilość'] * metal_price

        results.append(group)

    if results:
        final_df = pd.concat(results)
        return final_df
    else:
        return df

def total_storage_cost(df_portfolio: pd.DataFrame) -> float:
    """Oblicza całkowity koszt magazynowania."""
    if 'Koszt_magazynowania' in df_portfolio.columns:
        return df_portfolio['Koszt_magazynowania'].sum()
    else:
        return 0.0

#############################################################################
# FUNKCJE WIZUALIZACJI
#############################################################################

def plot_portfolio_value(df_portfolio: pd.DataFrame, currency: str = 'EUR'):
    """Rysuje interaktywny wykres wartości portfela w czasie."""
    if df_portfolio.empty:
        st.warning("Brak danych do wyświetlenia wykresu.")
        return

    # Obliczamy wartość depozytu: ilość * aktualna cena metalu
    df_portfolio['Wartość'] = df_portfolio['Ilość'] * df_portfolio['Cena jednostkowa']

    # Grupujemy po dacie i sumujemy wartość depozytu
    df_by_date = df_portfolio.groupby('Data').agg({
        'Wartość': 'sum'
    }).reset_index()

    # Dodajemy wykres wartości skumulowanej
    fig = go.Figure()
    
    # Dodajemy linię wartości portfela
    fig.add_trace(go.Scatter(
        x=df_by_date['Data'],
        y=df_by_date['Wartość'],
        mode='lines+markers',
        name='Wartość portfela',
        line=dict(color='#1E3A8A', width=3),
        marker=dict(size=8, color='#1E3A8A'),
        hovertemplate='%{x|%d.%m.%Y}<br>Wartość: %{y:,.2f} ' + currency
    ))
    
    # Konfigurujesz układ wykresu
    fig.update_layout(
        title=None,
        xaxis_title='Data',
        yaxis_title=f'Wartość portfela ({currency})',
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=10, r=10, t=10, b=10),
        height=400,
        template='plotly_white'
    )
    
    # Dodajemy pionowe linie dla ważnych momentów - np. krach
    for date_str, label in HISTORICAL_EVENTS.items():
        try:
            date = pd.to_datetime(date_str)
            if date >= df_by_date['Data'].min() and date <= df_by_date['Data'].max():
                fig.add_vline(
                    x=date, 
                    line_width=1, 
                    line_dash="dash", 
                    line_color="gray",
                    annotation_text=label,
                    annotation_position="top right"
                )
        except:
            continue
    
    # Wyświetlamy wykres
    st.plotly_chart(fig, use_container_width=True)

def plot_metals_allocation(summary_df: pd.DataFrame, currency: str = 'EUR') -> None:
    """Tworzy wykres kołowy pokazujący alokację metali w portfelu."""
    if summary_df.empty:
        st.warning("Brak danych do wyświetlenia wykresu alokacji.")
        return
    
    # Przygotowujemy dane do wykresu
    metals = summary_df['Metal'].tolist()
    values = summary_df['Kwota operacji'].tolist()
    
    # Kolory dla metali
    colors = [METAL_COLORS.get(metal, '#808080') for metal in metals]
    
    # Tworzymy wykres kołowy
    fig = go.Figure(data=[go.Pie(
        labels=metals,
        values=values,
        hole=.4,
        marker_colors=colors,
        textinfo='percent+label',
        hovertemplate='%{label}<br>Wartość: %{value:,.2f} ' + currency + '<br>%{percent}'
    )])
    
    fig.update_layout(
        showlegend=True,
        margin=dict(l=10, r=10, t=10, b=10),
        height=350,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        )
    )
    
    # Wyświetlamy wykres
    st.plotly_chart(fig, use_container_width=True)

def plot_price_history(
    metal_prices: pd.DataFrame, 
    start_date: datetime, 
    end_date: datetime, 
    currency: str = 'EUR'
) -> None:
    """Tworzy interaktywny wykres historii cen metali."""
    if metal_prices.empty:
        st.warning("Brak danych do wyświetlenia wykresu cen.")
        return
    
    # Konwertujemy daty do formatu datetime
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    
    # Filtrujemy dane w zakresie dat
    filtered_prices = metal_prices[
        (metal_prices['Data'] >= start_date) & 
        (metal_prices['Data'] <= end_date)
    ]
    
    if filtered_prices.empty:
        st.warning("Brak danych dla wybranego zakresu dat.")
        return
    
    # Tworzymy interaktywny wykres
    fig = go.Figure()
    
    # Dodajemy linie dla każdego metalu
    metals = {
        'Gold': 'Złoto',
        'Silver': 'Srebro',
        'Platinum': 'Platyna',
        'Palladium': 'Pallad'
    }
    
    # Dodajemy przełączniki dla metali
    metal_options = st.multiselect(
        "Wybierz metale do wyświetlenia:",
        list(metals.values()),
        default=list(metals.values())[:2],
        key="price_history_metals"
    )
    
    # Mapujemy nazwy polskie na angielskie
    reverse_metals = {v: k for k, v in metals.items()}
    selected_metals = [reverse_metals[m] for m in metal_options]
    
    # Jeśli nic nie wybrano, pokazujemy wszystkie
    if not selected_metals:
        selected_metals = list(metals.keys())
    
    # Dodajemy linie do wykresu
    for metal_eng, metal_pl in metals.items():
        if metal_eng in selected_metals:
            if metal_eng in filtered_prices.columns:
                fig.add_trace(go.Scatter(
                    x=filtered_prices['Data'],
                    y=filtered_prices[metal_eng],
                    mode='lines',
                    name=metal_pl,
                    line=dict(color=METAL_COLORS.get(metal_eng, '#808080'), width=2),
                    hovertemplate='%{x|%d.%m.%Y}<br>' + metal_pl + ': %{y:,.2f} ' + currency
                ))
    
    # Konfigurujemy układ wykresu
    fig.update_layout(
        xaxis_title="Data",
        yaxis_title=f"Cena ({currency})",
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=10, r=10, t=10, b=10),
        height=400,
        template='plotly_white'
    )
    
    # Wyświetlamy wykres
    st.plotly_chart(fig, use_container_width=True)

def plot_comparison_chart(
    metal_prices: pd.DataFrame, 
    start_date: datetime, 
    end_date: datetime, 
    currency: str = 'EUR'
) -> None:
    """Tworzy wykres porównawczy pokazujący relatywny zwrot z inwestycji w różne metale."""
    if metal_prices.empty:
        st.warning("Brak danych do wyświetlenia wykresu porównawczego.")
        return
    
    # Konwertujemy daty do formatu datetime
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    
    # Filtrujemy dane w zakresie dat
    filtered_prices = metal_prices[
        (metal_prices['Data'] >= start_date) & 
        (metal_prices['Data'] <= end_date)
    ]
    
    if filtered_prices.empty:
        st.warning("Brak danych dla wybranego zakresu dat.")
        return
    
    # Tworzymy DataFrame do porównania procentowego
    comparison_df = filtered_prices.copy()
    
    # Obliczamy indeks ceny (pierwszy dzień = 100)
    metals = {
        'Gold': 'Złoto',
        'Silver': 'Srebro',
        'Platinum': 'Platyna',
        'Palladium': 'Pallad'
    }
    
    for metal in metals.keys():
        if metal in comparison_df.columns:
            base_price = comparison_df[metal].iloc[0]
            if base_price > 0:
                comparison_df[f"{metal}_Index"] = (comparison_df[metal] / base_price) * 100
    
    # Tworzymy interaktywny wykres
    fig = go.Figure()
    
    # Dodajemy linie dla każdego metalu
    for metal_eng, metal_pl in metals.items():
        index_column = f"{metal_eng}_Index"
        if index_column in comparison_df.columns:
            fig.add_trace(go.Scatter(
                x=comparison_df['Data'],
                y=comparison_df[index_column],
                mode='lines',
                name=metal_pl,
                line=dict(color=METAL_COLORS.get(metal_eng, '#808080'), width=2),
                hovertemplate='%{x|%d.%m.%Y}<br>' + metal_pl + ': %{y:.2f}%'
            ))
    
    # Dodajemy linię 100% (początkowa wartość)
    fig.add_trace(go.Scatter(
        x=[comparison_df['Data'].iloc[0], comparison_df['Data'].iloc[-1]],
        y=[100, 100],
        mode='lines',
        name='Poziom początkowy',
        line=dict(color='gray', width=1, dash='dash'),
        hoverinfo='skip'
    ))
    
    # Konfigurujemy układ wykresu
    fig.update_layout(
        xaxis_title="Data",
        yaxis_title="Względna zmiana wartości (%)",
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=10, r=10, t=10, b=10),
        height=400,
        template='plotly_white'
    )
    
    # Wyświetlamy wykres
    st.plotly_chart(fig, use_container_width=True)

def plot_cumulative_investment(schedule_df: pd.DataFrame, currency: str = 'EUR') -> None:
    """Tworzy wykres skumulowanej inwestycji w czasie."""
    if schedule_df.empty:
        st.warning("Brak danych do wyświetlenia wykresu inwestycji.")
        return
    
    # Sortujemy po dacie
    schedule_df = schedule_df.sort_values('Data')
    
    # Obliczamy skumulowaną sumę
    schedule_df['Skumulowana kwota'] = schedule_df['Kwota'].cumsum()
    
    # Tworzymy wykres
    fig = go.Figure()
    
    # Dodajemy linie
    fig.add_trace(go.Scatter(
        x=schedule_df['Data'],
        y=schedule_df['Skumulowana kwota'],
        mode='lines',
        name='Skumulowana inwestycja',
        line=dict(color='#0891b2', width=3),
        fill='tozeroy',
        fillcolor='rgba(8, 145, 178, 0.2)',
        hovertemplate='%{x|%d.%m.%Y}<br>Zainwestowano: %{y:,.2f} ' + currency
    ))
    
    # Dodajemy słupki pojedynczych inwestycji
    fig.add_trace(go.Bar(
        x=schedule_df['Data'],
        y=schedule_df['Kwota'],
        name='Pojedyncze wpłaty',
        marker_color='#0e7490',
        hovertemplate='%{x|%d.%m.%Y}<br>Wpłata: %{y:,.2f} ' + currency
    ))
    
    # Konfigurujemy układ wykresu
    fig.update_layout(
        xaxis_title="Data",
        yaxis_title=f"Kwota ({currency})",
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=10, r=10, t=10, b=10),
        height=350,
        barmode='overlay',
        template='plotly_white'
    )
    
    # Wyświetlamy wykres
    st.plotly_chart(fig, use_container_width=True)

#############################################################################
# GŁÓWNA APLIKACJA
#############################################################################

def main():
    # Konfiguracja strony
    st.set_page_config(
        page_title="Prometalle | Symulator Inwestycji w Metale",
        page_icon="💰",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Ładowanie własnego CSS
    load_css()

    # Tytuł aplikacji z logo
    st.markdown("""
    <div style="display: flex; align-items: center; margin-bottom: 2rem;">
        <h1 style="margin: 0; flex-grow: 1;">Prometalle</h1>
        <span style="font-size: 2rem; margin-left: 1rem;">💰✨</span>
    </div>
    <p style="margin-top: -1rem; margin-bottom: 2rem; color: #64748b; font-size: 1.1rem;">
        Inteligentny symulator inwestycji w metale szlachetne
    </p>
    """, unsafe_allow_html=True)

    # Inicjalizacja stanu sesji
    if 'language' not in st.session_state:
        st.session_state.language = DEFAULT_LANGUAGE

    if 'simulation_results' not in st.session_state:
        st.session_state.simulation_results = None

    if 'show_results' not in st.session_state:
        st.session_state.show_results = False

    # Funkcja do ładowania danych
    @st.cache_data
    def load_data():
        try:
            metal_prices = load_metal_prices("data/metal_prices.csv")
            exchange_rates = load_exchange_rates("data/exchange_rates.csv")
            inflation_rates = load_inflation_rates("data/inflation_rates_ready.csv")
            return metal_prices, exchange_rates, inflation_rates, None
        except Exception as e:
            return None, None, None, str(e)

    # Ładowanie danych
    metal_prices, exchange_rates, inflation_rates, error_message = load_data()

    # Sprawdzenie błędów
    if error_message:
        st.error(f"Błąd ładowania danych: {error_message}")
        st.stop()

    if metal_prices is None or exchange_rates is None:
        st.error("Nie udało się załadować danych. Sprawdź pliki CSV.")
        st.stop()

    # Zakres dat
    min_date = metal_prices['Data'].min().date()
    max_date = metal_prices['Data'].max().date()

    # Panel boczny
	with st.sidebar:
    st.header(translate("simulation_settings", language=st.session_state.language))

    selected_section = st.radio(
        "⚙️ Wybierz sekcję ustawień:",
        options=["Ustawienia ogólne", "Alokacja kapitału", "Zakupy systematyczne", "Koszty magazynowe"]
    )

    if selected_section == "Ustawienia ogólne":
        selected_language_label = st.selectbox(
            translate("choose_language", language=st.session_state.language),
            options=[LANGUAGE_LABELS[code] for code in AVAILABLE_LANGUAGES],
            index=AVAILABLE_LANGUAGES.index(st.session_state.language)
        )
        selected_language = [code for code, label in LANGUAGE_LABELS.items() if label == selected_language_label][0]
        st.session_state.language = selected_language

        selected_currency = st.selectbox(
            translate("choose_currency", language=st.session_state.language),
            options=AVAILABLE_CURRENCIES,
            index=AVAILABLE_CURRENCIES.index(DEFAULT_CURRENCY)
        )

        selected_unit = st.selectbox(
            translate("choose_unit", language=st.session_state.language),
            options=AVAILABLE_UNITS,
            index=AVAILABLE_UNITS.index(DEFAULT_UNIT),
            format_func=lambda x: {"g": "Gramy (g)", "oz": "Uncje (oz)"}.get(x, x)
        )

        start_amount = st.number_input(
            label=translate("start_amount", language=st.session_state.language),
            min_value=100.0,
            value=100000.0,
            step=100.0,
            format="%.2f"
        )

        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input(
                label=translate("start_date", language=st.session_state.language),
                value=min_date,
                min_value=min_date,
                max_value=max_date
            )
        with col2:
            end_date = st.date_input(
                label=translate("end_date", language=st.session_state.language),
                value=max_date,
                min_value=min_date,
                max_value=max_date
            )

        purchase_margin = st.slider(
            translate("purchase_margin", language=st.session_state.language),
            min_value=0.0,
            max_value=5.0,
            value=2.0,
            step=0.1,
            format="%.1f"
        )

        sale_margin = st.slider(
            translate("sale_margin", language=st.session_state.language),
            min_value=0.0,
            max_value=5.0,
            value=1.5,
            step=0.1,
            format="%.1f"
        )

   
        
        # Karta 2: Alokacja
        with tab2:
            st.markdown(f"#### {translate('allocation_settings', language=st.session_state.language)}")
            
            # Wizualne slajdery alokacji z kolorami
            gold_allocation = st.slider(
                "🟡 Złoto (%)",
                0, 100, 40, step=5,
                help="Procent kapitału przeznaczony na inwestycję w złoto"
            )
            
            silver_allocation = st.slider(
                "⚪ Srebro (%)",
                0, 100, 30, step=5,
                help="Procent kapitału przeznaczony na inwestycję w srebro"
            )
            
            platinum_allocation = st.slider(
                "⚪ Platyna (%)",
                0, 100, 15, step=5,
                help="Procent kapitału przeznaczony na inwestycję w platynę"
            )
            
            palladium_allocation = st.slider(
                "🔘 Pallad (%)",
                0, 100, 15, step=5,
                help="Procent kapitału przeznaczony na inwestycję w pallad"
            )
            
            allocation_sum = gold_allocation + silver_allocation + platinum_allocation + palladium_allocation
            
            if allocation_sum == 100:
                st.success(f"{translate('total_allocation', language=st.session_state.language)}: {allocation_sum}%")
            else:
                st.warning(f"{translate('allocation_error', language=st.session_state.language)} ({allocation_sum}%)")
            
            # Podgląd alokacji w formie wykresu kołowego
            if allocation_sum > 0:
                alloc_data = {
                    'Metal': ['Złoto', 'Srebro', 'Platyna', 'Pallad'],
                    'Alokacja (%)': [gold_allocation, silver_allocation, platinum_allocation, palladium_allocation],
                    'Kolor': ['gold', 'silver', '#e5e4e2', '#8c8c9c']
                }
                alloc_df = pd.DataFrame(alloc_data)
                alloc_df = alloc_df[alloc_df['Alokacja (%)'] > 0]  # Filtrowanie wartości > 0
                
                fig = px.pie(
                    alloc_df, 
                    values='Alokacja (%)', 
                    names='Metal', 
                    color='Metal',
                    color_discrete_map={
                        'Złoto': 'gold',
                        'Srebro': 'silver',
                        'Platyna': '#e5e4e2',
                        'Pallad': '#8c8c9c'
                    },
                    hole=0.4
                )
                fig.update_layout(
                    margin=dict(t=0, b=0, l=0, r=0),
                    height=200,
                    showlegend=False
                )
                fig.update_traces(textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        # Karta 3: Zakupy systematyczne
        with tab3:
            frequency = st.selectbox(
                label=translate("frequency", language=st.session_state.language),
                options=["one_time", "weekly", "monthly", "quarterly"],
                index=0,
                format_func=lambda x: {
                    "one_time": translate("one_time", language=st.session_state.language),
                    "weekly": translate("weekly", language=st.session_state.language),
                    "monthly": translate("monthly", language=st.session_state.language),
                    "quarterly": translate("quarterly", language=st.session_state.language)
                }.get(x, x)
            )
            
            recurring_amount = 0.0
            purchase_day = 0
            
            if frequency != "one_time":
                recurring_amount = st.number_input(
                    label=translate("recurring_amount", language=st.session_state.language),
                    min_value=0.0,
                    value=250.0,
                    step=50.0,
                    format="%.2f"
                )
                
                if frequency == "weekly":
                    purchase_day = st.selectbox(
                        translate("purchase_day_weekly", language=st.session_state.language),
                        options=list(range(0, 5)),
                        index=0,
                        format_func=lambda x: {
                            0: "Poniedziałek",
                            1: "Wtorek",
                            2: "Środa",
                            3: "Czwartek",
                            4: "Piątek"
                        }.get(x, x)
                    )
                elif frequency == "monthly":
                    purchase_day = st.selectbox(
                        translate("purchase_day_monthly", language=st.session_state.language),
                        options=list(range(1, 29)),
                        index=0
                    )
                elif frequency == "quarterly":
                    purchase_day = st.selectbox(
                        translate("purchase_day_quarterly", language=st.session_state.language),
                        options=list(range(1, 91)),
                        index=0
                    )
        
        # Karta 4: Koszty magazynowe
        with tab4:
            storage_base = st.selectbox(
                translate("storage_base", language=st.session_state.language),
                options=["value", "invested_amount"],
                index=0,
                format_func=lambda x: {
                    "value": "Wartość metali",
                    "invested_amount": "Zainwestowana kwota"
                }.get(x, x)
            )
            
            storage_frequency = st.selectbox(
                translate("storage_frequency", language=st.session_state.language),
                options=["monthly", "yearly"],
                index=0,
                format_func=lambda x: {
                    "monthly": "Miesięczna",
                    "yearly": "Roczna"
                }.get(x, x)
            )
            
            storage_rate = st.number_input(
                translate("storage_rate", language=st.session_state.language),
                min_value=0.0,
                value=0.05,
                step=0.01,
                format="%.2f",
                help="Roczna stawka opłaty magazynowej jako procent"
            )
            
            vat_rate = st.number_input(
                translate("vat_rate", language=st.session_state.language),
                min_value=0.0,
                value=19.0,
                step=1.0,
                format="%.1f"
            )
            
            cover_method = st.selectbox(
                translate("cover_method", language=st.session_state.language),
                options=["cash", "gold", "silver", "platinum", "palladium", "all_metals"],
                index=0,
                format_func=lambda x: {
                    "cash": translate("cash", language=st.session_state.language),
                    "gold": translate("gold", language=st.session_state.language),
                    "silver": translate("silver", language=st.session_state.language),
                    "platinum": translate("platinum", language=st.session_state.language),
                    "palladium": translate("palladium", language=st.session_state.language),
                    "all_metals": translate("all_metals", language=st.session_state.language)
                }.get(x, x)
            )
        
        # Przycisk uruchomienia symulacji
        st.markdown("---")
        run_simulation = st.button(
            translate("start_simulation", language=st.session_state.language),
            type="primary",
            use_container_width=True
        )

    # Logika symulacji
    if run_simulation:
        if allocation_sum != 100:
            st.error(translate("allocation_error", language=st.session_state.language))
        else:
            with st.spinner('Uruchamianie symulacji...'):
                # Konwersja cen na wybraną walutę
                metal_prices_converted = convert_prices_to_currency(metal_prices, exchange_rates, selected_currency)
                
                # Generowanie harmonogramu zakupów
                if frequency != "one_time" and recurring_amount > 0:
                    schedule = generate_purchase_schedule(
                        start_date=start_date.strftime("%Y-%m-%d"),
                        end_date=end_date.strftime("%Y-%m-%d"),
                        frequency=frequency,
                        purchase_day=purchase_day,
                        purchase_amount=recurring_amount
                    )
                else:
                    schedule = pd.DataFrame()
                
                # Dodanie zakupu początkowego
                if start_amount > 0:
                    start_purchase = pd.DataFrame({
                        'Data': [pd.to_datetime(start_date)],
                        'Kwota': [start_amount]
                    })
                    schedule = pd.concat([start_purchase, schedule], ignore_index=True)
                
                # Alokacja
                allocation = {
                    "gold": gold_allocation,
                    "silver": silver_allocation,
                    "platinum": platinum_allocation,
                    "palladium": palladium_allocation
                }
                
                # Budowa portfela
                portfolio = build_portfolio(schedule, metal_prices_converted, allocation, purchase_margin)
                
                # Koszty magazynowe
                portfolio_with_storage = calculate_storage_costs(
                    df_portfolio=portfolio,
                    storage_fee_rate=storage_rate,
                    storage_base=storage_base,
                    storage_frequency=storage_frequency,
                    vat_rate=vat_rate,
                    cover_method=cover_method
                )
                
                # Zapisanie wyników do stanu sesji
                st.session_state.simulation_results = {
                    'portfolio': portfolio_with_storage,
                    'summary': aggregate_portfolio(portfolio_with_storage),
                    'schedule': schedule,
                    'metal_prices': metal_prices_converted,
                    'total_storage_cost': total_storage_cost(portfolio_with_storage),
                    'currency': selected_currency,
                    'unit': selected_unit,
                    'allocation': allocation,
                    'start_date': start_date,
                    'end_date': end_date
                }
                
                st.session_state.show_results = True

    # Wyświetlanie wyników
    if st.session_state.show_results and st.session_state.simulation_results is not None:
        results = st.session_state.simulation_results
        
        # Sekcja z podsumowaniem
        st.markdown("## 📊 Podsumowanie symulacji")
        
        # Karty z głównymi metrykami
        kol1, kol2, kol3, kol4 = st.columns(4)
        
        # Wartość portfela
        total_value = 0
        if not results['portfolio'].empty:
            total_value = (results['portfolio']['Ilość'] * results['portfolio']['Cena jednostkowa']).sum()
        
        # Całkowita zainwestowana kwota
        total_invested = results['schedule']['Kwota'].sum() if not results['schedule'].empty else 0
        
        # Stopa zwrotu
        roi = ((total_value - total_invested) / total_invested) * 100 if total_invested > 0 else 0
        
        # Koszty magazynowe
        storage_costs = results['total_storage_cost']
        
        with kol1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{total_value:,.2f} {results['currency']}</div>
                <div class="metric-label">Wartość portfela</div>
            </div>
            """, unsafe_allow_html=True)
        
        with kol2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{total_invested:,.2f} {results['currency']}</div>
                <div class="metric-label">Zainwestowana kwota</div>
            </div>
            """, unsafe_allow_html=True)
        
        with kol3:
            roi_color = "#16a34a" if roi >= 0 else "#dc2626"
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value" style="color: {roi_color}">{roi:+.2f}%</div>
                <div class="metric-label">Stopa zwrotu</div>
            </div>
            """, unsafe_allow_html=True)
        
        with kol4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{storage_costs:,.2f} {results['currency']}</div>
                <div class="metric-label">Koszty magazynowania</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Zakładki z wynikami
        tab1, tab2, tab3, tab4 = st.tabs([
            "📈 Wizualizacje", 
            "📝 Rejestr operacji", 
            "🔍 Podsumowanie portfela", 
            "📅 Harmonogram zakupów"
        ])
        
        with tab1:
            st.markdown("### Wizualizacje portfela")
            
            # Wykres wartości portfela w czasie
            st.markdown("""
            <div class="chart-container">
                <h4>Wartość portfela w czasie</h4>
            """, unsafe_allow_html=True)
            
            plot_portfolio_value(results['portfolio'], results['currency'])
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Dwa wykresy obok siebie
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                <div class="chart-container">
                    <h4>Alokacja metali</h4>
                """, unsafe_allow_html=True)
                
                plot_metals_allocation(results['summary'], results['currency'])
                
                st.markdown("</div>", unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div class="chart-container">
                    <h4>Skumulowana inwestycja</h4>
                """, unsafe_allow_html=True)
                
                plot_cumulative_investment(results['schedule'], results['currency'])
                
                st.markdown("</div>", unsafe_allow_html=True)
            
            # Historia cen metali
            st.markdown("""
            <div class="chart-container">
                <h4>Historia cen metali</h4>
            """, unsafe_allow_html=True)
            
            plot_price_history(
                results['metal_prices'],
                results['start_date'],
                results['end_date'],
                results['currency']
            )
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Wykres porównawczy zwrotu z metali
            st.markdown("""
            <div class="chart-container">
                <h4>Porównanie inwestycji w różne metale</h4>
            """, unsafe_allow_html=True)
            
            plot_comparison_chart(
                results['metal_prices'],
                results['start_date'],
                results['end_date'],
                results['currency']
            )
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        with tab2:
            st.subheader(translate("transaction_register", language=st.session_state.language))
            
            # Opcja eksportu danych
            if not results['portfolio'].empty:
                col1, col2 = st.columns([3, 1])
                with col2:
                    st.markdown(convert_df_to_csv_download_link(results['portfolio'], "rejestr_operacji.csv"), unsafe_allow_html=True)
            
            st.dataframe(
                results['portfolio'],
                column_config={
                    "Data": st.column_config.DateColumn("Data"),
                    "Typ operacji": st.column_config.TextColumn("Typ operacji"),
                    "Metal": st.column_config.TextColumn("Metal"),
                    "Ilość": st.column_config.NumberColumn("Ilość", format="%.5f"),
                    "Cena jednostkowa": st.column_config.NumberColumn(f"Cena ({results['currency']})", format="%.2f"),
                    "Kwota operacji": st.column_config.NumberColumn(f"Kwota ({results['currency']})", format="%.2f"),
                    "Koszt_magazynowania": st.column_config.NumberColumn(f"Koszt magazynowania ({results['currency']})", format="%.2f"),
                    "Kwota_po_kosztach": st.column_config.NumberColumn(f"Kwota po kosztach ({results['currency']})", format="%.2f"),
                },
                use_container_width=True,
                hide_index=True
            )
        
        with tab3:
            st.subheader(translate("portfolio_summary", language=st.session_state.language))
            
            if not results['summary'].empty:
                # Opcja eksportu danych
                col1, col2 = st.columns([3, 1])
                with col2:
                    st.markdown(convert_df_to_csv_download_link(results['summary'], "podsumowanie_portfela.csv"), unsafe_allow_html=True)
                
                # Dodanie kolumn z ceną i wartością
                summary_with_price = results['summary'].copy()
                
                # Pobierz ostatnie ceny metali
                latest_prices = results['metal_prices'].iloc[-1]
                
                # Dodaj kolumny
                for idx, row in summary_with_price.iterrows():
                    metal = row['Metal'].lower()
                    if metal in ['gold', 'silver', 'platinum', 'palladium']:
                        price_column = f"{metal.capitalize()}"
                        if price_column in latest_prices:
                            summary_with_price.at[idx, 'Aktualna cena'] = latest_prices[price_column]
                            summary_with_price.at[idx, 'Wartość aktualna'] = row['Ilość'] * latest_prices[price_column]
                
                st.dataframe(
                    summary_with_price,
                    column_config={
                        "Metal": st.column_config.TextColumn("Metal"),
                        "Ilość": st.column_config.NumberColumn("Ilość", format="%.5f"),
                        "Kwota operacji": st.column_config.NumberColumn(f"Zainwestowano ({results['currency']})", format="%.2f"),
                        "Aktualna cena": st.column_config.NumberColumn(f"Cena aktualna ({results['currency']})", format="%.2f"),
                        "Wartość aktualna": st.column_config.NumberColumn(f"Wartość aktualna ({results['currency']})", format="%.2f"),
                        "Zysk/Strata": st.column_config.NumberColumn(f"Zysk/Strata ({results['currency']})", format="%.2f"),
                        "ROI (%)": st.column_config.NumberColumn("ROI (%)", format="%.2f"),
                    },
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("Brak danych w podsumowaniu portfela.")
        
        with tab4:
            st.subheader(translate("purchase_schedule", language=st.session_state.language))
            
            if not results['schedule'].empty:
                # Opcja eksportu danych
                col1, col2 = st.columns([3, 1])
                with col2:
                    st.markdown(convert_df_to_csv_download_link(results['schedule'], "harmonogram_zakupow.csv"), unsafe_allow_html=True)
                
                st.dataframe(
                    results['schedule'],
                    column_config={
                        "Data": st.column_config.DateColumn("Data"),
                        "Kwota": st.column_config.NumberColumn(f"Kwota ({results['currency']})", format="%.2f"),
                    },
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("Brak danych w harmonogramie zakupów.")
        
        # Eksport wszystkich danych
        st.markdown("---")
        col1, col2 = st.columns([3, 1])
        with col2:
            export_data = {
                "Rejestr_operacji": results['portfolio'],
                "Podsumowanie_portfela": results['summary'],
                "Harmonogram_zakupów": results['schedule'],
                "Ceny_metali": results['metal_prices']
            }
            st.markdown("### Eksport wszystkich danych")
            st.markdown(create_excel_download_link(export_data, "prometalle_raport.xlsx"), unsafe_allow_html=True)
        
        # Dodaj stopkę z notkami
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #64748b; font-size: 0.8rem; margin-top: 2rem;">
            <p>Prometalle - Symulator inwestycji w metale szlachetne</p>
            <p>Dane historyczne LBMA (London Bullion Market Association)</p>
            <p>Symulacja nie stanowi porady inwestycyjnej. Wszystkie kwoty są przybliżone.</p>
        </div>
        """, unsafe_allow_html=True)

    else:
        # Strona główna z informacjami
        st.markdown("## 🌟 Witaj w Prometalle")
        
        st.markdown("""
        <div class="info-box">
            <h3>📈 Symulator inwestycji w metale szlachetne</h3>
            <p>
                Prometalle to zaawansowane narzędzie do analizy i symulacji inwestycji w metale szlachetne.
                Możesz planować swoje inwestycje w złoto, srebro, platynę i pallad w oparciu o rzeczywiste
                dane historyczne z London Bullion Market Association (LBMA).
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Informacje o funkcjach
        st.markdown("### 🛠️ Główne funkcje")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ✅ **Analiza historycznych cen metali**
            - Dane rynkowe od 1977 roku
            - Ceny spot z LBMA
            - Prezentacja trendów cenowych
            
            ✅ **Zaawansowane strategie inwestycyjne**
            - Zakupy jednorazowe i systematyczne
            - Automatyczny rebalancing portfela
            - Analiza kosztów przechowywania
            """)
        
        with col2:
            st.markdown("""
            ✅ **Wszechstronna analiza wyników**
            - Wykresy wartości portfela
            - Porównanie zwrotu z różnych metali
            - Obliczanie rzeczywistej stopy zwrotu
            
            ✅ **Profesjonalne narzędzia**
            - Eksport wyników do CSV i Excel
            - Wizualizacje interaktywne
            - Wielojęzyczny interfejs
            """)
        
        # Instrukcje korzystania z aplikacji
        st.markdown("### 🚀 Jak korzystać z aplikacji")
        
        st.markdown("""
        <div class="warning-box">
            <h3>📋 Instrukcja</h3>
            <p>
                1. Wybierz kwotę początkową inwestycji w panelu bocznym<br>
                2. Ustaw docelową alokację pomiędzy metalami<br>
                3. Opcjonalnie skonfiguruj systematyczne zakupy<br>
                4. Ustal parametry kosztów magazynowania<br>
                5. Kliknij przycisk "Rozpocznij symulację"<br>
                6. Analizuj wyniki w formie wykresów i tabel
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Informacja o danych
        st.markdown("### 📊 Dane historyczne")
        
        min_year = min_date.year
        max_year = max_date.year
        
        st.markdown(f"""
        Aplikacja wykorzystuje rzeczywiste dane historyczne cen metali szlachetnych z London Bullion Market Association (LBMA) 
        z okresu od **{min_year}** do **{max_year}** roku. Zakres dostępnych danych pozwala na przeprowadzenie dokładnych 
        analiz długoterminowych trendów i symulacji różnych strategii inwestycyjnych.
        """)
        
        # Stopka
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #64748b; font-size: 0.8rem; margin-top: 2rem;">
            <p>Prometalle - Symulator inwestycji w metale szlachetne</p>
            <p>Dane historyczne LBMA (London Bullion Market Association)</p>
            <p>Symulacja nie stanowi porady inwestycyjnej. Wszystkie kwoty są przybliżone.</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
