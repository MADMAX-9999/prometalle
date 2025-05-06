# /modules/analysis.py
# Moduł do analizy inwestycji w metale szlachetne

import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Union
from modules.inflation import get_inflation_rate

def calculate_roi(
    portfolio: pd.DataFrame,
    initial_investment: float,
    end_date: datetime
) -> Tuple[float, float, float]:
    """
    Oblicza stopę zwrotu z inwestycji (ROI).

    Args:
        portfolio: DataFrame z historią inwestycji.
        initial_investment: Początkowa kwota inwestycji.
        end_date: Data końcowa inwestycji.

    Returns:
        Tuple zawierający (ROI procentowo, wartość końcową, zysk/stratę).
    """
    if portfolio.empty:
        return 0.0, 0.0, 0.0
    
    # Obliczamy końcową wartość portfela
    portfolio_value = (portfolio['Ilość'] * portfolio['Cena jednostkowa']).sum()
    
    # Obliczamy zysk/stratę
    profit_loss = portfolio_value - initial_investment
    
    # Obliczamy ROI (%)
    if initial_investment > 0:
        roi_percent = (profit_loss / initial_investment) * 100
    else:
        roi_percent = 0.0
    
    return roi_percent, portfolio_value, profit_loss

def calculate_annualized_return(
    portfolio: pd.DataFrame,
    schedule: pd.DataFrame,
    end_date: datetime
) -> float:
    """
    Oblicza annualizowaną stopę zwrotu (CAGR).

    Args:
        portfolio: DataFrame z historią inwestycji.
        schedule: DataFrame z harmonogramem zakupów.
        end_date: Data końcowa inwestycji.

    Returns:
        Annualizowana stopa zwrotu (%).
    """
    if portfolio.empty or schedule.empty:
        return 0.0
    
    # Sortujemy harmonogram
    schedule = schedule.sort_values('Data')
    
    # Określamy datę początkową
    start_date = schedule['Data'].min()
    
    # Obliczamy końcową wartość portfela
    portfolio_value = (portfolio['Ilość'] * portfolio['Cena jednostkowa']).sum()
    
    # Całkowita zainwestowana kwota
    total_investment = schedule['Kwota'].sum()
    
    # Obliczamy okres inwestycji w latach
    years = (end_date - start_date).days / 365.25
    
    # Obliczamy annualizowaną stopę zwrotu (CAGR)
    if years > 0 and total_investment > 0:
        cagr = (((portfolio_value / total_investment) ** (1 / years)) - 1) * 100
    else:
        cagr = 0.0
    
    return cagr

def calculate_real_return(
    nominal_return: float,
    inflation_rates: pd.DataFrame,
    start_year: int,
    end_year: int,
    currency: str = 'EUR'
) -> float:
    """
    Oblicza realną stopę zwrotu po uwzględnieniu inflacji.

    Args:
        nominal_return: Nominalna stopa zwrotu (%).
        inflation_rates: DataFrame z danymi o inflacji.
        start_year: Rok początkowy inwestycji.
        end_year: Rok końcowy inwestycji.
        currency: Waluta (EUR, PLN, USD).

    Returns:
        Realna stopa zwrotu (%).
    """
    # Obliczamy średnią inflację w okresie
    years = list(range(start_year, end_year + 1))
    total_inflation = 1.0
    
    for year in years:
        inflation_rate = get_inflation_rate(inflation_rates, year, currency)
        total_inflation *= (1 + inflation_rate / 100)
    
    # Obliczamy realną stopę zwrotu
    real_return = ((1 + nominal_return / 100) / total_inflation - 1) * 100
    
    return real_return

