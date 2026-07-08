import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

print("Rozpoczynam masowe pobieranie danych z OLX...")

naglowki = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

zebrane_mieszkania = []
liczba_stron_do_pobrania = 15

#Pętla przechodząca przez kolejne strony
for strona in range(1, liczba_stron_do_pobrania + 1):
    print(f"-> Skanuję stronę numer {strona}...")

    # Tworzymy dynamiczny link z numerem strony
    url = f"https://www.olx.pl/nieruchomosci/mieszkania/sprzedaz/gdansk/?page={strona}"

    response = requests.get(url, headers=naglowki)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        karty_ogloszen = soup.find_all('div', {'data-cy': 'l-card'})

        for karta in karty_ogloszen:
            tekst_karty = karta.get_text(separator=" ", strip=True)

            # 1. Tytuł
            tytul_tag = karta.find('h6')
            tytul = tytul_tag.text.strip() if tytul_tag else "Brak tytułu"

            # 2. Cena
            cena_match = re.search(r"([\d\s]+)zł", tekst_karty)
            cena_pln = None
            if cena_match:
                cena_czysta = cena_match.group(1).replace(" ", "").replace("\xa0", "")
                try:
                    cena_pln = float(cena_czysta)
                except ValueError:
                    pass

            # 3. Metraż
            metraz_match = re.search(r"([\d\.,]+)\s*m²", tekst_karty)
            powierzchnia = None
            if metraz_match:
                metraz_czysty = metraz_match.group(1).replace(",", ".")
                try:
                    powierzchnia = float(metraz_czysty)
                except ValueError:
                    pass

            # 4. Dzielnica
            dzielnica_match = re.search(r"Gdańsk,\s*([A-Za-zZżźćńółęąśŻŹĆĄŚĘŁÓŃ\s\-]+)", tekst_karty)
            dzielnica = "Nieznana"
            if dzielnica_match:
                dzielnica = dzielnica_match.group(1).strip()

            # Zapisujemy do listy
            if cena_pln and powierzchnia:
                zebrane_mieszkania.append({
                    "Tytul": tytul,
                    "Dzielnica": dzielnica,
                    "Cena_PLN": cena_pln,
                    "Powierzchnia_m2": powierzchnia,
                    "Cena_za_m2": round(cena_pln / powierzchnia, 2)
                })

        #  Czekamy 2 sekundy przed wejściem na kolejną stronę, żeby nie dostać bana od OLX
        time.sleep(2)

    else:
        print(f"Błąd połączenia na stronie {strona}. Kod: {response.status_code}")

print(f"\nUkończono skanowanie! Pomyślnie przetworzono {len(zebrane_mieszkania)} pełnych ogłoszeń.")

# Zapisujemy do Excela
if zebrane_mieszkania:
    df = pd.DataFrame(zebrane_mieszkania)
    nazwa_pliku = "OLX_Mieszkania_Gdansk2.xlsx"
    df.to_excel(nazwa_pliku, index=False)
    print(f"Sukces! Dane zostały nadpisane w pliku: {nazwa_pliku}")