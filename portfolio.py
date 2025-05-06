# /main/portfolio.py

import pandas as pd

def build_portfolio(schedule: pd.DataFrame, metal_prices: pd.DataFrame, allocation: dict, purchase_margin: float = 2.0) -> pd.DataFrame:
    """
    Buduje rejestr operacji zakupowych na podstawie harmonogramu i alokacji.

    Args:
        schedule: DataFrame z harmonogramem zakupów.
        metal_prices: DataFrame z cenami metali.
        allocation: Słownik alokacji procentowej.
        purchase_margin: Marża (%) dodawana do ceny zakupu.

    Returns:
        DataFrame z rejestrem operacji.
    """
    portfolio_records = []

    for _, row in schedule.iterrows():
        date = pd.to_datetime(row['Data'])
        amount = row['Kwota']

        # Szukamy ceny na daną datę
        daily_prices = metal_prices[metal_prices['Data'] == date]

        if daily_prices.empty:
            # Jeśli brak cen w dniu zakupu, bierzemy pierwszy następny dostępny dzień
            daily_prices = metal_prices[metal_prices['Data'] > date].head(1)
            if daily_prices.empty:
                continue

        for metal, alloc_percent in allocation.items():
            if alloc_percent > 0:
                alloc_amount = amount * (alloc_percent / 100)
                metal_price = daily_prices[metal.capitalize()].values[0]
                price_with_margin = metal_price * (1 + purchase_margin / 100)
                quantity = alloc_amount / price_with_margin

                portfolio_records.append({
                    'Data': date,
                    'Typ operacji': 'Zakup',
                    'Metal': metal.capitalize(),
                    'Ilość': quantity,
                    'Cena jednostkowa': price_with_margin,
                    'Kwota operacji': alloc_amount,
                    'Koszt magazynowania': 0.0,
                    'Sprzedaż na koszty': 0.0
                })

    portfolio_df = pd.DataFrame(portfolio_records)
    return portfolio_df

def aggregate_portfolio(df_portfolio: pd.DataFrame) -> pd.DataFrame:
    """
    Agreguje wartości końcowe portfela.

    Args:
        df_portfolio: DataFrame rejestru operacji.

    Returns:
        DataFrame z podsumowaniem wartości metali.
    """
    if df_portfolio.empty:
        return pd.DataFrame()

    current_portfolio = df_portfolio.copy()
    metals_summary = current_portfolio.groupby('Metal').agg({
        'Ilość': 'sum',
        'Kwota operacji': 'sum'
    }).reset_index()

    return metals_summary
