# /modules/utils.py
# Funkcje pomocnicze dla aplikacji Prometalle

import pandas as pd
import numpy as np
import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Union, Any
import streamlit as st
from modules.config import UNITS_CONVERSION, DEFAULT_LANGUAGE, DEFAULT_CURRENCY

def load_csv_file(file_path: str, parse_dates: List[str] = None) -> pd.DataFrame:
    """
    Bezpieczne ładowanie pliku CSV z obsługą błędów.

    Args:
        file_path: Ścieżka do pliku CSV.
        parse_dates: Lista kolumn do interpretacji jako daty.

    Returns:
        DataFrame z danymi lub pusty DataFrame w przypadku błędu.
    """
    try:
        # Sprawdzenie czy plik istnieje
        if not os.path.exists(file_path):
            st.error(f"Nie znaleziono pliku: {file_path}")
            return pd.DataFrame()
        
        # Próba odczytu pliku
        if parse_dates:
            df = pd.read_csv(file_path, parse_dates=parse_dates)
        else:
            df = pd.read_csv(file_path)
        
        # Sprawdzenie czy DataFrame nie jest pusty
        if df.empty:
            st.warning(f"Plik {file_path} nie zawiera danych.")
        
        return df
    except Exception as e:
        st.error(f"Błąd podczas ładowania pliku {file_path}: {str(e)}")
        return pd.DataFrame()

def save_csv_file(df: pd.DataFrame, file_path: str, index: bool = False) -> bool:
    """
    Bezpieczny zapis DataFrame do pliku CSV.

    Args:
        df: DataFrame do zapisania.
        file_path: Ścieżka docelowa pliku CSV.
        index: Czy zapisać indeks.

    Returns:
        True jeśli zapisano pomyślnie, False w przypadku błędu.
    """
    try:
        # Upewniamy się, że ścieżka do katalogu istnieje
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        
        # Zapisujemy plik
        df.to_csv(file_path, index=index)
        return True
    except Exception as e:
        st.error(f"Błąd podczas zapisywania pliku {file_path}: {str(e)}")
        return False

def convert_currency(
    amount: float, 
    from_currency: str, 
    to_currency: str, 
    exchange_rates: pd.DataFrame,
    date: Optional[datetime] = None
) -> float:
    """
    Konwertuje kwotę z jednej waluty na drugą.

    Args:
        amount: Kwota do konwersji.
        from_currency: Waluta źródłowa.
        to_currency: Waluta docelowa.
        exchange_rates: DataFrame z kursami walut.
        date: Data konwersji (opcjonalnie).

    Returns:
        Skonwertowana kwota lub oryginalna kwota w przypadku błędu.
    """
    if from_currency == to_currency:
        return amount
    
    if exchange_rates.empty:
        return amount
    
    try:
        # Jeśli nie podano daty, bierzemy ostatni dostępny kurs
        if date is None:
            exchange_rate_row = exchange_rates.iloc[-1]
        else:
            # Szukamy kursu na daną datę lub najbliższą wcześniejszą
            exchange_rates_before = exchange_rates[exchange_rates['Data'] <= date]
            if exchange_rates_before.empty:
                exchange_rate_row = exchange_rates.iloc[0]
            else:
                exchange_rate_row = exchange_rates_before.iloc[-1]
        
        # Konwersja z EUR do innych walut
        if from_currency == 'EUR' and to_currency == 'PLN':
            return amount * exchange_rate_row['EUR_PLN']
        elif from_currency == 'EUR' and to_currency == 'USD':
            return amount * exchange_rate_row['EUR_USD']
        # Konwersja z innych walut do EUR
        elif from_currency == 'PLN' and to_currency == 'EUR':
            return amount / exchange_rate_row['EUR_PLN']
        elif from_currency == 'USD' and to_currency == 'EUR':
            return amount / exchange_rate_row['EUR_USD']
        # Konwersja między innymi walutami (poprzez EUR)
        elif from_currency == 'PLN' and to_currency == 'USD':
            eur_amount = amount / exchange_rate_row['EUR_PLN']
            return eur_amount * exchange_rate_row['EUR_USD']
        elif from_currency == 'USD' and to_currency == 'PLN':
            eur_amount = amount / exchange_rate_row['EUR_USD']
            return eur_amount * exchange_rate_row['EUR_PLN']
        else:
            # Nieznana kombinacja walut
            return amount
    except Exception as e:
        st.warning(f"Błąd podczas konwersji walut: {str(e)}")
        return amount

