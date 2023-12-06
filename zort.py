# Getting recomandations using spotipy and spotify api
import sys
import os
import spotipy
import spotipy.util as util
import spotipy.oauth2 as oauth2
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd

# Credentials

client_id = '12c0424057794147957982a43c8ccf7d'
client_secret = '17005834988f40b38d2ece89d4dce639'
redirect_uri = 'http://localhost:3000'

# Spotify API


scope = 'user-library-read playlist-read-private playlist-modify-private playlist-modify-public playlist-read-collaborative user-read-recently-played user-top-read user-read-playback-position user-read-playback-state user-modify-playback-state user-read-currently-playing app-remote-control streaming user-read-email user-read-private'


# Spotify API token

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope))

# Getting recomandations using spotipy and spotify api

def get_recomandations(artist_id):
    recomandations = sp.recommendations(seed_artists=[artist_id])
    recomandations_df = pd.DataFrame(columns=['track_name', 'artist_name'])
    for i, item in enumerate(recomandations['tracks']):
        recomandations_df.loc[i] = [item['name'], item['artists'][0]['name']]
    return recomandations_df

get_recomandations('0lAWpj5szCSwM4rUMHYmrr')

def get_recommendations_by_track(track_name, artist_name):
    results = sp.search(q='track:' + track_name + ' artist:' + artist_name, type='track')
    items = results['tracks']['items']
    if len(items) > 0:
        track = items[0]
        track_id = track['id']
        recommendations = sp.recommendations(seed_tracks=[track_id])
        recommendations_df = pd.DataFrame(columns=['track_name', 'artist_name'])
        for i, item in enumerate(recommendations['tracks']):
            recommendations_df.loc[i] = [item['name'], item['artists'][0]['name']]
        return recommendations_df
    else:
        return None
    
get_recommendations_by_track('The Less I Know The Better', 'Tame Impala')

# Get recommendations by audio features 

def get_recommendations_by_audio_features(track_name, artist_name):
    results = sp.search(q='track:' + track_name + ' artist:' + artist_name, type='track')
    items = results['tracks']['items']
    if len(items) > 0:
        track = items[0]
        track_id = track['id']
        audio_features = sp.audio_features(track_id)[0]
        audio_features_df = pd.DataFrame(audio_features, index=[0])
        recommendations = sp.recommendations(seed_tracks=[track_id], limit=10, **audio_features_df.to_dict(orient='records')[0])
        recommendations_df = pd.DataFrame(columns=['track_name', 'artist_name'])
        for i, item in enumerate(recommendations['tracks']):
            recommendations_df.loc[i] = [item['name'], item['artists'][0]['name']]
        return recommendations_df
    else:
        return None
    
get_recommendations_by_audio_features('The Less I Know The Better', 'Tame Impala')

# Get recommendations by only audio features

def get_recommendations_by_only_audio_features(danceability, energy, key, loudness, mode, speechiness, acousticness, instrumentalness, liveness, valence, tempo):
    recommendations = sp.recommendations(seed_tracks=['0c6xIDDpzE81m2q797ordA'], limit=30, **{'target_danceability': danceability, 'target_energy': energy, 'target_key': key, 'target_loudness': loudness, 'target_mode': mode, 'target_speechiness': speechiness, 'target_acousticness': acousticness, 'target_instrumentalness': instrumentalness, 'target_liveness': liveness, 'target_valence': valence, 'target_tempo': tempo})
    recommendations_df = pd.DataFrame(columns=['track_name', 'artist_name'])

    for i, item in enumerate(recommendations['tracks']):
        recommendations_df.loc[i] = [item['name'], item['artists'][0]['name']]
    return recommendations_df

get_recommendations_by_only_audio_features(0.5, 0.5, 0, -10, 1, 0.1, 0.5, 0.5, 0.5, 0.5, 100)