def calculate_risk_metrics(
    portfolio: pd.DataFrame,
    metal_prices: pd.DataFrame,
    start_date: datetime,
    end_date: datetime
) -> Dict[str, float]:
    """
    Oblicza metryki ryzyka dla portfela metali szlachetnych.

    Args:
        portfolio: DataFrame z historią inwestycji.
        metal_prices: DataFrame z cenami metali.
        start_date: Data początkowa.
        end_date: Data końcowa.

    Returns:
        Słownik z metrykami ryzyka (zmienność, max drawdown, Sharpe ratio).
    """
    if portfolio.empty or metal_prices.empty:
        return {
            'volatility': 0.0,
            'max_drawdown': 0.0,
            'sharpe_ratio': 0.0
        }
    
    # Filtrujemy ceny w zakresie dat
    filtered_prices = metal_prices[
        (metal_prices['Data'] >= start_date) & 
        (metal_prices['Data'] <= end_date)
    ]
    
    if filtered_prices.empty:
        return {
            'volatility': 0.0,
            'max_drawdown': 0.0,
            'sharpe_ratio': 0.0
        }
    
    # Tworzymy DataFrame z wartością portfela w czasie
    portfolio_value = []
    
    for date in filtered_prices['Data'].unique():
        # Pobieramy ceny na daną datę
        prices_on_date = filtered_prices[filtered_prices['Data'] == date].iloc[0]
        
        # Obliczamy wartość portfela dla każdego metalu
        value = 0.0
        
        for metal in ['Gold', 'Silver', 'Platinum', 'Palladium']:
            metal_holdings = portfolio[portfolio['Metal'] == metal.capitalize()]
            if not metal_holdings.empty:
                metal_quantity = metal_holdings['Ilość'].sum()
                metal_price = prices_on_date.get(metal, 0)
                value += metal_quantity * metal_price
        
        portfolio_value.append({
            'Data': date,
            'Wartość': value
        })
    
    # Tworzymy DataFrame
    df_value = pd.DataFrame(portfolio_value)
    
    if df_value.empty or len(df_value) < 2:
        return {
            'volatility': 0.0,
            'max_drawdown': 0.0,
            'sharpe_ratio': 0.0
        }
    
    # Obliczamy dzienne stopy zwrotu
    df_value['Return'] = df_value['Wartość'].pct_change()
    
    # Obliczamy zmienność (odchylenie standardowe dziennych stóp zwrotu, annualizowane)
    volatility = df_value['Return'].std() * np.sqrt(252) * 100  # w procentach
    
    # Obliczamy maksymalny drawdown
    df_value['Cummax'] = df_value['Wartość'].cummax()
    df_value['Drawdown'] = (df_value['Wartość'] - df_value['Cummax']) / df_value['Cummax'] * 100
    max_drawdown = abs(df_value['Drawdown'].min())
    
    # Obliczamy Sharpe ratio (przyjmujemy wolną od ryzyka stopę zwrotu na poziomie 1%)
    risk_free_rate = 0.01  # 1% rocznie
    mean_return = df_value['Return'].mean() * 252  # Annualizowana średnia stopa zwrotu
    sharpe_ratio = (mean_return - risk_free_rate) / (df_value['Return'].std() * np.sqrt(252)) if df_value['Return'].std() > 0 else 0
    
    return {
        'volatility': volatility,
        'max_drawdown': max_drawdown,
        'sharpe_ratio': sharpe_ratio
    }

def compare_investment_strategies(
    portfolio_data: Dict[str, pd.DataFrame],
    investment_amount: float,
    start_date: datetime,
    end_date: datetime,
    currency: str = 'EUR'
) -> pd.DataFrame:
    """
    Porównuje różne strategie inwestycyjne dla metali szlachetnych.

    Args:
        portfolio_data: Słownik z danymi portfeli dla różnych strategii.
        investment_amount: Kwota inwestycji.
        start_date: Data początkowa.
        end_date: Data końcowa.
        currency: Waluta.

    Returns:
        DataFrame z porównaniem strategii.
    """
    if not portfolio_data:
        return pd.DataFrame()
    
    comparison_results = []
    
    for strategy_name, portfolio_df in portfolio_data.items():
        if portfolio_df.empty:
            continue
        
        # Obliczamy podstawowe metryki
        final_value = (portfolio_df['Ilość'] * portfolio_df['Cena jednostkowa']).sum()
        profit_loss = final_value - investment_amount
        roi = (profit_loss / investment_amount) * 100 if investment_amount > 0 else 0
        
        # Obliczamy okres inwestycji w latach
        years = (end_date - start_date).days / 365.25
        
        # Obliczamy annualizowaną stopę zwrotu
        cagr = ((final_value / investment_amount) ** (1 / years) - 1) * 100 if years > 0 else 0
        
        # Zapisujemy wyniki
        comparison_results.append({
            'Strategia': strategy_name,
            'Wartość końcowa': final_value,
            'Zysk/Strata': profit_loss,
            'ROI (%)': roi,
            'Roczna stopa zwrotu (%)': cagr,
            'Okres (lata)': years
        })
    
    return pd.DataFrame(comparison_results)

