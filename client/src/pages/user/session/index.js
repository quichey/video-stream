import React, { useState } from "react";

import IconButtonVS from "../../../components/IconButton";
import SessionMenu from "./SessionMenu";

import { UserContext } from "../../../contexts/UserContext";

import UserIconImg from "../../../components/UserIconImg";

function SessionButton() {
  const [anchorEl, setAnchorEl] = useState(null);
  const { id, iconFileName, iconSASURL } = React.useContext(UserContext);

  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  return (
    <div>
      <IconButtonVS handleClick={handleClick}>
        <UserIconImg
          id={id}
          userIcon={iconFileName}
          userIconURL={iconSASURL}
          length="24px"
        />
      </IconButtonVS>
      <SessionMenu handleClose={handleClose} anchorEl={anchorEl} />
    </div>
  );
}

export default SessionButton;
