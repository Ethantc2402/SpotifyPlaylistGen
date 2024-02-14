import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom'; // Import useNavigate from react-router-dom
import "../css/home.css";

const HomePage = () => {
  const navigate = useNavigate(); // useNavigate hook for navigation

  useEffect(() => {
    // Check if the URL contains access token after redirection from Spotify
    const urlParams = new URLSearchParams(window.location.hash.substring(1)); // Remove '#' and parse URL
    const accessToken = urlParams.get('access_token');
    
    // If access token is present, user has logged in successfully
    if (accessToken) {
      // Redirect user to the main page or store the token in your application's state
      navigate('/main');
    }
  }, [navigate]);

  const handleLoginWithSpotify = () => {
    // Define your client ID and redirect URI
    const clientId = '52b7deed70ef4ae3bb2b4429ad67da13';
    const redirectUri = 'http://127.0.0.1:3000/';

    // Define the scopes your application needs
    const scopes = [
      'playlist-modify-public',
      // Add more scopes as needed
    ];

    // Construct the authorization URL
    const authorizeUrl = `https://accounts.spotify.com/authorize?client_id=${clientId}&redirect_uri=${encodeURIComponent(redirectUri)}&scope=${encodeURIComponent(scopes.join(' '))}&response_type=token&show_dialog=true`;

    // Redirect the user to the Spotify authorization page
    window.location.href = authorizeUrl;
  };

  return (
    <div className="home-page">
      <h1 className="title">Spotify Playlist Generator</h1>
      <p className="subtitle">Use the power of AI to create personalized playlists with your own preferences</p>
      <button className="login-button" onClick={handleLoginWithSpotify}>LOGIN WITH SPOTIFY</button>
    </div>
  );
};

export default HomePage;
