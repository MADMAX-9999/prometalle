# /main/storage_costs.py

import pandas as pd

def calculate_storage_costs(df_portfolio: pd.DataFrame, storage_fee_rate: float = 0.005, storage_base: str = "value", storage_frequency: str = "monthly", vat_rate: float = 19.0, cover_method: str = "cash") -> pd.DataFrame:
    """
    Oblicza koszty magazynowania i uwzględnia sposób ich pokrycia.

    Args:
        df_portfolio: DataFrame portfela.
        storage_fee_rate: roczna stawka opłaty magazynowej (%).
        storage_base: "value" lub "invested_amount".
        storage_frequency: "monthly" lub "yearly".
        vat_rate: podatek VAT (%).
        cover_method: sposób pokrycia kosztów (cash, gold, silver, platinum, palladium, all_metals).

    Returns:
        DataFrame z aktualizowanym portfelem.
    """

    df = df_portfolio.copy()

    # Ustalenie podstawy naliczania kosztu
    if storage_base == "value":
        base_column = "Kwota"
    else:
        base_column = "Kwota"

    # Stawka miesięczna lub roczna
    if storage_frequency == "monthly":
        period_rate = storage_fee_rate / 12 / 100
    else:
        period_rate = storage_fee_rate / 100

    vat_multiplier = 1 + vat_rate / 100

    # Grupa po dacie
    grouped = df.groupby('Data')

    results = []

    for date, group in grouped:
        period_cost_net = group[base_column].sum() * period_rate
        period_cost_gross = period_cost_net * vat_multiplier

        group = group.copy()
        group['Koszt_magazynowania'] = 0.0
        group['Kwota_po_kosztach'] = group[base_column]

        if cover_method == "cash":
            # Koszt pokrywany gotówką – bez zmiany metali
            group['Koszt_magazynowania'] = period_cost_gross / len(group)
            group['Kwota_po_kosztach'] = group[base_column] - group['Koszt_magazynowania']

        elif cover_method in ["gold", "silver", "platinum", "palladium"]:
            selected = group[group['Metal'] == cover_method.capitalize()]
            if not selected.empty:
                metal_price = selected.iloc[0]['Cena jednostkowa']
                grams_to_sell = period_cost_gross / metal_price
                group.loc[group['Metal'] == cover_method.capitalize(), 'Ilość'] -= grams_to_sell
                group['Koszt_magazynowania'] = period_cost_gross / len(group)
                group['Kwota_po_kosztach'] = group['Ilość'] * group['Cena jednostkowa']

        elif cover_method == "all_metals":
            total_value = group[base_column].sum()
            for idx, row in group.iterrows():
                share = row[base_column] / total_value if total_value > 0 else 0
                metal_share_cost = period_cost_gross * share
                metal_price = row['Cena jednostkowa']
                grams_to_sell = metal_share_cost / metal_price
                group.at[idx, 'Ilość'] -= grams_to_sell
                group.at[idx, 'Koszt_magazynowania'] = metal_share_cost
                group.at[idx, 'Kwota_po_kosztach'] = group.at[idx, 'Ilość'] * metal_price

        results.append(group)

    final_df = pd.concat(results)
    return final_df

def total_storage_cost(df_portfolio: pd.DataFrame) -> float:
    """
    Oblicza całkowity koszt magazynowania.

    Args:
        df_portfolio: DataFrame portfela.

    Returns:
        Całkowity koszt magazynowania.
    """
    if 'Koszt_magazynowania' in df_portfolio.columns:
        return df_portfolio['Koszt_magazynowania'].sum()
    else:
        return 0.0
