# /prometalle_app/app/core/inflation.py

import pandas as pd
from app.core.config import DEFAULT_INFLATION

# Funkcja do ładowania danych o inflacji
def load_inflation_rates(file_path: str) -> pd.DataFrame:
    """
    Ładuje dane o inflacji z pliku CSV.
    Jeśli plik nie istnieje lub jest błędny, zwraca domyślne wartości inflacji.
    """
    try:
        df = pd.read_csv(file_path)
        if {'Rok', 'waluta', 'roczna_inflacja'}.issubset(df.columns):
            return df
        else:
            raise ValueError("Brak wymaganych kolumn w pliku CSV.")
    except Exception as e:
        print(f"Błąd podczas ładowania pliku inflacji: {e}")
        # Zwróć domyślne inflacje w prostym DataFrame
        data = []
        for year in range(1997, 2030):
            for currency, rate in DEFAULT_INFLATION.items():
                data.append({'Rok': year, 'waluta': currency, 'roczna_inflacja': rate})
        return pd.DataFrame(data)

# Funkcja do pobrania inflacji dla konkretnego roku i waluty
def get_inflation_rate(df_inflation: pd.DataFrame, year: int, currency: str) -> float:
    """
    Zwraca roczną inflację dla podanego roku i waluty.
    Jeśli brak danych dla danego roku, zwraca domyślną wartość dla waluty.
    """
    try:
        rate = df_inflation[(df_inflation['Rok'] == year) & (df_inflation['waluta'] == currency)]['roczna_inflacja'].values
        if len(rate) > 0:
            return float(rate[0])
        else:
            return DEFAULT_INFLATION.get(currency, 0.02)
    except:
        return DEFAULT_INFLATION.get(currency, 0.02)
