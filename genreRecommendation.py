# ***************** ONLY RECOMMENDS BASED ON GENRE AND TEMPO **********************

# import spotipy
# from spotipy.oauth2 import SpotifyClientCredentials

# # function to get the Spotify URL's for songs that are recommended based on genre
# def get_spotify_info(track_id, sp):
#     track = sp.track(track_id)
#     audio_features = sp.audio_features([track_id])[0] # Retrieve audio features of the inputted song to get a relative tempo from
#     return track, audio_features


# def recommendByGenre_Tempo(song_name, sp):
#     # Querying the Spotify API to search for the input song
#     results = sp.search(q=song_name, type='track', limit=1)

#     # If the song was found, proceed with recommendations
#     if results['tracks']['items']:
#         input_track = results['tracks']['items'][0]
#         input_genre = input_track['artists'][0]['id']  # Assume the genre is based on the first artist of the track

#         # Get tempo of the input track
#         _, input_audio_features = get_spotify_info(input_track['id'], sp)
#         input_tempo = input_audio_features['tempo']

#         print("The input tempo in BPM is:", input_tempo)

#         # Get top tracks in the same genre as the input song with a target tempo
#         recommendations = sp.recommendations(seed_artists=[input_genre], target_tempo=[input_tempo], limit=11)  # Increase limit by 1 to filter out the input track

#         # Filter out the input track from the recommendations
#         recommendations['tracks'] = [track for track in recommendations['tracks'] if track['id'] != input_track['id']]

#         # Take only the top 10 recommendations after filtering
#         recommendations['tracks'] = recommendations['tracks'][:10]

#         # Add a column for Spotify URLs
#         recommendations['spotify_url'] = [get_spotify_info(track['id'], sp)[0]['external_urls']['spotify'] for track in recommendations['tracks']]

#         return recommendations

#     else:
#         print(f"No match found for the song '{song_name}'.")
#         return None




# if __name__ == "__main__":
#     # Take user input for the song name
#     user_input = input("Enter the name of a song from Spotify: ")

#     # Set up Spotify API credentials
#     client_id = 'cf9550faad1b4d2f93b868511b7bebf2'
#     client_secret = 'adc6e3b265824a4d8bcaee3da0a652e5'
#     client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
#     sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

#     # Get recommendations based on genre and target tempo
#     recommendations = recommendByGenre_Tempo(user_input, sp)

#     # Display recommendations including Spotify links
#     if recommendations is not None:
#         print("\nTop 10 Recommendations Based on Genre and Target Tempo:")
#         for track in recommendations['tracks']:
#             artists = ', '.join([artist['name'] for artist in track['artists']])
#             print(f"{track['name']} by {artists} (Popularity: {track['popularity']}, Artist Name: {track['artists'][0]['name']})")
#             print(f"Spotify Link: {track['external_urls']['spotify']}")
#             print()

# ***************** BELOW RECOMMENDS BASED ON TIMBRE AS WELL **********************

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def get_spotify_link(track_id, sp):
    return sp.track(track_id)

def recommendByGenre_Tempo_Timbre(song_name, artist_name, sp):
    # Querying the Spotify API to search for the inputted song and artist
    query = f"{song_name} {artist_name}"
    results = sp.search(q=query, type='track', limit=1)

    # If the song was found, proceed with recommendations
    if results['tracks']['items']:
        input_track = results['tracks']['items'][0]
        input_genre = input_track['artists'][0]['id']

        # Get tempo and timbre of the input track using audio analysis
        input_audio_analysis = sp.audio_analysis(input_track['id'])
        input_tempo = input_audio_analysis['track']['tempo']
        input_timbre = input_audio_analysis['segments'][0]['timbre']  # Using the first segment as an example, adjust as needed
        input_artist = input_track['artists'][0]['name']

        print("\nThe found tempo in BPM is:", input_tempo)
        print("The found timbre is:", input_timbre)
        print("The found artist is:", input_artist)

        # Define a timbre range (adjust as needed)
        timbre_range = [input_timbre[i] - 10 for i in range(len(input_timbre))] + [input_timbre[i] + 10 for i in range(len(input_timbre))]

        # Get top tracks in the same genre as the input song with a target tempo and timbre
        recommendations = sp.recommendations(seed_artists=[input_genre], target_tempo=[input_tempo], target_timbre=timbre_range, limit=11)

        # Filter out the input track from the recommendations
        recommendations['tracks'] = [track for track in recommendations['tracks'] if track['id'] != input_track['id']]

        # Take only the top 10 recommendations after filtering
        recommendations['tracks'] = recommendations['tracks'][:10]

        # Add a column for Spotify URLs
        recommendations['spotify_url'] = [get_spotify_link(track['id'], sp)['external_urls']['spotify'] for track in recommendations['tracks']]

        return recommendations

    else:
        print(f"No match found for the song '{song_name}'.")
        return None

if __name__ == "__main__":
    # Take user input for the song name
    user_input_song = input("Enter the name of a song from Spotify: ")
    user_input_artist = input("Enter the name of the artist of the song: ")

    # Set up Spotify API credentials
    client_id = 'cf9550faad1b4d2f93b868511b7bebf2'
    client_secret = 'adc6e3b265824a4d8bcaee3da0a652e5'
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # Get recommendations based on genre, target tempo, and target timbre
    recommendations = recommendByGenre_Tempo_Timbre(user_input_song, user_input_artist, sp)

    # Display recommendations including Spotify links
    if recommendations is not None:
        print("\nTop 10 Recommendations Based on Genre, Target Tempo, and Target Timbre:\n")
        for track in recommendations['tracks']:
            artists = ', '.join([artist['name'] for artist in track['artists']])
            print(f"{track['name']} by {artists} (Popularity: {track['popularity']}, Artist Name: {track['artists'][0]['name']})")
            print(f"Spotify Link: {track['external_urls']['spotify']}")
            print()

