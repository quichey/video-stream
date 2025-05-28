import { Container } from "@mui/material";

import useWindowDimensions from "./customHooks/useWindowDimensions";
import Pages from "./pages";

import logo from "./logo.svg";
import "./App.css";
import { useEffect } from "react";

function App() {
  const { width: windowWidth } = useWindowDimensions();
  return (
    <Container
      style={{
        paddingLeft: 0,
        paddingRight: 0,
        marginLeft: 0,
        marginRight: 0,
        width: windowWidth,
        maxWidth: windowWidth,
        //overflowX: "hidden",
      }}
    >
      <Pages />
    </Container>
  );
}

export default App;
