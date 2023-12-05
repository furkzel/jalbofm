import spotifyapitests as st
import pandas as pd
import numpy as np
import json

# We have a list of genres from Spotify's API, we will use this list to get songs from each genre. First, using the function of get_playlist_id_by_name from spotifyapitests.py, get songs and their audio features from each genre. Then, we will create a dataframe with all the songs and their audio features and save it as a json file.

file = open('genres.json', 'r')
genres = json.load(file)

# For all name in genres, get playlist id and audio features
# Create a dataframe with all the songs and their audio features and save it as a json file

def get_audio_features_by_genre(genres):
    df = pd.DataFrame()
    for i in range(len(genres)):
        genre = genres[i]
        playlist_id = st.get_playlist_id_by_name(genre)
        playlist_audio_features = st.get_playlist_audio_features(playlist_id)
        df = df.append(playlist_audio_features)
    df.to_json('genres_audio_features.json')
    return df
get_audio_features_by_genre(genres)