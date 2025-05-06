# /main/charts.py

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

def plot_portfolio_value(df_portfolio: pd.DataFrame):
    """
    Rysuje wykres wartości depozytu w czasie.

    Args:
        df_portfolio: DataFrame z historią inwestycji.
    """
    if df_portfolio.empty:
        st.warning("Brak danych do wyświetlenia wykresu.")
        return

    df_by_date = df_portfolio.groupby('Data').agg({
        'Kwota': 'sum'
    }).reset_index()

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df_by_date['Data'], df_by_date['Kwota'], marker='o')
    ax.set_title("Wartość depozytu w czasie")
    ax.set_xlabel("Data")
    ax.set_ylabel("Wartość depozytu")
    ax.grid(True)
    fig.autofmt_xdate()

    st.pyplot(fig)
