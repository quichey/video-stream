import * as React from "react";
import { Box } from "@mui/material";

import { ChannelContext } from "..";

export default function User() {
  const { id, name } = React.useContext(ChannelContext);
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
        {`Channel ID: ${id}: Channel Name: ${name}`}
      </p>
    </Box>
  );
}
