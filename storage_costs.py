# /main/storage_costs.py

import pandas as pd

def calculate_storage_costs(df_portfolio: pd.DataFrame, storage_fee_rate: float = 0.005) -> pd.DataFrame:
    """
    Dodaje kolumny kosztu magazynowania i wartości po kosztach.

    Args:
        df_portfolio: DataFrame z portfelem inwestycyjnym.
        storage_fee_rate: roczna stawka opłaty magazynowej (domyślnie 0,5%).

    Returns:
        DataFrame z dodatkowymi kolumnami.
    """
    df_portfolio['Koszt_magazynowania'] = df_portfolio['Kwota'] * storage_fee_rate
    df_portfolio['Kwota_po_kosztach'] = df_portfolio['Kwota'] - df_portfolio['Koszt_magazynowania']
    return df_portfolio

def total_storage_cost(df_portfolio: pd.DataFrame) -> float:
    """
    Oblicza łączny koszt magazynowania dla całego portfela.

    Args:
        df_portfolio: DataFrame z portfelem inwestycyjnym.

    Returns:
        Całkowity koszt magazynowania.
    """
    return df_portfolio['Koszt_magazynowania'].sum()