def convert_weight(amount: float, from_unit: str, to_unit: str) -> float:
    """
    Konwertuje wagę między jednostkami (g <-> oz).

    Args:
        amount: Ilość do konwersji.
        from_unit: Jednostka źródłowa ('g' lub 'oz').
        to_unit: Jednostka docelowa ('g' lub 'oz').

    Returns:
        Skonwertowana ilość.
    """
    if from_unit == to_unit:
        return amount
    
    # Konwersja z gramów na uncje
    if from_unit == 'g' and to_unit == 'oz':
        return amount / UNITS_CONVERSION['oz_to_g']
    
    # Konwersja z uncji na gramy
    elif from_unit == 'oz' and to_unit == 'g':
        return amount * UNITS_CONVERSION['oz_to_g']
    
    # W przypadku nieznanych jednostek zwracamy wartość bez zmian
    return amount

def format_number(
    value: float, 
    decimals: int = 2, 
    thousands_sep: str = ' ', 
    currency: Optional[str] = None,
    percentage: bool = False
) -> str:
    """
    Formatuje liczbę do czytelnej postaci.

    Args:
        value: Wartość do sformatowania.
        decimals: Liczba miejsc dziesiętnych.
        thousands_sep: Separator tysięcy.
        currency: Symbol waluty (opcjonalnie).
        percentage: Czy formatować jako procent.

    Returns:
        Sformatowana liczba jako string.
    """
    try:
        if np.isnan(value):
            return "N/A"
        
        if percentage:
            return f"{value:.{decimals}f}%".replace('.', ',')
        
        # Formatowanie liczby
        formatted = f"{value:,.{decimals}f}".replace(',', ' ').replace('.', ',')
        
        # Dodanie symbolu waluty
        if currency:
            return f"{formatted} {currency}"
        
        return formatted
    except:
        return str(value)

def calculate_date_range(
    start_date: datetime, 
    end_date: datetime
) -> Tuple[int, int, int]:
    """
    Oblicza okres czasu między datami w latach, miesiącach i dniach.

    Args:
        start_date: Data początkowa.
        end_date: Data końcowa.

    Returns:
        Krotka (lata, miesiące, dni).
    """
    # Obliczenie różnicy w dniach
    delta = end_date - start_date
    total_days = delta.days
    
    # Obliczenie lat, miesięcy i dni
    years = total_days // 365
    remaining_days = total_days % 365
    months = remaining_days // 30
    days = remaining_days % 30
    
    return years, months, days

def format_date_range(start_date: datetime, end_date: datetime, language: str = DEFAULT_LANGUAGE) -> str:
    """
    Formatuje zakres dat do czytelnej postaci.

    Args:
        start_date: Data początkowa.
        end_date: Data końcowa.
        language: Kod języka.

    Returns:
        Sformatowany zakres dat jako string.
    """
    years, months, days = calculate_date_range(start_date, end_date)
    
    # Formatowanie w zależności od języka
    if language == 'pl':
        years_str = f"{years} {'lat' if years == 0 or years >= 5 else 'lata'}" if years > 0 else ""
        months_str = f"{months} {'miesięcy' if months == 0 or months >= 5 else 'miesiące'}" if months > 0 else ""
        days_str = f"{days} {'dni' if days == 0 or days != 1 else 'dzień'}" if days > 0 else ""
    elif language == 'de':
        years_str = f"{years} {'Jahre' if years != 1 else 'Jahr'}" if years > 0 else ""
        months_str = f"{months} {'Monate' if months != 1 else 'Monat'}" if months > 0 else ""
        days_str = f"{days} {'Tage' if days != 1 else 'Tag'}" if days > 0 else ""
    else:  # domyślnie angielski
        years_str = f"{years} {'years' if years != 1 else 'year'}" if years > 0 else ""
        months_str = f"{months} {'months' if months != 1 else 'month'}" if months > 0 else ""
        days_str = f"{days} {'days' if days != 1 else 'day'}" if days > 0 else ""
    
    # Łączenie elementów
    elements = [elem for elem in [years_str, months_str, days_str] if elem]
    
    if len(elements) == 0:
        return "0 dni" if language == 'pl' else "0 Tage" if language == 'de' else "0 days"
    elif len(elements) == 1:
        return elements[0]
    elif len(elements) == 2:
        return f"{elements[0]} i {elements[1]}" if language == 'pl' else f"{elements[0]} und {elements[1]}" if language == 'de' else f"{elements[0]} and {elements[1]}"
    else:
        if language == 'pl':
            return f"{elements[0]}, {elements[1]} i {elements[2]}"
        elif language == 'de':
            return f"{elements[0]}, {elements[1]} und {elements[2]}"
        else:
            return f"{elements[0]}, {elements[1]} and {elements[2]}"

