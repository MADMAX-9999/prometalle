# Prometalle - Zaawansowany Symulator Inwestycji w Metale Szlachetne

![Prometalle Logo](https://img.shields.io/badge/Prometalle-Symulator_Metali_Szlachetnych-blue?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IiNGRkQ3MDAiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIj48cGF0aCBkPSJNMTIgMjJzOC0yIDgtMTBWNWwtOC0zLTggM3Y3YzAgOCA4IDEwIDggMTB6Ii8+PC9zdmc+)

Prometalle to interaktywna aplikacja Streamlit do zaawansowanej symulacji i analizy inwestycji w metale szlachetne (złoto, srebro, platyna, pallad) w oparciu o rzeczywiste historyczne dane LBMA (London Bullion Market Association).

## 🌟 Funkcje

- **Kompleksowa analiza portfela** - śledzenie wartości inwestycji w czasie rzeczywistym
- **Zaawansowane wizualizacje** - interaktywne wykresy i porównania różnych scenariuszy
- **Symulacja kosztów przechowywania** - uwzględnienie kosztów depozytariusza
- **Wielowalutowość** - obsługa PLN, EUR, USD
- **Symulacja zakupów systematycznych** - testowanie strategii regularnych inwestycji
- **Rebalancing portfela** - optymalizacja i utrzymanie docelowej alokacji
- **Prognozowanie przyszłych kosztów i wartości** - projekcje długoterminowe
- **Wielojęzyczność** - dostępna w języku polskim, angielskim i niemieckim
- **Eksport danych** - możliwość wygenerowania raportów PDF i plików Excel

## 📋 Wymagania

- Python 3.8+
- Streamlit 1.20+
- Pandas
- Plotly
- Matplotlib
- NumPy
- Reportlab (do generowania raportów PDF)

## 🚀 Instalacja

1. Sklonuj repozytorium:
```bash
git clone https://github.com/twoja-nazwa/prometalle.git
cd prometalle
```

2. Zainstaluj wymagane biblioteki:
```bash
pip install -r requirements.txt
```

3. Uruchom aplikację:
```bash
streamlit run app.py
```

## 📁 Struktura projektu

```
prometalle/
│
├── app.py                     # Główny plik aplikacji
├── requirements.txt           # Wymagane biblioteki
├── README.md                  # Dokumentacja projektu
│
├── data/                      # Dane historyczne
│   ├── metal_prices.csv       # Ceny metali szlachetnych
│   ├── exchange_rates.csv     # Kursy walutowe
│   └── inflation_rates_ready.csv # Dane o inflacji
│
├── assets/                    # Zasoby aplikacji
│   ├── styles.css             # Arkusz stylów
│   └── logo.png               # Logo aplikacji
│
└── modules/                   # Moduły funkcjonalne
    ├── analysis.py            # Analiza inwestycji
    ├── charts.py              # Funkcje wizualizacji 
    ├── config.py              # Konfiguracja aplikacji
    ├── inflation.py           # Obsługa inflacji
    ├── metals.py              # Obsługa cen metali
    ├── portfolio.py           # Zarządzanie portfelem
    ├── purchase_schedule.py   # Harmonogram zakupów
    ├── storage_costs.py       # Koszty magazynowania
    ├── translation.py         # Tłumaczenia
    └── utils.py               # Funkcje pomocnicze
```

## 📊 Przykłady użycia

### Podstawowa symulacja
1. Wybierz kwotę inwestycji (np. 100,000 EUR)
2. Ustal alokację między metalami (np. 40% złoto, 30% srebro, 15% platyna, 15% pallad)
3. Wybierz okres inwestycji
4. Kliknij "Rozpocznij symulację"

### Zakupy systematyczne
1. Ustaw częstotliwość (np. co miesiąc)
2. Określ kwotę systematycznego zakupu (np. 250 EUR)
3. Wybierz dzień zakupu
4. Uruchom symulację

### Analiza kosztów magazynowania
1. Ustaw stawkę magazynowania (np. 0.5% rocznie)
2. Wybierz podstawę naliczania (wartość metali lub kwota inwestycji)
3. Wybierz sposób pokrycia kosztów (gotówka, sprzedaż metali, itp.)
4. Uruchom symulację aby zobaczyć wpływ kosztów na portfel

## 🛠️ Zaawansowane funkcje

### Rebalancing portfela
Aplikacja umożliwia automatyczny rebalancing portfela zgodnie z docelową alokacją, co pozwala na utrzymanie pożądanej struktury portfela niezależnie od zmian cen poszczególnych metali.

### Prognozy
Moduł prognozowania umożliwia przewidywanie przyszłej wartości portfela w oparciu o historyczne dane i założenia dotyczące inflacji oraz wzrostu cen metali.

### Porównanie z innymi aktywami
Funkcja porównania pozwala zestawić wyniki inwestycji w metale szlachetne z innymi klasami aktywów, takimi jak indeksy giełdowe, obligacje czy nieruchomości.

## 📄 Licencja

Ten projekt jest udostępniany na licencji MIT. Szczegóły znajdują się w pliku LICENSE.

## 📬 Kontakt

W przypadku pytań lub uwag, prosimy o kontakt poprzez [Issues](https://github.com/twoja-nazwa/prometalle/issues) na GitHubie.

---

⚠️ *Prometalle to narzędzie edukacyjne i analityczne. Nie stanowi porady inwestycyjnej. Inwestowanie w metale szlachetne wiąże się z ryzykiem. Przed podjęciem decyzji inwestycyjnych zalecamy konsultację z profesjonalnym doradcą finansowym.*
