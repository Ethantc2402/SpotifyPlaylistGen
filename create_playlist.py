import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import tqdm as tqdm

# Replace with your own Client ID and Client Secret
CLIENT_ID = '52b7deed70ef4ae3bb2b4429ad67da13'
CLIENT_SECRET = 'fd3bc8e9c56547dea746a8af37eb6e58'

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

# user_song = input("Enter the song: ")
# list_of_songs = []
# while user_song != "quit":
#     result = spotifyObject.search(q=user_song)
#     list_of_songs.append(result['tracks']['items'][0]['uri'])
#     user_song = input("Enter the song: ")

# spotifyObject.user_playlist_add_tracks(user = username, playlist_id = playlist_id, tracks = list_of_songs)

user_input = input("Enter the track and artist (separated by comma): ")
list_of_songs = []

while user_input.lower() != "quit":
    user_input = user_input.split(',')
    print(user_input)
    track_name = user_input[0].strip()
    print(track_name)
    artist_name = user_input[1].strip() if len(user_input) > 1 else None
    print(artist_name)
    
    if artist_name:
        query = f"{track_name} {artist_name}"
    else:
        query = track_name
    
    result = spotifyObject.search(q=query)
    
    if len(result['tracks']['items']) > 0:
        list_of_songs.append(result['tracks']['items'][0]['uri'])
    else:
        print(f"No results found for '{track_name}' by '{artist_name}'")
    
    user_input = input("Enter the track and artist (separated by comma) or 'quit' to finish: ")

spotifyObject.user_playlist_add_tracks(user=username, playlist_id=playlist_id, tracks=list_of_songs)