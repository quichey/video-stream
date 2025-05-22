import * as React from "react";
import { Box } from "@mui/material";

import { UserContext } from "..";
import { HTTPContext } from "..";
import RecommendedVideos from "./RecommendedVideos";

export default function Home() {
  const userContext = React.useContext(UserContext);
  const httpContext = React.useContext(HTTPContext);
  const [videoList, setVideoList] = React.useState([])

  fetch(
    `${httpContext.serverURL}/video-list`,
    {
      method: "POST",
      // may need to use POST later for adding params
      // i think don't have to, could use query string
      // POST is probably more secure cause body is probably encrypted
      //method: "POST",
      // body: JSON.stringify({ limit: 30 }),
      // mode: "no-cors",
      body: httpContext.postRequestPayload
    },
  )
  .then((response) => response.json())
  .then((json) => {
    console.log(json);
    setVideoList(json.video_data);
    httpContext.refreshSessionToken(json);
  })
  .catch((error) => {
    console.log(error);
  });

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
          <RecommendedVideos videoList={videoList} />
        </Box>
        <Recommendations />
      </Box>
    </Box>
  );
}
