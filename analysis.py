import pandas as pd

print("\n ---- ANALIZA DZIAŁAŃ NIEPOŻĄDANYCH LEKÓW Z GRUPY GLP-1 ---- ")

# 1. Wczytanie danych

df = pd.read_csv("data/adverse_events.csv")

print(f"Liczba wierszy: {len(df)}")
print(f"Liczba kolumn: {len(df.columns)}")

# 2. Spis kolumn

print("\n ---- KOLUMNY ----")
for column in df.columns:
      print(column)


# 3. Brakujące wartości

print("\n---- BRAKUJĄCE WARTOŚCI ----")
empty = df.isna().sum()
print(empty)


# 4. Zgłoszenia i duplikaty

print("\n --- ZGŁOSZENIA --- ")
ilosc_rekordow = len(df)
print(f"Liczba rekordow: {ilosc_rekordow}")

print("\n---- DUPLIKATY ----")
duplikaty = df.duplicated().sum()
print(f"Liczba duplikatów: {duplikaty}")

print("\n---- UNIKALNE RAPORTY ----")
unique = df["safetyreportid"].nunique()
print(f"Liczba unikalnych ID raportów: {unique}")


# 5. Typy danych


print("\n---- TYPY DANYCH ----")
print(df.dtypes)


# 6. Wartości kategorii

print("\n ---- NAZWA SUBSTANCJI CZYNNEJ --- ")
print(df["generic_name"].value_counts())

print("\n ----- NAZWA HANDLOWA ---- ")
print(df["brand_queried"].value_counts())

print("\n---- PŁEĆ ----")
print(df["patient_sex"].value_counts(dropna=False))

print("\n---- JEDNOSTKA WIEKU ----")
print(df["patient_age_unit"].value_counts(dropna=False))

print("\n---- WYNIK REAKCJI ----")
print(df["reaction_outcome"].value_counts(dropna=False))

print("\n--- POWAŻNOŚĆ ZDARZENIA ---")
print(df["serious"].value_counts(dropna=False))


# 7. Statystyki masy ciała

print("\n---- STATYSTYKI MASY CIAŁA PACJENTÓW ----")
print(df["patient_weight_kg"].describe())

# 8. Uzupełnienie brakujących wartości. Usunięcie części brakujących rekordów.

print("\n ---- UZUPEŁNIENIE/USUNIĘCIE BRAKUJĄCYCH WARTOŚCI I KONTROLA BRAKÓW ----")

rekordy_przed = len(df)
df = df.dropna(how='all')
rekordy_po = len(df)

df.fillna({'patient_sex': 'Unknown'}, inplace=True)
df.fillna({'reaction_outcome': 'Unknown'}, inplace=True)


empty_patient_sex = df["patient_sex"].isna().sum()
empty_reaction_outcome = df["reaction_outcome"].isna().sum()


print(f"\nIlość brakujących danych w kolumnie patient_sex: {empty_patient_sex}")
print(f"\nIlość brakujących danych w kolumnie reaction_outcome: {empty_reaction_outcome}")

print(f"\nIlość całkowicie pustych rekordów które usunięto: {rekordy_przed - rekordy_po}")

rekordy_przed2 = len(df)
df = df.dropna(subset=['generic_name'])
rekordy_po2 = len(df)

print(f"\nIlość rekordów bez nazwy substancji czynnej, które zostały usunięte: {rekordy_przed2 - rekordy_po2}")


# 9. Kontrola braków.

print("\n---- BRAKI PO UZUPEŁNIENIU ----")
print(df.isna().sum())


# 10. Wiek w latach.

df["age_years"] = df["patient_age"].where(df["patient_age_unit"] == "Year")

print("\n ---- STATYSTYKI WIEKU W LATACH ---- ")
print(df["age_years"].describe())


# 11. Utworzenie tabeli unikalnych zgłoszeń.
# Do pracy na takich danych jak: wiek, waga, płeć pacjenta.

