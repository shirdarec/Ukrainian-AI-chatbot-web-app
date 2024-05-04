// import React from "react";
import styled from "styled-components";

const Container = styled.div`
  width: 450px;
  height: 700px;
  border-radius: 20px;
  font-size: 20px;
  color: #8a7f63;
`;

const Box = styled.div`
  display: flex;
  background: #ffffff;
  width: 450px;
  height: 700px;
  border-radius: 20px;
  z-index: -99;
  position: absolute;
  top: 10px;
  right: 35%;
`;

const Buttons = styled.div`
  width: 60%;
  margin-left: 22%;
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 40%;
`;

const Button = styled.button`
  width: 70%;
  background: #b5b5b5;
  margin: 2%;
  font-size: 70%;
  border-radius: 20px;
`;

function Explain() {
  return (
    <Container>
      <Box />
      Explain
      <Buttons>
        <Button>Case Processing Items</Button>
        <Button>Payment Dates</Button>
        <Button>Financial Support</Button>
        <Button>Rates</Button>
      </Buttons>
    </Container>
  );
}

export default Explain;
