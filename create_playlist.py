# Importing necessary libraries and modules
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import random
from dotenv import load_dotenv
import os

# Define a function to retrieve Spotify track link
def get_spotify_link(track_id, sp):
    return sp.track(track_id)

# Define a function to input track recommendations based on song name and artist name
def input_track_recommendations(song_name, artist_name, sp):
    # Query Spotify API to search for the song and artist
    query = f"{song_name} {artist_name}"
    results = sp.search(q=query, type='track', limit=1)

    # Proceed if the song is found
    if results['tracks']['items']:
        input_track = results['tracks']['items'][0]
        input_genre = input_track['artists'][0]['id']

        # Get audio analysis for the input track
        input_audio_analysis = sp.audio_analysis(input_track['id'])
        
        # Modify tempo randomly within a range
        extracted_tempo = input_audio_analysis['track']['tempo'] + random.randint(-10,10)
        tempo_factor = random.randint(-10,10)
        input_tempo = extracted_tempo + tempo_factor

        # Extract artist name and audio features
        input_artist = input_track['artists'][0]['name']
        input_audio_features = sp.audio_features(input_track['id'])[0]

        # Modify energy randomly within a range but ensure it stays between 0 and 1
        extracted_energy = input_audio_features['energy']
        energy_factor = random.uniform(-0.1, 0.1)
        input_energy = round(max(0, min(1, extracted_energy + energy_factor)), 3)

        # Similar modifications for valence, danceability, acousticness, and instrumentalness
        extracted_valence = input_audio_features['valence']
        valence_factor = random.uniform(-0.1, 0.1)
        input_valence = round(max(0, min(1, extracted_valence + valence_factor)), 3)

        extracted_danceability = input_audio_features['danceability']
        danceability_factor = random.uniform(-0.1, 0.1)
        input_danceability = round(max(0, min(1, extracted_danceability + danceability_factor)), 3)

        extracted_acousticness = input_audio_features['acousticness']
        acousticness_factor = random.uniform(-0.1, 0.1)
        input_acousticness = round(max(0, min(1, extracted_acousticness + acousticness_factor)), 3)

        extracted_instrumentalness = input_audio_features['instrumentalness']
        instrumentalness_factor = random.uniform(-0.1, 0.1)
        input_instrumentalness = round(max(0, min(1, extracted_instrumentalness + instrumentalness_factor)), 3)
        
        # print("Artist:", input_artist)
        # print("Track Name:", track_name)
        # print("Track features: ")
        # features = sp.audio_features(input_track['id'])[0]
        # for attribute, value in features.items():
        #     print(f"{attribute}: {value}")
        

        # Get recommendations based on the modified track features
        recommendations = sp.recommendations(seed_artists=[input_genre], target_tempo=[input_tempo], target_energy=[input_energy], target_valence=[input_valence], target_danceability=[input_danceability], target_acousticness=[input_acousticness], target_instrumentalness=[input_instrumentalness], limit=track_num)

        # Filter out the input track from the recommendations and truncate the list
        recommendations['tracks'] = [track for track in recommendations['tracks'] if track['id'] != input_track['id']]
        recommendations['tracks'] = recommendations['tracks'][:track_num - 1]

        # Add Spotify URLs to the recommendations
        recommendations['spotify_url'] = [get_spotify_link(track['id'], sp)['external_urls']['spotify'] for track in recommendations['tracks']]

        return recommendations
    
    else:
        print(f"No match found for the song '{song_name}'.")
        return None 

# Load environment variables containing sensitive information
load_dotenv()
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

# Initialize Spotify client with credentials
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Define scope for playlist modification and initialize SpotifyOAuth
scope = 'playlist-modify-public'
username = '31vxd2rpgrlanjxy6mu5fvcexoaq'
sp_oauth = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, scope=scope, username=username, redirect_uri='http://127.0.0.1:8080/')
access_token = sp_oauth.get_access_token(as_dict=False)
spotifyObject = spotipy.Spotify(auth=access_token)

# Interactively create a playlist
playlist_name = input("Enter a playlist name: ")
playlist_description = input("Enter a playlist description: ")
track_num = int(input("Enter the number of tracks in the playlist: "))
playlist = spotifyObject.user_playlist_create(user=username, name=playlist_name, public=True, description=playlist_description)
playlist_id = playlist['id']

# Prompt user for track and artist, then search and add the track to the playlist
user_input = input("Enter the track and artist (separated by comma): ")
list_of_songs = []
user_input = user_input.split(',')
track_name = user_input[0].strip()
artist_name = user_input[1].strip() if len(user_input) > 1 else None

# Search for the track and add it to the playlist
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

# Generate and display recommendations based on the input track
recommendations = input_track_recommendations(track_name, artist_name, sp)

if recommendations is not None:
    print("\nTop 10 Recommendations Based on Genre, Tempo, and Timbre:\n")
    for track in recommendations['tracks']:
        artists = ', '.join([artist['name'] for artist in track['artists']])
        list_of_songs.append(track['uri'])
        print(f"Added '{track['name']}' by '{artists}' to the '{playlist_name}' playlist!") 
        # print("Track features: ")
        # features = sp.audio_features(track['id'])[0]
        # for attribute, value in features.items():
        #     print(f"{attribute}: {value}")
        # print()

# Add recommended tracks to the playlist
spotifyObject.user_playlist_add_tracks(user=username, playlist_id=playlist_id, tracks=list_of_songs)