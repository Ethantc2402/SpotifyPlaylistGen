from flask import Flask, render_template, request
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

app = Flask(__name__)

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

@app.route('/', methods=['GET', 'POST'])
def index():
    error_message = None
    if request.method == 'POST':
        artist_name = request.form['artist_name']
        track_name = request.form['track_name']
        features, error_message = get_audio_features(artist_name, track_name)
        if features:
            return render_template('results.html', features=features)
    
    return render_template('index.html', error=error_message)

if __name__ == "__main__":
    app.run(debug=True)
