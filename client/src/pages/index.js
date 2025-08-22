import * as React from "react";
import { BrowserRouter, Routes, Route } from "react-router";
import { Box } from "@mui/material";

import Home from "./home";
import Watch from "./watch";
import User from "./user";
import VideoUpload from "./video_upload";
import Navbar from "./Navbar";

export const UserContext = React.createContext(null);

export const ChannelContext = React.createContext(null);

export const VideoContext = React.createContext(null);

export const serverURL = process.env.REACT_APP_SERVER_APP_URL || process.env.REACT_APP_API_BASE;
export const HTTPContext = React.createContext(null);

export default function Pages() {
  const [userID, setUserID] = React.useState(0);
  const [userName, setUserName] = React.useState("users_name_0");

  const [channelID, setChannelID] = React.useState(0);
  const [channelName, setChannelName] = React.useState("users_name_0");

  const [videoID, setVideoID] = React.useState(0);
  const [videoFileName, setVideoFileName] = React.useState();
  const [videoFileDir, setVideoFileDir] = React.useState();

  const [postRequestPayload, setPostRequestPayload] = React.useState(0);

  React.useEffect(() => {
    var payloadObject = {
      user_id: userID,
      user_name: userName,
      video_id: videoID,
      session_token: sessionStorage.getItem("tempSessionToken")
    };
    var payloadJSON = JSON.stringify(payloadObject);
    setPostRequestPayload(payloadJSON);
  }, [userID, userName, videoID]);

  return (
    <UserContext.Provider
      value={{
        id: userID,
        setID: setUserID,
        uName: userName,
        setName: setUserName,
      }}
    >
    <ChannelContext.Provider
      value={{
        id: channelID,
        setID: setChannelID,
        name: channelName,
        setName: setChannelName,
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
                <Route path="channel">
                  <Route path=":userID" element={<User />} />
                </Route>
                <Route
                  index
                  path="upload"
                  element={<VideoUpload />}
                />
              </Routes>
            </Box>
          </BrowserRouter>
        </HTTPContext.Provider>
      </VideoContext.Provider>
    </ChannelContext.Provider>
    </UserContext.Provider>
  );
}
