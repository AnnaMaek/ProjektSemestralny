import pandas as pd
import streamlit as st

from visualizations import (
    plot_substance_bar,
    plot_age_histogram,
    plot_weight_by_sex,
    plot_sex_bar,
    plot_age_weight
)

# ==========================================
# KONFIGURACJA APLIKACJI
# ==========================================

st.set_page_config(
    page_title="Analiza działań niepożądanych GLP-1",
    layout="wide"
)


# ==========================================
# TYTUŁ
# ==========================================

st.title("Analiza działań niepożądanych leków z grupy GLP-1")

st.write(
    "Aplikacja umożliwia analizę zgłoszonych działań "
    "niepożądanych z uwzględnieniem wieku, płci, "
    "substancji czynnej i powagi działania."
)


# ==========================================
# WCZYTANIE DANYCH
# ==========================================

df = pd.read_csv("data/adverse_events.csv")

df = df.dropna(how="all")

df.fillna(
    {
        "patient_sex": "Unknown",
        "reaction_outcome": "Unknown"
    },
    inplace=True
)

df = df.dropna(
    subset=["generic_name"]
)


# ==========================================
# PRZYGOTOWANIE DANYCH
# ==========================================

df.loc[
    df["patient_weight_kg"] < 30,
    "patient_weight_kg"
] = pd.NA

df.loc[
    df["patient_weight_kg"] > 500,
    "patient_weight_kg"
] = pd.NA

df.loc[
    df["patient_age"] < 12,
    "patient_age"
] = pd.NA


df["age_years"] = df["patient_age"].where(
    df["patient_age_unit"] == "Year"
)


df_unique = df.drop_duplicates(
    subset=["safetyreportid"]
)


# ==========================================
# PODSTAWOWE INFORMACJE
# ==========================================

st.subheader("Podstawowe informacje")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Liczba działań niepożądanych",
        len(df)
    )

with col2:
    st.metric(
        "Liczba unikalnych zgłoszeń",
        len(df_unique)
    )

with col3:
    st.metric(
        "Liczba substancji czynnych",
        df_unique["generic_name"].nunique()
    )

# ==========================================
# FILTRY
# ==========================================

st.sidebar.header("Filtry")


# Substancja czynna

substancje = sorted(
    df_unique["generic_name"].dropna().unique()
)

wybrana_substancja = st.sidebar.selectbox(
    "Substancja czynna",
    ["Wszystkie"] + substancje
)


# Płeć

plec = st.sidebar.selectbox(
    "Płeć",
    [
        "Wszystkie",
        "Female",
        "Male",
        "Unknown"
    ]
)


# Wiek

wiek_min = st.sidebar.number_input(
    "Minimalny wiek",
    min_value=12,
    max_value=120,
    value=12
)

wiek_max = st.sidebar.number_input(
    "Maksymalny wiek",
    min_value=12,
    max_value=120,
    value=120
)
poważność = st.sidebar.selectbox(
    "Powaga działania niepożądanego",
    [
        "Wszystkie",
        "Poważne",
        "Niepoważne"
    ]
)

if wiek_min > wiek_max:
    st.error("Minimalny wiek nie może być większy od maksymalnego.")
    st.stop()

# ==========================================
# FILTROWANIE ZGŁOSZEŃ
# ==========================================

# Filtrowanie unikalnych zgłoszeń
filtered_unique = df_unique.copy()

if wybrana_substancja != "Wszystkie":
    filtered_unique = filtered_unique[
        filtered_unique["generic_name"] == wybrana_substancja
    ]

if plec != "Wszystkie":
    filtered_unique = filtered_unique[
        filtered_unique["patient_sex"] == plec
    ]

filtered_unique = filtered_unique[
    (filtered_unique["age_years"] >= wiek_min) &
    (filtered_unique["age_years"] <= wiek_max)
]


# Filtrowanie wszystkich działań niepożądanych
filtered_df = df.copy()

if wybrana_substancja != "Wszystkie":
    filtered_df = filtered_df[
        filtered_df["generic_name"] == wybrana_substancja
    ]

if plec != "Wszystkie":
    filtered_df = filtered_df[
        filtered_df["patient_sex"] == plec
    ]

filtered_df = filtered_df[
    (filtered_df["age_years"] >= wiek_min) &
    (filtered_df["age_years"] <= wiek_max)
]

if poważność == "Poważne":
    filtered_df = filtered_df[
        filtered_df["serious"] == True
    ]



elif poważność == "Niepoważne":
    filtered_df = filtered_df[
        filtered_df["serious"] == False
    ]



# ==========================================
# WYNIK FILTROWANIA
# ==========================================

st.subheader("Wynik filtrowania")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Liczba unikalnych zgłoszeń",
        len(filtered_unique)
    )

with col2:
    st.metric(
        "Liczba działań niepożądanych",
        len(filtered_df)
    )

# ==========================================
# STATYSTYKI DLA PRZEFILTROWANYCH DANYCH
# ==========================================

st.subheader("Statystyki")

col1, col2, col3, col4 = st.columns(4)

with col1:
    sredni_wiek = filtered_unique["age_years"].mean()

    if pd.isna(sredni_wiek):
        st.metric("Średni wiek", "Brak danych")
    else:
        st.metric(
            "Średni wiek",
            f"{sredni_wiek:.2f} lat"
        )

with col2:
    mediana_wieku = filtered_unique["age_years"].median()

    if pd.isna(mediana_wieku):
        st.metric("Mediana wieku", "Brak danych")
    else:
        st.metric(
            "Mediana wieku",
            f"{mediana_wieku:.2f} lat"
        )

with col3:
    srednia_masa = filtered_unique["patient_weight_kg"].mean()

    if pd.isna(srednia_masa):
        st.metric("Średnia masa", "Brak danych")
    else:
        st.metric(
            "Średnia masa",
            f"{srednia_masa:.2f} kg"
        )

with col4:
    liczba_powaznych = (
        filtered_df["serious"] == True
    ).sum()

    st.metric(
        "Poważne działania",
        liczba_powaznych
    )
# ==========================================
# DANE DO WYKRESU SUBSTANCJI
# ==========================================

filtered_substances = (
    filtered_unique["generic_name"]
    .value_counts()
)
# ==========================================
# WYKRESY
# ==========================================

st.subheader("Liczba zgłoszeń według substancji czynnej")

fig = plot_substance_bar(filtered_substances)

st.pyplot(fig)


st.subheader("Rozkład wieku pacjentów")

fig_age = plot_age_histogram(filtered_unique)

st.pyplot(fig_age)


st.subheader("Rozkład masy ciała według płci")

fig_weight = plot_weight_by_sex(filtered_unique)

st.pyplot(fig_weight)


st.subheader("Zależność wieku i masy ciała")

fig_scatter = plot_age_weight(filtered_unique)

st.pyplot(fig_scatter)


st.subheader("Liczba zgłoszeń według płci")

fig_sex = plot_sex_bar(
    filtered_unique["patient_sex"].value_counts()
)

st.pyplot(fig_sex)