from pathlib import Path

import pandas as pd
from scipy.stats import pearsonr, spearmanr

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

# ── Parameters ───────────────────────────────────────────────
START_YEAR = 2000
END_YEAR = 2022

CRISIS_YEARS = {
    "Financial Crisis": [2008, 2009, 2010],
    "COVID": [2020, 2021],
}

# ── Load data ────────────────────────────────────────────────
billboard = pd.read_csv(BILLBOARD_PATH, encoding="latin-1")
billboard["year"] = billboard["Hot100 Ranking Year"]

master = pd.read_csv(MASTER_PATH)

# ── Data cleaning ────────────────────────────────────────────
billboard = billboard[
    ~billboard["Song"].str.contains("Karaoke", case=False, na=False)
]
billboard = billboard[
    ~billboard["Artist Names"].str.contains("Karaoke", case=False, na=False)
]

print(f"Songs after cleaning: {len(billboard)}")

billboard["Artist Names"] = (
    billboard["Artist Names"]
    .str.strip("[]")
    .str.replace("'", "", regex=False)
)

# ── Aggregate music features by year ────────────────────────
musik = (
    billboard.groupby("year")[["Valence", "Energy", "Danceability"]]
    .mean()
    .reset_index()
)

usa = master.loc[master["Country Code"] == "USA", ["Jahr", "GDP", "Unemployment", "Inflation"]].copy()
usa = usa.rename(columns={"Jahr": "year"})

# ── Merge and filter time range ─────────────────────────────
combined = musik.merge(usa, on="year", how="inner")
combined = combined[combined["year"].between(START_YEAR, END_YEAR)].copy()
combined = combined.sort_values("year").reset_index(drop=True)

# ── Correlation matrix for export ───────────────────────────
korrelation = combined[
    ["Valence", "Energy", "Danceability", "Unemployment"]
].corr()

target = korrelation["Unemployment"].drop("Unemployment").reset_index()
target.columns = ["Faktor", "Korrelation"]

target.to_csv(
    RESULTS_DIR / "correlation_clean.csv",
    index=False,
    sep=";",
    decimal=","
)

# ── Helper function ──────────────────────────────────────────
def corr_with_ci(x, y):
    tmp = pd.concat([x, y], axis=1).dropna()

    pearson = pearsonr(tmp.iloc[:, 0], tmp.iloc[:, 1])
    ci = pearson.confidence_interval(0.95)

    spearman_rho, spearman_p = spearmanr(tmp.iloc[:, 0], tmp.iloc[:, 1])

    return {
        "n": len(tmp),
        "pearson_r": pearson.statistic,
        "pearson_p": pearson.pvalue,
        "ci_low": ci.low,
        "ci_high": ci.high,
        "spearman_rho": spearman_rho,
        "spearman_p": spearman_p,
    }

# ── Main result: Energy vs Unemployment ─────────────────────
main_res = corr_with_ci(combined["Unemployment"], combined["Energy"])
print(f"Pearson Energy ↔ Unemployment: {main_res['pearson_r']:.3f}")
print(f"95% CI: [{main_res['ci_low']:.3f}, {main_res['ci_high']:.3f}]")
print(f"Pearson p-value: {main_res['pearson_p']:.4f}")
print(f"Spearman rho: {main_res['spearman_rho']:.3f}")
print(f"Spearman p-value: {main_res['spearman_p']:.4f}")

# ── Additional feature correlations ─────────────────────────
dance_res = corr_with_ci(combined["Unemployment"], combined["Danceability"])
val_res = corr_with_ci(combined["Unemployment"], combined["Valence"])

print(f"Danceability: r={dance_res['pearson_r']:.3f}, p={dance_res['pearson_p']:.4f}")
print(f"Valence: r={val_res['pearson_r']:.3f}, p={val_res['pearson_p']:.4f}")

# ── Energy vs macro indicators ──────────────────────────────
for indicator in ["Unemployment", "GDP", "Inflation"]:
    res = corr_with_ci(combined[indicator], combined["Energy"])
    print(f"Energy ↔ {indicator}: r={res['pearson_r']:.3f}, p={res['pearson_p']:.4f}")

# ── Lag analysis ────────────────────────────────────────────
lag_rows = []

for lag in range(-2, 4):
    shifted_energy = combined["Energy"].shift(lag)
    res = corr_with_ci(combined["Unemployment"], shifted_energy)
    res["Lag"] = lag
    res["Beschreibung"] = f"Unemployment(t) vs Energy(t{lag:+d})"
    lag_rows.append(res)

lag_df = pd.DataFrame(lag_rows)
print(lag_df.to_string(index=False))

# ── Song comparison lists ───────────────────────────────────
ergebnisse = []

for krise, jahre in CRISIS_YEARS.items():
    data = billboard[billboard["year"].isin(jahre)].copy()

    top_energie = (
        data.nlargest(20, "Energy")[["year", "Song", "Artist Names", "Energy"]]
        .drop_duplicates(subset=["Song", "Artist Names"])
        .head(10)
        .copy()
    )
    top_energie["Krise"] = krise
    top_energie["Typ"] = "Energetic"

    top_mellow = (
        data.nsmallest(20, "Energy")[["year", "Song", "Artist Names", "Energy"]]
        .drop_duplicates(subset=["Song", "Artist Names"])
        .head(10)
        .copy()
    )
    top_mellow["Krise"] = krise
    top_mellow["Typ"] = "Low Energy"

    ergebnisse.append(top_energie)
    ergebnisse.append(top_mellow)

# ── Save outputs ────────────────────────────────────────────
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

print("\nRobustness check:")
print(f"Pearson r = {main_res['pearson_r']:.3f}")
print(f"Spearman rho = {main_res['spearman_rho']:.3f}")
print("Both consistent?", abs(main_res['pearson_r'] - main_res['spearman_rho']) < 0.1)