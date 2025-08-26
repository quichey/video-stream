import React, { useState } from "react";
import {  Button, Typography } from "@mui/material";


export default function ButtonVS({ text, handleClick }) {

  return (
      <Button variant="contained" onClick={handleClick}>
        {text}
      </Button>
  );
}
