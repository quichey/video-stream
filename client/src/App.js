import React from "react";
import { Container } from "@mui/material";

import { UserProvider } from "./contexts/UserContext";
import { ChannelProvider } from "./contexts/ChannelContext";
import { VideoProvider } from "./contexts/VideoContext";
import { HTTPProvider } from "./contexts/HTTPContext";

import { useLoadSession } from "./customHooks/useLoadSession";
import useWindowDimensions from "./customHooks/useWindowDimensions";
import Pages from "./pages";

import Loading from "./components/Loading";

import "./App.css";

function App() {
  const { width: windowWidth } = useWindowDimensions();
  

  React.useEffect(() => {
    // Cleanup function: remove temp-session token from sessionStorage on unmount
    return () => {
      sessionStorage.removeItem("tempSessionToken");
    };
  }, []); // empty dependency array → cleanup on unmount

  // This will handle fetching session from the server and saving temp-session from cookie
  const sessionLoaded = useLoadSession();
  if (!sessionLoaded) return <Loading />;

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
