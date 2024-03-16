from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import random
from dotenv import load_dotenv
import os
import openai
import string
from openai import OpenAI
import requests

app = FastAPI()

# change this later to allow only specific origins (in production)
origins = [
    "http://127.0.0.1:3001",
    "http://localhost:3001"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DataModel(BaseModel):
    acousticness: str
    danceability: str
    energy: str
    instrumentalness: str
    mood_valence: str
    tempo: str
    prompt: str
    trackId: str

@app.get("/")
def index():
    return {"message": "Spotify Playlist Generator API running..."}

def playlist_generator(acousticness: str, danceability: str, energy: str, instrumentalness: str, mood_valence: str, tempo: str, prompt: str, trackId: str):
    if prompt is not None:
        promptActivate = True
    else:
        promptActivate = False
    if trackId is not None:
        inputActivate = True
    else:
        inputActivate = False

    # Check both conditions first
    if promptActivate and inputActivate:
        openai.api_key = os.getenv('openai.api_key')
        # Create a translation table to replace punctuation with None
        translator = str.maketrans('', '', string.punctuation)
        # Remove punctuation from the string
        final_prompt = prompt.translate(translator)

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (f"You are a playlist curator for Spotify. You are given this prompt: {final_prompt}. As a curator, pick the most relevant genre to this prompt ONLY FROM THIS LIST, do not pick any other genre outside of this list:"
                                "acoustic"
                                "afrobeat"
                                "alt-rock"
                                "alternative"
                                "ambient"
                                "anime"
                                "black-metal"
                                "bluegrass"
                                "blues"
                                "bossanova"
                                "brazil"
                                "breakbeat"
                                "british"
                                "cantopop"
                                "chicago-house"
                                "children"
                                "chill"
                                "classical"
                                "club"
                                "comedy"
                                "country"
                                "dance"
                                "dancehall"
                                "death-metal"
                                "deep-house"
                                "detroit-techno"
                                "disco"
                                "disney"
                                "drum-and-bass"
                                "dub"
                                "dubstep"
                                "edm"
                                "electro"
                                "electronic"
                                "emo"
                                "folk"
                                "forro"
                                "french"
                                "funk"
                                "garage"
                                "german"
                                "gospel"
                                "goth"
                                "grindcore"
                                "groove"
                                "grunge"
                                "guitar"
                                "happy"
                                "hard-rock"
                                "hardcore"
                                "hardstyle"
                                "heavy-metal"
                                "hip-hop"
                                "holidays"
                                "honky-tonk"
                                "house"
                                "idm"
                                "indian"
                                "indie"
                                "indie-pop"
                                "industrial"
                                "iranian"
                                "j-dance"
                                "j-idol"
                                "j-pop"
                                "j-rock"
                                "jazz"
                                "k-pop"
                                "kids"
                                "latin"
                                "latino"
                                "malay"
                                "mandopop"
                                "metal"
                                "metal-misc"
                                "metalcore"
                                "minimal-techno"
                                "movies"
                                "mpb"
                                "new-age"
                                "new-release"
                                "opera"
                                "pagode"
                                "party"
                                "philippines-opm"
                                "piano"
                                "pop"
                                "pop-film"
                                "post-dubstep"
                                "power-pop"
                                "progressive-house"
                                "psych-rock"
                                "punk"
                                "punk-rock"
                                "r-n-b"
                                "rainy-day"
                                "reggae"
                                "reggaeton"
                                "road-trip"
                                "rock"
                                "rock-n-roll"
                                "rockabilly"
                                "romance"
                                "sad"
                                "salsa"
                                "samba"
                                "sertanejo"
                                "show-tunes"
                                "singer-songwriter"
                                "ska"
                                "sleep"
                                "songwriter"
                                "soul"
                                "soundtracks"
                                "spanish"
                                "study"
                                "summer"
                                "swedish"
                                "synth-pop"
                                "tango"
                                "techno"
                                "trance"
                                "trip-hop"
                                "turkish"
                                "work-out"
                                "world-music"
                                "Also, assign values to the following track attributes: "
                                "Acousticness: A confidence measure from 0.0 to 1.0 of whether the track is acoustic. 1.0 represents high confidence the track is acoustic. Range: 0 - 1. "
                                "Danceability: Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable. "
                                "Energy: Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale. Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy. "
                                "Instrumentalness: Predicts whether a track contains no vocals. \"Ooh\" and \"aah\" sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly \"vocal\". The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0. "
                                "Tempo: The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo is the speed or pace of a given piece and derives directly from the average beat duration. Range: 60 - 180. "
                                "Valence: A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry). Range: 0 - 1. "
                                "Give me your response in the following format, and do not deviate from it: "                      
                                "Acousticness: <Acousticness Value> "
                                "Danceability: <Danceability Value> "
                                "Energy: <Energy Value> "
                                "Instrumentalness: <Instrumentalness Value> "
                                "Tempo: <Tempo Value> "
                                "Valence: <Valence Value>"
                                "Genre 1: <Genre #1> ")
                },
            ]
        )

        response_content = str(response.choices[0].message)

        # Extracting the content from the response string
        start = response_content.find("content='") + 9
        end = response_content.find("', role='")
        actual_content = response_content[start:end]

        # Splitting the actual content by newline to get each attribute line
        attribute_lines = actual_content.split("\\n")

        # Parsing each line and filling the dictionary
        dictionary = {}
        for line in attribute_lines:
            # Splitting each line into key and value
            key_value = line.split(": ")
            if len(key_value) == 2:
                # Assigning to dictionary, converting numeric values when necessary
                key, value = key_value
                if key in ['Acousticness', 'Danceability', 'Energy', 'Instrumentalness', 'Tempo', 'Valence']:
                    try:
                        dictionary[key] = float(value) if '.' in value else int(value)
                    except ValueError:
                        dictionary[key] = value  # In case of conversion error, keep original string
                else:
                    dictionary[key] = value

        dictionary["Genre 1"] = dictionary["Genre 1"].strip()

        genres = [
            "acoustic",
            "afrobeat",
            "alt-rock",
            "alternative",
            "ambient",
            "anime",
            "black-metal",
            "bluegrass",
            "blues",
            "bossanova",
            "brazil",
            "breakbeat",
            "british",
            "cantopop",
            "chicago-house",
            "children",
            "chill",
            "classical",
            "club",
            "comedy",
            "country",
            "dance",
            "dancehall",
            "death-metal",
            "deep-house",
            "detroit-techno",
            "disco",
            "disney",
            "drum-and-bass",
            "dub",
            "dubstep",
            "edm",
            "electro",
            "electronic",
            "emo",
            "folk",
            "forro",
            "french",
            "funk",
            "garage",
            "german",
            "gospel",
            "goth",
            "grindcore",
            "groove",
            "grunge",
            "guitar",
            "happy",
            "hard-rock",
            "hardcore",
            "hardstyle",
            "heavy-metal",
            "hip-hop",
            "holidays",
            "honky-tonk",
            "house",
            "idm",
            "indian",
            "indie",
            "indie-pop",
            "industrial",
            "iranian",
            "j-dance",
            "j-idol",
            "j-pop",
            "j-rock",
            "jazz",
            "k-pop",
            "kids",
            "latin",
            "latino",
            "malay",
            "mandopop",
            "metal",
            "metal-misc",
            "metalcore",
            "minimal-techno",
            "movies",
            "mpb",
            "new-age",
            "new-release",
            "opera",
            "pagode",
            "party",
            "philippines-opm",
            "piano",
            "pop",
            "pop-film",
            "post-dubstep",
            "power-pop",
            "progressive-house",
            "psych-rock",
            "punk",
            "punk-rock",
            "r-n-b",
            "rainy-day",
            "reggae",
            "reggaeton",
            "road-trip",
            "rock",
            "rock-n-roll",
            "rockabilly",
            "romance",
            "sad",
            "salsa",
            "samba",
            "sertanejo",
            "show-tunes",
            "singer-songwriter",
            "ska",
            "sleep",
            "songwriter",
            "soul",
            "soundtracks",
            "spanish",
            "study",
            "summer",
            "swedish",
            "synth-pop",
            "tango",
            "techno",
            "trance",
            "trip-hop",
            "turkish",
            "work-out",
            "world-music"
        ]

        if dictionary["Genre 1"] not in genres:
            dictionary["Genre 1"] = "Pop"

        print(dictionary)

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
                input_genre = trackId

                # Get audio analysis for the input track
                input_audio_analysis = sp.audio_analysis(input_track['id'])
                
                # Modify tempo randomly within a range
                if tempo is not None:
                    final_tempo = int(tempo)
                else:
                    extracted_tempo = input_audio_analysis['track']['tempo'] + random.randint(-10,10)
                    tempo_factor = random.randint(-10,10)
                    input_tempo = extracted_tempo + tempo_factor
                    final_tempo = (input_tempo + dictionary["Tempo"])/2

                # Extract artist name and audio features
                input_artist = input_track['artists'][0]['name']
                input_audio_features = sp.audio_features(input_track['id'])[0]

                # Modify energy randomly within a range but ensure it stays between 0 and 1
                if energy is not None:
                    final_energy = float(energy)
                else:
                    extracted_energy = input_audio_features['energy']
                    energy_factor = random.uniform(-0.1, 0.1)
                    input_energy = round(max(0, min(1, extracted_energy + energy_factor)), 3)
                    final_energy = (input_energy + dictionary["Energy"])/2

                # Similar modifications for valence, danceability, acousticness, and instrumentalness
                if mood_valence is not None:
                    final_valence = float(mood_valence)
                else:
                    extracted_valence = input_audio_features['valence']
                    valence_factor = random.uniform(-0.1, 0.1)
                    input_valence = round(max(0, min(1, extracted_valence + valence_factor)), 3)
                    final_valence = (input_valence + dictionary["Valence"])/2
                
                if danceability is not None:
                    final_danceability = float(danceability)
                else:
                    extracted_danceability = input_audio_features['danceability']
                    danceability_factor = random.uniform(-0.1, 0.1)
                    input_danceability = round(max(0, min(1, extracted_danceability + danceability_factor)), 3)
                    final_danceability = (input_danceability + dictionary["Danceability"])/2

                if acousticness is not None:
                    final_acousticness = float(acousticness)
                else:
                    extracted_acousticness = input_audio_features['acousticness']
                    acousticness_factor = random.uniform(-0.1, 0.1)
                    input_acousticness = round(max(0, min(1, extracted_acousticness + acousticness_factor)), 3)
                    final_acousticness = (input_acousticness + dictionary["Acousticness"])/2

                if instrumentalness is not None:
                    final_instrumentalness = float(instrumentalness)
                else:
                    extracted_instrumentalness = input_audio_features['instrumentalness']
                    instrumentalness_factor = random.uniform(-0.1, 0.1)
                    input_instrumentalness = round(max(0, min(1, extracted_instrumentalness + instrumentalness_factor)), 3)
                    final_instrumentalness = (input_instrumentalness + dictionary["Instrumentalness"])/2
                
                # Get recommendations based on the modified track features
                recommendations = sp.recommendations(seed_genres=[dictionary['Genre 1'].lower()], seed_artists=[input_genre], target_tempo=[final_tempo], target_energy=[final_energy], target_valence=[final_valence], target_danceability=[final_danceability], target_acousticness=[final_acousticness], target_instrumentalness=[final_instrumentalness], limit=track_num)

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
        playlist_name = "generated playlist"
        playlist_description = "this is a generated playlist"
        track_num = 14
        playlist = spotifyObject.user_playlist_create(user=username, name=playlist_name, public=True, description=playlist_description)
        playlist_id = playlist['id']

        # Prompt user for track and artist, then search and add the track to the playlist
        user_input = "one dance, drake"
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
            print(f"\nTop {track_num} Recommendations:\n")
            for track in recommendations['tracks']:
                artists = ', '.join([artist['name'] for artist in track['artists']])
                list_of_songs.append(track['uri'])
                print(f"Added '{track['name']}' by '{artists}' to the '{playlist_name}' playlist!")
                print("Track features: ")
                features = sp.audio_features(track['id'])[0]
                for attribute, value in features.items():
                    print(f"{attribute}: {value}")
                print()
                
        # Add recommended tracks to the playlist
        spotifyObject.user_playlist_add_tracks(user=username, playlist_id=playlist_id, tracks=list_of_songs)

        client = OpenAI(api_key = os.getenv(openai.api_key))

        # Call the API
        response = client.images.generate(
        model="dall-e-2",
        prompt= "Generate minimalist art",
        size="1024x1024",
        quality="standard",
        n=1,
        )

        # The URL of the generated image
        image_url = response.data[0].url

        # Download the image and save it to your laptop
        response = requests.get(image_url)  # Make a request to the image URL
        image_path = os.path.join(os.getcwd(), "generated_image.png")  # Specify the path where you want to save the image

        # Write the image to a file
        with open(image_path, 'wb') as f:
            f.write(response.content)

        print(f"Image saved to {image_path}")

    elif promptActivate:  # This will only be checked if the first condition is False
        openai.api_key = os.getenv('openai.api_key')
        # Create a translation table to replace punctuation with None
        translator = str.maketrans('', '', string.punctuation)
        # Remove punctuation from the string
        final_prompt = prompt.translate(translator)

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (f"You are a playlist curator for Spotify. You are given this prompt: {final_prompt}. As a curator, pick the most relevant ONE-WORD genre to this prompt ONLY FROM THIS LIST, do not pick any other genre outside of this list:"
                                "acoustic"
                                "afrobeat"
                                "alt-rock"
                                "alternative"
                                "ambient"
                                "anime"
                                "black-metal"
                                "bluegrass"
                                "blues"
                                "bossanova"
                                "brazil"
                                "breakbeat"
                                "british"
                                "cantopop"
                                "chicago-house"
                                "children"
                                "chill"
                                "classical"
                                "club"
                                "comedy"
                                "country"
                                "dance"
                                "dancehall"
                                "death-metal"
                                "deep-house"
                                "detroit-techno"
                                "disco"
                                "disney"
                                "drum-and-bass"
                                "dub"
                                "dubstep"
                                "edm"
                                "electro"
                                "electronic"
                                "emo"
                                "folk"
                                "forro"
                                "french"
                                "funk"
                                "garage"
                                "german"
                                "gospel"
                                "goth"
                                "grindcore"
                                "groove"
                                "grunge"
                                "guitar"
                                "happy"
                                "hard-rock"
                                "hardcore"
                                "hardstyle"
                                "heavy-metal"
                                "hip-hop"
                                "holidays"
                                "honky-tonk"
                                "house"
                                "idm"
                                "indian"
                                "indie"
                                "indie-pop"
                                "industrial"
                                "iranian"
                                "j-dance"
                                "j-idol"
                                "j-pop"
                                "j-rock"
                                "jazz"
                                "k-pop"
                                "kids"
                                "latin"
                                "latino"
                                "malay"
                                "mandopop"
                                "metal"
                                "metal-misc"
                                "metalcore"
                                "minimal-techno"
                                "movies"
                                "mpb"
                                "new-age"
                                "new-release"
                                "opera"
                                "pagode"
                                "party"
                                "philippines-opm"
                                "piano"
                                "pop"
                                "pop-film"
                                "post-dubstep"
                                "power-pop"
                                "progressive-house"
                                "psych-rock"
                                "punk"
                                "punk-rock"
                                "r-n-b"
                                "rainy-day"
                                "reggae"
                                "reggaeton"
                                "road-trip"
                                "rock"
                                "rock-n-roll"
                                "rockabilly"
                                "romance"
                                "sad"
                                "salsa"
                                "samba"
                                "sertanejo"
                                "show-tunes"
                                "singer-songwriter"
                                "ska"
                                "sleep"
                                "songwriter"
                                "soul"
                                "soundtracks"
                                "spanish"
                                "study"
                                "summer"
                                "swedish"
                                "synth-pop"
                                "tango"
                                "techno"
                                "trance"
                                "trip-hop"
                                "turkish"
                                "work-out"
                                "world-music"
                                "Also, assign values to the following track attributes: "
                                "Acousticness: A confidence measure from 0.0 to 1.0 of whether the track is acoustic. 1.0 represents high confidence the track is acoustic. Range: 0 - 1. "
                                "Danceability: Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable. "
                                "Energy: Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale. Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy. "
                                "Instrumentalness: Predicts whether a track contains no vocals. \"Ooh\" and \"aah\" sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly \"vocal\". The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0. "
                                "Tempo: The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo is the speed or pace of a given piece and derives directly from the average beat duration. Range: 60 - 180. "
                                "Valence: A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry). Range: 0 - 1. "
                                "Give me your response in the following format, and do not deviate from it: "                      
                                "Acousticness: <Acousticness Value> "
                                "Danceability: <Danceability Value> "
                                "Energy: <Energy Value> "
                                "Instrumentalness: <Instrumentalness Value> "
                                "Tempo: <Tempo Value> "
                                "Valence: <Valence Value>"
                                "Genre 1: <Genre #1> ")
                },
            ]
        )

        response_content = str(response.choices[0].message)

        # Extracting the content from the response string
        start = response_content.find("content='") + 9
        end = response_content.find("', role='")
        actual_content = response_content[start:end]

        # Splitting the actual content by newline to get each attribute line
        attribute_lines = actual_content.split("\\n")

        # Parsing each line and filling the dictionary
        dictionary = {}
        for line in attribute_lines:
            # Splitting each line into key and value
            key_value = line.split(": ")
            if len(key_value) == 2:
                # Assigning to dictionary, converting numeric values when necessary
                key, value = key_value
                if key in ['Acousticness', 'Danceability', 'Energy', 'Instrumentalness', 'Tempo', 'Valence']:
                    try:
                        dictionary[key] = float(value) if '.' in value else int(value)
                    except ValueError:
                        dictionary[key] = value  # In case of conversion error, keep original string
                else:
                    dictionary[key] = value

        dictionary["Genre 1"] = dictionary["Genre 1"].strip()

        genres = [
            "acoustic",
            "afrobeat",
            "alt-rock",
            "alternative",
            "ambient",
            "anime",
            "black-metal",
            "bluegrass",
            "blues",
            "bossanova",
            "brazil",
            "breakbeat",
            "british",
            "cantopop",
            "chicago-house",
            "children",
            "chill",
            "classical",
            "club",
            "comedy",
            "country",
            "dance",
            "dancehall",
            "death-metal",
            "deep-house",
            "detroit-techno",
            "disco",
            "disney",
            "drum-and-bass",
            "dub",
            "dubstep",
            "edm",
            "electro",
            "electronic",
            "emo",
            "folk",
            "forro",
            "french",
            "funk",
            "garage",
            "german",
            "gospel",
            "goth",
            "grindcore",
            "groove",
            "grunge",
            "guitar",
            "happy",
            "hard-rock",
            "hardcore",
            "hardstyle",
            "heavy-metal",
            "hip-hop",
            "holidays",
            "honky-tonk",
            "house",
            "idm",
            "indian",
            "indie",
            "indie-pop",
            "industrial",
            "iranian",
            "j-dance",
            "j-idol",
            "j-pop",
            "j-rock",
            "jazz",
            "k-pop",
            "kids",
            "latin",
            "latino",
            "malay",
            "mandopop",
            "metal",
            "metal-misc",
            "metalcore",
            "minimal-techno",
            "movies",
            "mpb",
            "new-age",
            "new-release",
            "opera",
            "pagode",
            "party",
            "philippines-opm",
            "piano",
            "pop",
            "pop-film",
            "post-dubstep",
            "power-pop",
            "progressive-house",
            "psych-rock",
            "punk",
            "punk-rock",
            "r-n-b",
            "rainy-day",
            "reggae",
            "reggaeton",
            "road-trip",
            "rock",
            "rock-n-roll",
            "rockabilly",
            "romance",
            "sad",
            "salsa",
            "samba",
            "sertanejo",
            "show-tunes",
            "singer-songwriter",
            "ska",
            "sleep",
            "songwriter",
            "soul",
            "soundtracks",
            "spanish",
            "study",
            "summer",
            "swedish",
            "synth-pop",
            "tango",
            "techno",
            "trance",
            "trip-hop",
            "turkish",
            "work-out",
            "world-music"
        ]

        print(dictionary)

        if dictionary["Genre 1"] not in genres:
            dictionary["Genre 1"] = "Pop"

        print(dictionary)

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
        list_of_songs = []
        sp_oauth = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, scope=scope, username=username, redirect_uri='http://127.0.0.1:8080/')
        access_token = sp_oauth.get_access_token(as_dict=False)
        spotifyObject = spotipy.Spotify(auth=access_token)

        # Interactively create a playlist
        playlist_name = "ai-generated playlist"
        playlist_description = "this is an ai-generated playlist"
        track_num = 14
        playlist = spotifyObject.user_playlist_create(user=username, name=playlist_name, public=True, description=playlist_description)
        playlist_id = playlist['id']

        # slidersActivate = input("Would you like to specify specific values for your playlist to possess? (y/n): ")
        # if slidersActivate == 'y':
        #     slidersActivate = True
        #     tempoValue = float(input("Select your preferred tempo (60 - 180 BPM, enter 0 if no preference): "))
        #     if tempoValue == 0:
        #         tempoValue = None
        #     energyValue = float(input("Select your preferred energy (0 - 1, enter 0 if no preference): "))
        #     if energyValue == 0:
        #         energyValue = None
        #     valenceValue = float(input("Select your preferred valence (0 - 1, enter 0 if no preference): "))
        #     if valenceValue == 0:
        #         valenceValue = None
        #     danceabilityValue = float(input("Select your preferred danceability (0 - 1, enter 0 if no preference): "))
        #     if danceabilityValue == 0:
        #         danceabilityValue = None
        #     acousticnessValue = float(input("Select your preferred acousticness (0 - 1, enter 0 if no preference): "))
        #     if acousticnessValue == 0:
        #         acousticnessValue = None
        #     instrumentalnessValue = float(input("Select your preferred instrumentalness (0 - 1, enter 0 if no preference): "))
        #     if instrumentalnessValue == 0:
        #         instrumentalnessValue = None
        # else:
        #     slidersActivate = False
        #     tempoValue = None
        #     energyValue = None
        #     valenceValue = None
        #     danceabilityValue = None
        #     acousticnessValue = None
        #     instrumentalnessValue = None

        # Modify tempo randomly within a range
        if tempo is not None:
            input_tempo = int(tempo)
        else:
            extracted_tempo = dictionary['Tempo']
            tempo_factor = random.randint(-10,10)
            input_tempo = extracted_tempo + tempo_factor

        # Modify energy randomly within a range but ensure it stays between 0 and 1
        if energy is not None:
            input_energy = float(energy)
        else:
            extracted_energy = dictionary['Energy']
            energy_factor = random.uniform(-0.1, 0.1)
            input_energy = round(max(0, min(1, extracted_energy + energy_factor)), 3)

        # Similar modifications for valence, danceability, acousticness, and instrumentalness
        if mood_valence is not None:
            input_valence = float(mood_valence)
        else:
            extracted_valence = dictionary['Valence']
            valence_factor = random.uniform(-0.1, 0.1)
            input_valence = round(max(0, min(1, extracted_valence + valence_factor)), 3)

        if danceability is not None:
            input_danceability = float(danceability)
        else:
            extracted_danceability = dictionary['Danceability']
            danceability_factor = random.uniform(-0.1, 0.1)
            input_danceability = round(max(0, min(1, extracted_danceability + danceability_factor)), 3)

        if acousticness is not None:
            input_acousticness = float(acousticness)
        else:
            extracted_acousticness = dictionary['Acousticness']
            acousticness_factor = random.uniform(-0.1, 0.1)
            input_acousticness = round(max(0, min(1, extracted_acousticness + acousticness_factor)), 3)

        if instrumentalness is not None:
            input_instrumentalness = float(instrumentalness)
        else:
            extracted_instrumentalness = dictionary['Instrumentalness']
            instrumentalness_factor = random.uniform(-0.1, 0.1)
            input_instrumentalness = round(max(0, min(1, extracted_instrumentalness + instrumentalness_factor)), 3)
            
        # Get recommendations based on the modified track features
        recommendations = sp.recommendations(seed_genres=[dictionary['Genre 1'].lower()], target_tempo=[input_tempo], target_energy=[input_energy], target_valence=[input_valence], target_danceability=[input_danceability], target_acousticness=[input_acousticness], target_instrumentalness=[input_instrumentalness], limit=track_num)

        list_of_songs = [track['uri'] for track in recommendations['tracks']]

        spotifyObject.user_playlist_add_tracks(user=username, playlist_id=playlist_id, tracks=list_of_songs)

        print("Playlist Generated!")

        # Replace YOUR_API_KEY with your OpenAI API key
        client = OpenAI(api_key = os.getenv(openai.api_key))

        # Call the API
        response = client.images.generate(
        model="dall-e-2",
        prompt= f"Generate minimalist art based on this genre: {dictionary['Genre 1']}",
        size="1024x1024",
        quality="standard",
        n=1,
        )

        # The URL of the generated image
        image_url = response.data[0].url

        # Download the image and save it to your laptop
        response = requests.get(image_url)  # Make a request to the image URL
        image_path = os.path.join(os.getcwd(), "generated_image.png")  # Specify the path where you want to save the image

        # Write the image to a file
        with open(image_path, 'wb') as f:
            f.write(response.content)

        print(f"Image saved to {image_path}")

    elif inputActivate:  # This will only be checked if the first and second conditions are False
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
                input_genre = trackId

                # Get audio analysis for the input track
                input_audio_analysis = sp.audio_analysis(input_track['id'])
                
                # Modify tempo randomly within a range
                if tempo is not None:
                    final_tempo = int(tempo)
                else:
                    extracted_tempo = input_audio_analysis['track']['tempo'] + random.randint(-10,10)
                    tempo_factor = random.randint(-10,10)
                    input_tempo = extracted_tempo + tempo_factor
                    final_tempo = (input_tempo + dictionary["Tempo"])/2

                # Extract artist name and audio features
                input_artist = input_track['artists'][0]['name']
                input_audio_features = sp.audio_features(input_track['id'])[0]

                # Modify energy randomly within a range but ensure it stays between 0 and 1
                if energy is not None:
                    final_energy = float(energy)
                else:
                    extracted_energy = input_audio_features['energy']
                    energy_factor = random.uniform(-0.1, 0.1)
                    input_energy = round(max(0, min(1, extracted_energy + energy_factor)), 3)
                    final_energy = (input_energy + dictionary["Energy"])/2

                # Similar modifications for valence, danceability, acousticness, and instrumentalness
                if mood_valence is not None:
                    final_valence = float(mood_valence)
                else:
                    extracted_valence = input_audio_features['valence']
                    valence_factor = random.uniform(-0.1, 0.1)
                    input_valence = round(max(0, min(1, extracted_valence + valence_factor)), 3)
                    final_valence = (input_valence + dictionary["Valence"])/2
                
                if danceability is not None:
                    final_danceability = float(danceability)
                else:
                    extracted_danceability = input_audio_features['danceability']
                    danceability_factor = random.uniform(-0.1, 0.1)
                    input_danceability = round(max(0, min(1, extracted_danceability + danceability_factor)), 3)
                    final_danceability = (input_danceability + dictionary["Danceability"])/2

                if acousticness is not None:
                    final_acousticness = float(acousticness)
                else:
                    extracted_acousticness = input_audio_features['acousticness']
                    acousticness_factor = random.uniform(-0.1, 0.1)
                    input_acousticness = round(max(0, min(1, extracted_acousticness + acousticness_factor)), 3)
                    final_acousticness = (input_acousticness + dictionary["Acousticness"])/2

                if instrumentalness is not None:
                    final_instrumentalness = float(instrumentalness)
                else:
                    extracted_instrumentalness = input_audio_features['instrumentalness']
                    instrumentalness_factor = random.uniform(-0.1, 0.1)
                    input_instrumentalness = round(max(0, min(1, extracted_instrumentalness + instrumentalness_factor)), 3)
                    final_instrumentalness = (input_instrumentalness + dictionary["Instrumentalness"])/2
                
                # Get recommendations based on the modified track features
                recommendations = sp.recommendations(seed_genres=[dictionary['Genre 1'].lower()], seed_artists=[input_genre], target_tempo=[final_tempo], target_energy=[final_energy], target_valence=[final_valence], target_danceability=[final_danceability], target_acousticness=[final_acousticness], target_instrumentalness=[final_instrumentalness], limit=track_num)

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
        playlist_name = "Playlist generated with input track"
        playlist_description = "Playlist generated with input track only"
        track_num = 14
        playlist = spotifyObject.user_playlist_create(user=username, name=playlist_name, public=True, description=playlist_description)
        playlist_id = playlist['id']

        # Prompt user for track and artist, then search and add the track to the playlist
        user_input = "one dance, drake"
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

        # slidersActivate = input("Would you like to specify specific values for your playlist to possess? (y/n): ")
        # if slidersActivate == 'y':
        #     slidersActivate = True
        #     tempoValue = float(input("Select your preferred tempo (60 - 180 BPM, enter 0 if no preference): "))
        #     if tempoValue == 0:
        #         tempoValue = None
        #     energyValue = float(input("Select your preferred energy (0 - 1, enter 0 if no preference): "))
        #     if energyValue == 0:
        #         energyValue = None
        #     valenceValue = float(input("Select your preferred valence (0 - 1, enter 0 if no preference): "))
        #     if valenceValue == 0:
        #         valenceValue = None
        #     danceabilityValue = float(input("Select your preferred danceability (0 - 1, enter 0 if no preference): "))
        #     if danceabilityValue == 0:
        #         danceabilityValue = None
        #     acousticnessValue = float(input("Select your preferred acousticness (0 - 1, enter 0 if no preference): "))
        #     if acousticnessValue == 0:
        #         acousticnessValue = None
        #     instrumentalnessValue = float(input("Select your preferred instrumentalness (0 - 1, enter 0 if no preference): "))
        #     if instrumentalnessValue == 0:
        #         instrumentalnessValue = None
        # else:
        #     slidersActivate = False
        #     tempoValue = None
        #     energyValue = None
        #     valenceValue = None
        #     danceabilityValue = None
        #     acousticnessValue = None
        #     instrumentalnessValue = None
            
        
        # Generate and display recommendations based on the input track
        recommendations = input_track_recommendations(track_name, artist_name, sp)

        if recommendations is not None:
            print(f"\nTop {track_num} Recommendations:\n")
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

        client = OpenAI(api_key = os.getenv(openai.api_key))

        # Call the API
        response = client.images.generate(
        model="dall-e-2",
        prompt= "Generate minimalist art",
        size="1024x1024",
        quality="standard",
        n=1,
        )

        # The URL of the generated image
        image_url = response.data[0].url

        # Download the image and save it to your laptop
        response = requests.get(image_url)  # Make a request to the image URL
        image_path = os.path.join(os.getcwd(), "generated_image.png")  # Specify the path where you want to save the image

        # Write the image to a file
        with open(image_path, 'wb') as f:
            f.write(response.content)

        print(f"Image saved to {image_path}")

@app.post("/post_features")
async def post_data(data: DataModel):
    
    # use the data to generate the playlist here
    playlist_generator(data.acousticness, data.danceability, data.energy, data.instrumentalness, data.mood_valence, data.tempo, data.prompt, data.trackId)
    return {"status": 200, "data": data}