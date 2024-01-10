# import pandas as pd
# import spotipy
# from spotipy.oauth2 import SpotifyClientCredentials

# # Pretty much just gets the Top 10 most poplular songs in the same genre as 
# # the inputted song name

# # function to get the Spotify URL's for songs that are recommended based on genre
# def get_spotify_url(track_name, artist_name, sp):
#     query = f"{track_name} {artist_name}"
#     # querying the Spotify API to search for the song
#     results = sp.search(q=query, type='track', limit=1)

#     # if the song was found, return the Spotify URL
#     if results['tracks']['items']:
#         return results['tracks']['items'][0]['external_urls']['spotify']
#     else:
#         return None

# def recommendByGenre(song_name, data, sp):
#     # filter data based on the input song name
#     # changing the case of the song name to lowercase for easier comparison
#     song_data = data[data['track_name'].str.lower() == song_name.lower()]

#     if song_data.empty:
#         # song was not found in the dataset
#         print(f"No match found for the song '{song_name}'.")
#         return

#     # extract the genre of the inputted song from the csv data
#     # returning a view of the selected row and column
#     input_genre = song_data.iloc[0]['genre']

#     # filter data based on the genre of the input song
#     # gives list of just the songs in the same genre as the input song
#     genre_matches = data[data['genre'] == input_genre]

#     # remove the actual inputted song from the list of matches
#     # making sure the song name is in lowercase for easier comparison
#     # and that there is no duplicate/repeated song names in the list
#     genre_matches = genre_matches[genre_matches['track_name'].str.lower() != song_name.lower()]

#     # sorting the top 10 matches by popularity (descending order)
#     top_recommendations = genre_matches.sort_values(by='popularity', ascending=False).head(10)

#     # add a column for Spotify URLs
#     top_recommendations['spotify_url'] = top_recommendations.apply(lambda row: get_spotify_url(row['track_name'], row['artist_name'], sp), axis=1)

#     # return the top 10 recommendation list
#     return top_recommendations

# # Only run the following code if this file is being run directly
# # to be later exported as a module to be used in other files
# # once the full filtering/recommendation process for songs is completed
# if __name__ == "__main__":
#     # load CSV data into a DataFrame using pandas library
#     spotify_data = pd.read_csv('SpotifyPlaylistGen\spotify_data.csv')

#     # take user input for the song name
#     user_input = input("Enter the name of a song from spotify: ")

#     # set up Spotify API credentials
#     # to set up your own credentials, go to https://developer.spotify.com/dashboard/
#     # get your id and secret and replace the values below
#     client_id = 'cf9550faad1b4d2f93b868511b7bebf2'
#     client_secret = 'adc6e3b265824a4d8bcaee3da0a652e5'
#     client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
#     sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

#     # get recommendations based on genre
#     recommendations = recommendByGenre(user_input, spotify_data, sp)

#     # display recommendations including Spotify links
#     if recommendations is not None:
#         print("\nTop 10 Recommendations Based on Genre:")
#         for index, row in recommendations[['artist_name', 'track_name', 'popularity', 'genre', 'spotify_url']].iterrows():
#             print(f"{row['track_name']} by {row['artist_name']} ({row['popularity']} popularity, Genre: {row['genre']})")
#             print(f"Spotify Link: {row['spotify_url']}")
#             print()


import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# function to get the Spotify URL's for songs that are recommended based on genre
def get_spotify_info(track_id, sp):
    track = sp.track(track_id)
    audio_features = sp.audio_features([track_id])[0] # Retrieve audio features of the inputted song to get a relative tempo from
    return track, audio_features

def get_artist_id_by_genre(genre, sp):
    results = sp.search(q=f'genre:"{genre}"', type='artist', limit=1)
    if results['artists']['items']:
        return results['artists']['items'][0]['id']
    else:
        return None

def recommendByGenre_Tempo(song_name, genre, sp):
    # Querying the Spotify API to search for the input song
    results = sp.search(q=song_name, type='track', limit=1)

    # If the song was found, proceed with recommendations
    if results['tracks']['items']:
        input_track = results['tracks']['items'][0]

        # Get tempo of the input track
        _, input_audio_features = get_spotify_info(input_track['id'], sp)
        input_tempo = input_audio_features['tempo']

        # Get an artist ID associated with the desired genre
        seed_artist = get_artist_id_by_genre(genre, sp)

        if seed_artist:
            # Get top tracks with a target tempo using the obtained artist ID as seed
            recommendations = sp.recommendations(seed_artists=[seed_artist], target_tempo=[input_tempo], limit=11)  # Increase limit by 1 to filter out the input track

            # Filter out the input track from the recommendations
            recommendations['tracks'] = [track for track in recommendations['tracks'] if track['id'] != input_track['id']]

            # Take only the top 10 recommendations after filtering
            recommendations = recommendations.head(10)

            # Add a column for Spotify URLs
            recommendations['spotify_url'] = [get_spotify_info(track['id'], sp)[0]['external_urls']['spotify'] for track in recommendations['tracks']]

            return recommendations

        else:
            print(f"No artist found for the specified genre '{genre}'.")
            return None

    else:
        print(f"No match found for the song '{song_name}'.")
        return None

if __name__ == "__main__":
    # Take user input for the song name
    user_input = input("Enter the name of a song from Spotify: ")

    # Set up Spotify API credentials
    client_id = 'cf9550faad1b4d2f93b868511b7bebf2'
    client_secret = 'adc6e3b265824a4d8bcaee3da0a652e5'
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # Get recommendations based on genre and target tempo
    recommendations = recommendByGenre_Tempo(user_input, sp)

    # Display recommendations including Spotify links
    if recommendations is not None:
        print("\nTop 10 Recommendations Based on Genre and Target Tempo:")
        for track in recommendations['tracks']:
            artists = ', '.join([artist['name'] for artist in track['artists']])
            print(f"{track['name']} by {artists} (Popularity: {track['popularity']}, Genre: {track['artists'][0]['name']})")
            print(f"Spotify Link: {track['external_urls']['spotify']}")
            print()

