import * as React from "react";
import { Box } from "@mui/material";


export default function Banner() {
  return (
    <Box
      component="form"
      sx={{
        "& > :not(style)": { m: 1, width: "100%" },
      }}
      noValidate
      display="flex"
      flexDirection="column"
      autoComplete="off"
      style={{
        width: "100%",
      }}
    >
      <p>
        Banner Image
      </p>
      <p>
        Change
      </p>
      <p>
        Remove
      </p>
    </Box>
  );
}
