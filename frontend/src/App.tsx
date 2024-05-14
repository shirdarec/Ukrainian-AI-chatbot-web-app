import React from "react";
import Explain from "./components/Explain";
import { withRouter, Link, Route, Switch } from "react-router-dom";
import "./App.css";
import Converter from "./components/Converter";
import styled from "styled-components";
import Landing from "./components/Landing";

const Box = styled.div`
  display: flex;
  background: #fc9a0e;
  width: 50%;
  height: 100%;
  border-radius: 20px;
  z-index: -100;
  position: absolute;
  top: 0%;
  left: 25%;
`;

function App() {
  return (
    <>
      <Switch>
        <Route exact path="/" component={withRouter(Landing)} />
        <Route exact path="/explain" component={withRouter(Explain)} />
      </Switch>
      <Box />
    </>
  );
}

export default App;
