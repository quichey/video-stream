import * as React from "react";
import { Box } from "@mui/material";

function VideoInfo({title, userName, userIcon, totalViews, uploadDate}) {
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
      {title}
      {userName}
      {userIcon}
      {totalViews}
      {uploadDate}
    </Box>
  );

}

export default function VideoTile({ id, fileName, fileDir, userName }) {
  const [title, setTitle] = React.useState("");
  const [userIcon, setUserIcon] = React.useState("");
  const [totalViews, setTotalViews] = React.useState("");
  const [uploadDate, setUploadDate] = React.useState("");
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
      <video controls width="100%" height="100%">
        <source src="/media/cc0-videos/flower.webm" type="video/webm" />
        <source
          src={`${process.env.PUBLIC_URL}/videos/${fileDir}/${fileName}`}
          type="video/mp4"
        />
      </video>
      <VideoInfo title={title} userName={userName} userIcon={userIcon} totalViews={totalViews} uploadDate={uploadDate} />
    </Box>
  );
}