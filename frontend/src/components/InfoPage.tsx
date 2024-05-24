import React from "react";
import { Link } from "react-router-dom";
import styled from "styled-components";

const Container = styled.div`
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
`;

const Streamlit = styled.iframe`
    @media screen and (max-width: 800px) {
        width: 300px;
    }
    @media screen and (min-width: 1200px) {
        width: 600px;
    }
    height: 600px;
    width: 400px;
`;

const InfoPage = () => {
  return (
    <Container>
      <Streamlit
        src="https://ukrainian-ai-chatbot.streamlit.app/?embed=true"
      ></Streamlit>
      <Link exact to="/explain">
        Explain
      </Link>
    </Container>
  );
};

export default InfoPage;
