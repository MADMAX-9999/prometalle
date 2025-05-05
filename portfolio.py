# /main/portfolio.py

import pandas as pd

def build_portfolio(schedule_df: pd.DataFrame, metal_prices_df: pd.DataFrame, allocation: dict) -> pd.DataFrame:
    """
    Buduje portfel inwestycyjny na podstawie harmonogramu zakupów i cen metali.

    Args:
        schedule_df: DataFrame z harmonogramem zakupów.
        metal_prices_df: DataFrame z cenami metali.
        allocation: procentowy podział inwestycji na metale (np. {"gold": 50, "silver": 30, "platinum": 10, "palladium": 10}).

    Returns:
        DataFrame z portfelem inwestycyjnym.
    """
    portfolio = []

    for _, row in schedule_df.iterrows():
        date = row['Data']
        amount = row['Kwota']

        prices_on_date = metal_prices_df[metal_prices_df['Data'] == date]
        if prices_on_date.empty:
            # Jeśli brak cen na daną datę, szukamy najbliższej następnej dostępnej daty
            prices_on_date = metal_prices_df[metal_prices_df['Data'] > date].head(1)

        if prices_on_date.empty:
            continue  # Jeśli nadal brak danych, pomijamy zakup

        prices_on_date = prices_on_date.iloc[0]

        for metal, percent in allocation.items():
            price = prices_on_date[f"{metal.capitalize()}_EUR"]
            metal_amount = (amount * (percent / 100)) / price
            portfolio.append({
                'Data': date,
                'Metal': metal,
                'Kwota': amount * (percent / 100),
                'Cena jednostkowa': price,
                'Ilość': metal_amount
            })

    return pd.DataFrame(portfolio)

def aggregate_portfolio(portfolio_df: pd.DataFrame) -> pd.DataFrame:
    """
    Agreguje wartości portfela według metalu.

    Args:
        portfolio_df: DataFrame z historią zakupów.

    Returns:
        DataFrame podsumowujący ilości i wartości.
    """
    summary = portfolio_df.groupby('Metal').agg({
        'Kwota': 'sum',
        'Ilość': 'sum'
    }).reset_index()
    return summary
