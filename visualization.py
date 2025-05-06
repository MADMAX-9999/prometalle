# /modules/visualization.py
# Moduł wizualizacji danych dla aplikacji Prometalle

import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from typing import Dict, Any, List, Tuple, Optional

# Konfiguracja kolorów dla metali
METAL_COLORS = {
    'Gold': '#FFD700',      # Złoto
    'Silver': '#C0C0C0',    # Srebro
    'Platinum': '#E5E4E2',  # Platyna
    'Palladium': '#8A8B8C', # Pallad
    'gold': '#FFD700',
    'silver': '#C0C0C0',
    'platinum': '#E5E4E2',
    'palladium': '#8A8B8C',
    'Złoto': '#FFD700',
    'Srebro': '#C0C0C0',
    'Platyna': '#E5E4E2',
    'Pallad': '#8A8B8C'
}

def plot_portfolio_value(df_portfolio: pd.DataFrame, currency: str = 'EUR'):
    """
    Rysuje interaktywny wykres wartości portfela w czasie.

    Args:
        df_portfolio: DataFrame z historią inwestycji.
        currency: Waluta do wyświetlenia wartości.
    """
    if df_portfolio.empty:
        st.warning("Brak danych do wyświetlenia wykresu.")
        return

    # Obliczamy wartość depozytu: ilość * aktualna cena metalu
    df_portfolio['Wartość'] = df_portfolio['Ilość'] * df_portfolio['Cena jednostkowa']

    # Grupujemy po dacie i sumujemy wartość depozytu
    df_by_date = df_portfolio.groupby('Data').agg({
        'Wartość': 'sum'
    }).reset_index()

    # Dodajemy wykres wartości skumulowanej
    fig = go.Figure()
    
    # Dodajemy linię wartości portfela
    fig.add_trace(go.Scatter(
        x=df_by_date['Data'],
        y=df_by_date['Wartość'],
        mode='lines+markers',
        name='Wartość portfela',
        line=dict(color='#1E3A8A', width=3),
        marker=dict(size=8, color='#1E3A8A'),
        hovertemplate='%{x|%d.%m.%Y}<br>Wartość: %{y:,.2f} ' + currency
    ))
    
    # Konfigurujesz układ wykresu
    fig.update_layout(
        title=None,
        xaxis_title='Data',
        yaxis_title=f'Wartość portfela ({currency})',
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=10, r=10, t=10, b=10),
        height=400,
        template='plotly_white'
    )
    
    # Dodajemy pionowe linie dla ważnych momentów - np. krach
    # Można dodać więcej oznaczonych dat, jeśli potrzeba
    important_dates = {
        '2008-09-15': 'Upadek Lehman Brothers',
        '2011-08-22': 'Szczyt ceny złota',
        '2020-03-23': 'Krach COVID-19'
    }
    
    for date_str, label in important_dates.items():
        try:
            date = pd.to_datetime(date_str)
            if date >= df_by_date['Data'].min() and date <= df_by_date['Data'].max():
                fig.add_vline(
                    x=date, 
                    line_width=1, 
                    line_dash="dash", 
                    line_color="gray",
                    annotation_text=label,
                    annotation_position="top right"
                )
        except:
            continue
    
    # Wyświetlamy wykres
    st.plotly_chart(fig, use_container_width=True)
    
    # Dodajemy statystyki pod wykresem
    if len(df_by_date) > 1:
        first_value = df_by_date['Wartość'].iloc[0]
        last_value = df_by_date['Wartość'].iloc[-1]
        change_value = last_value - first_value
        change_percent = (change_value / first_value * 100) if first_value > 0 else 0
        
        # Wyświetlamy statystyki w trzech kolumnach
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Wartość początkowa", 
                f"{first_value:,.2f} {currency}"
            )
        
        with col2:
            st.metric(
                "Wartość końcowa", 
                f"{last_value:,.2f} {currency}"
            )
        
        with col3:
            st.metric(
                "Zmiana", 
                f"{change_value:+,.2f} {currency} ({change_percent:+.2f}%)",
                delta=f"{change_percent:+.2f}%",
                delta_color="normal"
            )