def simulate_rebalancing(
    portfolio: pd.DataFrame,
    metal_prices: pd.DataFrame,
    target_allocation: Dict[str, float],
    rebalance_frequency: str = 'quarterly',
    start_date: datetime = None,
    end_date: datetime = None
) -> pd.DataFrame:
    """
    Symuluje rebalancing portfela metali szlachetnych.

    Args:
        portfolio: DataFrame z historią inwestycji.
        metal_prices: DataFrame z cenami metali.
        target_allocation: Docelowa alokacja (np. {'gold': 40, 'silver': 30, 'platinum': 15, 'palladium': 15}).
        rebalance_frequency: Częstotliwość rebalancingu ('monthly', 'quarterly', 'yearly').
        start_date: Data początkowa (opcjonalnie).
        end_date: Data końcowa (opcjonalnie).

    Returns:
        DataFrame z historią po rebalancingu.
    """
    if portfolio.empty or metal_prices.empty:
        return pd.DataFrame()
    
    # Kopiujemy portfel
    rebalanced_portfolio = portfolio.copy()
    
    # Ustalamy daty rebalancingu
    if start_date is None:
        start_date = portfolio['Data'].min()
    if end_date is None:
        end_date = portfolio['Data'].max()
    
    # Określamy częstotliwość rebalancingu
    if rebalance_frequency == 'monthly':
        freq = 'MS'  # Początek miesiąca
    elif rebalance_frequency == 'quarterly':
        freq = 'QS'  # Początek kwartału
    elif rebalance_frequency == 'yearly':
        freq = 'YS'  # Początek roku
    else:
        freq = 'QS'  # Domyślnie kwartalnie
    
    # Generujemy daty rebalancingu
    rebalance_dates = pd.date_range(start=start_date, end=end_date, freq=freq)
    
    # Funkcja do rebalancingu na daną datę
    def rebalance_on_date(date, portfolio_df):
        # Filtrujemy ceny na daną datę
        prices_on_date = metal_prices[metal_prices['Data'] >= date].iloc[0]
        
        # Obliczamy całkowitą wartość portfela
        total_value = 0
        metals_value = {}
        
        for metal in ['Gold', 'Silver', 'Platinum', 'Palladium']:
            metal_holdings = portfolio_df[portfolio_df['Metal'] == metal.capitalize()]
            if not metal_holdings.empty:
                metal_quantity = metal_holdings['Ilość'].sum()
                metal_price = prices_on_date.get(metal, 0)
                metal_value = metal_quantity * metal_price
                metals_value[metal.lower()] = metal_value
                total_value += metal_value
        
        # Obliczamy docelową wartość dla każdego metalu
        target_values = {}
        for metal, alloc in target_allocation.items():
            target_values[metal] = total_value * (alloc / 100)
        
        # Obliczamy różnicę między obecną a docelową wartością
        rebalance_actions = []
        
        for metal, target_value in target_values.items():
            current_value = metals_value.get(metal, 0)
            diff_value = target_value - current_value
            
            if abs(diff_value) > 1:  # Ignorujemy małe różnice
                metal_price = prices_on_date.get(metal.capitalize(), 0)
                if metal_price > 0:
                    diff_quantity = diff_value / metal_price
                    
                    rebalance_actions.append({
                        'Data': date,
                        'Typ operacji': 'Zakup' if diff_value > 0 else 'Sprzedaż',
                        'Metal': metal.capitalize(),
                        'Ilość': abs(diff_quantity),
                        'Cena jednostkowa': metal_price,
                        'Kwota operacji': abs(diff_value),
                        'Koszt magazynowania': 0.0,
                        'Sprzedaż na koszty': 0.0
                    })
        
        # Dodajemy akcje rebalancingu do portfela
        return pd.concat([portfolio_df, pd.DataFrame(rebalance_actions)], ignore_index=True)
    
    # Wykonujemy rebalancing na każdą datę
    for rebalance_date in rebalance_dates:
        rebalanced_portfolio = rebalance_on_date(rebalance_date, rebalanced_portfolio)
    
    return rebalanced_portfolio

