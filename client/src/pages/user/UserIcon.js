import * as React from "react";
import { Box } from "@mui/material";
import { NavLink } from "react-router";

import { ChannelContext } from "../../contexts/ChannelContext";
import UserIconImg from "../../components/UserIconImg";

export default function UserIcon({ id, userIcon, userName, userIconURL }) {
  const { setID, setName } = React.useContext(ChannelContext);

  const handleIconClick = React.useCallback(() => {
    setID(id);
    setName(userName);
  }, [id, userName, setID, setName]); //pretty sure this will cause inf loop

  return (
    <Box sx={{ maxWidth: 360 }} onClick={handleIconClick}>
      <NavLink to={`/channel/${id}`} end>
        <UserIconImg
          id={id}
          userIcon={userIcon}
          userIconURL={userIconURL}
          length="20px"
        />
      </NavLink>
    </Box>
  );
}
