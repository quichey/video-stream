import * as React from "react";
import { Box } from "@mui/material";
import { NavLink } from "react-router";

import { ChannelContext } from "..";

export default function UserIcon({ id, userIcon, userName }) {
  const { setID, setName } = React.useContext(ChannelContext);

  const handleIconClick = React.useCallback(() => {
    setID(id)
    setName(userName);
  }, [id, userName, setID, setName]); //pretty sure this will cause inf loop

  return (
    <Box  sx={{ maxWidth: 360 }} onClick={handleIconClick}>
      <NavLink to={`/channel/${id}`} end>
        <img
            alt={userIcon}
            src={`${process.env.PUBLIC_URL}/images/${id}/${userIcon}.png`}
            width="20px"
            height="20px"
        />
      </NavLink>
    </Box>
  );
}
