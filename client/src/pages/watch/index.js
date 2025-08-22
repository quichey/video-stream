import * as React from "react";
import { Box } from "@mui/material";


import Comments from "./comments/index";
import Recommendations from "./Recommendations";
import Video from "./Video";

export default function Watch() {
  // TODO: do logic for determining video data has been retrieved
  const  haveVideoData = false;
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
          <Video />
          {haveVideoData && <Comments />}
        </Box>
        <Recommendations />
      </Box>
    </Box>
  );
}
