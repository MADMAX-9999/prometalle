# /prometalle_app/app/core/metals.py

import pandas as pd

# Funkcja do ładowania danych o cenach metali
def load_metal_prices(file_path: str) -> pd.DataFrame:
    """
    Ładuje ceny metali z pliku CSV.
    Plik powinien zawierać kolumny: 'Data', 'metal', 'cena_w_EUR_g'.
    """
    try:
        df = pd.read_csv(file_path, parse_dates=['Data'])
        if {'Data', 'metal', 'cena_w_EUR_g'}.issubset(df.columns):
            return df
        else:
            raise ValueError("Brak wymaganych kolumn w pliku CSV.")
    except Exception as e:
        print(f"Błąd podczas ładowania pliku cen metali: {e}")
        return pd.DataFrame(columns=['Data', 'metal', 'cena_w_EUR_g'])

# Funkcja do pobrania ceny danego metalu w konkretnej dacie
def get_metal_price(df_metals: pd.DataFrame, metal: str, date: pd.Timestamp) -> float:
    """
    Zwraca cenę metalu na podaną datę.
    Jeśli brak ceny dla dokładnej daty, szuka najbliższego dnia po dacie.
    Jeśli nadal brak - zwraca 0.
    """
    try:
        df_filtered = df_metals[(df_metals['metal'] == metal) & (df_metals['Data'] >= date)].sort_values('Data')
        if not df_filtered.empty:
            return float(df_filtered.iloc[0]['cena_w_EUR_g'])
        else:
            return 0.0
    except:
        return 0.0
