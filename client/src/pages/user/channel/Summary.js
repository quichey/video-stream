import * as React from "react";
import { Box } from "@mui/material";

import { UserContext } from "../../../contexts/UserContext";
import { ChannelContext } from "../../contexts/ChannelContext";

export default function Summary() {
  const { id: loggedInUserID } = React.useContext(UserContext);
  const { id: channelID, name } = React.useContext(ChannelContext);

  const isChannelOwner = loggedInUserID === channelID
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
      {
        isChannelOwner ? (
            <>
                <p>
                    Customize Channel if logged in
                </p>
                <p>
                    Manage Videos if logged in
                </p>
            </>
        ): (
            <p>
                Subscribe if not logged in
            </p>
        )
      }
    </Box>
  );
}
