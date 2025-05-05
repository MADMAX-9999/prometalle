# /main/charts.py

import pandas as pd
import matplotlib.pyplot as plt

# Funkcja do tworzenia wykresu wartości portfela
def plot_portfolio_value(df_portfolio: pd.DataFrame) -> None:
    """
    Rysuje wykres wartości portfela w czasie.
    """
    if df_portfolio.empty:
        return

    # Grupowanie zakupów według daty
    df_by_date = df_portfolio.groupby('Data').agg({
        'Kwota_EUR': 'sum'
    }).sort_index()

    # Skumulowana wartość portfela
    df_by_date['Wartość skumulowana EUR'] = df_by_date['Kwota_EUR'].cumsum()

    # Rysowanie wykresu
    plt.figure(figsize=(10, 6))
    plt.plot(df_by_date.index, df_by_date['Wartość skumulowana EUR'], marker='o')
    plt.title("Rozwój wartości portfela w czasie")
    plt.xlabel("Data")
    plt.ylabel("Wartość portfela (EUR)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
