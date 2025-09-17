import React from "react";
import { MenuItem, Typography } from "@mui/material";
import { NavLink } from "react-router";

import { UserContext } from "../../../contexts/UserContext";
import { ChannelContext } from "../../../contexts/ChannelContext";

export default function ViewChannel() {
  const { id } = React.useContext(UserContext);
  const { setID } = React.useContext(ChannelContext);

  const handleClick = React.useCallback(
    (event) => {
      setID(id);
    },
    [id, setID],
  );

  if (!id) {
    return null;
  }

  return (
    <div>
      <MenuItem data-testid="view-channel-menu-item">
        <NavLink to={`/channel/${id}`} end>
          <Typography onClick={handleClick}>View Channel</Typography>
        </NavLink>
      </MenuItem>
    </div>
  );
}
