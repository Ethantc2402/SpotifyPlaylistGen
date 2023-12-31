import React from "react";
import RoomJoinPage from "./RoomJoinPage";
import CreateRoomPage from "./CreateRoomPage";
import HomePage from "./HomePage";
import RoomPage from "./RoomPage";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link,
  Redirect,
} from "react-router-dom";

const AppRoutes = () => {
  
  return (
    <Router>
      <Switch>
        <Route exact path="/" component={HomePage} />
        <Route path="/join" component={RoomJoinPage} />
        <Route path="/create" component={CreateRoomPage} />
        <Route path="/room/:roomCode" component={RoomPage} />
      </Switch>
    </Router>
  );
}

export default AppRoutes;
