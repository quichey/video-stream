import * as React from "react";
import { Box } from "@mui/material";

import { VideoContext } from "..";

import Comments from "./comments/index";
import Recommendations from "./Recommendations";
import Video from "./Video";

export default function Watch() {
  const { fileDir, fileName } =
    React.useContext(VideoContext);

  const loadedVideo = (fileDir !== undefined) && (fileName !== undefined)
  return (
    <Box
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
          {loadedVideo && <Comments />}
        </Box>
        <Recommendations />
      </Box>
    </Box>
  );
}
