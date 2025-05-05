# /prometalle_app/app/core/purchase_schedule.py

import pandas as pd
from datetime import datetime, timedelta

# Funkcja do generowania harmonogramu zakupów
def generate_purchase_schedule(
    start_date: str,
    end_date: str,
    frequency: str,
    purchase_day: int,
    purchase_amount: float
) -> pd.DataFrame:
    """
    Generuje harmonogram zakupów na podstawie częstotliwości:
    - 'weekly' (dzień tygodnia 0-6, poniedziałek-niedziela)
    - 'monthly' (dzień miesiąca 1-31)
    - 'quarterly' (dzień kwartału 1-31)

    Zwraca DataFrame z kolumnami: 'Data', 'Kwota'
    """
    schedule = []
    
    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)
    
    if frequency == 'weekly':
        # Co tydzień w określony dzień tygodnia
        current = start
        while current <= end:
            if current.weekday() == purchase_day:
                schedule.append({'Data': current, 'Kwota': purchase_amount})
            current += timedelta(days=1)

    elif frequency == 'monthly':
        # Co miesiąc w określony dzień
        current = start.replace(day=1)
        while current <= end:
            try:
                purchase_date = current.replace(day=purchase_day)
            except ValueError:
                # Dzień nie istnieje (np. 30 lutego) -> ostatni dzień miesiąca
                next_month = current + pd.DateOffset(months=1)
                purchase_date = next_month - pd.DateOffset(days=1)
            if purchase_date >= start and purchase_date <= end:
                schedule.append({'Data': purchase_date, 'Kwota': purchase_amount})
            current += pd.DateOffset(months=1)

    elif frequency == 'quarterly':
        # Co kwartał w określony dzień
        current = start.replace(day=1)
        while current <= end:
            try:
                purchase_date = current.replace(day=purchase_day)
            except ValueError:
                next_month = current + pd.DateOffset(months=1)
                purchase_date = next_month - pd.DateOffset(days=1)
            if purchase_date >= start and purchase_date <= end:
                schedule.append({'Data': purchase_date, 'Kwota': purchase_amount})
            current += pd.DateOffset(months=3)

    return pd.DataFrame(schedule)
