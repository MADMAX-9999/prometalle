# /main/metals.py

import pandas as pd

def load_metal_prices(file_path: str) -> pd.DataFrame:
    """Ładuje ceny metali z pliku CSV."""
    prices = pd.read_csv(file_path, parse_dates=["Data"])
    prices.sort_values("Data", inplace=True)
    return prices

def load_exchange_rates(file_path: str) -> pd.DataFrame:
    """Ładuje kursy walutowe z pliku CSV."""
    rates = pd.read_csv(file_path, parse_dates=["Data"])
    rates.sort_values("Data", inplace=True)
    return rates

def convert_prices_to_currency(prices_df: pd.DataFrame, rates_df: pd.DataFrame, currency: str) -> pd.DataFrame:
    """
    Konwertuje ceny metali na wybraną walutę (EUR, USD, PLN).

    Args:
        prices_df: DataFrame z cenami metali w EUR.
        rates_df: DataFrame z kursami EUR/PLN i EUR/USD.
        currency: "EUR", "USD" lub "PLN".

    Returns:
        DataFrame z cenami metali w wybranej walucie.
    """
    merged = pd.merge(prices_df, rates_df, on="Data", how="left")

    if currency == "EUR":
        return merged
    elif currency == "USD":
        merged["Gold_EUR"] = merged["Gold_EUR"] * merged["EUR_USD"]
        merged["Silver_EUR"] = merged["Silver_EUR"] * merged["EUR_USD"]
        merged["Platinum_EUR"] = merged["Platinum_EUR"] * merged["EUR_USD"]
        merged["Palladium_EUR"] = merged["Palladium_EUR"] * merged["EUR_USD"]
    elif currency == "PLN":
        merged["Gold_EUR"] = merged["Gold_EUR"] * merged["EUR_PLN"]
        merged["Silver_EUR"] = merged["Silver_EUR"] * merged["EUR_PLN"]
        merged["Platinum_EUR"] = merged["Platinum_EUR"] * merged["EUR_PLN"]
        merged["Palladium_EUR"] = merged["Palladium_EUR"] * merged["EUR_PLN"]
    else:
        raise ValueError(f"Unsupported currency: {currency}")

    return merged
