# Gdańsk-Real-Estate-Pricing-Model-and-Web-Scraper
## Cel Projektu (Business Objective)
Celem projektu było stworzenie narzędzia typu End-to-End do zautomatyzowanego pobierania, czyszczenia i analizy ofert z rynku nieruchomości w Gdańsku. Ostatecznym wynikiem jest w pełni interpretowalny model ekonometryczny, który wycenia wartość mieszkań na podstawie ich parametrów fizycznych oraz lokalizacji, przy zachowaniu odporności na problem przeuczenia (overfitting).

## Architektura i Technologie (Tech Stack)
* **Web Scraping:** Python, BeautifulSoup4, Requests
* **Przetwarzanie Danych:** Pandas, NumPy, Regex (Wyrażenia regularne)
* **Feature Engineering:** Geopy (Geokodowanie), One-Hot Encoding
* **Machine Learning / Ekonometria:** statsmodels (OLS), scikit-learn (LinearRegression, RepeatedKFold)

## Struktura Projektu (Project Structure)
```text
webscraper/
│
├── 01_scraper_olx.py                            # Skrypt pobierający dane z OLX
├── 02_03_data_engineering_and_modeling.ipynb    # Notatnik Jupyter z czyszczeniem danych i modelowaniem
├── OLX_Mieszkania_Gdansk.xlsx                   # Baza pobranych danych (przykładowa)
├── requirements.txt                             # Plik z wymaganymi bibliotekami
└── .gitignore                                   # Pliki ignorowane w repozytorium
```

## Metodologia i Przebieg Badania
Projekt składa się z dwóch głównych etapów:

1. **Zbieranie danych (`01_scraper_olx.py`):** 
   Napisanie własnego robota sieciowego (uwzględniającego paginację i "etykietę" scrapingu) w celu ekstrakcji surowych danych (Cena, Metraż, Lokalizacja) z portalu OLX.
2. **Analiza, Inżynieria Cech i Modelowanie (`02_03_data_engineering_and_modeling.ipynb`):**
   * Translacja brudnego tekstu na struktury danych.
   * Obsługa braków danych i wartości odstających (Outliers).
   * Transformacja zmiennych kategorycznych (dzielnice) z użyciem słowników i grupowanie w 4 kluczowe makroregiony w celu zapobiegania "klątwie wymiarowości".
   * Transformacja logarytmiczna zmiennej zależnej (Log-Lin Model) w celu stabilizacji wariancji i spłaszczenia rozkładu cen.
   * Zabezpieczenie przed idealną współliniowością (Dummy Variable Trap) poprzez celowe wykluczenie kategorii bazowej.
   * Weryfikacja stabilności algorytmu za pomocą powtarzanej walidacji krzyżowej (Repeated 5-Fold CV na 50 iteracjach).
   * Twarda diagnostyka ekonometryczna: weryfikacja braku współliniowości zmiennych za pomocą wskaźnika VIF (Variance Inflation Factor) oraz wizualna analiza reszt (Residuals vs Fitted plot) potwierdzająca homoskedastyczność.

## Główne Wnioski Analityczne (Insights)
* **Model OLS (Log-Lin)** zredukowany do 4 kluczowych makroregionów osiągnął stabilną wartość **R² na poziomie ok. 64%** na danych testowych w walidacji krzyżowej.
* **Znaczenie metrażu:** Każdy dodatkowy metr kwadratowy powierzchni zwiększa wycenę nieruchomości średnio o 1,65% (ceteris paribus).
* **Premia za prestiż:** Algorytm potwierdził, że mieszkania zlokalizowane w obrębie centralnego pasma Gdańska (np. Wrzeszcz, Śródmieście, Oliwa) są wyceniane średnio o ~38% wyżej w stosunku do dzielnic przemysłowo-portowych (bazy).
* **Pozytywna diagnostyka modelu:** Ostateczny model pomyślnie przeszedł testy założeń klasycznej regresji. Odpowiednie grupowanie makroregionów wyeliminowało problem współliniowości (wartości VIF bezpiecznie poniżej progu alarmowego), a transformacja Log-Lin skutecznie ustabilizowała wariancję błędów.

## 🚀 Jak uruchomić projekt (How to Run)
1. **Sklonuj repozytorium** na swój komputer.
2. **Zainstaluj wymagane biblioteki** za pomocą pliku `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```
3. **Uruchomienie pobierania danych (opcjonalnie):**
   ```bash
   python 01_scraper_olx.py
   ```
4. **Uruchomienie analizy:** Otwórz Jupyter Notebook i uruchom plik `02_03_data_engineering_and_modeling.ipynb`.

