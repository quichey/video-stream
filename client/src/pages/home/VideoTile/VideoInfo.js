import * as React from "react";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";

export default function VideoInfo({ title, userName, userIcon, totalViews, uploadDate }) {
  // do things here

  // add Toolbar for saving to playlists and etc when the tables for those are ready


  // would like someway to store profile pictures
  return (
    <Stack direction="row" spacing={1}>
      <Typography>{userIcon}</Typography>
        <Stack direction="column" spacing={1}>
            <Typography>{title}</Typography>
            <Typography>{userName}</Typography>
            <Stack direction="row" spacing={1}>
                <Typography>{totalViews}</Typography>
                <Typography>{uploadDate}</Typography>
            </Stack>
        </Stack>
    </Stack>
  );
}