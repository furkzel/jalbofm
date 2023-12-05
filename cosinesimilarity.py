import spotifyapitests as st
from sklearn.metrics.pairwise import cosine_similarity


def get_similar_tracks_from_dataset(link):
    
    ds = st.clean_audio_features_df('https://open.spotify.com/playlist/1glmheZVEvBoG8nqPynX1p?si=6c75db92c7424d35')
    ds_tracks = st.get_playlist_tracks(st.get_playlist_id('https://open.spotify.com/playlist/1glmheZVEvBoG8nqPynX1p?si=6c75db92c7424d35'))

    user_input = st.clean_audio_features_df(link)
    user_input_tracks = st.get_playlist_tracks(st.get_playlist_id(link))

    # Vectorize the dataset

    ds_vector = ds[['danceability', 'energy', 'key', 'loudness', 'speechiness', 'acousticness', 'instrumentalness',
                    'liveness', 'valence', 'duration', 'tempo']]
    user_input_vector = user_input[['danceability', 'energy', 'key', 'loudness', 'speechiness', 'acousticness', 'instrumentalness',
                                    'liveness', 'valence', 'duration', 'tempo']]
    # Calculate cosine similarity
    similarity = cosine_similarity(user_input_vector, ds_vector)

    # Create a list of indices sorted by similarity score
    similarity_list = similarity[0].tolist()
    similarity_list_sorted = sorted(similarity_list, reverse=True)
    similarity_list_sorted_indices = [similarity_list.index(i) for i in similarity_list_sorted]

    # Return top 10 similar tracks with their names and artists
    similar_tracks = ds_tracks.iloc[similarity_list_sorted_indices[:len(user_input_tracks)]]

    return similar_tracks
    

get_similar_tracks_from_dataset('https://open.spotify.com/playlist/2gG7y6PHiD2sw8st5jHUBY?si=89780bfbc90b4a79')

