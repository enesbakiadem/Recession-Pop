import pandas as pd
import ast

billboard = pd.read_csv("daten/raw/Billboard_Hot100_Songs_Spotify_1946-2022.csv", encoding='latin-1')
billboard['year'] = billboard['Hot100 Ranking Year']
billboard = billboard[billboard['year'].between(2000, 2022)]

def parse_genres(genre_str):
    try:
        return ast.literal_eval(genre_str)
    except:
        return []

billboard['genres_list'] = billboard['Artist(s) Genres'].apply(parse_genres)
billboard_exploded = billboard.explode('genres_list')
billboard_exploded = billboard_exploded[billboard_exploded['genres_list'] != '']

# Genre Kategorien
genre_mapping = {
    'Pop': ['pop', 'dance pop', 'electropop', 'synth-pop', 'bubblegum pop'],
    'Rap/Hip-Hop': ['rap', 'hip hop', 'hip-hop', 'trap', 'hip pop', 'southern hip hop'],
    'R&B': ['r&b', 'contemporary r&b', 'urban contemporary', 'new jack swing', 'motown', 'soul'],
    'Rock': ['rock', 'soft rock', 'classic rock', 'hard rock', 'rock-and-roll'],
    'Country': ['country', 'contemporary country', 'country road', 'modern country rock']
}

def kategorisieren(genre):
    for kategorie, keywords in genre_mapping.items():
        if genre in keywords:
            return kategorie
    return None

billboard_exploded['kategorie'] = billboard_exploded['genres_list'].apply(kategorisieren)
billboard_kategorien = billboard_exploded.dropna(subset=['kategorie'])

# Pro Song nur EINE Kategorie zählen!
billboard_unique = billboard_kategorien.drop_duplicates(subset=['year', 'Hot100 Rank', 'kategorie'])

genre_pro_jahr = billboard_unique.groupby(['year', 'kategorie']).size().reset_index(name='count')
print(genre_pro_jahr.to_string())