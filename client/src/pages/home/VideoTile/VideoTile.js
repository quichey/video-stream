import * as React from "react";
import Card from "@mui/material/Card";
import Divider from "@mui/material/Divider";
import { NavLink } from "react-router";

import { get_storage_url } from "../../../util/urls";
import VideoInfo from "./VideoInfo";

export default function VideoTile({ id, fileName, fileDir, userName, userIcon, userID, dateCreated, sasURL }) {

  const [title, setTitle] = React.useState("");
  const [totalViews, setTotalViews] = React.useState("");

  React.useEffect(() => {
    setTitle("test title");
    setTotalViews("test total views");
  }, []);

  /*
  const handleVideoClick = React.useCallback(() => {
    setID(id);
  }, [id, setID]); //pretty sure this will cause inf loop
  */

  return (
    //<Card variant="outlined" sx={{ maxWidth: 360 }} onClick={handleVideoClick}>
    <Card variant="outlined" sx={{ maxWidth: 360 }}>
      <NavLink to={`/watch/${id}`} end>
        <video controls width="100%" height="100%">
          <source
            src={get_storage_url("videos", fileDir, fileName, sasURL)}
            type="video/mp4"
          />
        </video>
      </NavLink>
      <Divider />
      <VideoInfo
        title={title}
        userName={userName}
        userIcon={userIcon}
        totalViews={totalViews}
        uploadDate={dateCreated}
        userID={userID}
        videoID={id}
      />
    </Card>
  );
}
