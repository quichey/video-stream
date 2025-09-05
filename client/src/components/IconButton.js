import React from "react";
import { IconButton } from "@mui/material";

export default function IconButtonVS({ handleClick, children }) {
  return (
    <IconButton variant="contained" onClick={handleClick}>
      {children}
    </IconButton>
  );
}
