import streamlit as st
import pandas as pd
import numpy as np
import joblib

# 1. Konfiguracja strony
st.set_page_config(page_title="Wycena Mieszkań - Gdańsk", page_icon="🏙️")
st.title("🏙️ Kalkulator Cen Mieszkań w Gdańsku")
st.markdown(
    "Aplikacja oparta na modelu ekonometrycznym (Regresja Wieloraka z transformacją Log-Lin), wytrenowanym na danych zebranych z portalu OLX.")

# NOWY ELEMENT: Rozwijana sekcja (Expander) z podziałem dzielnic
with st.expander("ℹ️ Zobacz, jakie dzielnice wchodzą w skład poszczególnych makroregionów"):
    st.markdown("""
    * **Centrum_Prestiż:** Śródmieście, Wrzeszcz, Oliwa, Przymorze, Żabianka, Aniołki, Brzeźno, Letnica, Strzyża, Piecki-Migowo
    * **Południe_Sypialnie:** Chełm, Ujeścisko, Jasień, Orunia, Siedlce
    * **Wschód_Portowe:** Nowy Port, Stogi, Rudniki, Krakowiec, Młyniska
    * **Obrzeża_Zachód:** Osowa, Kokoszki
    """)


# 2. Wczytanie zapisanego modelu
@st.cache_resource  # Zapamiętuje model, żeby nie ładować go przy każdym kliknięciu
def load_model():
    return joblib.load('model_wyceny_gdansk.pkl')


model = load_model()

# 3. Interfejs użytkownika (Pasek boczny)
st.sidebar.header("Parametry Mieszkania")

powierzchnia = st.sidebar.slider("Metraż (m²)", min_value=30.0, max_value=150.0, value=50.0, step=1.0)

# Nasze 4 główne makroregiony
makroregion = st.sidebar.selectbox("Wybierz lokalizację:", [
    "Wschód_Portowe (np. Nowy Port, Stogi)",
    "Centrum_Prestiż (np. Wrzeszcz, Oliwa, Śródmieście)",
    "Południe (np. Chełm, Jasień)",
    "Obrzeża_Zachód (np. Osowa, Kokoszki)"
])

# 4. Przetworzenie danych z interfejsu pod wymogi modelu
wektor_danych = {
    'const': 1.0,
    'Powierzchnia_m2': powierzchnia,
    'Centrum_Prestiż': 1.0 if "Centrum" in makroregion else 0.0,
    'Obrzeża_Zachód': 1.0 if "Obrzeża" in makroregion else 0.0,
    'Południe': 1.0 if "Południe" in makroregion else 0.0
}

# 5. Predykcja po wciśnięciu przycisku
if st.sidebar.button("Wyceń Mieszkanie 🚀"):
    X_nowe = pd.DataFrame([wektor_danych])

    log_cena = model.predict(X_nowe)[0]
    cena_pln = np.exp(log_cena)

    st.success("Analiza zakończona sukcesem!")
    st.metric(label="Szacowana wartość nieruchomości:", value=f"{cena_pln:,.0f} PLN".replace(',', ' '))
    st.write(f"Cena za metr kwadratowy: **{cena_pln / powierzchnia:,.0f} PLN**".replace(',', ' '))

    st.info(
        "💡 Pamiętaj: Wycena jest szacunkowa i opiera się na ofertach rynkowych (tzw. cenach ofertowych, a nie transakcyjnych). Kategoria 'Wschód_Portowe' służy jako baza odniesienia dla algorytmu.")
