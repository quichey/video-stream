import * as React from "react";
import { List } from "@mui/material";
import ListItem from "@mui/material/ListItem";

import VideoTile from "./VideoTile/VideoTile";

export default function RecommendedVideos({ videoList }) {
  return (
    <List
      sx={{ width: "100%", maxWidth: 360, bgcolor: "background.paper" }}
      data-testid="home-videos-list"
    >
      {videoList.map((videoInfo) => {
        return (
          <ListItem data-testid="home-video-list-item">
            <VideoTile
              id={videoInfo.id}
              fileName={videoInfo.file_name}
              fileDir={videoInfo.file_dir}
              userName={videoInfo.user_name}
              userIcon={videoInfo.user_icon}
              userID={videoInfo.user_id}
              dateCreated={videoInfo.date_created}
              sasURL={videoInfo.video_url}
              userIconURL={videoInfo.user_icon_url}
            ></VideoTile>
          </ListItem>
        );
      })}
    </List>
  );
}
