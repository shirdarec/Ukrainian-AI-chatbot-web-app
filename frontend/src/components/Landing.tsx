import React from "react";
import { Link } from "react-router-dom";
import styled from "styled-components";
import img from "../assets/1.png";

const Logo = styled.img`
  width: 40%;
  border-radius: 20px;
`;

const Landing = () => {
  return (
    <>
      <Logo src={img} />
      <Link exact to="/explain">explain</Link>
    </>
  );
};

export default Landing;