def plot_metals_allocation(summary_df: pd.DataFrame, currency: str = 'EUR') -> None:
    """
    Tworzy wykres kołowy pokazujący alokację metali w portfelu.

    Args:
        summary_df: DataFrame z podsumowaniem portfela metali.
        currency: Waluta do wyświetlenia wartości.
    """
    if summary_df.empty:
        st.warning("Brak danych do wyświetlenia wykresu alokacji.")
        return
    
    # Przygotowujemy dane do wykresu
    metals = summary_df['Metal'].tolist()
    values = summary_df['Kwota operacji'].tolist()
    
    # Kolory dla metali
    colors = [METAL_COLORS.get(metal, '#808080') for metal in metals]
    
    # Tworzymy wykres kołowy
    fig = go.Figure(data=[go.Pie(
        labels=metals,
        values=values,
        hole=.4,
        marker_colors=colors,
        textinfo='percent+label',
        hovertemplate='%{label}<br>Wartość: %{value:,.2f} ' + currency + '<br>%{percent}'
    )])
    
    fig.update_layout(
        showlegend=True,
        margin=dict(l=10, r=10, t=10, b=10),
        height=350,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        )
    )
    
    # Wyświetlamy wykres
    st.plotly_chart(fig, use_container_width=True)


def plot_price_history(
    metal_prices: pd.DataFrame, 
    start_date: datetime, 
    end_date: datetime, 
    currency: str = 'EUR'
) -> None:
    """
    Tworzy interaktywny wykres historii cen metali.

    Args:
        metal_prices: DataFrame z cenami metali.
        start_date: Data początkowa zakresu.
        end_date: Data końcowa zakresu.
        currency: Waluta cen.
    """
    if metal_prices.empty:
        st.warning("Brak danych do wyświetlenia wykresu cen.")
        return
    
    # Konwertujemy daty do formatu datetime
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    
    # Filtrujemy dane w zakresie dat
    filtered_prices = metal_prices[
        (metal_prices['Data'] >= start_date) & 
        (metal_prices['Data'] <= end_date)
    ]
    
    if filtered_prices.empty:
        st.warning("Brak danych dla wybranego zakresu dat.")
        return
    
    # Tworzymy interaktywny wykres
    fig = go.Figure()
    
    # Dodajemy linie dla każdego metalu
    metals = {
        'Gold': 'Złoto',
        'Silver': 'Srebro',
        'Platinum': 'Platyna',
        'Palladium': 'Pallad'
    }
    
    # Dodajemy przełączniki dla metali
    metal_options = st.multiselect(
        "Wybierz metale do wyświetlenia:",
        list(metals.values()),
        default=list(metals.values())[:2],
        key="price_history_metals"
    )
    
    # Mapujemy nazwy polskie na angielskie
    reverse_metals = {v: k for k, v in metals.items()}
    selected_metals = [reverse_metals[m] for m in metal_options]
    
    # Jeśli nic nie wybrano, pokazujemy wszystkie
    if not selected_metals:
        selected_metals = list(metals.keys())
    
    # Dodajemy linie do wykresu
    for metal_eng, metal_pl in metals.items():
        if metal_eng in selected_metals:
            metal_column = f"{metal_eng}"
            if metal_column in filtered_prices.columns:
                fig.add_trace(go.Scatter(
                    x=filtered_prices['Data'],
                    y=filtered_prices[metal_column],
                    mode='lines',
                    name=metal_pl,
                    line=dict(color=METAL_COLORS.get(metal_eng, '#808080'), width=2),
                    hovertemplate='%{x|%d.%m.%Y}<br>' + metal_pl + ': %{y:,.2f} ' + currency
                ))
    
    # Konfigurujemy układ wykresu
    fig.update_layout(
        xaxis_title="Data",
        yaxis_title=f"Cena ({currency})",
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=10, r=10, t=10, b=10),
        height=400,
        template='plotly_white'
    )
    
    # Wyświetlamy wykres
    st.plotly_chart(fig, use_container_width=True)
    
    # Dodajemy statystyki pod wykresem w formie tabeli
    if not filtered_prices.empty:
        stats_data = []
        
        for metal_eng, metal_pl in metals.items():
            if metal_eng in selected_metals:
                metal_column = f"{metal_eng}"
                if metal_column in filtered_prices.columns:
                    first_price = filtered_prices[metal_column].iloc[0]
                    last_price = filtered_prices[metal_column].iloc[-1]
                    min_price = filtered_prices[metal_column].min()
                    max_price = filtered_prices[metal_column].max()
                    change_value = last_price - first_price
                    change_percent = (change_value / first_price * 100) if first_price > 0 else 0
                    
                    stats_data.append({
                        "Metal": metal_pl,
                        "Cena początkowa": f"{first_price:.2f} {currency}",
                        "Cena końcowa": f"{last_price:.2f} {currency}",
                        "Zmiana %": f"{change_percent:+.2f}%",
                        "Minimum": f"{min_price:.2f} {currency}",
                        "Maksimum": f"{max_price:.2f} {currency}",
                    })
        
        if stats_data:
            stats_df = pd.DataFrame(stats_data)
            st.dataframe(stats_df, hide_index=True, use_container_width=True)


