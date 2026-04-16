# Recession Pop: Music in Times of Economic Crisis

Do economic crises influence the way music sounds?

> A data analysis project combining music data with macroeconomic indicators to explore cultural responses to economic crises.

This project explores whether changes in the economy are reflected in popular music — and whether cultural patterns like “Recession Pop” can be detected in data.

## 📸 Key Visuals

### Energy vs Unemployment — including the COVID anomaly
![Energy vs Unemployment](./visuals/01_energy_vs_unemployment.png)

### Lag Analysis
![Lag Analysis](./visuals/03_lag_analysis.png)

## 🎯 Research Question

Do economic conditions in the United States influence musical characteristics — and if so, how?

## 🧠 Background

“Recession Pop” describes a wave of energetic, dance-oriented music that emerged during the late 2000s financial crisis.

This project investigates whether this phenomenon can be observed statistically using Billboard Hot 100 data and Spotify audio features — and whether a similar pattern appeared during COVID-19.

## 📊 Data Sources

- Billboard Hot 100 (1946–2022) with Spotify audio features  
- World Bank data (USA): unemployment, GDP, inflation  

### Audio Features

- **Valence** – how positive or happy a song sounds  
- **Energy** – intensity and activity level  
- **Danceability** – how suitable a song is for dancing  

## ⚙️ Methodology

- Aggregation of Billboard data by year  
- Merging with US economic indicators  
- Pearson correlation analysis  
- Lag analysis (-2 to +3 years) to test delayed relationships between economy and music  
- Statistical significance testing (p-values)  
- Data visualization using Power BI  

## 📈 Key Results

- Overall, results suggest that economic downturns are associated with more energetic but less danceable music.

- **Energy** shows a moderate positive correlation with unemployment  
  *(r = 0.57, p = 0.0047, 95% CI [0.20, 0.79])*

- **Energy** is also negatively correlated with GDP  
  *(r = -0.65, p = 0.0008)*, supporting the link between economic downturns and higher musical energy

- **Danceability** shows a strong negative correlation  
  *(r = -0.68, p = 0.0004)*

- **Valence** shows no meaningful relationship  
  *(r = 0.06, p = 0.79)*

- Results are consistent across **Pearson and Spearman correlations**, indicating robustness  

- **Lag analysis** suggests that music reacts to economic changes with a short delay  
  *(strongest correlation at lag -1: r = 0.63)*

### COVID-19

No clear “Recession Pop” effect was observed during COVID-19 — suggesting that structural changes in music consumption may have altered the relationship.

Possible explanations:
- Increased digital media consumption  
- Social isolation reducing collective escapism  

## ⚠️ Limitations

- Billboard reflects chart success, not actual listening behavior  
- Spotify audio features for older songs are retroactively calculated  
- Limited sample size (23 data points)  
- Correlation does not imply causation  

## 🧹 Data Cleaning

- 172 karaoke entries removed (false audio features)
- Artist name formatting cleaned

## 🛠️ Tools

- Python (Pandas, SciPy)  
- Power BI  

## 🔬 Statistical Approach

- Pearson correlation for linear relationships  
- Spearman correlation for robustness  
- Confidence intervals to estimate uncertainty  
- Lag analysis to capture delayed effects  

## 💡 Key Insight

Music does not exist in isolation.

This analysis suggests that cultural output may systematically respond to economic conditions — in ways that are measurable, delayed, and statistically robust.