import React, { useState } from "react";
import AccountCircleIcon from "@mui/icons-material/AccountCircle";

import IconButtonVS from "../../../components/IconButton";
import SessionMenu from "./SessionMenu";

function SessionButton() {
  const [anchorEl, setAnchorEl] = useState(null);

  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };
  // TODO: use profiles ICON image as icon

  return (
    <div>
      <IconButtonVS IconComponent={<AccountCircleIcon />} handleClick={handleClick} />
      <SessionMenu handleClose={handleClose} anchorEl={anchorEl}/>
    </ div>
  );
}

export default SessionButton;
