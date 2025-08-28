import React, { useState } from "react";
import { Popover, Button, MenuItem, Typography } from "@mui/material";

import Login from "./Login";
import Logout from "./Logout";
import Register from "./Register";

export default function SessionMenu({ handleClose, anchorEl }) {

  const open = Boolean(anchorEl);
  const id = open ? "simple-popover" : undefined;

  return (
    <div>

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
        <Register />
      </Popover>
    </div>
  );
}