def compare_with_other_assets(
    metal_prices: pd.DataFrame,
    start_date: datetime,
    end_date: datetime,
    initial_investment: float = 100.0,
    currency: str = 'EUR'
) -> pd.DataFrame:
    """
    Porównuje zwrot z inwestycji w metale szlachetne z innymi klasami aktywów.
    
    Args:
        metal_prices: DataFrame z cenami metali.
        start_date: Data początkowa.
        end_date: Data końcowa.
        initial_investment: Początkowa kwota inwestycji (do indeksowania).
        currency: Waluta.
        
    Returns:
        DataFrame z porównaniem zwrotów.
    """
    # Filtrujemy dane metali w zakresie dat
    filtered_metals = metal_prices[
        (metal_prices['Data'] >= start_date) & 
        (metal_prices['Data'] <= end_date)
    ].copy()
    
    if filtered_metals.empty:
        return pd.DataFrame()
    
    # Obliczamy indeksy dla metali (bazując na wartości początkowej = initial_investment)
    comparison_data = []
    
    # Przygotowanie danych dla metali
    for metal in ['Gold', 'Silver', 'Platinum', 'Palladium']:
        if metal in filtered_metals.columns:
            base_price = filtered_metals[metal].iloc[0]
            if base_price > 0:
                last_price = filtered_metals[metal].iloc[-1]
                roi = (last_price / base_price - 1) * 100
                years = (end_date - start_date).days / 365.25
                
                # Annualizowana stopa zwrotu
                if years > 0:
                    cagr = ((last_price / base_price) ** (1 / years) - 1) * 100
                else:
                    cagr = 0
                
                comparison_data.append({
                    'Aktywo': f"{metal}",
                    'Zwrot całkowity (%)': roi,
                    'Roczna stopa zwrotu (%)': cagr,
                    'Wartość końcowa': initial_investment * (1 + roi/100)
                })
    
    # Dodajemy przykładowe klasy aktywów (benchmarki)
    # W rzeczywistej aplikacji te dane powinny być pobierane z API lub plików CSV
    
    # Przykład: Indeks giełdowy (symulowany)
    stock_index_roi = 65.0  # Przykładowy zwrot dla symulacji
    stock_index_cagr = ((1 + stock_index_roi/100) ** (1 / years) - 1) * 100 if years > 0 else 0
    
    comparison_data.append({
        'Aktywo': 'Indeks S&P 500',
        'Zwrot całkowity (%)': stock_index_roi,
        'Roczna stopa zwrotu (%)': stock_index_cagr,
        'Wartość końcowa': initial_investment * (1 + stock_index_roi/100)
    })
    
    # Przykład: Obligacje (symulowany)
    bonds_roi = 15.0  # Przykładowy zwrot dla symulacji
    bonds_cagr = ((1 + bonds_roi/100) ** (1 / years) - 1) * 100 if years > 0 else 0
    
    comparison_data.append({
        'Aktywo': 'Obligacje 10-letnie',
        'Zwrot całkowity (%)': bonds_roi,
        'Roczna stopa zwrotu (%)': bonds_cagr,
        'Wartość końcowa': initial_investment * (1 + bonds_roi/100)
    })
    
    # Przykład: Nieruchomości (symulowany)
    real_estate_roi = 45.0  # Przykładowy zwrot dla symulacji
    real_estate_cagr = ((1 + real_estate_roi/100) ** (1 / years) - 1) * 100 if years > 0 else 0
    
    comparison_data.append({
        'Aktywo': 'Nieruchomości',
        'Zwrot całkowity (%)': real_estate_roi,
        'Roczna stopa zwrotu (%)': real_estate_cagr,
        'Wartość końcowa': initial_investment * (1 + real_estate_roi/100)
    })
    
    # Przykład: Gotówka (uwzględniająca inflację)
    inflation_roi = -15.0  # Przykładowy zwrot po uwzględnieniu inflacji
    inflation_cagr = ((1 + inflation_roi/100) ** (1 / years) - 1) * 100 if years > 0 else 0
    
    comparison_data.append({
        'Aktywo': 'Gotówka (po inflacji)',
        'Zwrot całkowity (%)': inflation_roi,
        'Roczna stopa zwrotu (%)': inflation_cagr,
        'Wartość końcowa': initial_investment * (1 + inflation_roi/100)
    })
    
    return pd.DataFrame(comparison_data)
