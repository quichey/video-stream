import React from "react";
import { IconButton } from "@mui/material";

export default function IconButtonVS({
  handleClick,
  buttonProps = {},
  children,
}) {
  return (
    <IconButton variant="contained" onClick={handleClick} {...buttonProps}>
      {children}
    </IconButton>
  );
}
