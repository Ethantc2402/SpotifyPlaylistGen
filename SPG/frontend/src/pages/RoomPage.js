import React, { useState, useEffect } from "react";
import { Button, Grid, Typography } from "@material-ui/core";
import {  useHistory } from "react-router-dom";
const RoomPage = (props) => {
  const history = useHistory();
  const [votesToSkip, setVotesToSkip] = useState(2);
  const [guestCanPause, setGuestCanPause] = useState(false);
  const [isHost, setIsHost] = useState(false);
  const [roomCode, setRoomCode] = useState(props.match.params.roomCode);
  const [showSettings, setShowSettings] = useState(false);
  const [isSpotifyAuthenticated, setIsSpotifyAuthenticated] = useState(false);
  useEffect(() => {
    getRoomDetails();
  }, []);

  const authenticateSpotify = async () => {
    const isAuthorized = await checkSpotifyAuthenticated();
    setIsSpotifyAuthenticated(isAuthorized);
    if(isAuthorized) {
      await spotifyAPIAuthRedirect();
    }
  }

  const checkSpotifyAuthenticated = async () => {
    fetch("/spotifyAPI/is-authenticated").then(res => res.json()).then((data) => {
      setIsSpotifyAuthenticated(data.status);
      return data.status;
    })
  }

  const spotifyAPIAuthRedirect = async () => {
    fetch("/spotify/get-auth-url")
      .then((response) => response.json())
      .then((data) => {
        window.location.replace(data.url);
      });
  }

  const getRoomDetails = () => {
    const getRoomUrl = `/api/get-room?code=${roomCode}`;
    fetch(getRoomUrl).then((res) => {
      if(res.status === 200){
        return res.json();
      }else{
        history.push("/");
      }
    }).then(async (data) => {
        setVotesToSkip(data.votes_to_skip);
        setGuestCanPause(data.guest_can_pause);
        setIsHost(data.is_host);
        if(data.is_host){
          await authenticateSpotify();
        }
    });
  }

  const leaveRoom = () => {
    const leaveRoomUrl = "/api/leave-room";
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    };
    fetch(leaveRoomUrl, requestOptions)
    .then(() => {
      setRoomCode(null);
      props.history.push("/");
    });
  }

  const toggleShowSettings = () => {
    setShowSettings(!showSettings);
  }

  return (
    <Grid container spacing={1}>
      <Grid item xs={12} align="center">
        <Typography variant="h4" component="h4">
          Code: {roomCode}
        </Typography>
      </Grid>
      <Grid item xs={12} align="center">
      <Typography variant="h4" component="h4">
          Votes: {votesToSkip}
        </Typography>
      </Grid>
      <Grid item xs={12} align="center">
        <Typography variant="h4" component="h4">
          Guest Can Pause: {guestCanPause ? guestCanPause.toString() : ""}
        </Typography>
      </Grid>
      <Grid item xs={12} align="center">
        <Typography variant="h4" component="h4">
          Is Host: {isHost ? isHost.toString() : ""}
        </Typography>
      </Grid>
      {
        isHost && 
          <Grid item xs={12} align="center">
            <Button variant="contained" color='primary' onClick={toggleShowSettings}>
              Settings
            </Button>
          </Grid>
      }
      <Grid item xs={12} align="center">
        <Button variant="contained" color='secondary' onClick={leaveRoom}>
          Leave Room
        </Button>
      </Grid>
    </Grid>
  ); 
}

export default RoomPage;