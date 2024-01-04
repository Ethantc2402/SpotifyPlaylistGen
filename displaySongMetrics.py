import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sys

def get_audio_features(artist_name, track_name):
    # Spotify API credentials
    client_id = '4b2eac14dbbc4b4ba641fe7ede3bdaba'
    client_secret = '220c072743804b0dba9f56bd1897e821'
    credentials = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=credentials)

    # Search for the track
    results = sp.search(q=f"artist:{artist_name} track:{track_name}", limit=1)
    if not results['tracks']['items']:
        return "Track not found."

    # Get the first track's details
    track_details = results['tracks']['items'][0]
    if track_details['artists'][0]['name'].lower() != artist_name.lower():
        return "Artist and track combination not found."

    track_id = track_details['id']
    track_name = track_details['name']
    artist_name = track_details['artists'][0]['name']
    album_name = track_details['album']['name']

    # Fetch audio features
    features = sp.audio_features([track_id])[0]

    # Add track name, artist, and album name to the features dictionary
    features.update({
        'track_name': track_name,
        'artist_name': artist_name,
        'album_name': album_name
    })

    return features

if __name__ == "__main__":
    if len(sys.argv) > 2:
        artist_name = sys.argv[1]
        track_name = ' '.join(sys.argv[2:])
        features = get_audio_features(artist_name, track_name)
        if isinstance(features, dict):
            print(f"Track: {features['track_name']}")
            print(f"Artist: {features['artist_name']}")
            print(f"Album: {features['album_name']}")
            # Print other features as required
        else:
            print(features)
    else:
        print("Please provide an artist name and a track name.")
