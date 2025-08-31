import * as React from "react";
import { Box } from "@mui/material";

import { ChannelContext } from "../../../contexts/ChannelContext";

export default function Content() {
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
        Home tab
      </p>
      <p>
        Videos Tab
      </p>
      <p>
        Shorts tab
      </p>
      <p>
        Live tab
      </p>
      <p>
        Podcasts Tab
      </p>
      <p>
        playlists tab
      </p>
      <p>
        Posts tab
      </p>
    </Box>
  );
}
