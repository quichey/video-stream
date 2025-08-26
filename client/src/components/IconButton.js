import React, { useState } from "react";
import {  IconButton, Typography } from "@mui/material";


export default function IconButtonVS({ IconComponent, handleClick }) {

  return (
      <IconButton variant="contained" onClick={handleClick}>
        <IconComponent />
      </IconButton>
  );
}
