import * as React from "react";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";

import UserIcon from "../../user/UserIcon";

export default function VideoInfo({ title, userName, userIcon, totalViews, uploadDate, userID }) {
  // do things here

  // add Toolbar for saving to playlists and etc when the tables for those are ready


  // would like someway to store profile pictures

  // Many things are clickable
  // Video Title ----> Video watch page can do soon
  // Username ---> channel page
  // User icon ----> channel page
  return (
    <Stack direction="row" spacing={1}>
        <UserIcon id={userID} userIcon={userIcon} />
        <Stack direction="column" spacing={1}>
            <Typography variant="h6">{title}</Typography>
            <Typography>{userName}</Typography>
            <Stack direction="row" spacing={1}>
                <Typography>{totalViews}</Typography>
                <Typography>{uploadDate}</Typography>
            </Stack>
        </Stack>
    </Stack>
  );
}