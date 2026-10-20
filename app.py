import pandas as pd
import streamlit as st
from io import BytesIO
from datetime import datetime
from xml.sax.saxutils import escape

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    LongTable,
    TableStyle
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
FONT_DIR = BASE_DIR / "fonts"

pdfmetrics.registerFont(
    TTFont("DejaVu", str(FONT_DIR / "DejaVuSans.ttf"))
)

pdfmetrics.registerFont(
    TTFont("DejaVu-Bold", str(FONT_DIR / "DejaVuSans-Bold.ttf"))
)


from visualizations import (
    plot_substance_bar,
    plot_age_histogram,
    plot_weight_by_sex,
    plot_sex_bar,
    plot_age_weight,
    plot_top_reactions
)


def generuj_pdf_podsumowanie(filtry, statystyki, reakcje):
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm
    )

    styles = getSampleStyleSheet()

    styles["Normal"].fontName = "DejaVu"
    styles["Title"].fontName = "DejaVu-Bold"
    styles["Heading1"].fontName = "DejaVu-Bold"
    styles["Heading2"].fontName = "DejaVu-Bold"
    styles["Heading3"].fontName = "DejaVu-Bold"

    elements = []

    elements.append(
        Paragraph(
            "Raport z analizy działań niepożądanych leków GLP-1",
            styles["Title"]
        )
    )

    elements.append(Spacer(1, 10))

    elements.append(
        Paragraph(
            f"Data wygenerowania: {datetime.now():%Y-%m-%d %H:%M}",
            styles["Normal"]
        )
    )

    elements.append(Spacer(1, 20))

    # ZASTOSOWANE FILTRY
    elements.append(
        Paragraph("1. Zastosowane filtry", styles["Heading2"])
    )

    for nazwa, wartosc in filtry.items():
        elements.append(
            Paragraph(
                f"<b>{escape(str(nazwa))}:</b> "
                f"{escape(str(wartosc))}",
                styles["Normal"]
            )
        )

    elements.append(Spacer(1, 18))

    # STATYSTYKI
    elements.append(
        Paragraph("2. Wynik filtrowania i statystyki", styles["Heading2"])
    )

    tabela_statystyk = [
        ["Wskaźnik", "Wartość"]
    ]

    # Nagłówki drukowanymi literami
    dane_tabeli = [
        ["NAZWA STATYSTYKI", "WARTOŚĆ"],
    ]

    for nazwa, wartosc in statystyki.items():
        dane_tabeli.append([nazwa, str(wartosc)])

    tabela = Table(dane_tabeli, colWidths=[9 * cm, 7 * cm])

    tabela.setStyle(TableStyle([
        # Jasne tło nagłówka i czarny tekst
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E8EEF5")),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),

        # Czcionka obsługująca polskie znaki — także w tabeli
        ("FONTNAME", (0, 0), (-1, -1), "DejaVu"),
        ("FONTNAME", (0, 0), (-1, 0), "DejaVu-Bold"),

        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.white, colors.whitesmoke]),
        ("PADDING", (0, 0), (-1, -1), 7),
    ]))

    elements.append(tabela)
    elements.append(Spacer(1, 18))

    # NAJCZĘSTSZE DZIAŁANIA NIEPOŻĄDANE
    elements.append(
        Paragraph(
            "3. 15 najczęściej zgłaszanych działań niepożądanych",
            styles["Heading2"]
        )
    )

    if reakcje.empty:
        elements.append(
            Paragraph(
                "Brak danych o działaniach niepożądanych.",
                styles["Normal"]
            )
        )
    else:
        for i, (nazwa, liczba) in enumerate(reakcje.items(), start=1):
            elements.append(
                Paragraph(
                    f"{i}. {escape(str(nazwa))} — {liczba} wystąpień",
                    styles["Normal"]
                )
            )

    doc.build(elements)

    return buffer.getvalue()


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
    "substancji czynnej, nazwy handlowej i powagi działania."
)

