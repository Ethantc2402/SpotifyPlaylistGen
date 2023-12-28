import React from "react";
import { Button, Grid, Typography, TextField, FormHelperText, FormControl, Radio, RadioGroup, FormControlLabel } from "@material-ui/core";
import { Link } from "react-router-dom";

export default RoomJoinPage = (props) => {
  const defaultVotes = 2;
  return (
    <Grid container spacing={1}>
      <Grid item xs={12} alignItems="center" justifyContent="center">
        <Typography component="h4" variant="h4">
          Create a Room
        </Typography>
      </Grid>
    </Grid>
  );
}
