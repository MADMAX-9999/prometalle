# /main/prometalle.py

import streamlit as st
from config import AVAILABLE_LANGUAGES, AVAILABLE_CURRENCIES, AVAILABLE_UNITS, DEFAULT_LANGUAGE, DEFAULT_CURRENCY, DEFAULT_UNIT
from translation import translate
from purchase_schedule import generate_purchase_schedule
from metals import load_metal_prices
from portfolio import build_portfolio, aggregate_portfolio
from storage_costs import calculate_storage_costs, total_storage_cost
from charts import plot_portfolio_value
import pandas as pd
import datetime

# Funkcja inicjująca ekran startowy i symulację
def main():
    st.set_page_config(page_title="Prometalle", page_icon="✨", layout="wide")

    st.title("Prometalle – Symulacja inwestycji w metale szlachetne")

    with st.sidebar:
        st.header("Ustawienia symulacji")
        selected_language = st.selectbox(
            translate("choose_language"),
            options=AVAILABLE_LANGUAGES,
            format_func=lambda x: {"pl": "Polski", "en": "English", "de": "Deutsch"}.get(x, x)
        )
        selected_currency = st.selectbox(
            translate("choose_currency"),
            options=AVAILABLE_CURRENCIES
        )
        selected_unit = st.selectbox(
            translate("choose_unit"),
            options=AVAILABLE_UNITS,
            format_func=lambda x: {"g": "Gramy (g)", "oz": "Uncje (oz)"}.get(x, x)
        )

        start_amount = st.number_input("Kwota początkowa inwestycji (EUR)", min_value=100.0, value=10000.0, step=100.0)
        recurring_amount = st.number_input("Kwota zakupu systematycznego (EUR)", min_value=0.0, value=500.0, step=50.0)

        frequency = st.selectbox("Częstotliwość zakupów", options=["monthly", "quarterly", "weekly"])
        purchase_day = st.number_input("Dzień zakupu (tydzień: 0-6, miesiąc: 1-31)", min_value=0, max_value=31, value=15)

        years = st.slider("Okres inwestycji (lata)", 1, 30, 10)

        run_simulation = st.button("Rozpocznij symulację")

    if run_simulation:
        # Generowanie harmonogramu
        start_date = datetime.date.today()
        end_date = start_date + datetime.timedelta(days=years * 365)

        if recurring_amount > 0:
            schedule = generate_purchase_schedule(
                start_date=start_date.strftime("%Y-%m-%d"),
                end_date=end_date.strftime("%Y-%m-%d"),
                frequency=frequency,
                purchase_day=purchase_day,
                purchase_amount=recurring_amount
            )
        else:
            schedule = pd.DataFrame()

        if start_amount > 0:
            start_purchase = pd.DataFrame({
                'Data': [pd.to_datetime(start_date)],
                'Kwota': [start_amount]
            })
            schedule = pd.concat([start_purchase, schedule], ignore_index=True)

        st.subheader("Harmonogram zakupów")
        st.dataframe(schedule)

        # Załaduj ceny metali (tymczasowe dane przykładowe)
        metal_prices = load_metal_prices("metal_prices.csv")

        # Alokacja metali (przykład)
        allocation = {"gold": 50, "silver": 30, "platinum": 10, "palladium": 10}

        # Budowa portfela
        portfolio = build_portfolio(schedule, metal_prices, allocation)
        portfolio_with_storage = calculate_storage_costs(portfolio, storage_fee_rate=0.005)

        st.subheader("Zakupy i wartości metali")
        st.dataframe(portfolio_with_storage)

        # Podsumowanie
        summary = aggregate_portfolio(portfolio_with_storage)
        st.subheader("Podsumowanie portfela")
        st.dataframe(summary)

        # Łączne koszty magazynowania
        total_storage = total_storage_cost(portfolio_with_storage)
        st.success(f"Łączne koszty magazynowania: {total_storage:.2f} EUR")

        # Wykres wartości portfela
        st.subheader("Wykres wartości portfela")
        plot_portfolio_value(portfolio_with_storage)

if __name__ == "__main__":
    main()