tab_podsumowanie, tab_wizualizacje, tab_dane = st.tabs(
    ["Podsumowanie", "Wizualizacje", "Dane"]
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
# FILTRY
# ==========================================

st.sidebar.header("Filtry")



# SESSION STATE

if "wybrana_substancja" not in st.session_state:
    st.session_state["wybrana_substancja"] = "Wszystkie"

if "wybrana_nazwa_handlowa" not in st.session_state:
    st.session_state["wybrana_nazwa_handlowa"] = "Wszystkie"



# LISTA SUBSTANCJI


if st.session_state["wybrana_nazwa_handlowa"] == "Wszystkie":

    substancje = sorted(
        df_unique["generic_name"]
        .dropna()
        .unique()
    )

else:

    substancje = sorted(
        df_unique.loc[
            df_unique["brand_queried"]
            == st.session_state["wybrana_nazwa_handlowa"],
            "generic_name"
        ]
        .dropna()
        .unique()
    )



# ========== WYBÓR SUBSTANCJI ==========


wybrana_substancja = st.sidebar.selectbox(
    "Substancja czynna",
    ["Wszystkie"] + substancje,
    key="wybrana_substancja"
)



# LISTA NAZW HANDLOWYCH


if st.session_state["wybrana_substancja"] == "Wszystkie":

    nazwy_handlowe = sorted(
        df_unique["brand_queried"]
        .dropna()
        .unique()
    )

else:

    nazwy_handlowe = sorted(
        df_unique.loc[
            df_unique["generic_name"]
            == st.session_state["wybrana_substancja"],
            "brand_queried"
        ]
        .dropna()
        .unique()
    )



#  ========= WYBÓR NAZWY HANDLOWEJ =======


wybrana_nazwa_handlowa = st.sidebar.selectbox(
    "Nazwa handlowa",
    ["Wszystkie"] + nazwy_handlowe,
    key="wybrana_nazwa_handlowa"
)

# ========== PŁEĆ ===========

plec = st.sidebar.selectbox(
    "Płeć",
    [
        "Wszystkie",
        "Female",
        "Male",
        "Unknown"
    ]
)


# =========  WIEK =============

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

uwzglednij_brak_wieku = st.sidebar.checkbox(
    "Uwzględnij zgłoszenia bez podanego wieku",
    value = True
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

def filtruj_dane(data):
    wynik = data.copy()

    if wybrana_substancja != "Wszystkie":
        wynik = wynik[
            wynik["generic_name"] == wybrana_substancja
        ]

    if wybrana_nazwa_handlowa != "Wszystkie":
        wynik = wynik[
            wynik["brand_queried"] == wybrana_nazwa_handlowa
        ]

    if plec != "Wszystkie":
        wynik = wynik[
            wynik["patient_sex"] == plec
        ]

    zakres_wieku = (
        (wynik["age_years"] >= wiek_min) &
        (wynik["age_years"] <= wiek_max)
    )

    if uwzglednij_brak_wieku:
        wynik = wynik[
            zakres_wieku | wynik["age_years"].isna()
        ]
    else:
        wynik = wynik[zakres_wieku]

    return wynik


filtered_df = filtruj_dane(df)

if poważność == "Poważne":
    filtered_df = filtered_df[
        filtered_df["serious"] == True
    ]

elif poważność == "Niepoważne":
    filtered_df = filtered_df[
        filtered_df["serious"] == False
    ]

filtered_unique = filtered_df.drop_duplicates(
    subset=["safetyreportid"]
)

if filtered_df.empty:
    st.warning("Brak danych dla wybranych filtrów.")
    st.stop()

# ==========================================
# PODSTAWOWE INFORMACJE
# ==========================================

with tab_podsumowanie:

    st.markdown("## 📊 Podstawowe informacje")


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

    st.divider()

    with st.container(border=True):

        st.markdown("## 🎯 Wynik filtrowania")


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

        st.divider()

        st.subheader("Opis zastosowanych filtrów")

        # Substancja czynna
        if wybrana_substancja == "Wszystkie":
            opis_substancji = "wszystkie substancje czynne"
        else:
            opis_substancji = wybrana_substancja

        # Nazwa handlowa
        if wybrana_nazwa_handlowa == "Wszystkie":
            opis_nazwy_handlowej = "konkretna nazwa handlowa nie została wskazana"
        else:
            opis_nazwy_handlowej = wybrana_nazwa_handlowa

        # Płeć
        if plec == "Wszystkie":
            opis_plci = "wszystkie kategorie płci"
        elif plec == "Unknown":
            opis_plci = "brak danych dotyczących płci"
        elif plec == "Female":
            opis_plci = "kobiety"
        else:
            opis_plci = "mężczyźni"

        # Wiek
        opis_wieku = f"{wiek_min}-{wiek_max}"
        if uwzglednij_brak_wieku:
            opis_wieku += " oraz osoby bez podanego wieku"

        # Poważność działania
        if poważność == "Poważne":
            opis_powagi = "działania niepożądane oznaczone jako poważne"
        elif poważność == "Niepoważne":
            opis_powagi = "działania niepożądane które nie zostały zakwalifikowane jako poważne"
        else:
            opis_powagi = "działania niepożądane o każdym stopniu nasilenia"

        st.write(
            f"Analiza obejmuje {opis_substancji}, "
            f"nazwa(y) handlowa(e): {opis_nazwy_handlowej}, "
            f"{opis_plci}, wiek: {opis_wieku}, "
            f"stopień nasilenia: {opis_powagi}. "

        )
        st.divider()



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

            if poważność == "Poważne":
                st.metric(
                    "Liczba działań poważnych",
                    len(filtered_df)
                )

            elif poważność == "Niepoważne":
                st.metric(
                    "Liczba działań niepoważnych",
                    len(filtered_df)
                )

            else:
                st.metric(
                    "Liczba działań niepożądanych",
                    len(filtered_df)
                )

        st.divider()

        st.subheader("15 najczęściej zgłaszanych działań niepożądanych - liczba wystąpień:")

        top10_reactions = (
            filtered_df["reaction"]
            .dropna()
            .value_counts()
            .head(15)
        )

        if top10_reactions.empty:
            st.write("Brak danych o działaniach niepożądanych.")

        else:
            for reakcja, liczba in top10_reactions.items():
                st.write(f"- {reakcja}  -  {liczba} ")

    # ==========================================
    # POBIERANIE RAPORTU PDF
    # ==========================================

    st.divider()
    st.subheader("📄 Pobierz raport podsumowujący")

    filtry_pdf = {
        "Substancja czynna": opis_substancji,
        "Nazwa handlowa": opis_nazwy_handlowej,
        "Płeć": opis_plci,
        "Wiek": opis_wieku,
        "Powaga działania": opis_powagi
    }

    sredni_wiek_pdf = filtered_unique["age_years"].mean()
    mediana_wieku_pdf = filtered_unique["age_years"].median()
    srednia_masa_pdf = filtered_unique["patient_weight_kg"].mean()

    statystyki_pdf = {
        "Liczba działań niepożądanych": len(filtered_df),
        "Liczba unikalnych zgłoszeń": len(filtered_unique),
        "Średni wiek": (
            f"{sredni_wiek_pdf:.2f} lat"
            if pd.notna(sredni_wiek_pdf)
            else "Brak danych"
        ),
        "Mediana wieku": (
            f"{mediana_wieku_pdf:.2f} lat"
            if pd.notna(mediana_wieku_pdf)
            else "Brak danych"
        ),
        "Średnia masa ciała": (
            f"{srednia_masa_pdf:.2f} kg"
            if pd.notna(srednia_masa_pdf)
            else "Brak danych"
        ),
    }

    pdf = generuj_pdf_podsumowanie(
        filtry=filtry_pdf,
        statystyki=statystyki_pdf,
        reakcje=top10_reactions
    )

    st.download_button(
        label="📄 Pobierz raport PDF",
        data=pdf,
        file_name="podsumowanie_glp1.pdf",
        mime="application/pdf",
        key="pobierz_pdf_podsumowanie"
    )

# ==========================================
# DANE DO WYKRESU SUBSTANCJI
# ==========================================

filtered_substances = (
    filtered_unique["generic_name"]
    .value_counts()
)
# ==========================================
# WIZUALIZACJE
# ==========================================

with tab_wizualizacje:

    st.write(
        f"Wykresy utworzone są na podstawie wskazanych danych: "
        f"{opis_substancji}, "
        f"nazwa(y) handlowa(e): {opis_nazwy_handlowej}, "
        f"{opis_plci}, wiek: {opis_wieku}, "
        f"stopień nasilenia: {opis_powagi}. "

    )


    st.subheader("Liczba zgłoszeń według substancji czynnej")

    fig = plot_substance_bar(filtered_substances)

    st.pyplot(fig)

    st.subheader("Analiza wieku i płci")

    col1, col2 = st.columns(2)


    with col1:
        st.write("Rozkład wieku pacjentów")

        fig_age = plot_age_histogram(filtered_unique)

        st.pyplot(fig_age)

    with col2:
        st.write("Liczba zgłoszeń według płci")
        fig_sex = plot_sex_bar(
            filtered_unique["patient_sex"].value_counts()
        )
        st.pyplot(fig_sex)


    st.subheader("Analiza masy ciała")

    col1, col2 = st.columns(2)

    with col1:
        st.write("Zależność wieku i masy ciała")

        fig_scatter = plot_age_weight(filtered_unique)

        st.pyplot(fig_scatter)

    with col2:
        st.write("Rozkład masy ciała według płci")

        fig_weight = plot_weight_by_sex(filtered_unique)

        st.pyplot(fig_weight)



    st.subheader("15 najczęściej zgłaszanych działań niepożądanych")

    fig_top_reactions = plot_top_reactions(filtered_df)
    st.pyplot(fig_top_reactions)

# ==========================================
# DANE
# ==========================================

with tab_dane:

    st.subheader("Przefiltrowane dane")

    st.dataframe(
        filtered_df,
        width="stretch"
    )

    csv = filtered_df.to_csv(
        index=False
    ).encode("UTF-8")

    st.download_button(
        label="Pobierz dane CSV",
        data=csv,
        file_name="wyniki_filtrowania.csv",
        mime="text/csv"
    )
