// import React from "react";
import { useState } from "react";
import styled from "styled-components";

const Container = styled.div`
  width: x;
  height: 700px;
  border-radius: 20px;
  font-size: 20px;
  color: #8a7f63;
`;

const Box = styled.div`
  display: flex;
  background: #ffffff;
  width: 50%;
  height: 100%;
  border-radius: 20px;
  z-index: -99;
  position: absolute;
  top: 0%;
  left: 25%;
`;

const Buttons = styled.div`
  width: 60%;
  margin-left: 22%;
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 50%;
`;

const Button = styled.button`
  width: 200%;
  background: #b5b5b5;
  margin: 3%;
  font-size: 70%;
  border-radius: 20px;
`;

const infoPages = [
  {
    niceName: "Case Processing Items",
    name: "case-processing-items",
  },
  {
    niceName: "Payment Dates",
    name: "payment-dates",
  },
  {
    niceName: "Financial Support",
    name: "financial-support",
  },
  {
    niceName: "Rates",
    name: "rates",
  },
];

function Explain() {
  const [selected, setSelected] = useState("");

  return (
    <>
      <Box />
      <Container>
        Explain
        <Buttons>
          {infoPages.map((item, index) => (
            <Button
              onClick={() => {
                setSelected(item.name);
              }}
            >
              {item.niceName}
            </Button>
          ))}
        </Buttons>
        {selected}
      </Container>
    </>
  );
}

export default Explain;
