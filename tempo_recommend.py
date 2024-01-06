import pandas as pd

def recommendByTempo(artist_name, song_name, data):
    # Filter data based on the input song and artist names
    filtered_data = data[
        (data['track_name'].str.lower() == song_name.lower()) &
        (data['artist_name'].str.lower() == artist_name.lower())
    ]
    

    if filtered_data.empty:
        # Song with the artist was not found in the dataset
        print(f"No match found for the song '{song_name}' by '{artist_name}'.")
        return

    # Extract the tempo of the inputted song
    input_tempo = filtered_data.iloc[0]['tempo']
    
    print("You picked: " + filtered_data.iloc[0]['track_name'])
    print("From artist: " + filtered_data.iloc[0]['artist_name'])
    print("This song is of tempo: " + str(input_tempo))

    # Define the range for tempo similarity (you can adjust this range)
    tempo_range = 1

    # Filter data based on the tempo range
    tempo_matches = data[
        (data['tempo'] >= input_tempo - tempo_range) &
        (data['tempo'] <= input_tempo + tempo_range)
    ]

    # Remove the actual inputted song from the list of matches
    tempo_matches = tempo_matches[
        (tempo_matches['track_name'].str.lower() != song_name.lower()) |
        (tempo_matches['artist_name'].str.lower() != artist_name.lower())
    ]

    # Sorting the top 5 matches by popularity (descending order)
    top_recommendations = tempo_matches.sort_values(by = 'popularity', ascending = False).head(10)

    # Return the top 5 recommendation list
    return top_recommendations

if __name__ == "__main__":
    # Load CSV data into a DataFrame using pandas library
    spotify_data = pd.read_csv('spotify_data.csv')

    # Take user input for the song and artist names
    user_artist = input("Enter the name of the artist: ")
    user_song = input("Enter the name of a song in the CSV file: ")

    # Get recommendations based on genre considering both song and artist names
    recommendations = recommendByTempo(user_artist, user_song, spotify_data)

    # Display recommendations as just text
    if recommendations is not None:
        print("\nTop 10 Recommendations Based on Tempo, Sorted by Popularity (Descending):")
        print(recommendations[['artist_name', 'track_name', 'popularity', 'tempo']])