def export_to_excel(
    data_dict: Dict[str, pd.DataFrame], 
    file_path: str
) -> bool:
    """
    Eksportuje dane do pliku Excel.

    Args:
        data_dict: Słownik {nazwa_arkusza: dataframe}.
        file_path: Ścieżka do pliku Excel.

    Returns:
        True jeśli zapisano pomyślnie, False w przypadku błędu.
    """
    try:
        # Upewniamy się, że ścieżka do katalogu istnieje
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        
        # Tworzenie pliku Excel
        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            for sheet_name, df in data_dict.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        
        return True
    except Exception as e:
        st.error(f"Błąd podczas eksportu do Excela: {str(e)}")
        return False

def save_chart_to_file(fig, file_path: str, width: int = 800, height: int = 600) -> bool:
    """
    Zapisuje wykres Plotly do pliku.

    Args:
        fig: Obiekt wykresu Plotly.
        file_path: Ścieżka do pliku.
        width: Szerokość wykresu w pikselach.
        height: Wysokość wykresu w pikselach.

    Returns:
        True jeśli zapisano pomyślnie, False w przypadku błędu.
    """
    try:
        # Upewniamy się, że ścieżka do katalogu istnieje
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        
        # Określamy format na podstawie rozszerzenia
        extension = file_path.split('.')[-1].lower()
        
        if extension in ['png', 'jpeg', 'jpg', 'webp']:
            fig.write_image(file_path, width=width, height=height)
        elif extension == 'html':
            fig.write_html(file_path)
        elif extension == 'pdf':
            fig.write_image(file_path, width=width, height=height)
        elif extension == 'svg':
            fig.write_image(file_path, width=width, height=height)
        else:
            # Domyślnie PNG
            fig.write_image(file_path + '.png', width=width, height=height)
        
        return True
    except Exception as e:
        st.error(f"Błąd podczas zapisywania wykresu: {str(e)}")
        return False

