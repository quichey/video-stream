import * as React from "react";
import Card from "@mui/material/Card";
import Divider from "@mui/material/Divider";
import { NavLink } from "react-router";

import { VideoContext } from "../..";
import VideoInfo from "./VideoInfo";

export default function VideoTile({ id, fileName, fileDir, userName, userIcon, userID }) {
  const { setID } = React.useContext(VideoContext);

  const [title, setTitle] = React.useState("");
  const [totalViews, setTotalViews] = React.useState("");
  const [uploadDate, setUploadDate] = React.useState("");

  React.useEffect(() => {
    setTitle("test title");
    setTotalViews("test total views");
    setUploadDate("test upload date");
  }, []);

  const handleVideoClick = React.useCallback(() => {
    setID(id);
  }, [id, setID]); //pretty sure this will cause inf loop

  return (
    <Card variant="outlined" sx={{ maxWidth: 360 }} onClick={handleVideoClick}>
      <NavLink to={`/watch/${id}`} end>
        <video controls width="100%" height="100%">
          <source src="/media/cc0-videos/flower.webm" type="video/webm" />
          <source
            src={`${process.env.PUBLIC_URL}/videos/${fileDir}/${fileName}`}
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
        uploadDate={uploadDate}
        userID={userID}
      />
    </Card>
  );
}
