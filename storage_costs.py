# /prometalle_app/app/core/storage_costs.py

import pandas as pd

# Funkcja do obliczenia kosztów magazynowania
def calculate_storage_costs(
    df_portfolio: pd.DataFrame,
    storage_fee_rate: float
) -> pd.DataFrame:
    """
    Oblicza skumulowane koszty magazynowania aktywów.
    - storage_fee_rate w formacie np. 0.005 = 0.5% rocznie
    Zwraca DataFrame z dodaną kolumną 'Koszt_magazynowania_EUR'.
    """
    df_portfolio = df_portfolio.copy()

    # Oblicz koszt magazynowania dla każdej pozycji (proporcjonalnie do kwoty)
    df_portfolio['Koszt_magazynowania_EUR'] = df_portfolio['Kwota_EUR'] * storage_fee_rate

    return df_portfolio

# Funkcja do sumowania kosztów magazynowania

def total_storage_cost(df_portfolio: pd.DataFrame) -> float:
    """
    Sumuje wszystkie koszty magazynowania.
    """
    return df_portfolio['Koszt_magazynowania_EUR'].sum()
