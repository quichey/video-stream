import React, { useState } from "react";
import { Popover, Button, MenuItem, Typography } from "@mui/material";

export default function Login() {
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
        <MenuItem onClick={handleClose}>Login</MenuItem>
    </div>
  );
}