def plot_comparison_chart(
    metal_prices: pd.DataFrame, 
    start_date: datetime, 
    end_date: datetime, 
    currency: str = 'EUR'
) -> None:
    """
    Tworzy wykres porównawczy pokazujący relatywny zwrot z inwestycji w różne metale.
    
    Args:
        metal_prices: DataFrame z cenami metali.
        start_date: Data początkowa zakresu.
        end_date: Data końcowa zakresu.
        currency: Waluta cen.
    """
    if metal_prices.empty:
        st.warning("Brak danych do wyświetlenia wykresu porównawczego.")
        return
    
    # Konwertujemy daty do formatu datetime
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    
    # Filtrujemy dane w zakresie dat
    filtered_prices = metal_prices[
        (metal_prices['Data'] >= start_date) & 
        (metal_prices['Data'] <= end_date)
    ]
    
    if filtered_prices.empty:
        st.warning("Brak danych dla wybranego zakresu dat.")
        return
    
    # Tworzymy DataFrame do porównania procentowego
    comparison_df = filtered_prices.copy()
    
    # Obliczamy indeks ceny (pierwszy dzień = 100)
    metals = {
        'Gold': 'Złoto',
        'Silver': 'Srebro',
        'Platinum': 'Platyna',
        'Palladium': 'Pallad'
    }
    
    for metal in metals.keys():
        metal_column = f"{metal}"
        if metal_column in comparison_df.columns:
            base_price = comparison_df[metal_column].iloc[0]
            if base_price > 0:
                comparison_df[f"{metal}_Index"] = (comparison_df[metal_column] / base_price) * 100
    
    # Tworzymy interaktywny wykres
    fig = go.Figure()
    
    # Dodajemy linie dla każdego metalu
    for metal_eng, metal_pl in metals.items():
        index_column = f"{metal_eng}_Index"
        if index_column in comparison_df.columns:
            fig.add_trace(go.Scatter(
                x=comparison_df['Data'],
                y=comparison_df[index_column],
                mode='lines',
                name=metal_pl,
                line=dict(color=METAL_COLORS.get(metal_eng, '#808080'), width=2),
                hovertemplate='%{x|%d.%m.%Y}<br>' + metal_pl + ': %{y:.2f}%'
            ))
    
    # Dodajemy linię 100% (początkowa wartość)
    fig.add_trace(go.Scatter(
        x=[comparison_df['Data'].iloc[0], comparison_df['Data'].iloc[-1]],
        y=[100, 100],
        mode='lines',
        name='Poziom początkowy',
        line=dict(color='gray', width=1, dash='dash'),
        hoverinfo='skip'
    ))
    
    # Konfigurujemy układ wykresu
    fig.update_layout(
        xaxis_title="Data",
        yaxis_title="Względna zmiana wartości (%)",
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=10, r=10, t=10, b=10),
        height=400,
        template='plotly_white'
    )
    
    # Wyświetlamy wykres
    st.plotly_chart(fig, use_container_width=True)


