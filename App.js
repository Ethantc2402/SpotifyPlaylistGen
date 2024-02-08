// Import React hooks and CSS for styling
import React, { useState, useEffect } from 'react';
import './App.css'; 

// Spotify API credentials (Note: In a real app, it's unsafe to expose your client secret in frontend code)
const CLIENT_ID = "8238ed5e942f4b289d5c0ba44bf2427b";
const CLIENT_SECRET = "34ce0968afe74a29a655cd2c6f760ac9";

// Main App component
function App() {
  // State hooks for managing component state
  const [searchInput, setSearchInput] = useState(""); // Stores the user's search input
  const [accessToken, setAccessToken] = useState(""); // Stores the Spotify API access token
  const [tracks, setTracks] = useState([]); // Stores the search results (tracks)
  const [selectedTracks, setSelectedTracks] = useState(new Set()); // Tracks the user-selected tracks

  // useEffect hook to fetch the access token when the component mounts
  useEffect(() => {
    var authParameters = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: `grant_type=client_credentials&client_id=${CLIENT_ID}&client_secret=${CLIENT_SECRET}`
    };
    // Fetching the access token from Spotify
    fetch('https://accounts.spotify.com/api/token', authParameters)
      .then(result => result.json())
      .then(data => setAccessToken(data.access_token));
  }, []);

  // Function to search Spotify tracks based on the user's input
  async function search() {
    console.log("Search for: " + searchInput);
    var searchParameters = {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + accessToken
      }
    };

    // Fetching tracks from the Spotify API
    await fetch(`https://api.spotify.com/v1/search?q=${searchInput}&type=track&market=US&limit=5`, searchParameters)
      .then(response => response.json())
      .then(data => {
        // Checking if the data contains tracks and updating the state
        if(data.tracks && Array.isArray(data.tracks.items)) {
          setTracks(data.tracks.items);
        } else {
          console.error('Expected data.tracks to be an array, received:', data.tracks);
          setTracks([]);
        }
      });
  }

  // Function to handle clicks on tracks, toggling their selection state
  function handleTrackClick(trackId) {
    setSelectedTracks(prevSelectedTracks => {
      const newSelectedTracks = new Set(prevSelectedTracks);
      if (newSelectedTracks.has(trackId)) {
        console.log(trackId)
        newSelectedTracks.delete(trackId);
      } else {
        newSelectedTracks.add(trackId);
      }
      return newSelectedTracks;
    });
  }

  // Render function to display the UI
  return (
    <div className="App">
      <div className="search-container">
        <input
          type="text"
          className="search-box"
          placeholder="(Optional) Have a specific song in mind? Search here!"
          onKeyDown={event => {
            // Trigger search on Enter key press
            if (event.key === "Enter") {
              search();
            }
          }}
          onChange={event => setSearchInput(event.target.value)}
        />
        <button className="generate-button" onClick={search}>Search</button>
      </div>
      <div className="track-list">
        {tracks.map((track, index) => (      
          <div
            key={index}
            className={`track-item ${selectedTracks.has(track.id) ? 'selected' : ''}`}
            onClick={() => handleTrackClick(track.id)}
          >
          <img src={track.album.images[0].url} alt={track.name} className="track-image" />
          <div className="track-info">
            <div className="track-title">{track.name}</div>
            <div className="track-artist">{track.artists.map(artist => artist.name).join(', ')}</div>
          </div>
        </div>
        ))}
      </div>
    </div>
  );
}

export default App;
