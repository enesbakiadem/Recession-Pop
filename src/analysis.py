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

billboard["Artist Names"] = billboard["Artist Names"].str.strip("[]").str.replace("'", "")

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

korrelation = combined[['Valence', 'Energy', 'Danceability', 'Unemployment']].corr()

target = korrelation['Unemployment'].drop('Unemployment').reset_index()
target.columns = ['Faktor', 'Korrelation']

target.to_csv(
    RESULTS_DIR / "correlation_clean.csv",
    index=False,
    sep=";",
    decimal=","
)

korr, p_wert = stats.pearsonr(combined["Unemployment"], combined["Energy"])
print(f"Correlation Energy ↔ Unemployment: {korr:.3f}")
print(f"P-value: {p_wert:.4f}")

# ── Lag analysis ─────────────────────────────────────────────
lags = range(-2, 4)  # -2 bis +3 Jahre
lag_results = []

for lag in lags:
    if lag == 0:
        korr = combined['Unemployment'].corr(combined['Energy'])
        label = 'Kein Lag (gleichzeitig)'
    elif lag > 0:
        energy_shifted = combined['Energy'].shift(lag)
        korr = combined['Unemployment'].corr(energy_shifted)
        label = f'Unemployment -> Energy ({lag} year{"s" if lag > 1 else ""} later)'
    else:
        unemployment_shifted = combined['Unemployment'].shift(abs(lag))
        korr = combined['Energy'].corr(unemployment_shifted)
        label = f'Energy -> Unemployment ({abs(lag)} year{"s" if abs(lag) > 1 else ""} later)'
    
    lag_results.append({'Lag': lag, 'Korrelation': korr, 'Beschreibung': label})

lag_df = pd.DataFrame(lag_results)
print(lag_df.to_string(index=False))

# ── Song comparison lists ────────────────────────────────────
ergebnisse = []

for krise, jahre in CRISIS_YEARS.items():
    data = billboard[billboard["year"].isin(jahre)].copy()

    top_energie = data.nlargest(20, "Energy")[
    ["year", "Song", "Artist Names", "Energy"]
].drop_duplicates(subset=["Song"]).head(10).copy()
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

lag_df.to_csv(
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