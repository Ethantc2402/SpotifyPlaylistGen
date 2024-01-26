import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import tqdm as tqdm

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

        print("\nThe tempo in BPM is:", input_tempo)
        print("The timbre is:", input_timbre)
        print("The artist is:", input_artist)
        print("The track name is:", track_name)
        print("Track features: ")
        features = sp.audio_features(input_track['id'])[0]
        for attribute, value in features.items():
            print(f"{attribute}: {value}")

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

# Replace with your own Client ID and Client Secret
CLIENT_ID = '52b7deed70ef4ae3bb2b4429ad67da13'
CLIENT_SECRET = 'fd3bc8e9c56547dea746a8af37eb6e58'

client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

scope = 'playlist-modify-public'
username = '31vxd2rpgrlanjxy6mu5fvcexoaq'

# Initialize SpotifyOAuth with a redirect_uri
sp_oauth = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, scope=scope, username=username, redirect_uri='http://127.0.0.1:8080/')
access_token = sp_oauth.get_access_token(as_dict=False)

# Create the Spotify object using the obtained access token
spotifyObject = spotipy.Spotify(auth=access_token)

playlist_name = input("Enter a playlist name: ")
playlist_description = input("Enter a playlist description: ")

playlist = spotifyObject.user_playlist_create(user=username, name=playlist_name, public=True, description=playlist_description)
playlist_id = playlist['id']

user_input = input("Enter the track and artist (separated by comma): ")
list_of_songs = []

user_input = user_input.split(',')
track_name = user_input[0].strip()
artist_name = user_input[1].strip() if len(user_input) > 1 else None
    
if artist_name:
    query = f"{track_name} {artist_name}"
else:
    query = track_name
    
result = spotifyObject.search(q=query)
    
if len(result['tracks']['items']) > 0:
    list_of_songs.append(result['tracks']['items'][0]['uri'])
else:
    print(f"No results found for '{track_name}' by '{artist_name}'")

print(f"Added '{track_name}' by '{artist_name}' to the '{playlist_name}' playlist!")    

recommendations = recommendByGenre_Tempo_Timbre(track_name, artist_name, sp)

# Display recommendations including Spotify links
if recommendations is not None:
    print("\nTop 10 Recommendations Based on Genre, Tempo, and Timbre:\n")
    for track in recommendations['tracks']:
        artists = ', '.join([artist['name'] for artist in track['artists']])
        list_of_songs.append(track['uri'])
        print(f"Added '{track['name']}' by '{artists}' to the '{playlist_name}' playlist!") 
        print("Track features: ")
        features = sp.audio_features(track['id'])[0]
        for attribute, value in features.items():
            print(f"{attribute}: {value}")
        print()

spotifyObject.user_playlist_add_tracks(user=username, playlist_id=playlist_id, tracks=list_of_songs)