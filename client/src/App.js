import React from "react";
import { Container } from "@mui/material";

import { UserProvider } from "./contexts/UserContext";
import { ChannelProvider } from "./contexts/ChannelContext";
import { VideoProvider } from "./contexts/VideoContext";
import { HTTPProvider } from "./contexts/HTTPContext";

//import useWindowDimensions from "./customHooks/useWindowDimensions";
import Pages from "./pages";


import "./App.css";

function App() {
  //const { width: windowWidth } = useWindowDimensions();

  return (
    <UserProvider>
      <ChannelProvider>
        <VideoProvider>
          <HTTPProvider>
            <Container
              disableGutters
              maxWidth={false}
              sx={{ width: "100%" }}
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