def plot_cumulative_investment(schedule_df: pd.DataFrame, currency: str = 'EUR') -> None:
    """
    Tworzy wykres skumulowanej inwestycji w czasie.
    
    Args:
        schedule_df: DataFrame z harmonogramem zakupów.
        currency: Waluta kwot.
    """
    if schedule_df.empty:
        st.warning("Brak danych do wyświetlenia wykresu inwestycji.")
        return
    
    # Sortujemy po dacie
    schedule_df = schedule_df.sort_values('Data')
    
    # Obliczamy skumulowaną sumę
    schedule_df['Skumulowana kwota'] = schedule_df['Kwota'].cumsum()
    
    # Tworzymy wykres
    fig = go.Figure()
    
    # Dodajemy linie
    fig.add_trace(go.Scatter(
        x=schedule_df['Data'],
        y=schedule_df['Skumulowana kwota'],
        mode='lines',
        name='Skumulowana inwestycja',
        line=dict(color='#0891b2', width=3),
        fill='tozeroy',
        fillcolor='rgba(8, 145, 178, 0.2)',
        hovertemplate='%{x|%d.%m.%Y}<br>Zainwestowano: %{y:,.2f} ' + currency
    ))
    
    # Dodajemy słupki pojedynczych inwestycji
    fig.add_trace(go.Bar(
        x=schedule_df['Data'],
        y=schedule_df['Kwota'],
        name='Pojedyncze wpłaty',
        marker_color='#0e7490',
        hovertemplate='%{x|%d.%m.%Y}<br>Wpłata: %{y:,.2f} ' + currency
    ))
    
    # Konfigurujemy układ wykresu
    fig.update_layout(
        xaxis_title="Data",
        yaxis_title=f"Kwota ({currency})",
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=10, r=10, t=10, b=10),
        height=350,
        barmode='overlay',
        template='plotly_white'
    )
    
    # Wyświetlamy wykres
    st.plotly_chart(fig, use_container_width=True)
    
    # Dodajemy statystyki
    if len(schedule_df) > 0:
        total_invested = schedule_df['Kwota'].sum()
        avg_investment = schedule_df['Kwota'].mean()
        num_investments = len(schedule_df)
        
        # Wyświetlamy statystyki w trzech kolumnach
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Całkowita inwestycja", 
                f"{total_invested:,.2f} {currency}"
            )
        
        with col2:
            st.metric(
                "Średnia wpłata", 
                f"{avg_investment:,.2f} {currency}"
            )
        
        with col3:
            st.metric(
                "Liczba wpłat", 
                f"{num_investments}"
            )


def plot_cost_breakdown(portfolio_df: pd.DataFrame, currency: str = 'EUR') -> None:
    """
    Tworzy wykres rozkładu kosztów magazynowania.
    
    Args:
        portfolio_df: DataFrame z portfelem inwestycji.
        currency: Waluta kwot.
    """
    if portfolio_df.empty or 'Koszt_magazynowania' not in portfolio_df.columns:
        st.warning("Brak danych o kosztach magazynowania.")
        return
    
    # Grupujemy po dacie i metalu
    costs_by_date_metal = portfolio_df.groupby(['Data', 'Metal'])['Koszt_magazynowania'].sum().reset_index()
    
    # Tworzymy wykres
    fig = px.bar(
        costs_by_date_metal,
        x='Data',
        y='Koszt_magazynowania',
        color='Metal',
        color_discrete_map=METAL_COLORS,
        labels={
            'Data': 'Data',
            'Koszt_magazynowania': f'Koszt magazynowania ({currency})',
            'Metal': 'Metal'
        },
        title=None
    )
    
    # Konfigurujemy układ wykresu
    fig.update_layout(
        xaxis_title="Data",
        yaxis_title=f"Koszt magazynowania ({currency})",
        legend_title="Metal",
        hovermode="x unified",
        margin=dict(l=10, r=10, t=10, b=10),
        height=350,
        template='plotly_white'
    )
    
    # Wyświetlamy wykres
    st.plotly_chart(fig, use_container_width=True)
