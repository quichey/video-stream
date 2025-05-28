import * as React from "react";
import { Box } from "@mui/material";

import { useServerCall } from "../../customHooks/useServerCall";
import RecommendedVideos from "./RecommendedVideos";

export default function Home() {
  const [videoList, setVideoList] = React.useState([])
  const fetchData = useServerCall();
  
  const handleServer = React.useCallback((json) => {
    setVideoList(json.video_data);
  }, [])

  React.useEffect(() => {
    fetchData("video-list", handleServer);
  }, [fetchData, handleServer])

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
