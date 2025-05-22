import * as React from "react";
import { Box } from "@mui/material";

import Comments from "./comments/index";
import Navbar from "./Navbar";
import Recommendations from "./Recommendations";
import Video from "./Video";

export default function Watch({ userID, sessionToken, setSessionToken, videoID }) {
  return (
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
      <Box
        component="form"
        sx={{
          "& > :not(style)": { m: 1, width: "100%" },
        }}
        noValidate
        display="flex"
        flexDirection="row"
        autoComplete="off"
        style={{
          width: "100%",
        }}
      >
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
            width: "70%",
          }}
        >
          <Video userID={userID} sessionToken={sessionToken} setSessionToken={setSessionToken} />
          {
            sessionToken == undefined ? undefined :
            <Comments userID={userID} sessionToken={sessionToken} setSessionToken={setSessionToken} />
            }
        </Box>
        <Recommendations />
      </Box>
    </Box>
  );
}
