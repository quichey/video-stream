import React from "react";
import { Button } from "@mui/material";

export default function ButtonVS({ text, handleClick }) {
  return (
    <Button variant="contained" onClick={handleClick}>
      {text}
    </Button>
  );
}
