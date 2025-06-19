import * as React from "react";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";

export default function VideoInfo({ title, userName, userIcon, totalViews, uploadDate }) {
  // do things here

  // add Toolbar for saving to playlists and etc when the tables for those are ready
  return (
    <Stack direction="row" spacing={1}>
      <Typography>{userName}</Typography>
      <Typography>{title}</Typography>
      <Typography>{userIcon}</Typography>
      <Typography>{totalViews}</Typography>
      <Typography>{uploadDate}</Typography>
    </Stack>
  );
}