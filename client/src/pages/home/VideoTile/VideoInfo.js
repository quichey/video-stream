import * as React from "react";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";
import { NavLink } from "react-router";

import { ChannelContext } from "../..";
import { VideoContext } from "../..";

import UserIcon from "../../user/UserIcon";

export default function VideoInfo({ title, userName, userIcon, totalViews, uploadDate, userID, videoID }) {
  const { setID, setName } = React.useContext(ChannelContext);
  const { setID: setVideoID } = React.useContext(VideoContext);
  // do things here

  // add Toolbar for saving to playlists and etc when the tables for those are ready


  // would like someway to store profile pictures

  // Many things are clickable
  // Video Title ----> Video watch page can do soon
  // Username ---> channel page
  // User icon ----> channel page
  
    const handleTitleClick = React.useCallback(() => {
      setVideoID(videoID);
    }, [videoID, setVideoID]); 
  
  
    const handleChannelClick = React.useCallback(() => {
      setID(userID)
      setName(userName);
    }, [userID, userName, setID, setName]); 
  
  return (
    <Stack direction="row" useFlexGap spacing={1}>
        <UserIcon id={userID} userIcon={userIcon} userName={userName}/>
        <Stack direction="column" spacing={1}>
            <NavLink to={`/watch/${videoID}`} end>
                <Typography variant="h6" onClick={handleTitleClick}>{title}</Typography>
            </NavLink>
            <NavLink to={`/channel/${userID}`} end>
                <Typography onClick={handleChannelClick}>{userName}</Typography>
            </NavLink>
            <Stack direction="row" spacing={1}>
                <Typography>{totalViews}</Typography>
                <Typography>{uploadDate}</Typography>
            </Stack>
        </Stack>
    </Stack>
  );
}