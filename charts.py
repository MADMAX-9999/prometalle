# /main/charts.py

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

def plot_portfolio_value(df_portfolio: pd.DataFrame):
    """
    Rysuje wykres rzeczywistej wartości depozytu w czasie.

    Args:
        df_portfolio: DataFrame z historią inwestycji.
    """
    if df_portfolio.empty:
        st.warning("Brak danych do wyświetlenia wykresu.")
        return

    # Obliczamy wartość depozytu: ilość * aktualna cena metalu
    df_portfolio['Wartość depozytu'] = df_portfolio['Ilość'] * df_portfolio['Cena jednostkowa']

    # Grupujemy po dacie i sumujemy wartość depozytu
    df_by_date = df_portfolio.groupby('Data').agg({
        'Wartość depozytu': 'sum'
    }).reset_index()

    # Rysujemy wykres wartości depozytu
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df_by_date['Data'], df_by_date['Wartość depozytu'], marker='o')
    ax.set_title("Wartość depozytu w czasie")
    ax.set_xlabel("Data")
    ax.set_ylabel("Wartość depozytu")
    ax.grid(True)
    fig.autofmt_xdate()

    st.pyplot(fig)
