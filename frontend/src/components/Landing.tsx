import React from "react";
import styled from "styled-components";
import img from "../assets/1.png";

const Logo = styled.img`
  width: 200px;
  border-radius: 20px;
  margin-right: 25px;
`;

const Landing = () => {
  return (
    <>
      <Logo src={img} />
    </>
  );
};

export default Landing;
