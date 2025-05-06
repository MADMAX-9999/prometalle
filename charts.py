# /main/charts.py

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

def plot_portfolio_value(df_portfolio: pd.DataFrame):
    """
    Rysuje wykres wartości portfela w czasie.

    Args:
        df_portfolio: DataFrame z historią inwestycji.
    """
    if df_portfolio.empty:
        st.warning("Brak danych do wyświetlenia wykresu.")
        return

    df_by_date = df_portfolio.groupby('Data').agg({
        'Kwota_po_kosztach': 'sum'
    }).reset_index()

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df_by_date['Data'], df_by_date['Kwota_po_kosztach'], marker='o')
    ax.set_title("Rozwój wartości portfela w czasie")
    ax.set_xlabel("Data")
    ax.set_ylabel("Wartość portfela")
    ax.grid(True)
    fig.autofmt_xdate()

    st.pyplot(fig)
