from pathlib import Path
import pandas as pd

# ── Paths ────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# ── G20 Countries ─────────────────────────────────────────────
G20 = ['ARG', 'AUS', 'BRA', 'CAN', 'CHN', 'DEU', 'FRA', 'GBR',
       'IDN', 'IND', 'ITA', 'JPN', 'KOR', 'MEX', 'RUS', 'SAU',
       'ZAF', 'TUR', 'USA']

# ── Helper function ───────────────────────────────────────────
def clean_worldbank(filename, value_name):
    df = pd.read_csv(RAW_DIR / filename)
    df = df[df['Country Code'].isin(G20)]
    df = df[['Country Name', 'Country Code'] +
            [col for col in df.columns
             if col.startswith('196') or col.startswith('197') 
             or col.startswith('198') or col.startswith('199')
             or col.startswith('200') or col.startswith('201') 
             or col.startswith('202')]]
    df = df.melt(id_vars=['Country Name', 'Country Code'],
                 var_name='Jahr', value_name=value_name)
    df['Jahr'] = df['Jahr'].str[:4].astype(int)
    df[value_name] = pd.to_numeric(df[value_name], errors='coerce')
    return df

# ── Load and clean all indicators ────────────────────────────
gdp = clean_worldbank("GDP.csv", "GDP")
gdp_pc = clean_worldbank("GDP per capita.csv", "GDP_per_Capita")
inflation = clean_worldbank("Inflation.csv", "Inflation")
population = clean_worldbank("Population.csv", "Population")
unemployment = clean_worldbank("Unemployment.csv", "Unemployment")

# ── Merge all ─────────────────────────────────────────────────
master = gdp.merge(gdp_pc, on=['Country Name', 'Country Code', 'Jahr'])
master = master.merge(inflation, on=['Country Name', 'Country Code', 'Jahr'])
master = master.merge(population, on=['Country Name', 'Country Code', 'Jahr'])
master = master.merge(unemployment, on=['Country Name', 'Country Code', 'Jahr'])

# ── Save ──────────────────────────────────────────────────────
master.to_csv(PROCESSED_DIR / "master.csv", index=False)
print(f"master.csv saved: {master.shape[0]} rows, {master.shape[1]} columns")