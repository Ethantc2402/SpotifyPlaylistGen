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
