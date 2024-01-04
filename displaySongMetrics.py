import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def get_audio_features(artist_name, track_name):
    # Spotify API credentials
    client_id = 'YOUR_CLIENT_ID'
    client_secret = 'YOUR_CLIENT_SECRET'
    credentials = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=credentials)
    
    # Search for the track
    results = sp.search(q=f"artist:{artist_name} track:{track_name}", limit=1)
    if not results['tracks']['items']:
        return None, "Track not found."

    track_id = results['tracks']['items'][0]['id']

    # Fetch audio analysis data
    audio_analysis = sp.audio_analysis(track_id)

    # Extract features for all sections
    features = []
    for section in audio_analysis['sections']:
        section_data = {
            'start': section['start'],
            'duration': section['duration'],
            'confidence': section['confidence'],
            'loudness': section['loudness'],
            'tempo': section['tempo'],
            'tempo_confidence': section['tempo_confidence'],
            'key': section['key'],
            'key_confidence': section['key_confidence'],
            'mode': section['mode'],
            'mode_confidence': section['mode_confidence'],
            'time_signature': section['time_signature'],
            'time_signature_confidence': section['time_signature_confidence']
        }
        features.append(section_data)

    return features, None

# The get_overall_features function remains unchanged
