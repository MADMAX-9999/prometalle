# Symulator ReBalancingu Metali Szlachetnych (LBMA)

Interaktywna aplikacja Streamlit do analizy i symulacji budowy portfela z metali szlachetnych (złoto, srebro, platyna, pallad) w oparciu o historyczne ceny spot LBMA (London Bullion Market Association).

## 📦 Zawartość

- `app.py` – główny plik aplikacji Streamlit
- `lbma_data.csv` – historyczne ceny metali spot od 1977 roku w EUR (Złoto, Srebro, Platyna, Pallad)
- `requirements.txt` – wymagane biblioteki do uruchomienia aplikacji

## 🚀 Uruchomienie lokalne

1. Zainstaluj Streamlit i Pandas:

```bash
pip install -r requirements.txt
```

2. Uruchom aplikację:

```bash
streamlit run app.py
```

3. Aplikacja otworzy się automatycznie w Twojej przeglądarce.

## ☁️ Wdrożenie online (Streamlit Cloud)

1. Utwórz repozytorium na GitHub i dodaj do niego:
   - `app.py`
   - `lbma_data.csv`
   - `requirements.txt`

2. Zaloguj się do [Streamlit Cloud](https://streamlit.io/cloud)

3. Połącz konto z GitHub i wybierz repozytorium do publikacji

4. Kliknij „Deploy” – aplikacja będzie dostępna publicznie

## ⚙️ Funkcje aplikacji

- Ustawienia kapitału początkowego, alokacji i okresu inwestycji
- Symulacja ReBalancingu (do 2 wybranych dat)
- Uwzględnienie kosztów przechowywania i transakcji
- Praca na danych rzeczywistych z LBMA

## 📊 Dane LBMA

Dane pochodzą z dziennych notowań LBMA wyrażonych w EUR, oczyszczone i połączone do formatu CSV.

---

🛡️ *Zaprojektowane jako narzędzie analityczne – nie stanowi porady inwestycyjnej.*
