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

const InfoPage = () => {
  return (
    <Container>
      <iframe
        src="https://ukrainian-ai-chatbot.streamlit.app/?embed=true"
        height="600"
        width="400"
      ></iframe>
    <Link exact to="/explain">Explain</Link>
    </Container>
  );
};

export default InfoPage;
