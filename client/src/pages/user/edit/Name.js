import * as React from "react";
import { Box } from "@mui/material";

import { UserContext } from "../../../contexts/UserContext";
import { ChannelContext } from "../../../contexts/ChannelContext";


export default function Name() {
  const { id: loggedInUserID } = React.useContext(UserContext);
  const { id: channelID, name } = React.useContext(ChannelContext);

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
        Profile Icon
      </p>
      <p>
        Name
      </p>
      <p>
        @handle
      </p>
      <p>
        Description
      </p>
    </Box>
  );
}
