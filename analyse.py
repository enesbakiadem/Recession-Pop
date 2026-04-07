import pandas as pd

master = pd.read_csv("master.csv")

g20 = ['ARG', 'AUS', 'BRA', 'CAN', 'CHN', 'DEU', 'FRA', 'GBR', 
       'IDN', 'IND', 'ITA', 'JPN', 'KOR', 'MEX', 'RUS', 'SAU', 
       'ZAF', 'TUR', 'USA']

krisen = {
    'Finanzkrise': (2008, 2009),
    'Eurokrise': (2010, 2013),
    'COVID': (2020, 2021)
}

def gdp_veraenderung(land_code, jahr_von, jahr_bis):
    land = master[master['Country Code'] == land_code]
    wert_von = land[land['Jahr'] == jahr_von]['GDP'].values[0]
    wert_bis = land[land['Jahr'] == jahr_bis]['GDP'].values[0]
    return ((wert_bis - wert_von) / wert_von) * 100

#ergebnisse = []
#for land in g20:
    ergebnisse.append({
        'Land': land,
        'Finanzkrise': gdp_veraenderung(land, 2007, 2009),
        'Eurokrise': gdp_veraenderung(land, 2009, 2013),
        'COVID': gdp_veraenderung(land, 2019, 2020)
    })

#df_ergebnisse = pd.DataFrame(ergebnisse)
#print(df_ergebnisse.to_string())
#df_ergebnisse.to_csv("krisen_gdp.csv", index=False)
#print("Gespeichert!")
bra = master[master['Country Code'] == 'BRA']
print(bra[['Jahr', 'GDP']].to_string())



