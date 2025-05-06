# /app.py
# Główny plik aplikacji Prometalle

import streamlit as st
import pandas as pd
import numpy as np
import datetime
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path

# Import modułów lokalnych
from modules.config import (
    AVAILABLE_LANGUAGES, AVAILABLE_CURRENCIES, AVAILABLE_UNITS,
    DEFAULT_LANGUAGE, DEFAULT_CURRENCY, DEFAULT_UNIT,
    LANGUAGE_LABELS
)
from modules.translation import translate
from modules.purchase_schedule import generate_purchase_schedule
from modules.metals import load_metal_prices, load_exchange_rates, convert_prices_to_currency
from modules.portfolio import build_portfolio, aggregate_portfolio
from modules.storage_costs import calculate_storage_costs, total_storage_cost
from modules.visualization import (
    plot_portfolio_value, plot_metals_allocation, 
    plot_price_history, plot_comparison_chart,
    plot_cumulative_investment
)
from modules.inflation import load_inflation_rates, get_inflation_rate

# Konfiguracja strony
st.set_page_config(
    page_title="Prometalle | Symulator Inwestycji w Metale",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ładowanie własnego CSS
def load_css():
    css_file = Path("assets/styles.css")
    if css_file.exists():
        with open(css_file) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    else:
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
        </style>
        """, unsafe_allow_html=True)

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
    
    # Karty w panelu bocznym
    tab1, tab2, tab3, tab4 = st.tabs([
        "⚙️ " + translate("general_settings", language=st.session_state.language),
        "📊 " + translate("allocation_settings", language=st.session_state.language),
        "🔄 " + translate("recurring_purchase_settings", language=st.session_state.language),
        "💼 " + translate("storage_cost_settings", language=st.session_state.language)
    ])
    
    # Karta 1: Ustawienia ogólne
    with tab1:
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
                "weekly": "Co tydzień",
                "monthly": "Co miesiąc",
                "quarterly": "Co kwartał"
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
                },
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("Brak danych w podsumowaniu portfela.")
    
    with tab4:
        st.subheader(translate("purchase_schedule", language=st.session_state.language))
        
        if not results['schedule'].empty:
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
