import React, { useState } from "react";
import {  IconButton, Typography } from "@mui/material";


export default function IconButtonVS({ handleClick, children }) {

  return (
      <IconButton variant="contained" onClick={handleClick}>
        {children}
      </IconButton>
  );
}
