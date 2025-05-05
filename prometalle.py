# /prometalle_app/app.py

import streamlit as st
from app.core.config import AVAILABLE_LANGUAGES, AVAILABLE_CURRENCIES, AVAILABLE_UNITS, DEFAULT_LANGUAGE, DEFAULT_CURRENCY, DEFAULT_UNIT
from app.core.translation import translate

# Funkcja inicjująca ekran startowy
def main():
    st.set_page_config(page_title="Prometalle", page_icon="✨", layout="centered")

    # Nagłówek powitalny
    st.title(translate("welcome"))

    # Wybór języka
    selected_language = st.selectbox(
        translate("choose_language"),
        options=AVAILABLE_LANGUAGES,
        format_func=lambda x: {"pl": "Polski", "en": "English", "de": "Deutsch"}.get(x, x)
    )

    # Wybór waluty
    selected_currency = st.selectbox(
        translate("choose_currency"),
        options=AVAILABLE_CURRENCIES
    )

    # Wybór jednostki wagi
    selected_unit = st.selectbox(
        translate("choose_unit"),
        options=AVAILABLE_UNITS,
        format_func=lambda x: {"g": "Gramy (g)", "oz": "Uncje (oz)"}.get(x, x)
    )

    # Przycisk kontynuacji
    if st.button(translate("continue")):
        st.session_state.language = selected_language
        st.session_state.currency = selected_currency
        st.session_state.unit = selected_unit
        st.success(f"Ustawiono: {selected_language.upper()}, {selected_currency}, {selected_unit}")
        st.info("Wkrótce przejdziemy do symulacji portfela!")

if __name__ == "__main__":
    main()
