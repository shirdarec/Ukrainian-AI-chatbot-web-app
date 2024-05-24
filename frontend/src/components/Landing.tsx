import React from "react";
import { Link } from "react-router-dom";
import styled from "styled-components";
import img from "../assets/1.png";

const Logo = styled.img`
  width: 40%;
  border-radius: 20px;
`;

const Container = styled.div`
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
`;

const Landing = () => {
  return (
    <Container>
      <Logo src={img} />
      <Link exact to="/info">
        Chat
      </Link>
    </Container>
  );
};

export default Landing;
