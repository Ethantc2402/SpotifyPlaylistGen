import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def get_audio_features(artist_name, track_name):
    # Spotify API credentials
    client_id = '4b2eac14dbbc4b4ba641fe7ede3bdaba'
    client_secret = '220c072743804b0dba9f56bd1897e821'
    credentials = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=credentials)
    
    # Search for the track
    results = sp.search(q=f"artist:{artist_name} track:{track_name}", limit=1)
    if not results['tracks']['items']:
        return None, "Track not found."

    # Get the first track's details
    track_details = results['tracks']['items'][0]
    if track_details['artists'][0]['name'].lower() != artist_name.lower():
        return None, "Artist and track combination not found."

    track_id = track_details['id']

    # Fetch audio analysis data
    audio_analysis = sp.audio_analysis(track_id)

    # Extract features for all segments
    features = []
    for segment in audio_analysis['segments']:
        segment_features = {
            'start': segment['start'],
            'duration': segment['duration'],
            'confidence': segment['confidence'],
            'loudness_start': segment['loudness_start'],
            'loudness_max_time': segment['loudness_max_time'],
            'loudness_max': segment['loudness_max'],
            'loudness_end': segment['loudness_end'],
            'pitches': segment['pitches'],
            'timbre': segment['timbre']
        }
        features.append(segment_features)

    return features, None

def get_overall_features(artist_name, track_name):
    # Spotify API credentials
    client_id = '4b2eac14dbbc4b4ba641fe7ede3bdaba'
    client_secret = '220c072743804b0dba9f56bd1897e821'
    credentials = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=credentials)
    
    # Search for the track
    results = sp.search(q=f"artist:{artist_name} track:{track_name}", limit=1)
    if not results['tracks']['items']:
        return None, "Track not found."

    # Get the first track's details
    track_details = results['tracks']['items'][0]
    if track_details['artists'][0]['name'].lower() != artist_name.lower():
        return None, "Artist and track combination not found."

    # Fetch audio features
    audio_features = sp.audio_features([track_details['id']])

    # Extract overall features
    overall_features = {
        'danceability': audio_features[0]['danceability'],
        'energy': audio_features[0]['energy'],
        'valence': audio_features[0]['valence']
    }

    return overall_features, None
