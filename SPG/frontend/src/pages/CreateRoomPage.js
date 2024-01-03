import React, { useState } from "react";
import { Button, Grid, Typography, TextField, FormHelperText, FormControl, Radio, RadioGroup, FormControlLabel } from "@material-ui/core"; 
import { Link, useHistory } from "react-router-dom";

const CreateRoomPage = () => {
  const defaultProps = {
    votesToSkip: 2,
    guestCanPause: true,
  }
  let history = useHistory();
  const [guestCanPause, setGuestCanPause] = useState(defaultProps.guestCanPause);
  const [votesToSkip, setVotesToSkip] = useState(defaultProps.votesToSkip);

  const handleRoomButtonPressed = () => {
    const createRoomURL = '/api/create-room';
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        votes_to_skip: votesToSkip,
        guest_can_pause: guestCanPause,
      }),
    };
    fetch(createRoomURL, requestOptions)
      .then((response) => response.json())
      .then((data) => history.push(`/room/${data.code}`));
  }
  return (
    <Grid container spacing={1}>
      <Grid item xs={12} align="center">
        <Typography component="h4" variant="h4">
          Create A Room
        </Typography>
      </Grid>
      <Grid item xs={12} align="center">
        <FormControl component="fieldset">
          <FormHelperText>
            <div align="center">Guest Control of Playback State</div>
          </FormHelperText>
          <RadioGroup
            row
            defaultValue="true"
            onChange={(e) => setGuestCanPause(e.target.value)}
          >
            <FormControlLabel
              value="true"
              control={<Radio color="primary" />}
              label="Play/Pause"
              labelPlacement="bottom"
            />
            <FormControlLabel
              value="false"
              control={<Radio color="secondary" />}
              label="No Control"
              labelPlacement="bottom"
            />
          </RadioGroup>
        </FormControl>
      </Grid>
      <Grid item xs={12} align="center">
        <FormControl>
          <TextField
            required={true}
            type="number"
            onChange={(e) => setVotesToSkip(e.target.value)}
            defaultValue={defaultProps.votesToSkip}
            inputProps={{
              min: 1,
              style: { textAlign: "center" },
            }}
          />
          <FormHelperText>
            <div align="center">Votes Required To Skip Song</div>
          </FormHelperText>
        </FormControl>
      </Grid>
      <Grid item xs={12} align="center">
        <Button
          color="primary"
          variant="contained"
          onClick={handleRoomButtonPressed}
        >
          Create A Room
        </Button>
      </Grid>
      <Grid item xs={12} align="center">
        <Button color="secondary" variant="contained" to="/" component={Link}>
          Back
        </Button>
      </Grid>
    </Grid>
  );
}

export default CreateRoomPage;
