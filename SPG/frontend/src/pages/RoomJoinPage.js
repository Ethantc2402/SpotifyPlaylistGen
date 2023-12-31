import React, { useState } from "react";
import { Button, Grid, Typography, TextField } from "@material-ui/core"; 
import { Link, useHistory } from "react-router-dom";

const RoomJoinPage = () => {
    let history = useHistory();
    const [roomCode, setRoomCode] = useState("");
    const [error, setError] = useState("");

    const handleRoomCodeChange = (e) => {
        setRoomCode(e.target.value);
    }

    const joinRoom = () => {
        const requestOptions = {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                code: roomCode
            })
        };
        fetch('/api/join-room', requestOptions).then((res) => {
            if(res.ok) {
                history.push(`/room/${roomCode}`);
            } else {
                setError("Room not found.");
                setRoomCode("");
            }
        }).catch(error => console.log(error));
    }

    return (
        <Grid container spacing={1}>
            <Grid item xs={12} align="center">
                <Typography variant="h4" component="h4">
                    Join a Room
                </Typography>
            </Grid>
            <Grid item xs={12} align="center">
                <TextField 
                    error={error} 
                    label="Code"
                    placeholder="Enter a Room Code"
                    value={roomCode}
                    helperText={error}
                    variant="outlined"
                    onChange={handleRoomCodeChange}
                />
            </Grid>
            <Grid item xs={12} align="center">
                <Button variant="contained" color="primary" onClick={joinRoom}>
                    Enter Room
                </Button>
            </Grid>
            <Grid item xs={12} align="center">
                <Button variant="contained" color="secondary" to="/" component={Link}>
                    Back
                </Button>
            </Grid>
        </Grid>
    );
}

export default RoomJoinPage;
