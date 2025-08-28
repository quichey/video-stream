import React, { useState } from "react";
import { Popover, Button, MenuItem, Typography } from "@mui/material";

import Login from "./Login";
import Logout from "./Logout";
import Register from "./Register";

import { UserContext } from "../../../contexts/UserContext";

export default function SessionMenu({ handleClose, anchorEl }) {
    const { name } = React.useContext(UserContext);

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
        <Typography>
            {name}
        </Typography>
        <Login />
        <MenuItem onClick={handleClose}>Settings</MenuItem>
        <Logout />
        <Register />
      </Popover>
    </div>
  );
}