df_unique = df.drop_duplicates(subset=["safetyreportid"])

ilosc_zgloszen = len(df_unique)
ilosc_zgloszonych_dzialan_niepozadanych = len(df)
print(f"\nIlość unikalnych zgłoszeń: {ilosc_zgloszen}")
print(f"\nIlość zgłoszonych działań niepożadanych: {ilosc_zgloszonych_dzialan_niepozadanych} ")

# ------------------- FILTROWANIE DANYCH -------------------

# 12. Filtrowanie według wieku.

print("\n---FILTROWANIE WEDŁUG WIEKU ----")

age_under_18 = df_unique[df_unique["age_years"] < 18]
age_18_65 = df_unique[(df_unique["age_years"] >= 18) & (df_unique["age_years"] <= 65)]
age_over_65 = df_unique[df_unique["age_years"] > 65]
age_unknown = df_unique[df_unique["patient_age_unit"] == "Unknown" ]

print(f"\nLiczba zgłoszeń pacjentów poniżej 18 r.ż.: {len(age_under_18)}")
print(f"\nLiczba zgłoszeń pacjentów w wieku 18-65 lat: {len(age_18_65)}")
print(f"\nLiczba zgłoszeń pacjentów w wieku powyżej 65 lat: {len(age_over_65)}")
print(f"\nLiczba zgłoszeń pacjentów których wiek nie został podany: {len(age_unknown)} ")

# 13. Filtrowanie według płci.

print("\n---FILTROWANIE WEDŁUG PŁCI ----")

female = df_unique[df_unique["patient_sex"] == "Female"]
male = df_unique[df_unique["patient_sex"] == "Male"]
unknown = df_unique[df_unique["patient_sex"] == "Unknown"]

print(f"\nPłeć: kobieta, liczba zgłoszeń: {len(female)}")
print(f"\nPłeć: mężczyzna, liczba zgłoszeń: {len(male)}")
print(f"\nPłeć: nieznana, liczba zgłoszeń: {len(unknown)}")

# 14. Filtrowanie według substancji czynnej.
# Sprawdzamy ile zgłoszeń dotyczyło danej substancji.

print("\n--- FILTROWANIE WEDŁUG SUBSTANCJI CZYNNEJ ----")

semaglutide = df_unique[df_unique["generic_name"] == "semaglutide"]
exenatide = df_unique[df_unique["generic_name"] == "exenatide"]
liraglutide = df_unique[df_unique["generic_name"] == "liraglutide"]
tirzepatide = df_unique[df_unique["generic_name"] == "tirzepatide"]
albiglutide = df_unique[df_unique["generic_name"] == "albiglutide"]
dulaglutide = df_unique[df_unique["generic_name"] == "dulaglutide"]
lixisenatide = df_unique[df_unique["generic_name"] == "lixisenatide"]

print(f"\nLiczba zgłoszeń dotycząca semaglutide: {len(semaglutide)}")
print(f"Liczba zgłoszeń dotycząca exenatide: {len(exenatide)}")
print(f"Liczba zgłoszeń dotycząca liraglutide: {len(liraglutide)}")
print(f"Liczba zgłoszeń dotycząca tirzepatide: {len(tirzepatide)}")
print(f"Liczba zgłoszeń dotycząca albiglutide: {len(albiglutide)}")
print(f"Liczba zgłoszeń dotycząca dulaglutide: {len(dulaglutide)}")
print(f"Liczba zgłoszeń dotycząca lixisenatide: {len(lixisenatide)}")

# 15. Filtrowanie według powagi zgłoszeń.

print("\n --- FILTROWANIE WEDŁUG POWAŻNOŚCI ZGŁOSZONEGO DZIAŁANIA NIEPOŻĄDANEGO --- ")

serious = df[df["serious"] == True]
print(f"\nLiczba działań niepożądanych określonych jako poważne to: {len(serious)}")

