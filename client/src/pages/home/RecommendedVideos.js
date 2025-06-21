import * as React from "react";
import { List } from "@mui/material";
import ListItem from "@mui/material/ListItem";

import VideoTile from "./VideoTile/VideoTile";

export default function RecommendedVideos({ videoList }) {
  return (
    <List sx={{ width: "100%", maxWidth: 360, bgcolor: "background.paper" }}>
      {videoList.map((videoInfo) => {
        return (
          <ListItem>
            <VideoTile
              id={videoInfo.id}
              fileName={videoInfo.file_name}
              fileDir={videoInfo.file_dir}
              userName={videoInfo.user_name}
              userIcon={videoInfo.user_icon}
              userID={videoInfo.user_id}
              dateCreated={videoInfo.date_created}
            ></VideoTile>
          </ListItem>
        );
      })}
    </List>
  );
}
