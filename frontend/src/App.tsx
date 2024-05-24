import React from "react";
import Explain from "./components/Explain";
import { Link, Route, Routes } from "react-router-dom";
import "./App.css";
import Converter from "./components/Converter";
import styled from "styled-components";
import Landing from "./components/Landing";
import InfoPage from "./components/InfoPage";

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
      <Routes>
        <Route exact path="/" element={<Landing/>} />
        <Route exact path="/explain" element={<Explain/>} />
        <Route exact path="/info" element={<InfoPage/>} />
      </Routes>
      <Box />
      <Link exact to="/">Home</Link>
    </>
  );
}

export default App;
