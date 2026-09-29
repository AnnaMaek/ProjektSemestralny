import matplotlib.pyplot as plt
import seaborn as sns

def plot_age_histogram(df_unique):
    fig, ax = plt.subplots(figsize=(8, 6))

    df_unique["age_years"].dropna().plot(
        kind="hist",
        bins=20,
        edgecolor="black",
        ax=ax
    )

    ax.set_title("Rozkład wieku pacjentów")
    ax.set_xlabel("Wiek [lata]")
    ax.set_ylabel("Liczba zgłoszeń")

    fig.tight_layout()

    return fig

def plot_sex_bar(grupa_patient_sex):
    fig, ax = plt.subplots(figsize=(8, 6))

    grupa_patient_sex.plot(
        kind="bar",
        color="green",
        edgecolor="black",
        ax=ax
    )

    ax.set_title("Liczba zgłoszeń według płci")
    ax.set_xlabel("Płeć")
    ax.set_ylabel("Liczba zgłoszeń")
    ax.tick_params(axis="x", rotation=0)

    fig.tight_layout()

    return fig

def plot_substance_bar(grupa_subst):
    fig, ax = plt.subplots(figsize=(10, 6))

    grupa_subst.plot(
        kind="bar",
        edgecolor="black",
        color="purple",
        ax=ax
    )

    ax.set_title("Liczba zgłoszeń według substancji czynnej")
    ax.set_xlabel("Substancja czynna")
    ax.set_ylabel("Liczba zgłoszeń")
    ax.tick_params(axis="x", rotation=45)

    fig.tight_layout()

    return fig


def plot_age_weight(df_unique):
    data = df_unique[
        ["age_years", "patient_weight_kg"]
    ].dropna()

    fig, ax = plt.subplots(figsize=(10, 6))

    sns.scatterplot(
        data=data,
        x="age_years",
        y="patient_weight_kg",
        ax=ax
    )

    ax.set_title("Zależność wieku i masy ciała")
    ax.set_xlabel("Wiek [lata]")
    ax.set_ylabel("Masa ciała [kg]")

    fig.tight_layout()

    return fig

def plot_weight_by_sex(df_unique):
    data = df_unique[
        df_unique["patient_sex"].isin(["Female", "Male"])
    ]

    fig, ax = plt.subplots(figsize=(8, 6))

    sns.boxplot(
        data=data,
        x="patient_sex",
        y="patient_weight_kg",
        ax=ax
    )

    ax.set_title("Rozkład masy ciała według płci")
    ax.set_xlabel("Płeć")
    ax.set_ylabel("Masa ciała [kg]")

    fig.tight_layout()

    return fig