import * as React from "react";
import { BrowserRouter, Routes, Route } from "react-router";
import { Box } from "@mui/material";

import Home from "./home";
import Watch from "./watch";
import Navbar from "./Navbar";

export const UserContext = React.createContext(null);

export const VideoContext = React.createContext(null);

const serverURL = "http://127.0.0.1:5000";
export const HTTPContext = React.createContext(null);

export default function Pages() {
  const [userID, setUserID] = React.useState(0);
  const [userName, setUserName] = React.useState("users_name_0");
  const [sessionToken, setSessionToken] = React.useState(undefined);

  const [videoID, setVideoID] = React.useState(0);
  const [videoFileName, setVideoFileName] = React.useState();
  const [videoFileDir, setVideoFileDir] = React.useState();

  const [postRequestPayload, setPostRequestPayload] = React.useState(0);

  React.useEffect(() => {
    var payloadObject = {
      user_id: userID,
      user_name: userName,
      video_id: videoID,
    };
    if (sessionToken !== undefined) {
      payloadObject.token = sessionToken;
    }
    var payloadJSON = JSON.stringify(payloadObject);
    setPostRequestPayload(payloadJSON);
  }, [userID, userName, sessionToken, videoID]);

  const refreshSessionToken = React.useCallback((responseJSON) => {
    setSessionToken(responseJSON.session_info);
  }, []);

  return (
    <UserContext.Provider
      value={{
        id: userID,
        setID: setUserID,
        uName: userName,
        setName: setUserName,
        sessionToken: sessionToken,
      }}
    >
      <VideoContext.Provider
        value={{
          id: videoID,
          setID: setVideoID,
          fileName: videoFileName,
          setFileName: setVideoFileName,
          fileDir: videoFileDir,
          setFileDir: setVideoFileDir,
        }}
      >
        <HTTPContext.Provider
          value={{
            refreshSessionToken: refreshSessionToken,
            serverURL: serverURL,
            postRequestPayload: postRequestPayload,
          }}
        >
          <BrowserRouter>
            <Box
              component="form"
              sx={{
                "& > :not(style)": { m: 1, width: "100%" },
              }}
              noValidate
              display="flex"
              flexDirection="column"
              autoComplete="off"
              style={{
                width: "100%",
              }}
            >
              <Navbar />
              <Routes>
                <Route path="/" element={<Home />} />
                <Route path="watch">
                  <Route path=":videoID" element={<Watch />} />
                </Route>
              </Routes>
            </Box>
          </BrowserRouter>
        </HTTPContext.Provider>
      </VideoContext.Provider>
    </UserContext.Provider>
  );
}
