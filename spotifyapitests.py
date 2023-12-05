# Requirements

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import numpy as np
import json

# Credentials

credential_file = open('credentials.txt', 'r')
credentials = credential_file.readlines()
spotify_client_id = credentials[0].strip()
spotify_client_secret = credentials[1].strip()

# Spotify API

client_credentials_manager = SpotifyClientCredentials(client_id=spotify_client_id, client_secret=spotify_client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Geting playlist IDs by playlist link

def get_playlist_id(playlist_link):
    playlist_id = playlist_link.split('/')[4].split('?')[0]
    return playlist_id

# Getting playlist tracks names and artists by playlist ID as dataframe

def get_playlist_tracks(playlist_id):
    playlist = sp.playlist(playlist_id)
    tracks = playlist['tracks']
    tracks_df = pd.DataFrame(columns=['track_name', 'artist_name'])
    for i, item in enumerate(tracks['items']):
        track = item['track']
        tracks_df.loc[i] = [track['name'], track['artists'][0]['name']]
    return tracks_df

get_playlist_tracks('6wKAAcZN6103NTphY80lQn')

# Getting audio features by track name and artist name as dataframe

def get_audio_features(track_name, artist_name):
    results = sp.search(q='track:' + track_name + ' artist:' + artist_name, type='track')
    items = results['tracks']['items']
    if len(items) > 0:
        track = items[0]
        track_id = track['id']
        audio_features = sp.audio_features(track_id)[0]
        audio_features_df = pd.DataFrame(audio_features, index=[0])
        return audio_features_df
    else:
        return None
    
# Getting audio features by playlist ID as dataframe with their names and artists

def get_playlist_audio_features(playlist_id):
    playlist_tracks = get_playlist_tracks(playlist_id)
    playlist_audio_features = list()
    for i, row in playlist_tracks.iterrows():
        audio_features = get_audio_features(row['track_name'], row['artist_name'])
        if audio_features is not None:
            playlist_audio_features.append(audio_features)
    playlist_audio_features_df = pd.concat(playlist_audio_features, ignore_index=True)
    return playlist_audio_features_df

get_playlist_audio_features('6wKAAcZN6103NTphY80lQn')

# Now we can get audio features by playlist, that's great! But we need to get audio features by playlist link, not by playlist ID. So we need to combine all functions above.

def get_audio_features_by_playlist_link(playlist_link):
    playlist_id = get_playlist_id(playlist_link)
    playlist_audio_features_df = get_playlist_audio_features(playlist_id)
    return playlist_audio_features_df

get_audio_features_by_playlist_link('https://open.spotify.com/playlist/6wKAAcZN6103NTphY80lQn?si=b59411dcefc444b1')

# Finally we have to clean our data with tracks' names. We need to drop some columns and rows, and rename some columns. Let's do it! But we want to get clean data by playlist link, not by playlist ID. So we need to combine all functions above.

def clean_audio_features_df(playlist_link):
    playlist_audio_features_df = get_audio_features_by_playlist_link(playlist_link)
    playlist_audio_features_df = playlist_audio_features_df.drop(['type', 'id', 'uri', 'track_href', 'analysis_url'], axis=1)
    playlist_audio_features_df = playlist_audio_features_df.dropna()
    playlist_audio_features_df = playlist_audio_features_df.reset_index(drop=True)
    playlist_audio_features_df = playlist_audio_features_df.rename(columns={'duration_ms': 'duration'})
    return playlist_audio_features_df

clean_audio_features_df('https://open.spotify.com/playlist/6wKAAcZN6103NTphY80lQn?si=b59411dcefc444b1')



# We want to get most followed playlists by playlist name.

def get_playlist_id_by_name(playlist_name):
    results = sp.search(q='playlist:' + playlist_name, type='playlist')
    items = results['playlists']['items']
    if len(items) > 0:
        playlist = items[0]
        playlist_id = playlist['id']
        return playlist_id
    else:
        return None
    
get_playlist_tracks(get_playlist_id_by_name('doom'))