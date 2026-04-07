import pandas as pd

# G20 Länder
g20 = ['ARG', 'AUS', 'BRA', 'CAN', 'CHN', 'DEU', 'FRA', 'GBR', 
       'IDN', 'IND', 'ITA', 'JPN', 'KOR', 'MEX', 'RUS', 'SAU', 
       'ZAF', 'TUR', 'USA']

def bereinigen(df, wert_name):
    df = df[df['Country Code'].isin(g20)]
    df = df[['Country Name', 'Country Code'] + 
            [col for col in df.columns if col.startswith('200') or col.startswith('201') or col.startswith('202')]]
    df = df.melt(id_vars=['Country Name', 'Country Code'], 
                 var_name='Jahr', value_name=wert_name)
    df['Jahr'] = df['Jahr'].str[:4].astype(int)
    df[wert_name] = pd.to_numeric(df[wert_name], errors='coerce')
    return df

# CSVs einlesen
gdp = pd.read_csv("GDP.csv")
gdp_pc = pd.read_csv("GDP per capita.csv")
inflation = pd.read_csv("Inflation.csv")
population = pd.read_csv("Population.csv")
unemployment = pd.read_csv("Unemployment.csv")

# Bereinigen
gdp_clean = bereinigen(gdp, 'GDP')
print(gdp_clean.head(10))
print(gdp_clean.shape)

# Alle bereinigen
gdp_clean = bereinigen(gdp, 'GDP')
gdp_pc_clean = bereinigen(gdp_pc, 'GDP_per_Capita')
inflation_clean = bereinigen(inflation, 'Inflation')
population_clean = bereinigen(population, 'Population')
unemployment_clean = bereinigen(unemployment, 'Unemployment')

# Zusammenführen
master = gdp_clean.merge(gdp_pc_clean, on=['Country Name', 'Country Code', 'Jahr'])
master = master.merge(inflation_clean, on=['Country Name', 'Country Code', 'Jahr'])
master = master.merge(population_clean, on=['Country Name', 'Country Code', 'Jahr'])
master = master.merge(unemployment_clean, on=['Country Name', 'Country Code', 'Jahr'])

print(master.head(10))
print(master.shape)
print(master.isnull().sum())

master.to_csv("master.csv", index=False)
print("Master CSV gespeichert!")