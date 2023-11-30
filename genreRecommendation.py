import pandas as pd

def recommendByGenre(song_name, data):
    # filter data based on the input song name
    # changing the case of the song name to lowercase for easier comparison
    song_data = data[data['track_name'].str.lower() == song_name.lower()]

    if song_data.empty:
        # song was not found in the dataset
        print(f"No match found for the song '{song_name}'.")
        return

    # extract the genre of the inputted song
    input_genre = song_data.iloc[0]['genre']

    # filter data based on the genre of the input song
    # gives list of just the songs in the same genre as the input song
    genre_matches = data[data['genre'] == input_genre]

    # remove the actual inputted song from the list of matches
    genre_matches = genre_matches[genre_matches['track_name'].str.lower() != song_name.lower()]

    # sorting the top 5 matches by popularity (descending order)
    top_recommendations = genre_matches.sort_values(by='popularity', ascending=False).head(5)

    # return the top 5 recommendation list
    return top_recommendations

# Only run the following code if this file is being run directly
# to be later exported as a module
if __name__ == "__main__":
    # load CSV data into a DataFrame using pandas library
    spotify_data = pd.read_csv('SpotifyPlaylistGen\spotify_data.csv')

    # take user input for the song name
    user_input = input("Enter the name of a song in the CSV file: ")

    # get recommendations based on genre
    recommendations = recommendByGenre(user_input, spotify_data)

    # display recommendations as just text
    if recommendations is not None:
        print("\nTop 5 Recommendations Based on Genre:")
        print(recommendations[['artist_name', 'track_name', 'popularity', 'genre']])
        