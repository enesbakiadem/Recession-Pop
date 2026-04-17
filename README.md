# Recession Pop: Music in Times of Economic Crisis

Do economic crises influence the way music sounds?

> A data analysis project combining music data with macroeconomic indicators to explore how culture reacts to economic pressure.

I first came across the idea of “Recession Pop” — the claim that music became more energetic during the financial crisis. 

This made me question whether the relationship between economic conditions and music actually holds — and led to this analysis.

## 📸 Key Visuals

### Energy vs Unemployment — including the COVID anomaly
![Energy vs Unemployment](./visuals/01_energy_vs_unemployment.png)

### Lag Analysis
![Lag Analysis](./visuals/03_lag_analysis.png)

## 🎯 Research Question

Do economic conditions in the United States influence musical characteristics — and if so, how?

## 🧠 Background

“Recession Pop” describes a wave of energetic, dance-oriented music that emerged during the late 2000s financial crisis.

This project explores whether this phenomenon can be observed statistically using Billboard Hot 100 data and Spotify audio features — and whether a similar pattern appeared during COVID-19.

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
- Spearman correlation as a robustness check  
- Lag analysis (-2 to +3 years) to test delayed relationships  
- Statistical significance testing (p-values)  
- Data visualization using Power BI  

## 📈 Key Results

The analysis reveals a consistent pattern:

During economic downturns, music becomes more energetic while losing danceability.

At the same time, the data indicates that music does not lead economic changes — it follows them.

| Feature       | r     | p-value | Interpretation              |
|---------------|-------|---------|-----------------------------|
| Energy        | +0.57 | 0.0047  | Rises with unemployment     |
| Danceability  | -0.68 | 0.0004  | Falls with unemployment     |
| Valence       | +0.06 | 0.79    | No meaningful relationship  |

**Lag Analysis (Energy)**  
The strongest correlation appears one year after the economic shock *(r = 0.63, lag +1)*, suggesting that music reacts to economic conditions with a short delay rather than immediately.

**Robustness**  
To check whether this result is stable, I also used Spearman correlation.

The result remains similar (ρ = 0.53), which suggests that the relationship is not driven by outliers or strict linear assumptions.

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

## 🔬 Statistical Note

Pearson correlation is used here as an exploratory measure of linear association.  
Given the small sample size and potential violations of statistical assumptions, the results should be interpreted with caution.

The analysis is intended to highlight patterns rather than establish causal relationships.

## 🧹 Data Cleaning

- 172 karaoke entries removed (incorrect audio features)  
- Artist name formatting standardized  

## 🛠️ Tools

- Python (Pandas, SciPy)  
- Power BI  

## 💡 Key Insight

Music does not exist in isolation.

The results suggest that economic pressure shapes music — but not immediately.

Instead, cultural responses seem to build up over time, reflecting shared experiences.

## 🤖 Use of AI (Transparency)

AI tools were used to support wording, structuring, and parts of the code.

The core analysis, interpretation, and all decisions were developed independently.