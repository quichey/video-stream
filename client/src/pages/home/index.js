import * as React from "react";
import { Box } from "@mui/material";

import RecommendedVideos from "./RecommendedVideos";

export default function Home() {
  const [userID, setUserID] = React.useState(0)
  const [sessionToken, setSessionToken] = React.useState()
  const [videoList, setVideoList] = React.useState([])

  var temp_user = {
    "user_id": userID,
    "user_name": "blah",
    //"token": sessionToken,
  };
  var post_req_data = JSON.stringify(temp_user)
  fetch(
    "http://127.0.0.1:5000/video-list",
    {
      method: "POST",
      // may need to use POST later for adding params
      // i think don't have to, could use query string
      // POST is probably more secure cause body is probably encrypted
      //method: "POST",
      // body: JSON.stringify({ limit: 30 }),
      // mode: "no-cors",
      body: post_req_data
    },
  )
  .then((response) => response.json())
  .then((json) => {
    console.log(json);
    setVideoList(json.video_data);
    setSessionToken(json.session_info);
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
