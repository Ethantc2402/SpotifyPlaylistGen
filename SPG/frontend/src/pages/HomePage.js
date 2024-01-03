import React, { useEffect } from "react";
import { Button, ButtonGroup, Grid, Typography } from "@material-ui/core"; 
import { Link, useHistory } from "react-router-dom";

const HomePage = () => {
  let history = useHistory();
  useEffect(() => {
    const userAuthUrl = '/api/user-in-room';
    fetch(userAuthUrl).then(res => res.json()).then(data => {
      if(data.code) {
        history.push(`/room/${data.code}`);
      }
    })
  })

  return (
    <Grid container spacing={3}>
      <Grid item xs={12} align="center">
        <Typography component="h3" variant="h3">
          House Party
        </Typography>
      </Grid>
      <Grid item xs={12} align="center">
        <ButtonGroup disableElevation variant="contained" color="primary">
          <Button color="primary" to="/join" component={Link}>
            Join a Room
          </Button>
          <Button color="secondary" to="/create" component={Link}>
            Create a Room
          </Button>
        </ButtonGroup>
      </Grid>
    </Grid>
  );
}

export default HomePage;
