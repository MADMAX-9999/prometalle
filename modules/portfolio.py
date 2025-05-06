# /modules/portfolio.py
# Moduł obsługi operacji na portfelu metali szlachetnych

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Union

def build_portfolio(
    schedule: pd.DataFrame,
    metal_prices: pd.DataFrame,
    allocation: dict,
    purchase_margin: float = 2.0
) -> pd.DataFrame:
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

    # Sprawdzamy, czy harmonogram i ceny metali nie są puste
    if schedule.empty or metal_prices.empty:
        return pd.DataFrame()

    # Sprawdzamy, czy alokacja jest poprawna (suma = 100%)
    allocation_sum = sum(allocation.values())
    if allocation_sum != 100:
        raise ValueError(f"Suma alokacji musi wynosić 100%, aktualna wartość: {allocation_sum}%")

    # Dla każdego wpisu w harmonogramie zakupów
    for _, row in schedule.iterrows():
        date = pd.to_datetime(row['Data'])
        amount = row['Kwota']

        # Szukamy ceny na daną datę
        daily_prices = metal_prices[metal_prices['Data'] == date]

        if daily_prices.empty:
            # Jeśli brak cen w dniu zakupu, bierzemy pierwszy następny dostępny dzień
            daily_prices = metal_prices[metal_prices['Data'] > date].head(1)
            if daily_prices.empty:
                # Jeśli brak cen po dacie zakupu, bierzemy ostatni dostępny dzień przed zakupem
                daily_prices = metal_prices[metal_prices['Data'] < date].tail(1)
                if daily_prices.empty:
                    # Jeśli nadal brak cen, pomijamy ten zakup
                    continue

        # Dla każdego metalu w alokacji
        for metal, alloc_percent in allocation.items():
            if alloc_percent > 0:
                alloc_amount = amount * (alloc_percent / 100)
                
                # Określamy kolumnę z ceną metalu
                metal_column = metal.capitalize()
                
                if metal_column in daily_prices.columns:
                    metal_price = daily_prices[metal_column].iloc[0]
                    price_with_margin = metal_price * (1 + purchase_margin / 100)
                    quantity = alloc_amount / price_with_margin

                    portfolio_records.append({
                        'Data': date,
                        'Typ operacji': 'Zakup',
                        'Metal': metal.capitalize(),
                        'Ilość': quantity,
                        'Cena jednostkowa': price_with_margin,
                        'Kwota operacji': alloc_amount,
                        'Koszt_magazynowania': 0.0,
                        'Kwota_po_kosztach': alloc_amount
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

    # Pobieramy operacje z odpowiednimi ilościami
    current_portfolio = df_portfolio.copy()
    
    # Grupujemy po metalu i obliczamy sumy
    metals_summary = current_portfolio.groupby('Metal').agg({
        'Ilość': 'sum',
        'Kwota operacji': 'sum',
        'Cena jednostkowa': 'last'  # Ostatnia znana cena
    }).reset_index()
    
    # Dodajemy kolumnę z aktualną wartością
    metals_summary['Wartość aktualna'] = metals_summary['Ilość'] * metals_summary['Cena jednostkowa']
    
    # Obliczamy zysk/stratę
    metals_summary['Zysk/Strata'] = metals_summary['Wartość aktualna'] - metals_summary['Kwota operacji']
    
    # Obliczamy ROI
    metals_summary['ROI (%)'] = (metals_summary['Zysk/Strata'] / metals_summary['Kwota operacji'] * 100)
    metals_summary['ROI (%)'] = metals_summary['ROI (%)'].replace([np.inf, -np.inf], 0)
    metals_summary['ROI (%)'] = metals_summary['ROI (%)'].fillna(0)
    
    return metals_summary

def rebalance_portfolio(
    df_portfolio: pd.DataFrame,
    metal_prices: pd.DataFrame,
    target_allocation: Dict[str, float],
    rebalance_date: datetime,
    sale_margin: float = 1.5
) -> pd.DataFrame:
    """
    Wykonuje rebalancing portfela do docelowej alokacji.

    Args:
        df_portfolio: DataFrame z rejestrem operacji.
        metal_prices: DataFrame z cenami metali.
        target_allocation: Słownik z docelową alokacją (%).
        rebalance_date: Data rebalancingu.
        sale_margin: Marża (%) odejmowana od ceny sprzedaży.

    Returns:
        DataFrame z zaktualizowanym rejestrem operacji.
    """
    if df_portfolio.empty or metal_prices.empty:
        return df_portfolio

    # Sprawdzamy, czy suma alokacji to 100%
    allocation_sum = sum(target_allocation.values())
    if abs(allocation_sum - 100) > 0.01:  # Małe zaokrąglenie jest tolerowane
        raise ValueError(f"Suma alokacji musi wynosić 100%, aktualna wartość: {allocation_sum}%")

    # Pobieramy ceny metali na datę rebalancingu
    daily_prices = metal_prices[metal_prices['Data'] >= rebalance_date].head(1)
    
    if daily_prices.empty:
        # Jeśli brak cen na datę rebalancingu, bierzemy ostatnią dostępną datę
        daily_prices = metal_prices.tail(1)
        if daily_prices.empty:
            # Jeśli nadal brak cen, zwracamy portfel bez zmian
            return df_portfolio

    # Agregujemy obecny stan portfela
    current_holdings = df_portfolio.groupby('Metal').agg({
        'Ilość': 'sum'
    }).reset_index()

    # Obliczamy obecną wartość każdego metalu i całego portfela
    total_value = 0
    current_values = {}
    
    for _, row in current_holdings.iterrows():
        metal = row['Metal']
        quantity = row['Ilość']
        
        if metal.lower() in [m.lower() for m in target_allocation.keys()]:
            price_column = metal
            if price_column in daily_prices.columns:
                metal_price = daily_prices[price_column].iloc[0]
                metal_value = quantity * metal_price
                current_values[metal.lower()] = {
                    'quantity': quantity,
                    'price': metal_price,
                    'value': metal_value
                }
                total_value += metal_value

    # Jeśli portfel ma wartość zerową, nie wykonujemy rebalancingu
    if total_value == 0:
        return df_portfolio

    # Obliczamy docelową wartość dla każdego metalu
    target_values = {}
    for metal, alloc in target_allocation.items():
        target_values[metal.lower()] = total_value * (alloc / 100)

    # Rejestr operacji rebalancingu
    rebalance_records = []

    # Dla każdego metalu porównujemy obecną i docelową wartość
    for metal, target_value in target_values.items():
        current_value = current_values.get(metal.lower(), {'value': 0, 'quantity': 0, 'price': 0})
        value_diff = target_value - current_value['value']
        
        # Jeśli różnica jest istotna (powyżej 1% wartości portfela), wykonujemy operację
        if abs(value_diff) > (total_value * 0.01):
            metal_price = current_value['price']
            
            if metal_price > 0:
                if value_diff > 0:
                    # Kupujemy więcej metalu
                    quantity_to_buy = value_diff / metal_price
                    purchase_price = metal_price * (1 + sale_margin / 100)  # Z marżą zakupu
                    
                    rebalance_records.append({
                        'Data': rebalance_date,
                        'Typ operacji': 'Rebalancing - Zakup',
                        'Metal': metal.capitalize(),
                        'Ilość': quantity_to_buy,
                        'Cena jednostkowa': purchase_price,
                        'Kwota operacji': value_diff,
                        'Koszt_magazynowania': 0.0,
                        'Kwota_po_kosztach': value_diff
                    })
                else:
                    # Sprzedajemy nadmiar metalu
                    quantity_to_sell = abs(value_diff) / metal_price
                    sale_price = metal_price * (1 - sale_margin / 100)  # Z marżą sprzedaży
                    
                    rebalance_records.append({
                        'Data': rebalance_date,
                        'Typ operacji': 'Rebalancing - Sprzedaż',
                        'Metal': metal.capitalize(),
                        'Ilość': -quantity_to_sell,  # Ujemna ilość oznacza sprzedaż
                        'Cena jednostkowa': sale_price,
                        'Kwota operacji': -abs(value_diff),  # Ujemna kwota oznacza wpływ gotówki
                        'Koszt_magazynowania': 0.0,
                        'Kwota_po_kosztach': -abs(value_diff)
                    })

    # Dodajemy operacje rebalancingu do portfela
    if rebalance_records:
        rebalance_df = pd.DataFrame(rebalance_records)
        updated_portfolio = pd.concat([df_portfolio, rebalance_df], ignore_index=True)
        return updated_portfolio
    else:
        # Jeśli nie było operacji rebalancingu, zwracamy portfel bez zmian
        return df_portfolio

def execute_sell_operation(
    df_portfolio: pd.DataFrame,
    metal: str,
    quantity: float,
    sale_date: datetime,
    metal_prices: pd.DataFrame,
    sale_margin: float = 1.5
) -> Tuple[pd.DataFrame, float]:
    """
    Wykonuje operację sprzedaży metalu z portfela.

    Args:
        df_portfolio: DataFrame z rejestrem operacji.
        metal: Nazwa metalu do sprzedaży.
        quantity: Ilość metalu do sprzedaży.
        sale_date: Data sprzedaży.
        metal_prices: DataFrame z cenami metali.
        sale_margin: Marża (%) odejmowana od ceny sprzedaży.

    Returns:
        Krotka (zaktualizowany portfel, przychód ze sprzedaży).
    """
    if df_portfolio.empty or quantity <= 0:
        return df_portfolio, 0.0

    # Normalizujemy nazwę metalu
    metal = metal.capitalize()

    # Sprawdzamy, czy mamy wystarczającą ilość metalu w portfelu
    current_holdings = df_portfolio.groupby('Metal').agg({
        'Ilość': 'sum'
    }).reset_index()
    
    metal_holding = current_holdings[current_holdings['Metal'] == metal]
    if metal_holding.empty or metal_holding['Ilość'].iloc[0] < quantity:
        raise ValueError(f"Niewystarczająca ilość metalu {metal} w portfelu. Dostępne: {metal_holding['Ilość'].iloc[0] if not metal_holding.empty else 0}, Żądane: {quantity}")

    # Pobieramy cenę metalu na datę sprzedaży
    daily_prices = metal_prices[metal_prices['Data'] >= sale_date].head(1)
    
    if daily_prices.empty:
        # Jeśli brak cen na datę sprzedaży, bierzemy ostatnią dostępną datę
        daily_prices = metal_prices.tail(1)
        if daily_prices.empty:
            raise ValueError("Brak danych o cenach metali.")

    # Sprawdzamy, czy kolumna z ceną metalu istnieje
    if metal not in daily_prices.columns:
        raise ValueError(f"Brak danych o cenie metalu {metal}.")

    # Pobieramy cenę metalu
    metal_price = daily_prices[metal].iloc[0]
    sale_price = metal_price * (1 - sale_margin / 100)  # Z marżą sprzedaży
    
    # Obliczamy przychód ze sprzedaży
    sale_revenue = quantity * sale_price

    # Dodajemy operację sprzedaży do rejestru
    sale_operation = pd.DataFrame([{
        'Data': sale_date,
        'Typ operacji': 'Sprzedaż',
        'Metal': metal,
        'Ilość': -quantity,  # Ujemna ilość oznacza sprzedaż
        'Cena jednostkowa': sale_price,
        'Kwota operacji': -sale_revenue,  # Ujemna kwota oznacza wpływ gotówki
        'Koszt_magazynowania': 0.0,
        'Kwota_po_kosztach': -sale_revenue
    }])

    # Aktualizujemy portfel
    updated_portfolio = pd.concat([df_portfolio, sale_operation], ignore_index=True)
    
    return updated_portfolio, sale_revenue

def calculate_portfolio_value(
    df_portfolio: pd.DataFrame,
    metal_prices: pd.DataFrame,
    date: Optional[datetime] = None
) -> float:
    """
    Oblicza wartość portfela na daną datę.

    Args:
        df_portfolio: DataFrame z rejestrem operacji.
        metal_prices: DataFrame z cenami metali.
        date: Data wyceny portfela (opcjonalnie, domyślnie ostatnia dostępna).

    Returns:
        Wartość portfela.
    """
    if df_portfolio.empty or metal_prices.empty:
        return 0.0

    # Jeśli nie podano daty, używamy ostatniej dostępnej
    if date is None:
        daily_prices = metal_prices.iloc[-1]
    else:
        # Pobieramy ceny metali na podaną datę lub najbliższą dostępną
        daily_prices = metal_prices[metal_prices['Data'] <= date].iloc[-1] if not metal_prices[metal_prices['Data'] <= date].empty else metal_prices.iloc[0]

    # Agregujemy obecny stan portfela
    current_holdings = df_portfolio.groupby('Metal').agg({
        'Ilość': 'sum'
    }).reset_index()

    # Obliczamy wartość portfela
    portfolio_value = 0.0
    
    for _, row in current_holdings.iterrows():
        metal = row['Metal']
        quantity = row['Ilość']
        
        if metal in daily_prices:
            metal_price = daily_prices[metal]
            metal_value = quantity * metal_price
            portfolio_value += metal_value

    return portfolio_value

def calculate_metal_weights(df_portfolio: pd.DataFrame, metal_prices: pd.DataFrame) -> pd.DataFrame:
    """
    Oblicza wagi poszczególnych metali w portfelu.

    Args:
        df_portfolio: DataFrame z rejestrem operacji.
        metal_prices: DataFrame z cenami metali.

    Returns:
        DataFrame z wagami metali.
    """
    if df_portfolio.empty or metal_prices.empty:
        return pd.DataFrame()

    # Pobieramy ostatnie dostępne ceny metali
    latest_prices = metal_prices.iloc[-1]

    # Agregujemy stan portfela
    current_holdings = df_portfolio.groupby('Metal').agg({
        'Ilość': 'sum'
    }).reset_index()

    # Obliczamy wartość każdego metalu
    metal_values = []
    total_value = 0.0
    
    for _, row in current_holdings.iterrows():
        metal = row['Metal']
        quantity = row['Ilość']
        
        if metal in latest_prices:
            metal_price = latest_prices[metal]
            metal_value = quantity * metal_price
            metal_values.append({
                'Metal': metal,
                'Ilość': quantity,
                'Cena': metal_price,
                'Wartość': metal_value
            })
            total_value += metal_value

    # Obliczamy wagi metali
    weights_df = pd.DataFrame(metal_values)
    
    if not weights_df.empty and total_value > 0:
        weights_df['Waga (%)'] = weights_df['Wartość'] / total_value * 100
    else:
        weights_df['Waga (%)'] = 0.0

    return weights_df

def calculate_average_purchase_price(df_portfolio: pd.DataFrame, metal: str) -> float:
    """
    Oblicza średnią cenę zakupu danego metalu.

    Args:
        df_portfolio: DataFrame z rejestrem operacji.
        metal: Nazwa metalu.

    Returns:
        Średnia cena zakupu.
    """
    if df_portfolio.empty:
        return 0.0

    # Normalizujemy nazwę metalu
    metal = metal.capitalize()

    # Filtrujemy operacje zakupu danego metalu
    purchases = df_portfolio[(df_portfolio['Metal'] == metal) & (df_portfolio['Typ operacji'] == 'Zakup')]
    
    if purchases.empty:
        return 0.0

    # Obliczamy średnią ważoną cenę zakupu
    total_quantity = purchases['Ilość'].sum()
    total_cost = (purchases['Ilość'] * purchases['Cena jednostkowa']).sum()
    
    if total_quantity > 0:
        return total_cost / total_quantity
    else:
        return 0.0

def calculate_portfolio_performance(
    df_portfolio: pd.DataFrame,
    metal_prices: pd.DataFrame,
    start_date: datetime,
    end_date: datetime,
    frequency: str = 'monthly'
) -> pd.DataFrame:
    """
    Oblicza wyniki portfela w czasie.

    Args:
        df_portfolio: DataFrame z rejestrem operacji.
        metal_prices: DataFrame z cenami metali.
        start_date: Data początkowa.
        end_date: Data końcowa.
        frequency: Częstotliwość obliczeń ('daily', 'weekly', 'monthly', 'quarterly', 'yearly').

    Returns:
        DataFrame z wynikami portfela.
    """
    if df_portfolio.empty or metal_prices.empty:
        return pd.DataFrame()

    # Określamy częstotliwość dat
    if frequency == 'daily':
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    elif frequency == 'weekly':
        date_range = pd.date_range(start=start_date, end=end_date, freq='W')
    elif frequency == 'monthly':
        date_range = pd.date_range(start=start_date, end=end_date, freq='MS')
    elif frequency == 'quarterly':
        date_range = pd.date_range(start=start_date, end=end_date, freq='QS')
    elif frequency == 'yearly':
        date_range = pd.date_range(start=start_date, end=end_date, freq='YS')
    else:
        date_range = pd.date_range(start=start_date, end=end_date, freq='MS')  # Domyślnie miesięcznie

    # Filtrujemy ceny metali w zakresie dat
    filtered_prices = metal_prices[(metal_prices['Data'] >= start_date) & (metal_prices['Data'] <= end_date)]
    
    # Przygotowujemy dane wyników
    performance_data = []
    
    for date in date_range:
        # Filtrujemy operacje do danej daty
        operations_until_date = df_portfolio[df_portfolio['Data'] <= date]
        
        if operations_until_date.empty:
            continue
        
        # Obliczamy wartość portfela na daną datę
        portfolio_value = calculate_portfolio_value(operations_until_date, filtered_prices, date)
        
        # Obliczamy łączną zainwestowaną kwotę do danej daty
        invested_amount = operations_until_date[operations_until_date['Typ operacji'] == 'Zakup']['Kwota operacji'].sum()
        
        # Obliczamy zysk/stratę
        profit_loss = portfolio_value - invested_amount
        
        # Obliczamy ROI
        roi = (profit_loss / invested_amount * 100) if invested_amount > 0 else 0.0
        
        # Dodajemy dane do wyników
        performance_data.append({
            'Data': date,
            'Wartość portfela': portfolio_value,
            'Zainwestowana kwota': invested_amount,
            'Zysk/Strata': profit_loss,
            'ROI (%)': roi
        })
    
    return pd.DataFrame(performance_data)
