import * as React from "react";
import { Box } from "@mui/material";

import { HTTPContext } from "..";

import RecommendedVideos from "./RecommendedVideos";

export default function Home() {
  const httpContext = React.useContext(HTTPContext);
  const [videoList, setVideoList] = React.useState([])

  React.useEffect(() => {
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

  }, [httpContext])

  return (
    <Box
      component="form"
      sx={{
        "& > :not(style)": { m: 1, width: "100%" },
      }}
      noValidate
      autoComplete="off"
      style={{
        width: "100%",
      }}
    >
      <RecommendedVideos videoList={videoList} />
    </Box>
  );
}
