import * as React from "react";
import Card from "@mui/material/Card";
import { NavLink } from "react-router";


export default function UserIcon({ id, userIcon }) {
    const [channelID, setChannelID] = React.useState()

  const handleIconClick = React.useCallback(() => {
    console.log(channelID)
    setChannelID(id);
  }, [id, channelID]); //pretty sure this will cause inf loop

  return (
    <Card variant="outlined" sx={{ maxWidth: 360 }} onClick={handleIconClick}>
      <NavLink to={`/channel/${id}`} end>
        <img
            alt={userIcon}
            src={`${process.env.PUBLIC_URL}/images/${id}/${userIcon}.png`}
            width="20px"
            height="20px"
        />
      </NavLink>
    </Card>
  );
}
