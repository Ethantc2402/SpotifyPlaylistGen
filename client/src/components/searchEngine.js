// Import React hooks and CSS for styling
import React, { useState, useEffect } from "react";
import "../css/searchEngine.css";

// Spotify API credentials (Note: In a real app, it's unsafe to expose your client secret in frontend code)
const CLIENT_ID = "8238ed5e942f4b289d5c0ba44bf2427b";
const CLIENT_SECRET = "34ce0968afe74a29a655cd2c6f760ac9";

// Main App component
function SearchEngine({ setTrackId: setTrackId }) {
  // State hooks for managing component state
  const [searchInput, setSearchInput] = useState(""); // Stores the user's search input
  const [accessToken, setAccessToken] = useState(""); // Stores the Spotify API access token
  const [tracks, setTracks] = useState([]); // Stores the search results (tracks)
  const [selectedTrack, setSelectedTrack] = useState(""); // Tracks the user-selected tracks

  // useEffect hook to fetch the access token when the component mounts
  useEffect(() => {
    var authParameters = {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: `grant_type=client_credentials&client_id=${CLIENT_ID}&client_secret=${CLIENT_SECRET}`,
    };
    // Fetching the access token from Spotify
    fetch("https://accounts.spotify.com/api/token", authParameters)
      .then((result) => result.json())
      .then((data) => setAccessToken(data.access_token));

    searchInput === "" ? setTracks([]) : search();
  }, [searchInput]);

  // Function to search Spotify tracks based on the user's input
  async function search() {
    var searchParameters = {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + accessToken,
      },
    };

    // Fetching tracks from the Spotify API
    await fetch(
      `https://api.spotify.com/v1/search?q=${searchInput}&type=track&market=US&limit=5`,
      searchParameters
    )
      .then((response) => response.json())
      .then((data) => {
        // Checking if the data contains tracks and updating the state
        if (data.tracks && Array.isArray(data.tracks.items)) {
          setTracks(data.tracks.items);
        } else {
          console.error(
            "Expected data.tracks to be an array, received:",
            data.tracks
          );
          setTracks([]);
        }
      });
  }

  useEffect(() => {
    setTrackId(selectedTrack);
  }, [selectedTrack]);

  return (
    <div className="App">
      <div className="search-container">
        <input
          type="text"
          className="search-box"
          id="trackId"
          placeholder="(Optional) Have a specific song in mind? Search here!"
          onChange={(event) => setSearchInput(event.target.value)}
        />
      </div>
      <div className="track-list">
        {tracks.map((track, index) => (
          <div
            key={index}
            className={`track-item ${
              selectedTrack === track.id ? "selected" : ""
            }`}
            onClick={() => setSelectedTrack(track.id)}
          >
            <img
              src={track.album.images[0].url}
              alt={track.name}
              className="track-image"
            />
            <div className="track-info">
              <div className="track-title">{track.name}</div>
              <div className="track-artist">
                {track.artists.map((artist) => artist.name).join(", ")}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default SearchEngine;
