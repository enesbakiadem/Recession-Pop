# Recession Pop – Musikenergie vs. Wirtschaftskrisen USA

## Forschungsfrage
Spiegelt sich die wirtschaftliche Lage der USA in den 
Musikpräferenzen wider – und wenn ja, wie?

## Hintergrund
„Recession Pop" ist ein Begriff der ursprünglich für einen 
Musikstil der späten 2000er Jahre geprägt wurde – Dance-Pop 
und Electropop die während der Finanzkrise in den USA entstanden.
Diese Analyse untersucht ob sich dieser kulturelle Effekt 
statistisch in den Billboard Hot-100 Daten nachweisen lässt 
und ob er sich bei COVID 2020 wiederholt hat.

## Datenquellen
- Billboard Hot-100 (1946–2022) mit Spotify Audio Features
- Weltbank: US Arbeitslosigkeit und BIP

## Audio Features (Spotify)
Die Analyse basiert auf drei Spotify Audio Features die jedem 
Song automatisch zugewiesen werden:
- **Valence** – Fröhlichkeit eines Songs (0 = sehr melancholisch, 1 = sehr fröhlich)
- **Energy** – Intensität und Aktivität eines Songs (0 = ruhig, 1 = sehr energetisch)
- **Danceability** – Wie gut ein Song zum Tanzen geeignet ist (0 = schlecht, 1 = sehr gut)

## Ergebnisse
- Energy korreliert stark positiv mit Arbeitslosigkeit (r=0.61, p=0.002)
- Danceability korreliert stark negativ (r=-0.69)
- Valence zeigt kaum Zusammenhang (r=0.05)
- Lag-Analyse: Musik folgt Wirtschaft mit ~1 Jahr Verzögerung (r=0.66)
- COVID 2020: kein Recession Pop Effekt – mögliche Erklärungen: digitale 
  Informationsüberflutung durch Social Media sowie soziale Isolation durch 
  Lockdowns verhinderten kollektiven Eskapismus durch Musik

## Limitation
- Billboard misst Charterfolg nicht Hörverhalten
- Spotify Audio Features für ältere Songs retroaktiv berechnet
- Nur 23 Datenpunkte
- Korrelation ≠ Kausalität

## Tools
Python (Pandas, SciPy), Power BI für Visualisierung

## Methodik
1. Weltbank Rohdaten bereinigt und auf USA gefiltert
2. Billboard Hot-100 Daten mit Spotify Audio Features verknüpft
3. Pearson Korrelationsanalyse zwischen Audio Features und Arbeitslosigkeit
4. Lag-Analyse (1 Jahr Verzögerung) zur Prüfung ob Musik der Wirtschaft folgt oder umgekehrt
5. Signifikanztest (p-Wert) zur statistischen Absicherung der Ergebnisse
6. Visualisierung in Power BI