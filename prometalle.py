# /main/prometalle.py

import streamlit as st
import pandas as pd
import datetime
from config import AVAILABLE_LANGUAGES, AVAILABLE_CURRENCIES, AVAILABLE_UNITS, DEFAULT_LANGUAGE, DEFAULT_CURRENCY, DEFAULT_UNIT
from translation import translate
from purchase_schedule import generate_purchase_schedule
from metals import load_metal_prices, load_exchange_rates, convert_prices_to_currency
from portfolio import build_portfolio, aggregate_portfolio
from storage_costs import calculate_storage_costs, total_storage_cost
from charts import plot_portfolio_value

LANGUAGE_LABELS = {
    "pl": "Polski",
    "en": "English",
    "de": "Deutsch"
}

def main():
    st.set_page_config(page_title="Prometalle", page_icon="✨", layout="wide")

    st.title("Prometalle – Symulacja inwestycji w metale szlachetne")

    if 'language' not in st.session_state:
        st.session_state.language = 'pl'

    try:
        metal_prices = load_metal_prices("metal_prices.csv")
        exchange_rates = load_exchange_rates("exchange_rates.csv")
    except Exception as e:
        st.error(f"Błąd ładowania danych: {e}")
        return

    if metal_prices.empty or exchange_rates.empty:
        st.error("Brak danych w plikach CSV.")
        return

    min_date = metal_prices['Data'].min().date()
    max_date = metal_prices['Data'].max().date()

    with st.sidebar:
        st.header(translate("simulation_settings", language=st.session_state.language))

        with st.expander(translate("general_settings", language=st.session_state.language), expanded=False):
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

        st.markdown(translate("allocation_settings", language=st.session_state.language))

        gold_allocation = st.slider("Złoto (%)", 0, 100, 40, step=5)
        silver_allocation = st.slider("Srebro (%)", 0, 100, 30, step=5)
        platinum_allocation = st.slider("Platyna (%)", 0, 100, 15, step=5)
        palladium_allocation = st.slider("Pallad (%)", 0, 100, 15, step=5)

        allocation_sum = gold_allocation + silver_allocation + platinum_allocation + palladium_allocation

        st.write(f"**{translate('total_allocation', language=st.session_state.language)}:** {allocation_sum}%")

        if allocation_sum != 100:
            st.warning(translate("allocation_error", language=st.session_state.language))

        start_date = st.date_input(
            label=translate("start_date", language=st.session_state.language),
            value=min_date,
            min_value=min_date,
            max_value=max_date
        )

        end_date = st.date_input(
            label=translate("end_date", language=st.session_state.language),
            value=max_date,
            min_value=min_date,
            max_value=max_date
        )

        with st.expander(translate("recurring_purchase_settings", language=st.session_state.language), expanded=False):
            frequency = st.selectbox(
                label=translate("frequency", language=st.session_state.language),
                options=["one_time", "weekly", "monthly", "quarterly"],
                index=0
            )

            recurring_amount = 0.0
            purchase_day = 0

            if frequency != "one_time":
                recurring_amount = st.number_input(
                    label=translate("recurring_amount", language=st.session_state.language),
                    min_value=0.0,
                    value=250.0,
                    step=50.0
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

        with st.expander(translate("storage_cost_settings", language=st.session_state.language), expanded=False):
            storage_base = st.selectbox(
                translate("storage_base", language=st.session_state.language),
                options=["value", "invested_amount"],
                index=0
            )

            storage_frequency = st.selectbox(
                translate("storage_frequency", language=st.session_state.language),
                options=["monthly", "yearly"],
                index=0
            )

            storage_rate = st.number_input(
                translate("storage_rate", language=st.session_state.language),
                min_value=0.0,
                value=0.05,
                step=0.01,
                format="%.2f"
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
                index=0
            )

        run_simulation = st.button(translate("start_simulation", language=st.session_state.language))

    if run_simulation:
        if allocation_sum != 100:
            st.error(translate("allocation_error", language=st.session_state.language))
            return

        metal_prices_converted = convert_prices_to_currency(metal_prices, exchange_rates, selected_currency)

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

        if start_amount > 0:
            start_purchase = pd.DataFrame({
                'Data': [pd.to_datetime(start_date)],
                'Kwota': [start_amount]
            })
            schedule = pd.concat([start_purchase, schedule], ignore_index=True)

        st.subheader(translate("purchase_schedule", language=st.session_state.language))
        st.dataframe(schedule)

        allocation = {
            "gold": gold_allocation,
            "silver": silver_allocation,
            "platinum": platinum_allocation,
            "palladium": palladium_allocation
        }

        portfolio = build_portfolio(schedule, metal_prices_converted, allocation)
        portfolio_with_storage = calculate_storage_costs(
            portfolio,
            storage_fee_rate=storage_rate,
            storage_base=storage_base,
            storage_frequency=storage_frequency,
            vat_rate=vat_rate,
            cover_method=cover_method
        )

        st.subheader(translate("portfolio_values", language=st.session_state.language))
        st.dataframe(portfolio_with_storage)

        summary = aggregate_portfolio(portfolio_with_storage)
        st.subheader(translate("portfolio_summary", language=st.session_state.language))
        st.dataframe(summary)

        total_storage = total_storage_cost(portfolio_with_storage)
        st.success(f"{translate('storage_costs', language=st.session_state.language)}: {total_storage:.2f} {selected_currency}")

        st.subheader(translate("portfolio_chart", language=st.session_state.language))
        plot_portfolio_value(portfolio_with_storage)

if __name__ == "__main__":
    main()
