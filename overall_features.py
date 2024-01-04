import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def get_overall_features(artist_name, track_name):
    # Spotify API credentials - Replace with your own credentials
    client_id = '4b2eac14dbbc4b4ba641fe7ede3bdaba'
    client_secret = '220c072743804b0dba9f56bd1897e821'
    credentials = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=credentials)

    # Search for the track
    results = sp.search(q=f"artist:{artist_name} track:{track_name}", limit=1)
    if not results['tracks']['items']:
        return None, "Track not found."

    track_details = results['tracks']['items'][0]
    track_id = track_details['id']

    # Fetch track-level audio features
    track_features = sp.audio_features([track_id])[0]
    overall_features = {
        'danceability': track_features['danceability'],
        'energy': track_features['energy'],
        'key': track_features['key']
        # You can add more features here as needed
    }

    return overall_features, None

# Example usage
if __name__ == "__main__":
    artist = "Artist Name"
    track = "Track Name"
    features, error = get_overall_features(artist, track)
    if features:
        print(features)
    else:
        print(error)
