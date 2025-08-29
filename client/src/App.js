import React from "react";
import { Container } from "@mui/material";

import { UserProvider } from "./contexts/UserContext";
import { ChannelProvider } from "./contexts/ChannelContext";
import { VideoProvider } from "./contexts/VideoContext";
import { HTTPProvider } from "./contexts/HTTPContext";

import useWindowDimensions from "./customHooks/useWindowDimensions";
import Pages from "./pages";


import "./App.css";

function App() {
  const { width: windowWidth } = useWindowDimensions();

  return (
    <UserProvider>
      <ChannelProvider>
        <VideoProvider>
          <HTTPProvider>
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
          </HTTPProvider>
        </VideoProvider>
      </ChannelProvider>
    </UserProvider>
  );
}

export default App;
