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

LANGUAGE_LABELS = {
    "pl": "Polski",
    "en": "English",
    "de": "Deutsch"
}

# Funkcja inicjująca ekran startowy i symulację
def main():
    st.set_page_config(page_title="Prometalle", page_icon="✨", layout="wide")

    st.title("Prometalle – Symulacja inwestycji w metale szlachetne")

    if 'language' not in st.session_state:
        st.session_state.language = 'pl'

    with st.sidebar:
        st.header(translate("simulation_settings", language=st.session_state.language))

        selected_language_label = st.selectbox(
            translate("choose_language", language=st.session_state.language),
            options=[LANGUAGE_LABELS[code] for code in AVAILABLE_LANGUAGES],
            index=AVAILABLE_LANGUAGES.index('pl')
        )
        selected_language = [code for code, label in LANGUAGE_LABELS.items() if label == selected_language_label][0]
        st.session_state.language = selected_language

        selected_currency = st.selectbox(
            translate("choose_currency", language=st.session_state.language),
            options=AVAILABLE_CURRENCIES,
            index=AVAILABLE_CURRENCIES.index('EUR')
        )
        selected_unit = st.selectbox(
            translate("choose_unit", language=st.session_state.language),
            options=AVAILABLE_UNITS,
            index=AVAILABLE_UNITS.index('g'),
            format_func=lambda x: {"g": "Gramy (g)", "oz": "Uncje (oz)"}.get(x, x)
        )

        start_amount = st.number_input(
            label=translate("start_amount", language=st.session_state.language),
            min_value=100.0,
            value=100000.0,
            step=100.0
        )
        recurring_amount = st.number_input(
            label=translate("recurring_amount", language=st.session_state.language),
            min_value=0.0,
            value=250.0,
            step=50.0
        )

        frequency = st.selectbox(
            label=translate("frequency", language=st.session_state.language),
            options=["weekly", "monthly", "quarterly"],
            index=0
        )

        if frequency == "weekly":
            purchase_day = st.selectbox(
                translate("purchase_day_weekly", language=st.session_state.language),
                options=list(range(0, 5)),
                index=0
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

        years = st.slider(
            label=translate("investment_period", language=st.session_state.language),
            min_value=1,
            max_value=30,
            value=10
        )

        run_simulation = st.button(translate("start_simulation", language=st.session_state.language))

    if run_simulation:
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

        st.subheader(translate("purchase_schedule", language=st.session_state.language))
        st.dataframe(schedule)

        metal_prices = load_metal_prices("metal_prices.csv")

        allocation = {"gold": 50, "silver": 30, "platinum": 10, "palladium": 10}

        portfolio = build_portfolio(schedule, metal_prices, allocation)
        portfolio_with_storage = calculate_storage_costs(portfolio, storage_fee_rate=0.005)

        st.subheader(translate("portfolio_values", language=st.session_state.language))
        st.dataframe(portfolio_with_storage)

        summary = aggregate_portfolio(portfolio_with_storage)
        st.subheader(translate("portfolio_summary", language=st.session_state.language))
        st.dataframe(summary)

        total_storage = total_storage_cost(portfolio_with_storage)
        st.success(f"{translate('storage_costs', language=st.session_state.language)}: {total_storage:.2f} EUR")

        st.subheader(translate("portfolio_chart", language=st.session_state.language))
        plot_portfolio_value(portfolio_with_storage)

if __name__ == "__main__":
    main()
