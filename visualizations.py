import matplotlib.pyplot as plt
import seaborn as sns

def plot_age_histogram(df_unique):
    plt.figure(figsize=(8, 6))
    df_unique["age_years"].plot(kind="hist", bins=20, edgecolor="black")
    plt.title("Rozkład wieku pacjentów")
    plt.xlabel("Wiek [lata]")
    plt.ylabel("Ilość zgłoszeń")

    plt.show()


def plot_sex_bar(grupa_patient_sex):
    plt.figure(figsize=(8, 6))
    grupa_patient_sex.plot(kind="bar", edgecolor="black", color="green")
    plt.title("Liczba zgłoszeń według płci")
    plt.xlabel("Płeć")
    plt.ylabel("Ilość zgłoszeń")

    plt.show()

def plot_substance_bar(grupa_subst):
    grupa_subst.plot(kind="bar", figsize=(10, 6), color="purple", edgecolor="black")
    plt.title("Liczba zgłoszeń według substancji czynnej")
    plt.xlabel("Substancja czynna")
    plt.ylabel("Liczba zgłoszeń")
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.show()


def plot_age_weight(df_unique):
    sns.scatterplot(data=df_unique, x="age_years", y="patient_weight_kg", alpha=0.3)
    plt.title("Zależność wieku i masy ciała")
    plt.xlabel("Wiek [lata]")
    plt.ylabel("Masa ciała [kg]")

    plt.show()


def plot_weight_by_sex(df_unique):

    plt.figure(figsize=(6, 6))

    sns.boxplot(data=df_unique[df_unique["patient_sex"].isin(["Female", "Male"])], x="patient_sex",
                y="patient_weight_kg")

    plt.title("Rozkład masy ciała według płci")
    plt.xlabel("Płeć")
    plt.ylabel("Masa ciała [kg]")

    plt.tight_layout()
    plt.show()