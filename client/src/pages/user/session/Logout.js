import React, { useState } from "react";
import { Popover, Button, MenuItem, Typography } from "@mui/material";

export default function Logout() {

  const handleClick = (event) => {
  };


  return (
    <div>
        <MenuItem onClick={handleClick}>Logout</MenuItem>
    </div>
  );
}
