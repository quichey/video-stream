import React, { useState } from "react";
import { Popover, Button, MenuItem, Typography } from "@mui/material";

import Login from "./Login";
import Logout from "./Logout";

export default function SessionMenu() {
  const [anchorEl, setAnchorEl] = useState(null);

  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const open = Boolean(anchorEl);
  const id = open ? "simple-popover" : undefined;

  return (
    <div>
      <Button variant="contained" onClick={handleClick}>
        Open Menu
      </Button>

      <Popover
        id={id}
        open={open}
        anchorEl={anchorEl}
        onClose={handleClose}
        anchorOrigin={{
          vertical: "bottom",
          horizontal: "left",
        }}
        transformOrigin={{
          vertical: "top",
          horizontal: "left",
        }}
      >
        <Login />
        <MenuItem onClick={handleClose}>Settings</MenuItem>
        <Logout />
      </Popover>
    </div>
  );
}
