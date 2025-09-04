import * as React from "react";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";
import { NavLink } from "react-router";

import { ChannelContext } from "../../../contexts/ChannelContext";
import { VideoContext } from "../../../contexts/VideoContext";

import UserIcon from "../../user/UserIcon";

function formatTimeAgo(date) {
  const now = new Date();
  const seconds = Math.floor((now - date) / 1000);

  if (seconds < 60) {
    return new Intl.RelativeTimeFormat("en").format(-seconds, "second");
  }

  const minutes = Math.floor(seconds / 60);
  if (minutes < 60) {
    return new Intl.RelativeTimeFormat("en").format(-minutes, "minute");
  }

  const hours = Math.floor(minutes / 60);
  if (hours < 24) {
    return new Intl.RelativeTimeFormat("en").format(-hours, "hour");
  }

  const days = Math.floor(hours / 24);
  if (days < 7) {
    return new Intl.RelativeTimeFormat("en").format(-days, "day");
  }

  const weeks = Math.floor(days / 7);
  if (weeks < 4) {
    // Approximately a month
    return new Intl.RelativeTimeFormat("en").format(-weeks, "week");
  }

  const months = Math.floor(days / 30.44); // Average days in a month
  if (months < 12) {
    return new Intl.RelativeTimeFormat("en").format(-months, "month");
  }

  const years = Math.floor(days / 365.25); // Average days in a year
  return new Intl.RelativeTimeFormat("en").format(-years, "year");
}

export default function VideoInfo({
  title,
  userName,
  userIcon,
  totalViews,
  uploadDate,
  userID,
  videoID,
  userIconURL,
}) {
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
    setID(userID);
    setName(userName);
  }, [userID, userName, setID, setName]);

  return (
    <Stack direction="row" useFlexGap spacing={1}>
      <UserIcon
        id={userID}
        userIcon={userIcon}
        userName={userName}
        userIconURL={userIconURL}
      />
      <Stack direction="column" spacing={1}>
        <NavLink to={`/watch/${videoID}`} end>
          <Typography variant="h6" onClick={handleTitleClick}>
            {title}
          </Typography>
        </NavLink>
        <NavLink to={`/channel/${userID}`} end>
          <Typography onClick={handleChannelClick}>{userName}</Typography>
        </NavLink>
        <Stack direction="row" spacing={1}>
          <Typography>{totalViews}</Typography>
          <Typography>-</Typography>
          <Typography>{formatTimeAgo(new Date(uploadDate))}</Typography>
        </Stack>
      </Stack>
    </Stack>
  );
}
