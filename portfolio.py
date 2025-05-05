# /prometalle_app/app/core/portfolio.py

import pandas as pd
from app.core.metals import get_metal_price

# Funkcja do budowania portfela inwestycyjnego
def build_portfolio(
    purchase_schedule: pd.DataFrame,
    df_metals: pd.DataFrame,
    allocation: dict,
    base_currency: str = 'EUR'
) -> pd.DataFrame:
    """
    Tworzy portfel inwestora na podstawie harmonogramu zakupów, cen metali i alokacji procentowej.
    """
    portfolio = []

    for idx, row in purchase_schedule.iterrows():
        purchase_date = row['Data']
        amount_total = row['Kwota']

        for metal, percent in allocation.items():
            allocated_amount = amount_total * percent / 100.0

            # Pobierz cenę metalu w dniu zakupu (lub najbliższego dnia)
            price_per_gram_eur = get_metal_price(df_metals, metal, purchase_date)

            if price_per_gram_eur > 0:
                grams_purchased = allocated_amount / price_per_gram_eur
            else:
                grams_purchased = 0

            portfolio.append({
                'Data': purchase_date,
                'Metal': metal,
                'Kwota_EUR': allocated_amount,
                'Cena_EUR_g': price_per_gram_eur,
                'Gramatura': grams_purchased
            })

    return pd.DataFrame(portfolio)

# Funkcja do agregowania portfela w czasie
def aggregate_portfolio(df_portfolio: pd.DataFrame) -> pd.DataFrame:
    """
    Sumuje gramaturę metali w czasie.
    """
    df_agg = df_portfolio.groupby(['Metal']).agg({
        'Kwota_EUR': 'sum',
        'Gramatura': 'sum'
    }).reset_index()

    return df_agg
