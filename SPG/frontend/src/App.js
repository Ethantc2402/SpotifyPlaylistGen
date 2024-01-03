import React from "react";
import { render } from "react-dom";
import AppRoutes from "./pages/AppRoutes";

const App = () => {

  return (
    <div className="center">
      <AppRoutes />
    </div>
  );
}

const appDiv = document.getElementById("app");
render(<App />, appDiv);
