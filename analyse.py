import pandas as pd

master = pd.read_csv("master.csv")

g20 = ['ARG', 'AUS', 'BRA', 'CAN', 'CHN', 'DEU', 'FRA', 'GBR', 
       'IDN', 'IND', 'ITA', 'JPN', 'KOR', 'MEX', 'RUS', 'SAU', 
       'ZAF', 'TUR', 'USA']

def gdp_veraenderung(land_code, jahr_von, jahr_bis):
    land = master[master['Country Code'] == land_code]
    wert_von = land[land['Jahr'] == jahr_von]['GDP'].values[0]
    wert_bis = land[land['Jahr'] == jahr_bis]['GDP'].values[0]
    return ((wert_bis - wert_von) / wert_von) * 100

ergebnisse = []
for land in g20:
    ergebnisse.append({
        'Land': land,
        'Finanzkrise': gdp_veraenderung(land, 2007, 2009),
        'Eurokrise': gdp_veraenderung(land, 2009, 2013),
        'COVID': gdp_veraenderung(land, 2019, 2020)
    })

df_ergebnisse = pd.DataFrame(ergebnisse)
print(df_ergebnisse.to_string())
df_ergebnisse.to_csv("krisen_gdp.csv", index=False)
print("Gespeichert!")

def unemployment_veraenderung(land_code, jahr_von, jahr_bis):
    land = master[master['Country Code'] == land_code]
    wert_von = land[land['Jahr'] == jahr_von]['Unemployment'].values[0]
    wert_bis = land[land['Jahr'] == jahr_bis]['Unemployment'].values[0]
    return wert_bis - wert_von  # Prozentpunkte, nicht %

unemployment_ergebnisse = []
for land in g20:
    unemployment_ergebnisse.append({
        'Land': land,
        'Finanzkrise': unemployment_veraenderung(land, 2007, 2009),
        'Eurokrise': unemployment_veraenderung(land, 2009, 2013),
        'COVID': unemployment_veraenderung(land, 2019, 2020)
    })

df_unemployment = pd.DataFrame(unemployment_ergebnisse)
print(df_unemployment.to_string())
df_unemployment.to_csv("krisen_unemployment.csv", index=False)

def inflation_veraenderung(land_code, jahr_von, jahr_bis):
    land = master[master['Country Code'] == land_code]
    wert_von = land[land['Jahr'] == jahr_von]['Inflation'].values[0]
    wert_bis = land[land['Jahr'] == jahr_bis]['Inflation'].values[0]
    return wert_bis - wert_von

inflation_ergebnisse = []
for land in g20:
    inflation_ergebnisse.append({
        'Land': land,
        'Finanzkrise': inflation_veraenderung(land, 2007, 2009),
        'Eurokrise': inflation_veraenderung(land, 2009, 2013),
        'COVID': inflation_veraenderung(land, 2019, 2020)
    })

df_inflation = pd.DataFrame(inflation_ergebnisse)
print(df_inflation.to_string())
df_inflation.to_csv("krisen_inflation.csv", index=False)

#def land_detail(land_code):
#    land = master[master['Country Code'] == land_code]
#    print(land[['Jahr', 'Inflation']].to_string())

#land_detail('ITA')

def gdp_pc_veraenderung(land_code, jahr_von, jahr_bis):
    land = master[master['Country Code'] == land_code]
    wert_von = land[land['Jahr'] == jahr_von]['GDP_per_Capita'].values[0]
    wert_bis = land[land['Jahr'] == jahr_bis]['GDP_per_Capita'].values[0]
    return ((wert_bis - wert_von) / wert_von) * 100

gdp_pc_ergebnisse = []
for land in g20:
    gdp_pc_ergebnisse.append({
        'Land': land,
        'Finanzkrise': gdp_pc_veraenderung(land, 2007, 2009),
        'Eurokrise': gdp_pc_veraenderung(land, 2009, 2013),
        'COVID': gdp_pc_veraenderung(land, 2019, 2020)
    })

df_gdp_pc = pd.DataFrame(gdp_pc_ergebnisse)
print(df_gdp_pc.to_string())
df_gdp_pc.to_csv("krisen_gdp_per_capita.csv", index=False)