def generate_report_data(
    portfolio: pd.DataFrame,
    summary: pd.DataFrame,
    metal_prices: pd.DataFrame,
    schedule: pd.DataFrame,
    start_date: datetime,
    end_date: datetime,
    currency: str = DEFAULT_CURRENCY
) -> Dict[str, Any]:
    """
    Generuje dane do raportu z symulacji.

    Args:
        portfolio: DataFrame portfela.
        summary: DataFrame podsumowania.
        metal_prices: DataFrame cen metali.
        schedule: DataFrame harmonogramu zakupów.
        start_date: Data początkowa.
        end_date: Data końcowa.
        currency: Waluta.

    Returns:
        Słownik z danymi do raportu.
    """
    # Obliczanie podstawowych statystyk
    total_investment = schedule['Kwota'].sum() if not schedule.empty else 0
    current_value = (summary['Ilość'] * summary['Cena jednostkowa']).sum() if not summary.empty else 0
    profit_loss = current_value - total_investment
    roi_percent = (profit_loss / total_investment * 100) if total_investment > 0 else 0
    
    # Obliczanie czasu trwania inwestycji
    years, months, days = calculate_date_range(start_date, end_date)
    duration_str = format_date_range(start_date, end_date)
    
    # Pobieranie cen początkowych i końcowych metali
    metals_data = {}
    metals = ['Gold', 'Silver', 'Platinum', 'Palladium']
    
    filtered_prices = metal_prices[
        (metal_prices['Data'] >= start_date) & 
        (metal_prices['Data'] <= end_date)
    ]
    
    if not filtered_prices.empty:
        start_prices = filtered_prices.iloc[0]
        end_prices = filtered_prices.iloc[-1]
        
        for metal in metals:
            if metal in filtered_prices.columns:
                start_price = start_prices[metal]
                end_price = end_prices[metal]
                price_change = end_price - start_price
                price_change_percent = (price_change / start_price * 100) if start_price > 0 else 0
                
                metals_data[metal] = {
                    'start_price': start_price,
                    'end_price': end_price,
                    'change': price_change,
                    'change_percent': price_change_percent
                }
    
    # Podsumowanie metali w portfelu
    metals_summary = []
    if not summary.empty:
        for _, row in summary.iterrows():
            metal = row['Metal']
            quantity = row['Ilość']
            invested = row['Kwota operacji']
            current_value_metal = quantity * row['Cena jednostkowa']
            profit_loss_metal = current_value_metal - invested
            roi_percent_metal = (profit_loss_metal / invested * 100) if invested > 0 else 0
            
            metals_summary.append({
                'metal': metal,
                'quantity': quantity,
                'invested': invested,
                'current_value': current_value_metal,
                'profit_loss': profit_loss_metal,
                'roi_percent': roi_percent_metal
            })
    
    # Podsumowanie kosztów magazynowania
    storage_costs = 0
    if 'Koszt_magazynowania' in portfolio.columns:
        storage_costs = portfolio['Koszt_magazynowania'].sum()
    
    # Przygotowanie danych do raportu
    report_data = {
        'total_investment': total_investment,
        'current_value': current_value,
        'profit_loss': profit_loss,
        'roi_percent': roi_percent,
        'start_date': start_date,
        'end_date': end_date,
        'duration_years': years,
        'duration_months': months,
        'duration_days': days,
        'duration_str': duration_str,
        'metals_data': metals_data,
        'metals_summary': metals_summary,
        'storage_costs': storage_costs,
        'currency': currency
    }
    
    return report_data

