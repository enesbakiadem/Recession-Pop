from pathlib import Path

import pandas as pd
from scipy import stats

# ── Paths ────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
RESULTS_DIR = DATA_DIR / "results"

BILLBOARD_PATH = RAW_DIR / "Billboard_Hot100_Songs_Spotify_1946-2022.csv"
MASTER_PATH = PROCESSED_DIR / "master.csv"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# ── Parameters ────────────────────────────────────────────────
START_YEAR = 2000
END_YEAR = 2022

CRISIS_YEARS = {
    "Finanzkrise": [2008, 2009, 2010],
    "COVID": [2020, 2021],
}

# ── Load data ─────────────────────────────────────────────────
billboard = pd.read_csv(BILLBOARD_PATH, encoding="latin-1")
billboard["year"] = billboard["Hot100 Ranking Year"]

master = pd.read_csv(MASTER_PATH)

# ── Data cleaning ─────────────────────────────────────────────
billboard = billboard[
    ~billboard["Song"].str.contains("Karaoke", case=False, na=False)
]
billboard = billboard[
    ~billboard["Artist Names"].str.contains("Karaoke", case=False, na=False)
]

print(f"Songs after cleaning: {len(billboard)}")

# ── Aggregate music features by year ─────────────────────────
musik = (
    billboard.groupby("year")[["Valence", "Energy", "Danceability"]]
    .mean()
    .reset_index()
)

usa = master[master["Country Code"] == "USA"][
    ["Jahr", "GDP", "Unemployment", "Inflation"]
].copy()
usa = usa.rename(columns={"Jahr": "year"})

# ── Merge and filter time range ──────────────────────────────
combined = musik.merge(usa, on="year")
combined = combined[combined["year"].between(START_YEAR, END_YEAR)].copy()

# ── Correlation analysis ─────────────────────────────────────
korrelation = combined[
    ["Valence", "Energy", "Danceability", "Unemployment"]
].corr()

korr, p_wert = stats.pearsonr(combined["Unemployment"], combined["Energy"])
print(f"Correlation Energy ↔ Unemployment: {korr:.3f}")
print(f"P-value: {p_wert:.4f}")

# ── Lag analysis ─────────────────────────────────────────────
combined["Energy_lag1"] = combined["Energy"].shift(1)
combined["Unemployment_lag1"] = combined["Unemployment"].shift(1)

lag_korr = combined["Unemployment"].corr(combined["Energy_lag1"])
lag_korr2 = combined["Energy"].corr(combined["Unemployment_lag1"])

print(f"Unemployment → Energy (1 year later): {lag_korr:.3f}")
print(f"Energy → Unemployment (1 year later): {lag_korr2:.3f}")

# ── Song comparison lists ────────────────────────────────────
ergebnisse = []

for krise, jahre in CRISIS_YEARS.items():
    data = billboard[billboard["year"].isin(jahre)].copy()

    top_energie = data.nlargest(10, "Energy")[
        ["year", "Song", "Artist Names", "Energy"]
    ].copy()
    top_energie["Krise"] = krise
    top_energie["Typ"] = "Energetisch"

    top_mellow = data.nsmallest(10, "Energy")[
        ["year", "Song", "Artist Names", "Energy"]
    ].copy()
    top_mellow["Krise"] = krise
    top_mellow["Typ"] = "Mellow"

    ergebnisse.append(top_energie)
    ergebnisse.append(top_mellow)

# ── Save outputs ─────────────────────────────────────────────
combined.to_csv(
    PROCESSED_DIR / "musik_wirtschaft_final.csv",
    index=False,
    decimal=",",
    sep=";",
)

korrelation.to_csv(
    RESULTS_DIR / "korrelation.csv",
    decimal=",",
    sep=";",
)

combined[["year", "Unemployment", "Energy", "Energy_lag1"]].dropna().to_csv(
    RESULTS_DIR / "lag_analyse.csv",
    index=False,
    decimal=",",
    sep=";",
)

pd.concat(ergebnisse).to_csv(
    RESULTS_DIR / "songs_vergleich.csv",
    index=False,
    decimal=",",
    sep=";",
)

print("All files saved successfully.")