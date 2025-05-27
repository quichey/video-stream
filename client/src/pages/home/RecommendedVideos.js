import * as React from "react";
import { List } from "@mui/material";
import ListItem from "@mui/material/ListItem";

import { UserContext } from "..";

import VideoTile from "./VideoTile";


export default function RecommendedVideos({ videoList }) {
  const setRecommendedVideos = React.useContext(UserContext).setRecommendedVideos
  React.useEffect(() => {
    setRecommendedVideos(videoList);
  }, [videoList, setRecommendedVideos]);
  return (
    <List sx={{ width: "100%", maxWidth: 360, bgcolor: "background.paper" }}>
      {videoList.map((videoInfo) => {
        return (
          <ListItem>
            <VideoTile
              id={videoInfo.id}
              fileName={videoInfo.file_name}
              fileDir={videoInfo.file_dir}
              userName={videoInfo.userName}
            >
            </VideoTile>
          </ListItem>
        );
      })}
    </List>
  );
}