def generate_pdf_report(
    report_data: Dict[str, Any],
    output_path: str,
    language: str = DEFAULT_LANGUAGE
) -> bool:
    """
    Generuje raport PDF z wynikami symulacji.
    Wymaga zainstalowanej biblioteki ReportLab.

    Args:
        report_data: Dane do raportu.
        output_path: Ścieżka do pliku PDF.
        language: Kod języka.

    Returns:
        True jeśli zapisano pomyślnie, False w przypadku błędu.
    """
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        
        # Tworzenie stylów
        styles = getSampleStyleSheet()
        title_style = styles['Heading1']
        subtitle_style = styles['Heading2']
        normal_style = styles['Normal']
        
        # Tworzenie dokumentu
        doc = SimpleDocTemplate(output_path, pagesize=A4)
        elements = []
        
        # Tytuł raportu
        if language == 'pl':
            title = "Raport z symulacji inwestycji w metale szlachetne"
        elif language == 'de':
            title = "Bericht zur Simulation von Investitionen in Edelmetalle"
        else:
            title = "Precious Metals Investment Simulation Report"
        
        elements.append(Paragraph(title, title_style))
        elements.append(Spacer(1, 0.5*cm))
        
        # Podstawowe informacje
        if language == 'pl':
            period_text = f"Okres inwestycji: {report_data['start_date'].strftime('%d.%m.%Y')} - {report_data['end_date'].strftime('%d.%m.%Y')} ({report_data['duration_str']})"
        elif language == 'de':
            period_text = f"Anlagezeitraum: {report_data['start_date'].strftime('%d.%m.%Y')} - {report_data['end_date'].strftime('%d.%m.%Y')} ({report_data['duration_str']})"
        else:
            period_text = f"Investment period: {report_data['start_date'].strftime('%m/%d/%Y')} - {report_data['end_date'].strftime('%m/%d/%Y')} ({report_data['duration_str']})"
        
        elements.append(Paragraph(period_text, normal_style))
        elements.append(Spacer(1, 0.3*cm))
        
        # Podsumowanie finansowe
        currency = report_data['currency']
        
        if language == 'pl':
            financial_title = "Podsumowanie finansowe"
            investment_text = f"Zainwestowana kwota: {format_number(report_data['total_investment'], currency=currency)}"
            value_text = f"Aktualna wartość: {format_number(report_data['current_value'], currency=currency)}"
            profit_text = f"Zysk/Strata: {format_number(report_data['profit_loss'], currency=currency)}"
            roi_text = f"Stopa zwrotu: {format_number(report_data['roi_percent'], decimals=2, percentage=True)}"
            storage_text = f"Koszty magazynowania: {format_number(report_data['storage_costs'], currency=currency)}"
        elif language == 'de':
            financial_title = "Finanzielle Zusammenfassung"
            investment_text = f"Investierter Betrag: {format_number(report_data['total_investment'], currency=currency)}"
            value_text = f"Aktueller Wert: {format_number(report_data['current_value'], currency=currency)}"
            profit_text = f"Gewinn/Verlust: {format_number(report_data['profit_loss'], currency=currency)}"
            roi_text = f"Rendite: {format_number(report_data['roi_percent'], decimals=2, percentage=True)}"
            storage_text = f"Lagerkosten: {format_number(report_data['storage_costs'], currency=currency)}"
        else:
            financial_title = "Financial Summary"
            investment_text = f"Invested amount: {format_number(report_data['total_investment'], currency=currency)}"
            value_text = f"Current value: {format_number(report_data['current_value'], currency=currency)}"
            profit_text = f"Profit/Loss: {format_number(report_data['profit_loss'], currency=currency)}"
            roi_text = f"Return on Investment: {format_number(report_data['roi_percent'], decimals=2, percentage=True)}"
            storage_text = f"Storage costs: {format_number(report_data['storage_costs'], currency=currency)}"
        
        elements.append(Paragraph(financial_title, subtitle_style))
        elements.append(Spacer(1, 0.2*cm))
        elements.append(Paragraph(investment_text, normal_style))
        elements.append(Paragraph(value_text, normal_style))
        elements.append(Paragraph(profit_text, normal_style))
        elements.append(Paragraph(roi_text, normal_style))
        elements.append(Paragraph(storage_text, normal_style))
        elements.append(Spacer(1, 0.5*cm))
        
        # Tabela z podsumowaniem metali
        if report_data['metals_summary']:
            if language == 'pl':
                metals_title = "Podsumowanie metali w portfelu"
                table_headers = ["Metal", "Ilość", "Zainwestowano", "Wartość aktualna", "Zysk/Strata", "Stopa zwrotu"]
            elif language == 'de':
                metals_title = "Zusammenfassung der Metalle im Portfolio"
                table_headers = ["Metall", "Menge", "Investiert", "Aktueller Wert", "Gewinn/Verlust", "Rendite"]
            else:
                metals_title = "Metals Summary in Portfolio"
                table_headers = ["Metal", "Quantity", "Invested", "Current Value", "Profit/Loss", "ROI"]
            
            elements.append(Paragraph(metals_title, subtitle_style))
            elements.append(Spacer(1, 0.2*cm))
            
            # Przygotowanie danych do tabeli
            table_data = [table_headers]
            
            for metal_data in report_data['metals_summary']:
                row = [
                    metal_data['metal'],
                    format_number(metal_data['quantity'], decimals=3),
                    format_number(metal_data['invested'], currency=currency),
                    format_number(metal_data['current_value'], currency=currency),
                    format_number(metal_data['profit_loss'], currency=currency),
                    format_number(metal_data['roi_percent'], decimals=2, percentage=True)
                ]
                table_data.append(row)
            
            # Tworzenie tabeli
            table = Table(table_data, repeatRows=1)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('ALIGN', (0, 1), (0, -1), 'LEFT'),
                ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            
            elements.append(table)
            elements.append(Spacer(1, 0.5*cm))
        
        # Stopka
        if language == 'pl':
            footer_text = "Wygenerowano przez Prometalle - Symulator inwestycji w metale szlachetne"
        elif language == 'de':
            footer_text = "Generiert von Prometalle - Simulator für Investitionen in Edelmetalle"
        else:
            footer_text = "Generated by Prometalle - Precious Metals Investment Simulator"
        
        date_now = datetime.now().strftime("%d.%m.%Y %H:%M")
        footer = Paragraph(f"{footer_text} | {date_now}", ParagraphStyle(name='Footer', fontsize=8, alignment=1))
        
        elements.append(Spacer(1, 1*cm))
        elements.append(footer)
        
        # Budowanie dokumentu
        doc.build(elements)
        return True
    except Exception as e:
        st.error(f"Błąd podczas generowania raportu PDF: {str(e)}")
        return False
